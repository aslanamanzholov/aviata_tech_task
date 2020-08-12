#!/bin/bash
sudo apt-get remove docker docker-engine docker.io containerd runc

sudo apt-get update && sudo apt-get install apt-transport-https ca-certificates \
curl gnupg-agent software-properties-common

curl -fsSL https://get.docker.com -o get-docker.sh && chmod +x get-docker.sh && sudo ./get-docker.sh

sudo usermod -aG docker $USER && rm get-docker.sh

sudo curl \
-L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose
-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose && \
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
