---
type: "domain"
tags: [domain]
---

# Cryptography

> A sub-language of its own. You don't need to implement crypto, but you must read its dialect: symmetric vs asymmetric, hashing vs HMAC vs signature, the PKI ecosystem, TLS, and the post-quantum horizon.

## Terms in this domain

- [[ACME]] — Automatic Certificate Management Environment — the Let's Encrypt protocol.
- [[Asymmetric Encryption]] — Key pair: public encrypts / verifies, private decrypts / signs.
- [[Block Cipher]] — Encrypts fixed-size chunks (AES).
- [[Certificate Authority]] — Trusted issuer of digital certificates.
- [[Certificate Pinning]] — Hardcoding which certificate or key a client will accept.
- [[Chain of Trust]] — A sequence of cryptographic vouchers from a trusted root down to a leaf, where each link signs the next — so trusting one anchor transitively validates the whole path.
- [[Code Signing]] — Signing executables and packages so origin and integrity verify.
- [[CRL and OCSP]] — Mechanisms to check if a certificate has been revoked.
- [[CSR]] — Certificate Signing Request.
- [[Digital Signature]] — Hash of a message encrypted with the signer's private key; anyone with the public key can verify.
- [[DNS-01 Challenge]] — The ACME challenge type that proves control of a domain by publishing a given token as a `_acme-challenge` TXT record, rather than serving a file over HTTP.
- [[Forward Secrecy]] — Compromise of long-term keys doesn't reveal past session data.
- [[Hash Function]] — One-way function producing a fixed-length digest.
- [[HMAC]] — Hash-based Message Authentication Code.
- [[HSM]] — Hardware Security Module.
- [[IV]] — Initialization Vector.
- [[KDF]] — Key Derivation Function.
- [[Key Exchange]] — Protocol to establish a shared secret over an insecure channel.
- [[mTLS]] — Mutual TLS.
- [[Nonce]] — Number used once.
- [[OpenPGP]] — Content-level encryption and signing with self-managed keys and no central certificate authority.
- [[Pepper]] — A site-wide secret added alongside the salt, stored separately (e.g.
- [[PKI]] — Public Key Infrastructure.
- [[Plaintext and Ciphertext]] — Pre- and post-encryption data.
- [[PQC]] — Post-Quantum Cryptography.
- [[S-MIME]] — Signing and encrypting mail content with X.509 certificates, so intermediaries carrying the message cannot read it.
- [[Salt]] — Random data added to a password before hashing to defeat rainbow tables.
- [[SNI]] — The TLS extension where the client states the hostname it wants at the start of the handshake, so a server hosting many sites on one IP can present the right certificate.
- [[STARTTLS]] — A command upgrading an open plaintext connection to TLS — deployable everywhere, and strippable by an active attacker.
- [[Symmetric Encryption]] — Same key encrypts and decrypts.
- [[TLS]] — Transport Layer Security.
- [[Wildcard Certificate]] — A TLS certificate valid for all single-label subdomains of a name via a `*.example.com` entry, so one cert covers `a.example.com`, `b.example.com`, and so on.
- [[X.509]] — Standard certificate format binding a public key to an identity, signed by a CA.
- [[Zero-Knowledge Proof]] — Proving a statement true without revealing anything beyond its truth.

---
← Back to [[_Home]]