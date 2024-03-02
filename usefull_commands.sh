docker-compose -f mongo_db/docker-compose.mongo_db.yml up -d


& minikube -p minikube docker-env --shell powershell | Invoke-Expression
minikube image load villagersflaskapp:latest

kubectl get nodes -o wide

minikube service flask-service