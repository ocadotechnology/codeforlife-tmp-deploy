from django.core import management

def main():
    management.call_command("collectstatic")
    management.call_command("collectstatic", "--settings=pipeline_settings.py")


if __name__ == "__main__":
    main()