---
type: "term"
branch: "DevOps & SRE"
aliases: ["Deployment Key"]
tags: ["devops", "iam"]
status: "developed"
---

# Deploy Key

> **Branch:** [[12 - DevOps & SRE|DevOps & SRE]]
> **Also known as:** Deployment Key

An [[SSH]] key granted access to exactly **one repository** on a code forge (GitHub, GitLab, Gitea), read-only or read-write — as opposed to a personal key or token, which carries the whole account's reach.

**Context.** The point is blast radius: a build server, CI runner, or semi-trusted automation host that needs one repo gets a key that *can't* touch anything else, and revoking it is one click that affects nothing else. That makes deploy keys the accepted way to put a credential on a machine you deliberately don't fully trust — the key is scoped, auditable, and disposable. Standard hygiene: one dedicated keypair per repo per host (never reuse), pair it with a host alias in `~/.ssh/config` so the right key meets the right remote, and record it in the password manager like any other [[Secret]]. Forges enforce the no-reuse rule anyway — a key can be a deploy key for only one repo.

## See also

- [[SSH]]
- [[Secret]]
- [[Least Privilege]]
- [[CI]]

## Often confused with

- [[Bearer Token]] — a personal access token authenticates *you* with account-wide (or token-scoped) reach over HTTPS; a deploy key authenticates *a machine* to a single repo over SSH.

## Further reading

- [GitHub Docs: Managing deploy keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys)
