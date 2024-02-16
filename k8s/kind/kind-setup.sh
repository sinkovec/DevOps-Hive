#!/bin/bash

set -o errexit

# 1. Create registry container unless it already exists
reg_name='kind-registry'
reg_port='5001'
if [ "$(docker inspect -f '{{.State.Running}}' "${reg_name}" 2>/dev/null || true)" != 'true' ]; then
  docker run \
    -d --restart=always -p "127.0.0.1:${reg_port}:5000" --network bridge --name "${reg_name}" \
    registry:2
fi

# 2. Create kind cluster with containerd registry config dir enabled
# TODO: kind will eventually enable this by default and this patch will
# be unnecessary.
#
# See:
# https://github.com/kubernetes-sigs/kind/issues/2875
# https://github.com/containerd/containerd/blob/main/docs/cri/config.md#registry-configuration
# See: https://github.com/containerd/containerd/blob/main/docs/hosts.md
kind create cluster --config=kind-cluster.yaml

# 3. Add the registry config to the nodes
#
# This is necessary because localhost resolves to loopback addresses that are
# network-namespace local.
# In other words: localhost in the container is not localhost on the host.
#
# We want a consistent name that works from both ends, so we tell containerd to
# alias localhost:${reg_port} to the registry container when pulling images
REGISTRY_DIR="/etc/containerd/certs.d/localhost:${reg_port}"
for node in $(kind get nodes -n hive-cluster); do
  docker exec "${node}" mkdir -p "${REGISTRY_DIR}"
  cat <<EOF | docker exec -i "${node}" cp /dev/stdin "${REGISTRY_DIR}/hosts.toml"
[host."http://${reg_name}:5000"]
EOF
done

# 4. Connect the registry to the cluster network if not already connected
# This allows kind to bootstrap the network but ensures they're on the same network
if [ "$(docker inspect -f='{{json .NetworkSettings.Networks.kind}}' "${reg_name}")" = 'null' ]; then
  docker network connect "kind" "${reg_name}"
fi

# 5. Document the local registry
# https://github.com/kubernetes/enhancements/tree/master/keps/sig-cluster-lifecycle/generic/1755-communicating-a-local-registry
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: local-registry-hosting
  namespace: kube-public
data:
  localRegistryHosting.v1: |
    host: "localhost:${reg_port}"
    help: "https://kind.sigs.k8s.io/docs/user/local-registry/"
EOF


# # 6. Setup ingress-nginx
# kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
# sleep 20
# # wait until its ready
# kubectl wait --namespace ingress-nginx \
#   --for=condition=ready pod \
#   --selector=app.kubernetes.io/component=controller \
#   --timeout=90s

# 7. Bootstrap cluster with ArgoCD and default application sets.
# For some reason, ApplicationSet CRD are not detected in the first run, resulting in an incomplete setup.
# Therefore, the kustomization is run twice to ensure ApplicationSets are installed.
kubectl apply -k ../bootstrap/overlays/default || true
sleep 5
kubectl apply -k ../bootstrap/overlays/default

# 8. Load docker images to local registry
docker pull ghcr.io/sinkovec/hive-app:latest --platform linux/amd64 && docker tag ghcr.io/sinkovec/hive-app:latest localhost:5001/sinkovec/hive-app:latest && docker push localhost:5001/sinkovec/hive-app:latest

echo "Setup complete. Run ./kind-cleanup.sh to cleanup"
