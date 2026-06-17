---
type: cheatsheet
area: Containers
aliases: [docker-compose, compose]
tags: [containers]
status: stable
---

# docker

> **Area:** [[Containers]]

Daily-driver reference for working with containers. Covers the mental model, installation on
the common platforms, the everyday command surface, Compose, Dockerfiles, cleanup, and the
gotchas that bite when you haven't touched this in a while. Every block is annotated so the
*why* is on the page, not just the *what*.

> Modern Docker speaks **Compose V2**: the subcommand is `docker compose` (space, built-in
> plugin). The old hyphenated `docker-compose` was the standalone Python tool (Compose V1)
> and is superseded — see §2.9.

---

## Table of contents

1. Mental model
2. Installation (per platform)
3. Images
4. Containers
5. `docker run` flag reference
6. Volumes & bind mounts
7. Networks
8. Docker Compose
9. Dockerfile quick reference
10. Registries
11. System & cleanup
12. Inspecting & debugging
13. Gotchas / paper cuts
14. Extras

---

## 1. Mental model

Four primitives. Almost everything is CRUD on these.

| Thing | What it is | Lifecycle |
| --- | --- | --- |
| **Image** | Read-only template (layers). Built from a Dockerfile or pulled. | Immutable; tagged; cached. |
| **Container** | A running (or stopped) instance of an image + a writable layer. | Created → started → stopped → removed. |
| **Volume** | Docker-managed persistent storage, decoupled from any container. | Outlives containers until pruned. |
| **Network** | Virtual network connecting containers (and optionally the host). | Created on demand; `bridge` default. |

Key consequence: **containers are disposable, data is not.** Anything you want to keep lives
in a volume or a bind mount, never in the container's writable layer (which vanishes on
`docker rm`).

The daemon (`dockerd`) does the work; the CLI (`docker`) just talks to it over a socket
(`/var/run/docker.sock`). That socket is root-equivalent — see §13.

---

## 2. Installation

Pick the section for your platform. On Linux the **official Docker repository** is the
recommended source on Debian/Fedora families (distro packages lag); Arch ships current Docker
directly. Always finish with the **post-install** steps in §2.7.

### 2.1 Arch / CachyOS / Manjaro / EndeavourOS

Docker is in the official `extra` repo — no third-party repos needed. Compose and buildx are
packaged separately.

```bash
sudo pacman -Syu                                      # never install on a partial upgrade
sudo pacman -S docker docker-compose docker-buildx    # engine + compose plugin + buildx
sudo systemctl enable --now docker.service            # start now + on every boot
```

`docker-compose` here provides the V2 `docker compose` subcommand. `docker-buildx` enables
`docker buildx` (BuildKit / multi-arch builds).

### 2.2 Debian / Ubuntu / Mint / Pop!_OS / Kali / Parrot — official repo

```bash
# 1. Remove any distro/unofficial packages that would conflict
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
  sudo apt remove -y $pkg
done

# 2. Add Docker's official GPG key into the modern keyrings dir
sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 3. Add the repository (signed-by pins it to the key above)
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 4. Install engine + CLI + containerd + buildx + compose plugins
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

> **Debian vs Ubuntu:** on pure Debian, swap both `.../linux/ubuntu` paths for `.../linux/debian`.
>
> **Kali / Parrot gotcha:** these are Debian-derived but `$VERSION_CODENAME` resolves to
> something Docker's repo doesn't publish (e.g. `kali-rolling`), so the repo line 404s. Fix:
> hard-code the Debian codename the release tracks (e.g. `bookworm`) and use the
> `.../linux/debian` path. Verify with `cat /etc/debian_version`.

### 2.3 Fedora / RHEL / Rocky / Alma — official repo

Fedora ships Podman by default; install Docker CE when you specifically need the Docker
engine/Compose/BuildKit.

```bash
# 1. Remove conflicting older packages (OK if none are present)
sudo dnf remove docker docker-client docker-client-latest docker-common \
  docker-latest docker-latest-logrotate docker-logrotate docker-selinux \
  docker-engine-selinux docker-engine

# 2. Add the repo — SYNTAX DIFFERS BY DNF VERSION
sudo dnf -y install dnf-plugins-core

#   Fedora 41 and earlier (DNF4):
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
#   Fedora 42+ (DNF5) — the older syntax errors out here:
sudo dnf config-manager addrepo --from-repofile=https://download.docker.com/linux/fedora/docker-ce.repo

# 3. Install
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

For RHEL/Rocky/Alma use the `.../linux/rhel/docker-ce.repo` (or `centos`) repofile instead of
the Fedora one. SELinux is enforcing on these — see the `:z`/`:Z` mount note in §13.

### 2.4 Convenience script — any Linux, quick & dirty

Wraps the official-repo setup. **Testing/dev environments only** — not for production, and
don't re-run it to upgrade (use the package manager).

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm get-docker.sh
```

### 2.5 macOS — Docker Desktop

No native Linux kernel on macOS, so Docker runs inside a managed VM via Docker Desktop.

```bash
brew install --cask docker        # or download the .dmg from docker.com
```

Pick the **Apple Silicon** or **Intel** build to match the chip. Launch Docker Desktop once so
the daemon starts; the `docker` and `docker compose` CLIs install with it.

### 2.6 Windows — Docker Desktop + WSL2

```powershell
wsl --install                         # enable WSL2 first if not already present
winget install Docker.DockerDesktop   # or download the installer from docker.com
```

Use the **WSL2 backend** (default, recommended) rather than Hyper-V. After install, reboot,
launch Docker Desktop, and run docker commands from PowerShell or inside a WSL2 distro.

### 2.7 Post-install (Linux) — REQUIRED

```bash
# Run docker without sudo. WARNING: the docker group is root-equivalent (§13).
sudo usermod -aG docker $USER
newgrp docker                      # apply to the current shell, or just log out/in

# Make sure the daemon is enabled at boot (Arch users already did this)
sudo systemctl enable --now docker.service

# Verify
docker run hello-world             # pulls + runs a tiny test image
docker version                     # client + daemon versions
docker compose version             # confirms the Compose V2 plugin is present
```

### 2.8 Rootless mode (optional, hardening)

Runs the daemon as your user instead of root — smaller blast radius.

```bash
dockerd-rootless-setuptool.sh install     # sets up a per-user rootless daemon
# then point the CLI at the rootless socket per the script's printed instructions
```

Trade-offs: some features (low ports <1024, certain network/storage drivers) need extra config
under rootless. Fine for most dev workloads.

### 2.9 Compose V2 vs V1

| | Invocation | What it is | Status |
| --- | --- | --- | --- |
| **V2** | `docker compose` (space) | Go plugin, ships with current Docker | Use this |
| **V1** | `docker-compose` (hyphen) | Old standalone Python tool | Superseded / legacy |

All examples in §8 use the `docker compose` form. If you hit ancient docs using
`docker-compose`, the subcommands are identical — just drop the hyphen.

---

## 3. Images

```bash
docker pull nginx:1.27               # pull a specific tag (pin tags; avoid :latest drift)
docker images                        # list local images  (alias: docker image ls)
docker image ls -a                   # include intermediate layers

docker build -t myapp:1.0 .          # build from ./Dockerfile, tag it
docker build -t myapp:1.0 -f Dockerfile.prod .   # custom Dockerfile name
docker build --no-cache -t myapp:1.0 .           # ignore the layer cache
docker build --build-arg VERSION=1.0 -t myapp .  # pass an ARG

docker tag myapp:1.0 registry.example.com/myapp:1.0   # retag (e.g. for a registry)
docker rmi myapp:1.0                 # remove an image  (alias: docker image rm)
docker image prune                   # drop dangling (untagged) images
docker image prune -a                # drop ALL images not used by a container

docker history myapp:1.0             # show layers + sizes (find the fat layer)
docker inspect nginx:1.27            # full JSON metadata
docker save myapp:1.0 -o myapp.tar   # export image to a tarball (air-gapped transfer)
docker load -i myapp.tar             # import it on the other side
```

---

## 4. Containers

```bash
# Run — the workhorse. See §5 for the full flag table.
docker run -d --name web -p 8080:80 nginx:1.27   # detached, named, port-mapped
docker run --rm -it ubuntu:24.04 bash            # throwaway interactive shell
docker run -d --restart unless-stopped redis     # survive daemon/host restarts

docker ps                            # running containers
docker ps -a                         # include stopped ones
docker ps -q                         # IDs only (great for scripting — see §14)

docker exec -it web bash             # shell INTO a running container (or: sh)
docker exec web env                  # run a one-off command, capture output

docker logs web                      # container's stdout/stderr
docker logs -f --tail 100 web        # follow live, last 100 lines

docker stop web                      # SIGTERM, then SIGKILL after grace period
docker start web                     # restart a stopped container
docker restart web
docker kill web                      # immediate SIGKILL

docker rm web                        # remove a STOPPED container
docker rm -f web                     # force-remove a running one
docker rename web frontend           # rename

docker cp web:/etc/nginx/nginx.conf ./nginx.conf   # copy OUT of a container
docker cp ./index.html web:/usr/share/nginx/html/  # copy INTO a container

docker stats                         # live CPU/mem/IO per container (top-like)
docker top web                       # processes inside the container
docker port web                      # show published port mappings
docker inspect web                   # full JSON state + config
docker commit web myapp:snapshot     # freeze a container into a new image (debug aid)
```

---

## 5. `docker run` flag reference

The flags you actually reach for daily:

| Flag | Meaning | Example |
| --- | --- | --- |
| `-d`, `--detach` | Run in background | `docker run -d nginx` |
| `-it` | Interactive + TTY (combine `-i -t`) | `docker run -it ubuntu bash` |
| `--rm` | Auto-remove on exit | `docker run --rm alpine echo hi` |
| `--name` | Name the container | `--name web` |
| `-p`, `--publish` | `host:container` port | `-p 8080:80` |
| `-P` | Publish all EXPOSEd ports to random host ports | `-P` |
| `-v`, `--volume` | Mount volume or bind | `-v data:/var/lib/db` |
| `--mount` | Verbose, explicit mount syntax | `--mount type=bind,src=...,dst=...` |
| `-e`, `--env` | Set an env var | `-e TZ=Europe/Berlin` |
| `--env-file` | Load env vars from a file | `--env-file .env` |
| `--network` | Attach to a network | `--network mynet` |
| `--restart` | Restart policy | `--restart unless-stopped` |
| `-w`, `--workdir` | Working dir inside container | `-w /app` |
| `-u`, `--user` | Run as UID/user | `-u 1000:1000` |
| `-h`, `--hostname` | hostname inside container | `-h db01` |
| `--memory` / `--cpus` | Resource limits | `--memory 512m --cpus 1.5` |
| `--entrypoint` | Override the image entrypoint | `--entrypoint sh` |

Restart policies: `no` (default), `on-failure[:max]`, `always`, `unless-stopped`. Use
`unless-stopped` for services you want back after a reboot but not after you deliberately stop
them.

---

## 6. Volumes & bind mounts

Three storage flavours:

- **Named volume** — Docker-managed, lives under `/var/lib/docker/volumes/`. Best for databases
  and app state. Survives `docker rm`.
- **Bind mount** — maps a host path into the container. Best for source code in dev. The host
  path **must be absolute**.
- **tmpfs** — in-memory, never hits disk. For secrets/scratch.

```bash
# Named volume
docker volume create appdata
docker run -d -v appdata:/var/lib/postgresql/data postgres:16

# Bind mount (host:container) — note the absolute host path
docker run -d -v "$PWD/src":/app:ro node:22        # :ro = read-only

# tmpfs
docker run --tmpfs /tmp:size=64m alpine

docker volume ls                     # list volumes
docker volume inspect appdata        # where it lives, when created
docker volume rm appdata             # remove (must be unused)
docker volume prune                  # remove all unused volumes  ⚠ deletes data
```

Mount-option suffixes: `:ro` read-only, `:rw` read-write (default), and on SELinux systems
`:z` (shared) / `:Z` (private) to relabel — see §13.

---

## 7. Networks

Default driver is `bridge`. Containers on the **same user-defined bridge** can reach each other
**by container name** (built-in DNS) — this is why Compose services can use the service name as
a hostname.

```bash
docker network ls                    # list networks
docker network create mynet          # user-defined bridge (gets name-based DNS)
docker run -d --name db --network mynet postgres
docker run -d --name api --network mynet myapi   # 'api' can reach 'db' by name

docker network inspect mynet         # subnet, connected containers, gateway
docker network connect mynet web     # attach a running container
docker network disconnect mynet web
docker network prune                 # remove unused networks
```

Driver cheat: `bridge` (single host, default), `host` (share host's network stack, no
isolation, no port mapping needed), `none` (no networking), `overlay` (multi-host / Swarm),
`macvlan` (container gets its own MAC/IP on the LAN).

---

## 8. Docker Compose

Declarative multi-container stacks. One `compose.yaml` describes services, networks, volumes;
one command brings it up.

### Annotated compose file

```yaml
# compose.yaml  — the 'version:' top-level key is obsolete in V2; omit it.
services:
  web:
    build: .                       # build from local Dockerfile…
    # image: myapp:1.0             # …or pull/run a prebuilt image instead
    ports:
      - "8080:80"                  # host:container
    environment:
      - TZ=Europe/Berlin
    env_file:
      - .env                       # load extra vars from a file
    volumes:
      - ./src:/app                 # bind mount for live code
    depends_on:
      - db                         # start ordering (NOT readiness — see healthcheck)
    restart: unless-stopped
    networks: [appnet]
    healthcheck:                   # used by depends_on: condition: service_healthy
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 10s
      retries: 5

  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: example
    volumes:
      - dbdata:/var/lib/postgresql/data   # named volume = persistent data
    networks: [appnet]

volumes:
  dbdata:                          # declare the named volume

networks:
  appnet:                          # declare the user-defined network
```

### Everyday Compose commands

```bash
docker compose up -d                 # build/create/start the whole stack, detached
docker compose up -d --build         # force a rebuild of changed images first
docker compose down                  # stop + remove containers/networks (keeps volumes)
docker compose down -v               # …also remove named volumes  ⚠ deletes data

docker compose ps                    # status of services in this project
docker compose logs -f               # follow logs from ALL services
docker compose logs -f web           # …or just one
docker compose exec web bash         # shell into a running service
docker compose run --rm web pytest   # one-off command in a fresh throwaway container

docker compose build                 # build images without starting
docker compose pull                  # pull updated images for image-based services
docker compose restart web           # restart a single service
docker compose stop / start          # stop/start without removing
docker compose config                # render + validate the merged config (lint)
docker compose top                   # processes across services
```

### Useful extras

```bash
docker compose up -d --scale web=3   # run 3 replicas of 'web' (needs no fixed host port)
docker compose -f compose.prod.yaml up -d         # use a non-default file
docker compose -f base.yaml -f override.yaml up    # layer files (later wins)
docker compose --profile debug up    # only start services tagged with that profile
docker compose --env-file .env.prod up -d
```

`depends_on` only controls **start order**, not readiness. To wait for a dependency to be
*healthy*, give it a `healthcheck` and use the long form:
`depends_on: { db: { condition: service_healthy } }`.

---

## 9. Dockerfile quick reference

| Instruction | Purpose |
| --- | --- |
| `FROM` | Base image (and stage name: `FROM x AS build`) |
| `WORKDIR` | Set/create working dir for following instructions |
| `COPY` | Copy from build context into the image |
| `ADD` | Like COPY but also untars/fetches URLs (prefer COPY) |
| `RUN` | Execute a command at build time (creates a layer) |
| `ENV` | Persistent environment variable |
| `ARG` | Build-time variable (`--build-arg`), not in final image |
| `EXPOSE` | Document a port (doesn't publish it) |
| `VOLUME` | Declare a mount point |
| `USER` | Drop to a non-root user |
| `CMD` | Default command/args (overridable at `run`) |
| `ENTRYPOINT` | Fixed executable; `CMD` becomes its default args |
| `HEALTHCHECK` | How Docker tests container health |
| `LABEL` | Metadata key=value |

### Annotated example (multi-stage)

```dockerfile
# --- build stage ---
FROM golang:1.23 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download                  # cached unless go.mod/go.sum change
COPY . .
RUN CGO_ENABLED=0 go build -o /app ./cmd/server

# --- runtime stage: tiny final image ---
FROM gcr.io/distroless/static
COPY --from=build /app /app          # pull only the binary from the build stage
USER nonroot
EXPOSE 8080
ENTRYPOINT ["/app"]
```

Build-cache rule of thumb: **order layers from least- to most-frequently changed.** Copy
dependency manifests and install deps *before* copying source, so editing code doesn't bust the
dependency layer.

`CMD` vs `ENTRYPOINT`: `ENTRYPOINT` is the thing that always runs; `CMD` supplies default
arguments the caller can override. Use exec form (`["binary","arg"]`) not shell form to get
proper signal handling.

---

## 10. Registries

```bash
docker login                         # Docker Hub
docker login registry.example.com    # private/self-hosted registry

# Tag for the target registry, then push
docker tag myapp:1.0 registry.example.com/team/myapp:1.0
docker push registry.example.com/team/myapp:1.0

docker pull registry.example.com/team/myapp:1.0
docker logout registry.example.com
```

Image names are `[registry/][namespace/]name[:tag]`. No registry prefix ⇒ Docker Hub. No tag ⇒
`:latest` (avoid relying on it; pin tags).

---

## 11. System & cleanup

Docker hoards disk — stopped containers, dangling images, orphaned volumes, the build cache.
Reclaim it deliberately.

```bash
docker system df                     # how much space images/containers/volumes/cache use
docker system df -v                  # per-object breakdown (find the offender)

docker container prune               # remove all stopped containers
docker image prune                   # remove dangling images
docker image prune -a                # remove all images not used by a container
docker volume prune                  # remove unused volumes        ⚠ deletes data
docker network prune                 # remove unused networks
docker builder prune                 # clear the BuildKit build cache

# The big hammer — everything unused at once
docker system prune                  # containers + networks + dangling images + build cache
docker system prune -a --volumes     # …also all unused images AND volumes  ⚠⚠
```

Reclaim-space workflow when the disk is full: `docker system df -v` to see what's big →
targeted prune (usually `docker builder prune` + `docker image prune -a`) → only reach for
`system prune -a --volumes` when you accept losing all unused data.

---

## 12. Inspecting & debugging

```bash
docker inspect web                                   # full JSON
docker inspect --format '{{.State.Status}}' web      # just the status
docker inspect --format '{{.NetworkSettings.IPAddress}}' web   # the IP
docker inspect --format '{{json .Config.Env}}' web   # env vars as JSON

docker logs -f --tail 200 web                        # most-recent logs, follow
docker exec -it web sh                               # poke around inside
docker events                                        # live stream of daemon events
docker stats --no-stream                             # one-shot resource snapshot
docker diff web                                      # files changed vs the image
```

"Container won't start / exits immediately" workflow:

1. `docker ps -a` — confirm it's exited and check the exit code.
2. `docker logs <name>` — read the actual error.
3. `docker inspect <name>` — verify env, mounts, command, entrypoint.
4. Reproduce interactively: `docker run --rm -it --entrypoint sh <image>` and run the start
   command by hand.

Daemon-level logs (Linux): `journalctl -u docker -f` (see [[systemd]]).

---

## 13. Gotchas / paper cuts

| Symptom / trap | Reality |
| --- | --- |
| Added user to `docker` group | That group is **root-equivalent** — anyone in it can mount the host fs as root via a container. Treat it like sudo. |
| Bind mount "not found" / odd behavior | Host path must be **absolute** (`$PWD/x`, not `./x`) for the long `--mount` form; relative works for `-v` but resolves against CWD. |
| `Cannot start … port is already allocated` | Another process (or container) holds the host port. `docker ps` / `ss -tlnp`, change the `-p` host side. |
| Edited a file in the container, gone after restart | The writable layer is ephemeral. Persist via a volume or bind mount. |
| `down` deleted my database | `docker compose down -v` removes named volumes. Plain `down` keeps them. |
| `:latest` pulled a different image than yesterday | `latest` is just a mutable tag. Pin explicit versions. |
| Dockerfile edit didn't take effect | Layer cache. `--no-cache`, or reorder so the changed step isn't behind a cached one. |
| Permission denied on bind mount (Fedora/RHEL) | SELinux. Add `:z` (shared) or `:Z` (private), e.g. `-v "$PWD":/app:Z`. |
| `COPY failed: no such file` | The file must be inside the **build context** (the dir passed to `build`) and not excluded by `.dockerignore`. |
| Compose service can't reach another by name | They must share a network. Compose puts them on one by default — check you didn't override `networks:` on only one. |
| `docker-compose: command not found` | You have V2: use `docker compose` (space). |
| GUI app in a container won't display | X11: pass `-e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix`. Wayland is compositor-specific and more involved. |

---

## 14. Extras

### One-liners

```bash
docker stop $(docker ps -q)              # stop every running container
docker rm -f $(docker ps -aq)            # force-remove ALL containers
docker rmi $(docker images -q)           # remove ALL images
docker exec -it $(docker ps -q -f name=web) sh   # shell into the 'web' container
docker logs -f $(docker ps -q -f name=web)       # follow that container's logs
docker compose logs -f --tail 50         # tail all compose services
docker inspect -f '{{.Name}} -> {{.State.Health.Status}}' $(docker ps -q)  # health of all

# Find what's eating disk, then reclaim
docker system df -v
docker builder prune -f && docker image prune -af
```

### fish abbreviations

fish-native (`abbr`) — drop into `~/.config/fish/config.fish` so they expand inline:

```fish
abbr -a d   docker
abbr -a dc  'docker compose'
abbr -a dps 'docker ps'
abbr -a dpa 'docker ps -a'
abbr -a dim 'docker images'
abbr -a dex 'docker exec -it'
abbr -a dl  'docker logs -f --tail 100'
abbr -a dcu 'docker compose up -d'
abbr -a dcd 'docker compose down'
abbr -a dcl 'docker compose logs -f'
abbr -a dprune 'docker system prune -af'
```

### `--format` cookbook

Docker's `--format` takes Go templates. Handy ones:

```bash
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker images --format 'table {{.Repository}}:{{.Tag}}\t{{.Size}}'
docker inspect --format '{{.NetworkSettings.IPAddress}}' <container>
docker inspect --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{"\n"}}{{end}}' <container>
```

### Environment variables worth knowing

| Var | Effect |
| --- | --- |
| `DOCKER_BUILDKIT=1` | Use BuildKit for `docker build` (faster, better caching; default in current Docker) |
| `COMPOSE_FILE` | Default compose file(s), `:`-separated — skip repeating `-f` |
| `COMPOSE_PROJECT_NAME` | Override the project name (container/volume prefix) |
| `DOCKER_HOST` | Point the CLI at a remote/rootless daemon (e.g. `ssh://user@host`) |
| `DOCKER_DEFAULT_PLATFORM` | Force a platform, e.g. `linux/amd64` on Apple Silicon |

## Further reading
- [Docker documentation](https://docs.docker.com/)
- [Compose file reference](https://docs.docker.com/reference/compose-file/)
