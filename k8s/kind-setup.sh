#!/bin/bash

set -e

# create kind cluster from config
kind create cluster --config=kind-cluster.yaml

# setup ingress-nginx
echo "Apply nginx-ingres static manifests"
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

echo "Wait until ingress-nginx is ready.."
sleep 20
# wait until its ready
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s

echo "Setup complete. Run kind delete cluster -n hive-cluster to cleanup"

# build hive app docker image
docker build ../app/ -t sinkovec/hive-app:0.0.1

# load docker image into kind cluster
kind load docker-image sinkovec/hive-app:0.0.1

# apply app manifest
kubectl apply -f hive.yaml