---
type: cheatsheet
area: "Containers"
aliases: [kubernetes, k8s]
tags: [containers, kubernetes, kubectl, k8s]
status: working
---

# kubectl

> **Area:** [[Containers]]

The Kubernetes CLI. Manages clusters, namespaces, workloads, configs, and debugging. This sheet covers the everyday surface — enough to deploy, inspect, and troubleshoot; not cluster administration.

---

## 1. Context and cluster

```bash
kubectl config get-contexts         # list all clusters/contexts
kubectl config current-context      # which context is active
kubectl config use-context prod     # switch context
kubectl config set-context --current --namespace=myns   # set default namespace for context

kubectl cluster-info                # API server endpoint and add-ons
kubectl get nodes                   # node list and status
kubectl get nodes -o wide           # + IP, OS, kernel
kubectl describe node worker-1      # detailed node info: capacity, conditions, events
```

## 2. Core workload commands

```bash
# Get resources
kubectl get pods                        # pods in current namespace
kubectl get pods -n kube-system         # pods in a specific namespace
kubectl get pods -A                     # pods in ALL namespaces
kubectl get pods -o wide                # + node, IP
kubectl get pods -w                     # watch: live updates
kubectl get pod mypod -o yaml           # full manifest
kubectl get pod mypod -o json | jq .status.phase

kubectl get deployments
kubectl get services
kubectl get ingress
kubectl get configmaps
kubectl get secrets
kubectl get all                         # pods + svc + deploy + rs in current namespace

# Describe (narrative output with Events section — very useful for debugging)
kubectl describe pod mypod
kubectl describe deployment myapp
kubectl describe node worker-1

# Logs
kubectl logs mypod                      # last n lines from pod
kubectl logs mypod -c init-container    # specific container in a multi-container pod
kubectl logs mypod -f                   # follow
kubectl logs mypod --previous           # logs from previous (crashed) container
kubectl logs -l app=myapp               # logs from all pods with a label
kubectl logs mypod --since 1h
kubectl logs mypod --tail=100
```

## 3. Exec and port-forward

```bash
kubectl exec -it mypod -- sh            # shell into a running pod
kubectl exec -it mypod -c mycontainer -- bash   # specific container

kubectl port-forward pod/mypod 8080:80          # forward local 8080 → pod port 80
kubectl port-forward svc/myservice 8080:80       # forward via service
kubectl port-forward deployment/myapp 8080:80
# Ctrl+C to stop

kubectl cp mypod:/var/log/app.log ./app.log      # copy file from pod
kubectl cp ./config.yaml mypod:/app/config.yaml  # copy file to pod
```

## 4. Apply, create, delete

```bash
kubectl apply -f manifest.yaml          # apply (create or update)
kubectl apply -f ./k8s/                 # apply all manifests in a directory
kubectl apply -k ./k8s/overlays/prod/  # Kustomize overlay

kubectl create -f manifest.yaml         # create only (error if exists)
kubectl delete -f manifest.yaml         # delete what the manifest describes
kubectl delete pod mypod                # delete by name
kubectl delete pod mypod --grace-period=0 --force   # force-delete stuck pod

# Rollout management
kubectl rollout status deployment/myapp
kubectl rollout history deployment/myapp
kubectl rollout undo deployment/myapp           # roll back to previous revision
kubectl rollout undo deployment/myapp --to-revision=3
kubectl rollout restart deployment/myapp        # rolling restart (picks up new ConfigMap)

# Scale
kubectl scale deployment myapp --replicas=5
kubectl autoscale deployment myapp --min=2 --max=10 --cpu-percent=70
```

## 5. Edit in-cluster resources

```bash
kubectl edit deployment myapp           # opens $EDITOR; saves immediately on write/exit
kubectl patch deployment myapp -p '{"spec":{"replicas":3}}'
kubectl set image deployment/myapp mycontainer=myimage:2.0   # update image in-place
kubectl set env deployment/myapp ENV=production
```

## 6. Labels, selectors, and filtering

```bash
kubectl get pods -l app=myapp
kubectl get pods -l app=myapp,env=prod
kubectl get pods -l 'env in (prod, staging)'
kubectl label pod mypod env=prod           # add/update label
kubectl annotate pod mypod owner=alice
```

## 7. Namespaces

```bash
kubectl get namespaces
kubectl create namespace staging
kubectl delete namespace staging       # deletes EVERYTHING in that namespace
kubectl get all -n staging

# Work in a namespace without specifying -n every time
kubectl config set-context --current --namespace=staging
```

## 8. ConfigMaps and Secrets

```bash
kubectl create configmap myconfig --from-file=./config/
kubectl create configmap myconfig --from-literal=key=value
kubectl get configmap myconfig -o yaml

kubectl create secret generic mysecret --from-literal=password='<secret>'
kubectl create secret tls mytls --cert=tls.crt --key=tls.key
kubectl get secret mysecret -o jsonpath='{.data.password}' | base64 -d
```

## 9. Debugging

```bash
# Why is a pod not starting?
kubectl describe pod mypod | tail -30         # look at Events section
kubectl logs mypod --previous                 # logs before last crash

# Pod stuck in Pending
kubectl describe pod mypod | grep -A10 Events
# Common causes: no nodes with available resources, image pull failure, PVC not bound

# Run a debug container (ephemeral)
kubectl debug -it mypod --image=busybox --target=mypod   # shares namespaces with pod
kubectl run -it debug --image=alpine --rm -- sh           # scratch pod, deleted on exit

# Check resource usage
kubectl top pods                   # requires metrics-server
kubectl top nodes
```

---

## Daily workflows

### "Deploy a new version"
```bash
kubectl set image deployment/myapp app=myimage:2.1
kubectl rollout status deployment/myapp    # watch until complete
```

### "Tail logs from all pods of a deployment"
```bash
kubectl logs -l app=myapp -f --max-log-requests=10
```

### "Forward a service port for local testing"
```bash
kubectl port-forward svc/mydb 5432:5432
```

### "Debug a CrashLoopBackOff pod"
```bash
kubectl describe pod mypod          # check Events for error
kubectl logs mypod --previous       # previous crash output
```

## Gotchas / Golden rules

1. **`kubectl apply` vs `kubectl create`** — use `apply` for GitOps and idempotent workflows; `create` fails if the resource exists. Almost always use `apply`.
2. **`kubectl delete namespace` is irreversible and immediate** — it deletes every resource in the namespace; there is no recycle bin.
3. **`kubectl edit` saves immediately on exit** — `:wq` in vim or saving in your editor applies the change to the live cluster; `:q!` (discard) to abort.
4. **`kubectl exec` in a distroless container has no shell** — debug with `kubectl debug` instead, which attaches an ephemeral sidecar with tools.
5. **Context mistakes are the most dangerous kubectl mistake** — always confirm `kubectl config current-context` before a destructive command on production; add `PS1` prompt customisation or kubectx to make the context visible.
