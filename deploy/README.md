``` $ scp -i /path/to/cert.pem deploy/prod/* ubuntu@ec2-18-217-172-120.us-east-2.compute.amazonaws.com:/srv/aviata_tech_task ```
``` $ scp -i /path/to/cert.pem deploy/prod/* ubuntu@ec2-18-217-172-120.us-east-2.compute.amazonaws.com:/srv/aviata_tech_task ```
``` $ docker push aslanamanzholov/aviata_tech_task:master ```

first time:
``` $ cp deploy/prod/generic.nginx.conf deploy/prod/nginx.conf ```
``` $ sed -i 's/DOMAIN_NAME/asdfg.ga/g' deploy/prod/nginx.conf ```
setup domain name at setup.sh
``` $ ssh user@host ```
``` $ sudo mkdir /srv/aviata_tech_task/ ```
``` $ sudo chown -R user /srv/aviata_tech_task/ ```
``` $ scp deploy/prod/* user@host:/srv/aviata_tech_task/ ```
``` $ ssh user@host "cd /srv/aviata_tech_task/ && chmod +x setup.sh && sudo ./setup.sh" ```

every time:
``` $ scp -i /path/to/aviata_tech_task.pem deploy/prod/* user@host:/srv/aviata_tech_task/ ```
``` $ ssh -i /path/to/aviata_tech_task user@host "cd /srv/aviata_tech_task/ && sudo docker-compose pull && sudo docker-compose down && sudo docker-compose up -d" ```


TODO: Automate using Travis/GitLab/Circle CI
