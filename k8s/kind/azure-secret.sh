#!/bin/bash

CURRENT_DIR=$(dirname "$0")

if [ ! -f $CURRENT_DIR/azure-credentials.json ]; then
    TENANT_ID=$1
    SUBSCRIPTION_ID=$2
    az login --tenant $TENANT_ID --use-device-code
    az ad sp create-for-rbac --sdk-auth --role Owner --scopes /subscriptions/$SUBSCRIPTION_ID > $CURRENT_DIR/azure-credentials.json
fi

until kubectl wait --for=jsonpath='{.status.phase}'=Active namespace/crossplane; do
  sleep 3
done

kubectl create secret generic azure-secret -n crossplane --from-file=creds=$CURRENT_DIR/azure-credentials.json
kubectl describe secret azure-secret -n crossplane
