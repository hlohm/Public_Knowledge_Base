---
type: "map"
tags: [map, os]
---

# Operating Systems

> The layer that turns hardware into something programs can share safely: processes, memory, files, the kernel.

## Terms in this branch (37)

- [[Atomic Write]] — Updating a file so a crash mid-write leaves either the whole old or whole new content, never a torn mix — write-to-temp, fsync, rename.
- [[Boot Loader]] — The small program that bridges firmware and OS: loaded by UEFI/BIOS, it loads the kernel (plus initramfs/drivers) and hands over control.
- [[Capabilities]] — Root's power split into ~40 discrete privileges a process can hold or drop individually.
- [[Context Switch]] — Saving the state of one process/thread and restoring another's so a single CPU can interleave many of them, creating the illusion of simultaneity.
- [[Critical Section]] — A stretch of code that touches shared state and therefore must not be executed by more than one thread at a time — the region a [[Mutex]] or [[Semaphore]] exists to protect.
- [[Daemon]] — A long-running background process with no controlling terminal, providing a service (web server, sshd, cron).
- [[Deadlock]] — A standstill where two or more threads each hold a resource the other needs and none will release, so all wait forever.
- [[Driver]] — The kernel-side translator between the OS's generic device interfaces and one piece of hardware's actual registers, queues, and quirks.
- [[Drop-in Unit]] — A small `.conf` fragment in a `<unit>.d/` directory that systemd merges over a unit file — override settings without touching the vendor's file.
- [[File Descriptor]] — The small integer a Unix process uses to refer to an open I/O resource — file, socket, pipe, device.
- [[File System]] — The scheme an OS uses to organise data on storage into files and directories, tracking names, locations, sizes, permissions, and timestamps.
- [[FUSE]] — A kernel interface that lets an ordinary userspace process implement a filesystem — sshfs, rclone and friends.
- [[Inode]] — The on-disk structure (in Unix-style file systems) holding a file's metadata and the locations of its data blocks — everything except its name.
- [[Kernel]] — The core of an OS, running in privileged mode with full hardware access.
- [[Kernel Space]] — The privileged execution environment of the kernel and (in monolithic designs) its drivers: full hardware access, shared address space, no safety net.
- [[Locale]] — The bundle of settings telling programs how to format dates, numbers and messages for a human — per-category via LANG and the LC_* variables.
- [[Microkernel]] — Kernel design that keeps only the irreducible minimum in kernel space (scheduling, IPC, basic memory) and runs drivers, file systems, and services as isolated user-space processes talking via messages.
- [[Monolithic Kernel]] — Kernel design where the whole OS core — scheduling, memory, file systems, drivers, network stack — runs as one program in kernel space.
- [[Mutex]] — A synchronisation primitive ensuring only one thread enters a critical section at a time, preventing concurrent access to shared data.
- [[Operating System]] — The software layer that manages hardware and provides services — scheduling, memory, files, devices, security — so programs can run without each reinventing them.
- [[Page Fault]] — An exception raised when a program accesses a virtual page that isn't currently in physical RAM, prompting the OS to fetch or map it.
- [[Paging]] — Dividing virtual and physical memory into fixed-size pages (typically 4 KiB) and mapping between them via page tables, so each process sees its own contiguous address space over scattered physical frames.
- [[Permissions]] — Rules governing who may read, write, or execute a file or directory.
- [[Preemption]] — The scheduler's right to interrupt a running task at any time (via timer interrupt) and give the CPU to another — as opposed to cooperative multitasking, where tasks must yield voluntarily.
- [[Process]] — A running program together with its own isolated address space, file handles, and execution state.
- [[Race Condition]] — A bug where the result depends on the unpredictable timing of concurrent operations on shared state — e.g.
- [[Resilvering]] — Rebuilding redundancy onto a replacement disk from the surviving members — ZFS's word for a RAID rebuild, copying live data only.
- [[Runtime Power Management]] — The kernel framework that suspends individual devices to low-power states while the system keeps running — a laptop dGPU dropping to D3cold.
- [[Scheduler]] — The kernel component that decides which ready process/thread runs next and for how long, balancing fairness, responsiveness, and throughput.
- [[Semaphore]] — A counter-based synchronisation primitive (Dijkstra) that lets up to N threads proceed; threads wait when the count hits zero and signal when done.
- [[Shell]] — A program that interprets your commands and runs other programs — the text interface to the OS.
- [[Swap]] — Disk space (swap partition/file, Windows pagefile) used as overflow for RAM: when memory pressure rises, the kernel evicts cold pages to disk and reloads them on access.
- [[System Call]] — The controlled gateway a user-space program uses to ask the kernel for a privileged service — open a file, send on a socket, allocate memory.
- [[Thread]] — An independent flow of execution within a process.
- [[User Space]] — Where ordinary programs run: unprivileged CPU mode, own virtual address space, every privileged action requested from the kernel via [[System Call]].
- [[Virtual Memory]] — An abstraction giving each process its own large, contiguous-looking address space, mapped behind the scenes onto physical RAM (and disk) in fixed-size pages.
- [[ZFS]] — A combined filesystem and volume manager: pooled storage, copy-on-write, end-to-end checksums, snapshots, and built-in redundancy in one design.

---
← Back to [[_Home]]
