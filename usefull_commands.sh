docker-compose -f mongo_db/docker-compose.mongo_db.yml up -d


& minikube -p minikube docker-env --shell powershell | Invoke-Expression
minikube image load villagersflaskapp:latest




kubectl get nodes -o wide

minikube service flask-service

kubectl apply -f flask-service.yaml



#Commands to run to create eks cluster

#Creates initial cluster
eksctl create cluster --name villagers-cluster --version 1.29 --region eu-west-2 --nodegroup-name villagers-nodes --node-type t3.micro --nodes 4 --profile dev

#Use this to update auth to allow iam access..
 kubectl edit -n kube-system configmap/aws-auth

# then add this to the file that opens
 mapUsers: |
  - userarn: arn:aws:iam::123456789012:user/IAM_USER_NAME
    username: IAM_USER_NAME
    groups:
      - system:masters

#Then run these commands to add flask and mongo db
kubectl apply -f flask-deployment.yaml
kubectl apply -f mongo-deployment.yaml
kubectl apply -f flask-service.yaml 
kubectl apply -f mongodb-service.yaml


#After this can run
kubect get pods
#To get the available pods, then want to get logs from flask pod
kubectl logs flask-deployment-55bd96bbfd-4gmmb
#Use queries like this to get more recent logs
kubectl logs flask-deployment-55bd96bbfd-4gmmb --since=1m


#Then to connect to mongodb locally run
#whereh mongodb id found from get pods
 kubectl port-forward mongodb-deployment-74c6dd967f-fqhv4 27017:27017