---
type: "term"
branch: "Graphics, Media & HCI"
aliases: ["Raster Graphics", "Bitmap"]
tags: ["media", "fundamental"]
status: "developed"
---

# Raster

> **Branch:** [[14 - Graphics, Media & HCI|Graphics, Media & HCI]]
> **Also known as:** Raster Graphics, Bitmap

Image representation as a grid of [[Pixel]]s — fixed [[Resolution]], scales badly upward, but can depict anything. PNG, JPEG, and your screen's framebuffer are raster; the opposite pole is [[Vector Graphics]].

**Context.** Raster vs vector is the first question of any graphics task: photos are inherently raster, logos and UI icons want vectors (infinite zoom, tiny files), and **rasterization** is the one-way bridge — vectors render *to* raster for display, but pixels never gracefully become curves again. Choosing raster for a logo is the mistake everyone makes exactly once.

## See also

- [[Pixel]]
- [[Vector Graphics]]
- [[Resolution]]
- [[Rendering]]
- [[Lossy Compression]]

## Further reading

- [Wikipedia: Raster graphics](https://en.wikipedia.org/wiki/Raster_graphics)
