# CBDC-project-deploy-swarm

## Deploy the swarm service

```
chmod -R +rw ./data/mysql

source deploy.sh
```

## Follow logs

```
sudo docker service logs --raw -f cbdcdeploy_bank-django-service
sudo docker service logs --raw -f cbdcdeploy_bank-database-service
```