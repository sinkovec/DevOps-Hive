#!/bin/bash

kind delete cluster -n kind-hive-cluster
docker rm -f hive-cluster-control-plane
docker rm -f kind-registry
