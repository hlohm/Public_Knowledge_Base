---
type: cheatsheet
area: "Containers"
aliases: [Dockerfile, Containerfile, docker build]
tags: [containers, docker, dockerfile, image-build, oci]
status: working
---

# Dockerfile Patterns

> **Area:** [[Containers]]

Writing efficient, secure container images. Covers instruction syntax, layer caching, multi-stage builds, distroless images, and the patterns that separate production images from development hacks.

---

## 1. Instruction reference

```dockerfile
FROM debian:12-slim                 # base image; always pin a tag (not :latest)
ARG VERSION=1.0                     # build-time variable (not available at runtime)
ENV APP_HOME=/app                   # runtime environment variable
WORKDIR /app                        # set working directory (creates it if absent)
COPY src/ ./src/                    # copy files (preferred over ADD for local files)
ADD https://example.com/file.tar.gz /tmp/   # ADD: also fetches URLs and extracts tarballs
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*
EXPOSE 8080                         # document the port (does not publish; use -p at runtime)
USER 1000:1000                      # switch to non-root user (UID:GID)
ENTRYPOINT ["/usr/bin/myapp"]       # fixed executable; CMD provides default arguments
CMD ["--config", "/etc/myapp.conf"] # default arguments (overridden by docker run <cmd>)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -sf http://localhost:8080/health || exit 1
VOLUME ["/data"]                    # declare a mount point (prefer explicit -v at runtime)
LABEL org.opencontainers.image.version="1.0.0"  # OCI metadata
STOPSIGNAL SIGTERM                  # signal to stop the container (default SIGTERM)
SHELL ["/bin/bash", "-c"]           # override shell for RUN instructions
ONBUILD COPY . .                    # trigger on downstream FROM (for base images)
```

## 2. Layer caching: the critical mental model

Each instruction creates a layer. Layers are cached and reused if neither the instruction nor any earlier layer has changed. **Order instructions from least-to-most-frequently-changing** to maximise cache hits:

```dockerfile
# BAD: COPY . before installing dependencies — any source change busts the dependency cache
FROM python:3.12-slim
WORKDIR /app
COPY . .                        # changes on every commit ← cache bust
RUN pip install -r requirements.txt  # reinstalled every time

# GOOD: copy requirements first, then source
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .         # only changes when dependencies change
RUN pip install -r requirements.txt  # cached unless requirements.txt changed
COPY . .                        # copy source last
```

**Rule: put `COPY` for source code after installing dependencies.**

## 3. Multi-stage builds

Multi-stage builds produce small, secure images: the build stage contains compilers and build tools; the runtime stage contains only the compiled artifact.

```dockerfile
# Stage 1: build
FROM golang:1.22 AS builder
WORKDIR /build
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /myapp ./cmd/myapp

# Stage 2: runtime (scratch = empty image; no shell, no OS)
FROM scratch
COPY --from=builder /myapp /myapp
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
EXPOSE 8080
USER 65534:65534   # nobody
ENTRYPOINT ["/myapp"]
```

Common runtime bases ranked by attack surface:

| Base | Size | Shell | Package manager | Use when |
|---|---|---|---|---|
| `scratch` | 0 MB | no | no | Go/Rust static binaries |
| `gcr.io/distroless/static` | ~2 MB | no | no | Go binaries needing CA certs |
| `gcr.io/distroless/base` | ~20 MB | no | no | dynamic binaries (glibc) |
| `alpine:3` | ~7 MB | sh | apk | need a shell or tools |
| `debian:12-slim` | ~75 MB | bash | apt | glibc, wider compatibility |

## 4. Minimising image size

```dockerfile
# Combine RUN commands to avoid intermediate layers
RUN apt-get update \
 && apt-get install -y --no-install-recommends nginx \
 && rm -rf /var/lib/apt/lists/*   # clean apt cache in the same layer

# For package managers: always clean in the same RUN instruction
RUN dnf install -y nginx && dnf clean all
RUN pip install --no-cache-dir -r requirements.txt
RUN npm ci --only=production && npm cache clean --force

# .dockerignore — exclude unnecessary files from the build context
# .git
# node_modules
# *.md
# tests/
# .env
```

## 5. Security best practices

```dockerfile
# Non-root user (most important single security improvement)
RUN groupadd -r -g 1001 myapp && useradd -r -u 1001 -g myapp -M myapp
USER myapp:myapp

# Read-only filesystem (enforce at runtime with --read-only)
# In unit tests / compose: add volumes for writeable paths

# Don't embed secrets in images — use runtime env vars or secrets mounts:
# docker run --env-file .env myimage
# docker run --mount type=secret,id=mysecret myimage
# In Dockerfile: avoid ARG/ENV for secrets; they appear in docker history

# Pin versions of base images (use digest for maximum security)
FROM debian@sha256:<digest>
# Or at minimum a specific version tag, never :latest

# Drop capabilities at runtime (not in Dockerfile, but document the intent):
# docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myimage
```

## 6. ENTRYPOINT vs CMD patterns

```dockerfile
# Pattern 1: exec form (recommended) — no shell; signals go directly to PID 1
ENTRYPOINT ["/myapp"]
CMD ["--port", "8080"]

# Pattern 2: shell form — wraps in /bin/sh -c; signals go to sh, not the app (problematic)
ENTRYPOINT /myapp --port 8080   # avoid for long-running processes

# Pattern 3: wrapper script (for initialisation before exec)
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["myapp", "--port", "8080"]
# docker-entrypoint.sh should end with: exec "$@"
```

## 7. Build commands

```bash
docker build -t myapp:1.0 .
docker build -f Dockerfile.prod -t myapp:prod .
docker build --no-cache -t myapp:latest .             # force rebuild (ignore cache)
docker build --build-arg VERSION=2.0 -t myapp:2.0 .
docker build --target builder -t myapp:debug .        # build only up to a specific stage

docker image history myapp:1.0                        # show layers and sizes
dive myapp:1.0                                        # interactive layer explorer (if installed)
docker image inspect myapp:1.0 | jq '.[0].Config'    # image config and metadata
```

---

## Daily workflows

### "Build and run a quick local image"
```bash
docker build -t myapp:dev . && docker run --rm -p 8080:8080 myapp:dev
```

### "Verify the final image has no shell (distroless)"
```bash
docker run --rm myapp:prod sh     # should fail: exec: "sh" not found
```

### "Find large layers to optimise"
```bash
docker image history myapp:1.0 --no-trunc | sort -k4 -h
```

## Gotchas / Golden rules

1. **Never use `:latest` in production** — it is not a version; it points to whatever was pushed last; pin to a digest or specific tag.
2. **`EXPOSE` does nothing at runtime** — it is documentation; you still need `-p 8080:80` in `docker run` or the port mapping in Compose.
3. **Secrets in `ARG` or `ENV` are visible in `docker history`** — even if you `RUN unset MYSECRET`, the value is in the layer; use `--secret` (BuildKit) instead.
4. **Shell form of `ENTRYPOINT` breaks signal handling** — `docker stop` sends SIGTERM to `/bin/sh`, not your app; the app receives SIGKILL after the grace period and does not clean up. Use exec form: `ENTRYPOINT ["/myapp"]`.
5. **Build context is the whole directory by default** — `docker build .` sends everything in `.` to the daemon; a large `node_modules` or `.git` massively slows builds; always create a `.dockerignore`.
