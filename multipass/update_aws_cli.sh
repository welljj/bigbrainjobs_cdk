#!/bin/bash
CURRENT_ARCH=$(uname -m)
curl "https://awscli.amazonaws.com/awscli-exe-linux-${CURRENT_ARCH}.zip" -o "awscliv2.zip"
unzip ./awscliv2.zip
if command -v aws
then
echo "updating"
sudo ./aws/install --update
else
echo "installing"
sudo ./aws/install
fi
rm -rf ./aws
rm -rf ./awscliv2.zip