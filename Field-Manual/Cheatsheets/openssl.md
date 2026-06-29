---
type: cheatsheet
area: "Networking & Protocols"
aliases: [tls, ssl, openssl]
tags: [tls, certificates, pki, openssl, security]
status: working
---

# TLS / openssl

> **Area:** [[Networking & Protocols]]

Inspecting certificates, testing TLS endpoints, generating keys and CSRs, and working with certificate files. `openssl` is the Swiss Army knife; `curl` and `nmap` fill in gaps for quick endpoint checks.

---

## 1. Inspect a server's certificate

```bash
# Connect and display the certificate chain
openssl s_client -connect example.com:443 -showcerts < /dev/null

# Show just the end-entity certificate in human-readable form
openssl s_client -connect example.com:443 < /dev/null 2>/dev/null \
  | openssl x509 -noout -text

# Quick: expiry date only
openssl s_client -connect example.com:443 < /dev/null 2>/dev/null \
  | openssl x509 -noout -dates

# Subject and issuer
openssl s_client -connect example.com:443 < /dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer

# SANs (Subject Alternative Names — the hostnames the cert covers)
openssl s_client -connect example.com:443 < /dev/null 2>/dev/null \
  | openssl x509 -noout -ext subjectAltName

# SNI: when a server hosts multiple certs, specify the hostname
openssl s_client -connect 192.0.2.1:443 -servername example.com < /dev/null
```

## 2. Parse a certificate file

```bash
openssl x509 -in cert.pem -noout -text         # full human-readable dump
openssl x509 -in cert.pem -noout -subject       # subject DN
openssl x509 -in cert.pem -noout -issuer        # issuer DN
openssl x509 -in cert.pem -noout -dates         # notBefore / notAfter
openssl x509 -in cert.pem -noout -fingerprint -sha256   # fingerprint
openssl x509 -in cert.pem -noout -serial        # serial number
openssl x509 -in cert.pem -noout -ext subjectAltName    # SANs

# Convert DER → PEM
openssl x509 -in cert.der -inform DER -out cert.pem -outform PEM

# Convert PEM → DER
openssl x509 -in cert.pem -out cert.der -outform DER
```

## 3. Generate keys and certificates

```bash
# Generate a private key (EC — preferred; RSA as fallback)
openssl ecparam -name prime256v1 -genkey -noout -out key.pem       # P-256
openssl ecparam -name secp384r1  -genkey -noout -out key.pem       # P-384
openssl genrsa -out key.pem 4096    # RSA 4096 (for legacy systems)

# Generate a Certificate Signing Request (CSR)
openssl req -new -key key.pem -out csr.pem \
  -subj "/C=DE/ST=Berlin/L=Berlin/O=Example GmbH/CN=example.com"

# Add SANs to the CSR (required for modern browsers)
openssl req -new -key key.pem -out csr.pem \
  -subj "/CN=example.com" \
  -addext "subjectAltName=DNS:example.com,DNS:www.example.com"

# Inspect a CSR
openssl req -in csr.pem -noout -text

# Self-signed certificate (dev / internal use only)
openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:P-256 \
  -keyout key.pem -out cert.pem -days 365 -nodes \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
```

## 4. Verify and validate

```bash
# Verify a certificate against a CA bundle
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt cert.pem

# Verify against a specific CA
openssl verify -CAfile ca.pem cert.pem

# Verify a certificate chain (include intermediate)
openssl verify -CAfile ca.pem -untrusted intermediate.pem cert.pem

# Check that a private key matches a certificate
openssl x509 -noout -modulus -in cert.pem | openssl md5
openssl rsa  -noout -modulus -in key.pem  | openssl md5
# The md5 hashes must match

# Check certificate revocation via OCSP
openssl ocsp \
  -issuer issuer.pem \
  -cert cert.pem \
  -url $(openssl x509 -in cert.pem -noout -ocsp_uri) \
  -text
```

## 5. TLS version and cipher testing

```bash
# Test which TLS versions a server accepts
openssl s_client -connect example.com:443 -tls1   2>&1 | grep -E 'CONNECTED|alert'
openssl s_client -connect example.com:443 -tls1_1 2>&1 | grep -E 'CONNECTED|alert'
openssl s_client -connect example.com:443 -tls1_2 2>&1 | grep -E 'CONNECTED|alert'
openssl s_client -connect example.com:443 -tls1_3 2>&1 | grep -E 'CONNECTED|alert'

# Test a specific cipher suite
openssl s_client -connect example.com:443 -cipher 'ECDHE-RSA-AES256-GCM-SHA384' < /dev/null

# List available ciphers
openssl ciphers -v 'ALL:COMPLEMENTOFALL'
openssl ciphers -v 'HIGH:!aNULL:!MD5'    # recommended filter: strong only

# Start date / protocol from s_client output
openssl s_client -connect example.com:443 < /dev/null 2>&1 | grep -E 'Protocol|Cipher'
```

## 6. Certificate bundles and formats

```bash
# View all certs in a bundle (PEM can contain multiple)
openssl crl2pkcs7 -nocrl -certfile bundle.pem | openssl pkcs7 -print_certs -noout -text

# Extract certs from a PKCS#12 (.pfx / .p12)
openssl pkcs12 -in cert.pfx -clcerts -nokeys -out cert.pem     # certificate only
openssl pkcs12 -in cert.pfx -nocerts -nodes -out key.pem       # private key (unencrypted)
openssl pkcs12 -in cert.pfx -cacerts -nokeys -out chain.pem    # CA chain

# Create a PKCS#12 from PEM files
openssl pkcs12 -export -in cert.pem -inkey key.pem -certfile chain.pem -out bundle.pfx
```

## 7. Hashing and encoding (quick reference)

```bash
openssl dgst -sha256 file.txt           # SHA-256 hash of a file
openssl dgst -sha256 -sign key.pem -out sig.bin file.txt   # sign
openssl dgst -sha256 -verify pubkey.pem -signature sig.bin file.txt  # verify

openssl rand -hex 32                    # 32 random bytes in hex (e.g., for secrets)
openssl rand -base64 48                 # 48 random bytes in base64

openssl enc -aes-256-cbc -in plain.txt -out encrypted.bin -k <passphrase>
openssl enc -d -aes-256-cbc -in encrypted.bin -out plain.txt -k <passphrase>
```

---

## Daily workflows

### "Check when a certificate expires"
```bash
openssl s_client -connect example.com:443 < /dev/null 2>/dev/null \
  | openssl x509 -noout -dates
```

### "Confirm a new cert covers all required hostnames"
```bash
openssl s_client -connect example.com:443 < /dev/null 2>/dev/null \
  | openssl x509 -noout -ext subjectAltName
```

### "Generate a key + self-signed cert for local testing"
```bash
openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:P-256 \
  -keyout key.pem -out cert.pem -days 365 -nodes \
  -subj "/CN=localhost" -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
```

### "Verify that a key and cert belong together"
```bash
diff <(openssl x509 -noout -modulus -in cert.pem | md5sum) \
     <(openssl rsa  -noout -modulus -in key.pem  | md5sum)
```

## Gotchas / Golden rules

1. **`< /dev/null` is required to prevent `s_client` from hanging** — without it, `s_client` waits for stdin after connecting; redirect from `/dev/null` so it exits immediately after the handshake.
2. **SANs are mandatory; CN is ignored by modern browsers** — a cert with only a CN field will fail validation in Chrome, Firefox, and Safari since ~2017; always include at least one SAN.
3. **`-nodes` means "no DES encryption" on the private key, not "no nodes"** — it outputs the private key in plaintext; never use `-nodes` for production keys stored at rest.
4. **PKCS#12 / PFX passphrase is required** — some tools (Windows, Java) will not import a `.p12` without a passphrase; use `-passout pass:<pw>` when creating.
5. **`openssl verify` only checks the certificate chain, not expiry by default** — to also check the validity period, add `-check_time`.
