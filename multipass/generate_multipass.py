import configparser
import pathlib

import yaml

current_dir = pathlib.Path(__file__).parent
home_path = pathlib.Path.home()
git_config_path = home_path / ".gitconfig"
aws_config_path = home_path / ".aws" / "config"
aws_credentials_path = home_path / ".aws" / "credentials"

with open(current_dir / "update_aws_cli.sh", "r") as f:
    update_aws_cli = f.read()

with open(pathlib.Path.home() / ".ssh" / "id_rsa.pub") as f:
    ssh_public_key = f.read().strip()


config = configparser.ConfigParser()
config.read([git_config_path, aws_config_path, aws_credentials_path])

git_name = config["user"]["name"]
git_email = config["user"]["email"]

aws_region = config["default"]["region"]
aws_output = config["default"]["output"]
aws_access_key_id = config["default"]["aws_access_key_id"]
aws_secret_access_key = config["default"]["aws_secret_access_key"]

yaml_data = {
    "package_update": True,
    "package_upgrade": True,
    "package_reboot_if_required": True,
    "ssh_authorized_keys": [ssh_public_key],
    "packages": [
        "python3-venv",
        "python3-dev",
        "build-essential",
        "postgresql-server-dev-all",
        "postgresql-postgis",
        "postgis",
        "direnv",
        "unzip",
    ],
    "snap": {"commands": ["snap refresh"]},
    "write_files": [
        {
            "path": "/home/ubuntu/.bashrc",
            "content": '\neval "$(direnv hook bash)"\n',
            "owner": "ubuntu:ubuntu",
            "append": True,
            "defer": True,
        },
        {
            "path": "/home/ubuntu/update_aws_cli.sh",
            "content": update_aws_cli,
            "owner": "ubuntu:ubuntu",
            "defer": True,
            "permissions": "0755",
        },
    ],
    "runcmd": [
        f'sudo -u ubuntu git config --global user.name "{git_name}"',
        f"sudo -u ubuntu git config --global user.email {git_email}",
        "bash /home/ubuntu/update_aws_cli.sh",
        f'sudo -u ubuntu aws configure set aws_access_key_id "{aws_access_key_id}"',
        f'sudo -u ubuntu aws configure set aws_secret_access_key "{aws_secret_access_key}"',
        f'sudo -u ubuntu aws configure set region "{aws_region}"',
        f'sudo -u ubuntu aws configure set output "{aws_output}"',
        "curl -sL https://deb.nodesource.com/setup_lts.x | bash -",
        "apt install -y nodejs",
        "npm install -g npm@latest",
        "npm update -g",
        "npm install -g npm-check-updates",
        "npm install -g aws-cdk",
        "sudo -u postgres psql -c \"CREATE USER geodjango WITH SUPERUSER PASSWORD 'geodjango';\"",
        'sudo -u postgres psql -c "CREATE DATABASE geodjango OWNER geodjango;"',
    ],
}

with open(current_dir / "multipass.yaml", "w") as f:
    yaml.dump(yaml_data, f, sort_keys=False)
