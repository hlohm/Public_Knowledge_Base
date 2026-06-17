---
type: "term"
branch: "Operating Systems"
tags: [os]
status: "developed"
---

# Inode

> **Branch:** [[03 - Operating Systems|Operating Systems]]

The on-disk structure (in Unix-style file systems) holding a file's metadata and the locations of its data blocks — everything *except* its name.

**Context.** Because the name lives in a directory pointing at the inode (not in the inode), one file can have several names: that's a hard link. Running out of inodes can fill a disk that still shows free space.

## See also

- [[File System]]
- [[Hard Link]]
- [[Symlink]]

## Further reading

- [Wikipedia: Inode](https://en.wikipedia.org/wiki/Inode)
