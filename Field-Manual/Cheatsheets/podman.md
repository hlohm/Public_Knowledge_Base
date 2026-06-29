---
type: cheatsheet
area: "Containers"
aliases: []
tags: [containers, podman, rootless, oci]
status: working
---

# podman

> **Area:** [[Containers]]

Daemonless, rootless-first OCI container engine. CLI is largely compatible with Docker; key differences are rootless operation by default, no background daemon, and native pod support. See [[docker]] for the Docker-specific sheet.

> **90% of `docker` commands work as `podman` commands.** The differences below are the ones that actually catch you out.

---

## 1. Container lifecycle

```bash
podman run -d --name myapp -p 8080:80 nginx       # run in background
podman run --rm -it alpine sh                      # interactive, deleted on exit
podman run -v /host/data:/container/data:Z nginx   # volume mount; :Z sets SELinux label
podman ps                                          # running containers
podman ps -a                                       # all containers (including stopped)
podman stop myapp
podman start myapp
podman restart myapp
podman rm myapp
podman rm -f myapp                                 # force-remove running container
podman logs myapp
podman logs -f myapp                               # follow logs
podman exec -it myapp sh                           # exec into running container
podman inspect myapp                               # full container config in JSON
```

## 2. Images

```bash
podman pull docker.io/library/nginx                # full registry path (no Docker Hub default)
podman pull quay.io/fedora/fedora
podman images                                      # list local images
podman rmi nginx                                   # remove image
podman image prune                                 # remove dangling images
podman image prune -a                              # remove all unused images
podman tag nginx:latest myregistry.example.com/myapp:1.0
podman push myregistry.example.com/myapp:1.0

# Build from Containerfile (or Dockerfile)
podman build -t myapp:1.0 .
podman build -f Containerfile.prod -t myapp:prod .
```

## 3. Key differences from Docker

**No daemon — processes run as your user:**
```bash
# Docker: containers run as root daemon, even if user passes -u
# Podman rootless: containers are user processes; map to unprivileged UIDs via /etc/subuid

# Check rootless support
podman info --format '{{.Host.IDMappings}}'
cat /etc/subuid | grep $(whoami)    # should show a range like alice:100000:65536
```

**Registry defaults — no implicit Docker Hub:**
```bash
# Docker: 'nginx' → docker.io/library/nginx (implicit)
# Podman: 'nginx' prompts to choose registry unless configured

# Configure short-name resolution
cat /etc/containers/registries.conf.d/00-shortnames.conf
# Or always use full image paths: docker.io/library/nginx
```

**Volume mounts and SELinux:**
```bash
# On SELinux-enforcing systems (RHEL, Fedora), bind mounts need :Z or :z
podman run -v /host/dir:/container/dir:Z myapp    # :Z = private (unshared) label
podman run -v /host/dir:/container/dir:z myapp    # :z = shared label
# Omitting :Z/:z = SELinux denies the mount access
```

**Systemd integration — run containers as services:**
```bash
# Generate a systemd unit for a running container
podman generate systemd --new --name myapp > ~/.config/systemd/user/myapp.service
systemctl --user daemon-reload
systemctl --user enable --now myapp

# Quadlet (podman 4.4+): preferred modern approach
# Create ~/.config/containers/systemd/myapp.container:
# [Container]
# Image=docker.io/library/nginx
# PublishPort=8080:80
# Volume=/host/data:/data:Z
#
# Then: systemctl --user daemon-reload && systemctl --user start myapp
```

**Pods (group of containers sharing network namespace):**
```bash
podman pod create --name mypod -p 8080:80
podman run -d --pod mypod --name frontend nginx
podman run -d --pod mypod --name backend mybackend:latest
podman pod ps
podman pod stop mypod
podman pod rm mypod
```

## 4. Networks and volumes

```bash
# Networks
podman network ls
podman network create mynet
podman run -d --network mynet --name svc1 myimage
podman network inspect mynet

# Volumes
podman volume create mydata
podman volume ls
podman volume inspect mydata
podman run -v mydata:/data myimage
podman volume rm mydata
```

## 5. Compose (podman-compose)

```bash
podman-compose up -d           # requires podman-compose (separate package)
podman-compose down
podman-compose ps

# Alternative: podman 4.x has built-in compose support
podman compose up -d
```

## 6. Housekeeping

```bash
podman system df               # disk usage by images/containers/volumes
podman system prune            # remove stopped containers, unused networks, dangling images
podman system prune -a         # also remove unused images
podman system prune --volumes  # also remove unused volumes
```

---

## Daily workflows

### "Run a one-off command in a container without leaving traces"
```bash
podman run --rm -it python:3.12 python3 -c "import sys; print(sys.version)"
```

### "Run a service as a systemd user unit (rootless)"
```bash
podman run -d --name myapp -p 8080:80 myapp:latest
podman generate systemd --new --name myapp > ~/.config/systemd/user/myapp.service
systemctl --user enable --now myapp
```

### "Debug why SELinux is blocking a volume mount"
```bash
ausearch -m avc -ts recent | grep container
# Then add :Z to the -v flag and restart the container
```

## Gotchas / Golden rules

1. **Always use full image paths** — `podman pull nginx` may prompt or pick the wrong registry; use `docker.io/library/nginx`.
2. **`:Z` on every bind mount on SELinux systems** — forgetting it gives a silent permission denied inside the container.
3. **Rootless containers lose their bind mounts across `loginctl enable-linger` changes** — enable lingering so user units and containers survive logout: `loginctl enable-linger $(whoami)`.
4. **`podman generate systemd --new` vs without `--new`** — `--new` generates a unit that creates a fresh container on start; without it, the unit manages a specific container ID that will no longer exist after `podman rm`.
5. **Port numbers below 1024 require root in rootless mode** — even with `-p 80:80`; either map to a high port (`-p 8080:80`) or adjust `net.ipv4.ip_unprivileged_port_start` via sysctl.
