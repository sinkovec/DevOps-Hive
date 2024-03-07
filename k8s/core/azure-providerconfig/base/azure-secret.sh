#!/bin/bash

TENANT_ID=$1
SUBSCRIPTION_ID=$2

if [ ! -f ./azure-credentials.json ]; then
    az login --tenant $TENANT_ID --use-device-code
    az ad sp create-for-rbac --sdk-auth --role Owner --scopes /subscriptions/$2 > azure-credentials.json
fi

kubectl create secret generic azure-secret -n crossplane --from-file=creds=./azure-credentials.json
kubectl describe secret azure-secret -n crossplane
