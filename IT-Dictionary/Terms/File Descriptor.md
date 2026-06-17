---
type: "term"
branch: "Operating Systems"
aliases: ["fd", "Handle"]
tags: ["os"]
status: "developed"
---

# File Descriptor

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** fd, Handle

The small integer a Unix process uses to refer to an open I/O resource — file, socket, pipe, device. 0/1/2 are stdin/stdout/stderr; Windows calls the equivalent a **handle**.

**Context.** 'Everything is a file' cashes out here: the same read/write/close calls work on files, sockets, and pipes because they're all just fds. Shell redirection (`2>&1`) is fd manipulation; 'too many open files' is fd exhaustion (a leak or an undersized `ulimit`); and `lsof` — list open files — is the tool that turns fds into answers.

## See also

- [[Inode]]
- [[Socket]]
- [[Process]]
- [[Shell]]
- [[File System]]

## Further reading

- [Wikipedia: File descriptor](https://en.wikipedia.org/wiki/File_descriptor)
