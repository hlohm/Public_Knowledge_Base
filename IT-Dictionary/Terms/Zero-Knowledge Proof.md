---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["ZKP", "Zero-Knowledge Protocol"]
tags: ["crypto"]
status: "developed"
---

# Zero-Knowledge Proof

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** ZKP, Zero-Knowledge Protocol

A protocol in which a prover convinces a verifier that a statement is true — "I know the password", "this transaction is valid", "I paid for this service" — without revealing anything beyond the truth of the statement itself. A sound ZKP leaks zero bits of the underlying secret.

**Context.** The trick that decouples *proving* from *disclosing*. Practical systems (zk-SNARKs, zk-STARKs) power privacy-preserving payments and credentials: a client can prove it holds a valid subscription without linking the proof to its identity, which is how anonymity networks sell bandwidth without keeping user accounts. The same machinery underlies private blockchain transactions (Zcash) and verifiable computation, where a server proves it ran a program correctly without the client re-running it.

## See also

- [[Asymmetric Encryption]]
- [[Unlinkability]]
- [[Digital Signature]]

## Often confused with

- [[Digital Signature]] — a signature proves *who* said something; a ZKP proves *that* something is true while hiding the evidence.

## Further reading

- [Wikipedia: Zero-knowledge proof](https://en.wikipedia.org/wiki/Zero-knowledge_proof)
