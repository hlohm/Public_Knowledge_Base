---
type: "map"
tags: [map, hardware]
---

# Hardware & Architecture

> What the machine is physically made of and how the CPU actually executes — registers, caches, buses, ISAs.

## Terms in this branch (38)

- [[ALU]] — The combinational circuit that actually computes — integer add/subtract, AND/OR/XOR, shifts, comparisons — taking operands from registers and setting status flags (zero, carry, overflow).
- [[BIOS]] — The original PC firmware: initialize hardware (POST), find a boot device, load the first sector (MBR), go.
- [[Branch Divergence]] — The performance penalty on a SIMT machine when threads in the same warp take different paths through a conditional, forcing the hardware to run each path serially with the inactive lanes masked off.
- [[Branch Prediction]] — A CPU mechanism that guesses the outcome of a conditional branch so the pipeline can keep fetching and executing instead of stalling until the branch resolves.
- [[Cache]] — Small, fast memory near the CPU that holds recently- or likely-used data so the processor avoids slow trips to main RAM.
- [[Cache Coherence]] — The guarantee that, in a system where several caches sit over shared memory, every processor sees a consistent value for any given memory location.
- [[Cache Line]] — The unit of transfer between memory and CPU caches — typically 64 bytes.
- [[Cache Miss]] — When data the CPU needs isn't in the cache, forcing a slower fetch from a lower level (or RAM).
- [[CISC]] — A design with a large set of powerful, variable-length instructions, some doing whole operations (memory-to-memory add) in one step.
- [[Core]] — One independent processing unit on a CPU die — its own ALUs, registers, L1/L2 cache, instruction stream.
- [[CPU]] — The component that executes instructions — fetching them from memory, decoding, and performing arithmetic, logic, and control.
- [[Firmware]] — Low-level software stored on a device that controls its hardware directly — sitting between pure hardware and the operating system.
- [[GPU]] — A processor with thousands of simple cores optimised for doing the same operation across huge amounts of data in parallel (originally pixels).
- [[Instruction Set]] — The contract between hardware and software: the set of instructions a CPU understands, its registers, and memory model.
- [[Interrupt]] — A signal that makes the CPU pause its current work, save state, and jump to a handler to deal with an event — a key press, a packet arriving, a timer firing.
- [[Latency Hiding]] — Keeping execution units busy during long-latency operations (chiefly memory access) by having other independent work ready to run, instead of by making the slow operation itself faster.
- [[Locality of Reference]] — The empirical law that programs reuse what they just touched (temporal locality) and touch what's next to it (spatial locality).
- [[Memory Hierarchy]] — The pyramid of storage from registers (sub-ns, bytes) through L1/L2/L3 cache (ns, MBs) and RAM (~100 ns, GBs) to SSD (~100 µs) and beyond — each level bigger, slower, and cheaper per byte than the one above.
- [[MMU]] — Hardware that translates the virtual addresses programs use into physical RAM addresses, and enforces access permissions, page by page.
- [[Moore's Law]] — The observation (Gordon Moore, 1965) that the number of transistors on a chip roughly doubles every ~two years.
- [[NUMA]] — A shared-memory architecture in which memory is physically split among processors (sockets), so a core reaches its local memory faster than another socket's memory.
- [[NVLink]] — NVIDIA's high-bandwidth interconnect that lets GPUs read and write each other's memory directly — far faster than PCIe — and, at rack scale, lets many GPUs share a single memory fabric.
- [[Out-of-Order Execution]] — A CPU technique that executes instructions as their inputs become ready rather than in strict program order, while retiring results in order, to keep execution units busy through stalls.
- [[Pipeline]] — Overlapping the stages of consecutive instructions (fetch, decode, execute…) like an assembly line, so a new instruction can start before the previous finishes.
- [[Protection Ring]] — Hardware-enforced privilege levels that bound what code may do.
- [[RAM]] — Fast, volatile working memory the CPU reads and writes directly.
- [[Register]] — A tiny, extremely fast storage location inside the CPU holding a value the processor is working on right now.
- [[RISC]] — A design philosophy favouring a small set of simple, fixed-length instructions that each do little but execute fast, leaning on the compiler to compose them.
- [[SIMD]] — An execution model in which one instruction operates on several data elements at once, through wide vector registers and parallel lanes.
- [[SIMT]] — The GPU execution model in which many threads are programmed as if independent, but the hardware runs them in fixed-size lockstep groups that share one instruction stream.
- [[Speculative Execution]] — Executing instructions before it is certain they are needed — typically past a predicted branch — and discarding the work if the guess was wrong.
- [[SSD]] — Non-volatile storage built from flash memory with no moving parts, vastly faster than a spinning hard disk, especially for random access.
- [[Streaming Multiprocessor]] — The core building block of an NVIDIA GPU: a self-contained processor with its own warp schedulers, register file, execution units and L1/shared memory.
- [[Systolic Array]] — A hardware architecture: a regular grid of simple processing elements that rhythmically pass data to their neighbours, computing operations like matrix multiplication with minimal control logic and memory traffic.
- [[Tensor Core]] — A specialised GPU execution unit that performs a small matrix multiply-accumulate as a single operation, sharply accelerating the dense linear algebra at the heart of deep learning.
- [[TPM]] — A dedicated secure crypto-processor (a discrete chip, or a firmware equivalent) that stores keys, performs cryptographic operations, and holds integrity measurements in tamper-resistant Platform Configuration Registers (PCRs).
- [[UEFI]] — The modern replacement for legacy BIOS: the [[Firmware]] interface that initialises hardware and hands control to an operating-system [[Boot Loader]].
- [[Warp]] — The fixed-size group of GPU threads (32 on NVIDIA hardware) that execute one instruction in lockstep under the SIMT model.

---
← Back to [[_Home]]
