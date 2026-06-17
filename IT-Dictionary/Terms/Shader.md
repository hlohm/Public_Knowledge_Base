---
type: "term"
branch: "Graphics, Media & HCI"
aliases: ["GPU Shader", "Pixel Shader", "Vertex Shader"]
tags: ["media", "hw"]
status: "developed"
---

# Shader

> **Branch:** [[14 - Graphics, Media & HCI|Graphics, Media & HCI]]
> **Also known as:** GPU Shader, Pixel Shader, Vertex Shader

A small program that runs on the GPU for every vertex or every pixel — originally to compute shading (hence the name), now the general mechanism for programmable graphics and the ancestor of GPU compute.

**Context.** Shaders are massive parallelism made tangible: the same function over millions of pixels per frame is the workload GPUs were *built* for, and compute shaders/CUDA generalized exactly that model into [[GPGPU|general GPU computing]]. Shader compilation stutter in games and 'shadertoy' demos are the everyday sightings; the vertex→fragment pipeline is the conceptual core.

## See also

- [[GPU]]
- [[Rendering]]
- [[SIMT]]
- [[Pixel]]
- [[Ray Tracing]]

## Further reading

- [Wikipedia: Shader](https://en.wikipedia.org/wiki/Shader)
