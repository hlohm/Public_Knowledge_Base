---
type: "term"
branch: "Operating Systems"
aliases: ["Filesystem in Userspace"]
tags: [os]
status: "developed"
---

# FUSE

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** Filesystem in Userspace

A kernel interface that lets an ordinary userspace process implement a filesystem: the kernel accepts normal file operations and forwards them to the process, which answers them however it likes — from an SSH connection, a cloud bucket, an archive file.

**Context.** FUSE is why you can `mount` things that aren't disks without writing kernel code: sshfs (a remote host over [[SSH]]), rclone/s3fs (object storage), archivemount. Perfect for ad-hoc jobs like mounting remote storage as a backup target. The costs and gotchas: every operation round-trips through userspace, so it's slower than a native mount; by default only the mounting user sees the files (`allow_other` changes that); and each tool brings its own remote-path syntax quirks — sshfs, for instance, treats `host:` (login directory) and `host:/` (root) differently, which matters on servers that chroot you.

## See also

- [[File System]]
- [[User Space]]
- [[System Call]]
- [[SSH]]

## Further reading

- [Wikipedia: Filesystem in Userspace](https://en.wikipedia.org/wiki/Filesystem_in_Userspace)
