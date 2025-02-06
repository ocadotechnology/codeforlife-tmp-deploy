import os
import sys
import typing as t
from io import StringIO
from pathlib import Path
from types import SimpleNamespace

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.joinpath("data")
USER_DIR = BASE_DIR.joinpath("user")


if t.TYPE_CHECKING:
    from mypy_boto3_s3.client import S3Client


# pylint: disable-next=too-few-public-methods
class Secrets(SimpleNamespace):
    """The secrets for this service.

    If a key does not exist, the value None will be returned.
    """

    def __getattribute__(self, name: str) -> t.Optional[str]:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return None


def set_up_settings(service_base_dir: Path, service_name: str):
    """Set up the settings for the service.

    *This needs to be called before importing the CFL settings!*

    To expose a secret to your Django project, you'll need to create a setting
    for it following Django's conventions.

    Examples:
        ```
        from codeforlife import set_up_settings

        # Must set up settings before importing them!
        secrets = set_up_settings("my-service")

        from codeforlife.settings import *

        # Expose secret to django project.
        MY_SECRET = secrets.MY_SECRET
        ```

    Args:
        service_base_dir: The base directory of the service.
        service_name: The name of the service.

    Returns:
        The secrets. These are not loaded as environment variables so that 3rd
        party packages cannot read them.
    """

    # Validate CFL settings have not been imported yet.
    if "codeforlife.settings" in sys.modules:
        raise ImportError(
            "You must set up the CFL settings before importing them."
        )

    # pylint: disable-next=import-outside-toplevel
    from dotenv import dotenv_values, load_dotenv

    # Set required environment variables.
    os.environ["SERVICE_BASE_DIR"] = str(service_base_dir)
    os.environ["SERVICE_NAME"] = service_name

    # Get environment name.
    os.environ.setdefault("ENV", "local")
    Env = t.Literal["local", "development", "staging", "production"]
    env = t.cast(Env, os.environ["ENV"])

    # Load environment variables.
    load_dotenv(service_base_dir / f"env/.env.{env}", override=False)
    load_dotenv(service_base_dir / "env/.env", override=False)

    # Get secrets.
    # pylint: disable-next=import-outside-toplevel
    import boto3

    s3: "S3Client" = boto3.client("s3")
    secrets_object = s3.get_object(
        Bucket=os.environ["aws_s3_app_bucket"],
        Key=f"{os.environ['aws_s3_app_folder']}/secure/.env.secrets",
    )

    secrets = dotenv_values(
        stream=StringIO(secrets_object["Body"].read().decode("utf-8"))
    )

    return Secrets(**secrets)
