import os
import typing as t
from io import StringIO
from pathlib import Path
from types import SimpleNamespace

import boto3
from dotenv import dotenv_values

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
    s3: "S3Client" = boto3.client("s3")
    secrets_object = s3.get_object(
        Bucket=os.environ["aws_s3_app_bucket"],
        Key=f"{os.environ['aws_s3_app_folder']}/secure/.env.secrets",
    )

    secrets = dotenv_values(
        stream=StringIO(secrets_object["Body"].read().decode("utf-8"))
    )

    return Secrets(**secrets)
