---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam", "protocol"]
status: "developed"
---

# JWT

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

**J**SON **W**eb **T**oken. Compact, signed (and optionally encrypted) JSON containing claims. Pronounced 'jot'.

**Context.** Self-contained and stateless, which is both the appeal and the trap: a JWT can't be revoked before expiry without reintroducing server-side state, so keep lifetimes short. Implementation classics: `alg:none` acceptance, signature-verification skips, and secrets weak enough to crack offline. Decode-and-inspect at jwt.io is a daily debugging move; remember signed ≠ encrypted — anyone can *read* the claims.

## See also

- [[Claim]]
- [[Token]]
- [[OIDC]]

## Further reading

- [RFC 7519: JSON Web Token](https://datatracker.ietf.org/doc/html/rfc7519)
