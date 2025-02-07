import subprocess


def main():
    subprocess.run("python", "manage.py", "collectstatic", "--noinput", check=True)
    subprocess.run(
        "python",
        "manage.py",
        "collectstatic",
        "settings=pipeline_settings",
        "--noinput",
        check=True,
    )


if __name__ == "__main__":
    main()
