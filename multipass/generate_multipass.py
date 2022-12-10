import pathlib
from git import Repo

import yaml

current_dir = pathlib.Path(__file__).parent
repo = Repo(current_dir.parent)

with open(current_dir / "update_aws_cli.sh", "rb") as f:
    update_aws_cli = f.read()

with open(pathlib.Path.home() / ".ssh" / "id_rsa.pub") as f:
    ssh_public_key = f.read().strip()

git_name = repo.config_reader().get_value("user", "name")
git_email = repo.config_reader().get_value("user", "email")

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
