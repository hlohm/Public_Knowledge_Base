---
type: cheatsheet
area: "CLI Tools"
aliases: []
tags: [http, api, download, tls, networking]
status: working
---

# curl

> **Area:** [[CLI Tools]]

Transfer data to or from a server using any of curl's supported protocols — HTTP(S), FTP, SFTP, SCP, and more. The everyday tool for testing APIs, downloading files, and inspecting TLS.

> Versions differ. `--json` (shorthand for `-H 'Content-Type: application/json' -H 'Accept: application/json' -d`) requires curl 7.82+.

---

## 1. Basic requests

```bash
curl https://example.com                      # GET; print body to stdout
curl -I https://example.com                   # HEAD only — response headers, no body
curl -X POST https://api.example.com/things   # explicit method (uppercase)
curl -X DELETE https://api.example.com/things/1
```

## 2. Headers

```bash
curl -H 'Authorization: Bearer <token>' https://api.example.com/me
curl -H 'Content-Type: application/json' \
     -H 'Accept: application/json' \
     https://api.example.com/data

# Send multiple headers; -H can be repeated
curl -H 'X-Request-ID: abc123' -H 'X-Client: test' https://example.com
```

## 3. Request body

```bash
# POST JSON (7.82+)
curl --json '{"name":"Alice","role":"admin"}' -X POST https://api.example.com/users

# POST JSON (older curl)
curl -X POST \
     -H 'Content-Type: application/json' \
     -d '{"name":"Alice"}' \
     https://api.example.com/users

# Read body from a file
curl -X POST -H 'Content-Type: application/json' -d @payload.json https://api.example.com/

# HTML form (urlencoded)
curl -d 'user=alice&pass=secret' https://example.com/login

# Multipart form (file upload)
curl -F 'file=@/path/to/file.csv' -F 'label=import' https://example.com/upload
```

## 4. Authentication

```bash
curl -u alice:secret https://example.com/protected   # HTTP Basic; curl encodes to Base64
curl -u alice https://example.com/protected          # prompt for password

# Bearer token
curl -H 'Authorization: Bearer <token>' https://api.example.com/

# Digest auth
curl --digest -u alice:secret https://example.com/digest/
```

## 5. Output and download

```bash
curl -o output.html https://example.com               # save to named file
curl -O https://example.com/file.tar.gz               # save using the remote filename
curl -L -O https://example.com/redirect-to-file       # -L follows redirects

# Resume an interrupted download
curl -C - -O https://example.com/large-file.iso

# Download silently (no progress) and pipe
curl -s https://api.example.com/data | jq .

# Show progress bar instead of stats
curl --progress-bar -O https://example.com/large-file.iso

# Rate-limit the transfer (useful on production hosts)
curl --limit-rate 1M -O https://example.com/large-file.iso
```

## 6. TLS and certificates

```bash
# Skip certificate verification — useful for self-signed certs in dev; never on production
curl -k https://self-signed.example.com

# Specify a CA bundle
curl --cacert /path/to/ca-bundle.pem https://internal.example.com

# Client certificate authentication (mTLS)
curl --cert /path/to/client.crt --key /path/to/client.key https://mtls.example.com

# Inspect a server's TLS certificate without making a full request
curl -svo /dev/null https://example.com 2>&1 | grep -A20 'Server certificate'

# Force a specific TLS version
curl --tls-max 1.2 https://example.com    # cap at TLS 1.2
curl --tlsv1.3 https://example.com        # require TLS 1.3 minimum
```

## 7. Debugging

```bash
curl -v https://example.com              # verbose: shows request + response headers, TLS handshake
curl -sv https://example.com 2>&1        # verbose to stdout for piping/grep

# Full protocol trace to file
curl --trace trace.txt https://example.com

# Show only response headers (useful for quick status check)
curl -sI https://example.com | head -5

# Time the request
curl -w "\n%{time_total}s total  %{http_code}\n" -so /dev/null https://example.com

# Full timing breakdown
curl -w "@-" -so /dev/null https://example.com <<'EOF'
     dns: %{time_namelookup}s
 connect: %{time_connect}s
     tls: %{time_appconnect}s
  ttfb:   %{time_starttransfer}s
   total: %{time_total}s
    code: %{http_code}
EOF
```

## 8. Config and reuse

```bash
# ~/.curlrc — defaults applied to every curl invocation
# silent = true
# show-error = true

# Per-request config file
curl -K config-file.txt https://example.com
# config-file.txt:
#   header = "Authorization: Bearer <token>"
#   silent

# Cookies: save and reuse session
curl -c cookies.txt https://example.com/login -d 'user=alice&pass=secret'
curl -b cookies.txt https://example.com/dashboard
```

---

## Daily workflows

### "Test a REST API endpoint"
```bash
curl -s -H 'Authorization: Bearer <token>' \
     https://api.example.com/v1/users | jq .
```

### "POST JSON and inspect the response"
```bash
curl -s --json '{"key":"value"}' -X POST https://api.example.com/resource \
  | jq '{id: .id, status: .status}'
```

### "Check if a site redirects to HTTPS"
```bash
curl -sIL http://example.com | grep -E '^HTTP|^Location'
```

### "Debug a failing TLS connection"
```bash
curl -v https://example.com 2>&1 | grep -E 'SSL|TLS|certificate|error'
```

### "Download a file, verify it arrived complete"
```bash
curl -L -O --retry 3 https://example.com/release.tar.gz
sha256sum -c release.tar.gz.sha256
```

## Files & locations

| Path | What |
|---|---|
| `~/.curlrc` | User default options (one option per line) |
| `/etc/curlrc` | System-wide defaults |

## Gotchas / Golden rules

1. **`-s` suppresses the progress meter but also errors** — pair it with `-S` (`--show-error`) so failures still print: `curl -sS`.
2. **`-k` / `--insecure` is never acceptable in production scripts** — if you need a custom CA, use `--cacert`.
3. **Redirects are not followed by default** — add `-L` whenever the target URL might redirect (download links, shortened URLs, HTTP→HTTPS).
4. **`-d` sends urlencoded by default** — if you omit `-H 'Content-Type: application/json'` your JSON string arrives as form data; the server sees garbage.
5. **Credentials in command history** — use `curl -u alice` (password prompted) or a `.netrc` file instead of `-u alice:secret` in a shared shell.
