---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["Key Derivation Function"]
tags: ["crypto"]
status: "developed"
---

# KDF

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** Key Derivation Function

**K**ey **D**erivation **F**unction. Turns a password into a key, deliberately slowly. Modern: **Argon2**; older but solid: **bcrypt**, **scrypt**, **PBKDF2**.

**Context.** Two distinct jobs share the name: password hashing (Argon2, bcrypt — deliberately slow to brute-force) and key derivation from existing secrets (HKDF — fast, used inside TLS and Signal). Choosing a fast hash like SHA-256 for passwords is the canonical mistake; tune the work factor so login costs ~100ms.

## See also

- [[Salt]]
- [[Pepper]]
- [[Hash Function]]

## Further reading

- [OWASP: Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
