---
type: "domain"
tags: [domain]
---

# Cryptography

> A sub-language of its own. You don't need to implement crypto, but you must read its dialect: symmetric vs asymmetric, hashing vs HMAC vs signature, the PKI ecosystem, TLS, and the post-quantum horizon.

## Terms in this domain

- [[Asymmetric Encryption]] — Key pair: public encrypts / verifies, private decrypts / signs.
- [[Block Cipher]] — Encrypts fixed-size chunks (AES).
- [[Certificate Authority]] — Trusted issuer of digital certificates.
- [[Chain of Trust]] — Sequence of certs from end-entity → intermediate CA(s) → root CA.
- [[CRL and OCSP]] — Mechanisms to check if a certificate has been revoked.
- [[Digital Signature]] — Hash of a message encrypted with the signer's private key; anyone with the public key can verify.
- [[Forward Secrecy]] — Compromise of long-term keys doesn't reveal past session data.
- [[Hash Function]] — One-way function producing a fixed-length digest.
- [[HMAC]] — Hash-based Message Authentication Code.
- [[HSM]] — Hardware Security Module.
- [[IV]] — Initialization Vector.
- [[KDF]] — Key Derivation Function.
- [[Key Exchange]] — Protocol to establish a shared secret over an insecure channel.
- [[mTLS]] — Mutual TLS.
- [[Nonce]] — Number used once.
- [[Pepper]] — A site-wide secret added alongside the salt, stored separately (e.g.
- [[PKI]] — Public Key Infrastructure.
- [[Plaintext and Ciphertext]] — Pre- and post-encryption data.
- [[PQC]] — Post-Quantum Cryptography.
- [[Salt]] — Random data added to a password before hashing to defeat rainbow tables.
- [[Symmetric Encryption]] — Same key encrypts and decrypts.
- [[TLS]] — Transport Layer Security.
- [[X.509]] — Standard certificate format binding a public key to an identity, signed by a CA.

---
← Back to [[_Home]]