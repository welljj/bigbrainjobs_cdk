import pathlib

import yaml

current_dir = pathlib.Path(__file__).parent

with open(current_dir / "gunicorn.service", "rb") as f:
    gunicorn_service = f.read()

with open(current_dir / "gunicorn.socket", "rb") as f:
    gunicorn_socket = f.read()

with open(current_dir / "nginx.conf", "rb") as f:
    nginx_conf = f.read()

with open(current_dir / "direnv.toml", "rb") as f:
    direnv_conf = f.read()


def get_yaml():
    user_data = {
        "package_update": True,
        "package_upgrade": True,
        "package_reboot_if_required": True,
        "packages": [
            "git",
            "build-essential",
            "libpq-dev",
            "python3-dev",
            "postgresql",
            "python3-venv",
            "gunicorn",
            "nginx",
            "direnv",
            "nano",
        ],
        "write_files": [
            {
                "path": "/etc/systemd/system/gunicorn.service",
                "content": gunicorn_service,
            },
            {"path": "/etc/systemd/system/gunicorn.socket", "content": gunicorn_socket},
            {"path": "/etc/nginx/sites-available/default", "content": nginx_conf},
            {
                "path": "/home/ubuntu/.bashrc",
                "owner": "ubuntu:ubuntu",
                "content": '\neval "$(direnv hook bash)"\n',
                "append": True,
                "defer": True,
            },
            {
                "path": "/home/ubuntu/.config/direnv/direnv.toml",
                "owner": "ubuntu:ubuntu",
                "content": direnv_conf,
                "defer": True,
            },
        ],
        "runcmd": [
            "sudo -u postgres psql -c \"ALTER USER postgres WITH PASSWORD 'postgres'\"",
            "python3 -m venv /home/ubuntu/venv",
            "/home/ubuntu/venv/bin/python -m pip install -U pip setuptools wheel",
            "git clone https://github.com/cald/bigbrainjobs.git /home/ubuntu/bigbrainjobs",
            "/home/ubuntu/venv/bin/python -m pip install -r /home/ubuntu/bigbrainjobs/requirements.txt",
            "systemctl enable --now gunicorn.socket",
            "nginx -s reload",
        ],
    }

    return yaml.dump(user_data, sort_keys=False)
