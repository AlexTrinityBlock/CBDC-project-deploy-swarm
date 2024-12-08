# 構建 bank-django-service 映像
docker build -t asia-east1-docker.pkg.dev/cbdc-demo/cbdc-artifact-registry/bank-django-service:latest ./dockerfiles/bank-django-service

# 構建 user-cryptography-support-flask-service 映像
docker build -t asia-east1-docker.pkg.dev/cbdc-demo/cbdc-artifact-registry/user-cryptography-support-flask-service:latest ./dockerfiles/user-cryptography-support-flask-service

# 推送 bank-django-service 映像
docker push asia-east1-docker.pkg.dev/cbdc-demo/cbdc-artifact-registry/bank-django-service:latest

# 推送 user-cryptography-support-flask-service 映像
docker push asia-east1-docker.pkg.dev/cbdc-demo/cbdc-artifact-registry/user-cryptography-support-flask-service:latest