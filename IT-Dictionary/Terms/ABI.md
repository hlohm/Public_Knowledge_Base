---
type: "term"
branch: "Software Engineering"
aliases: ["Application Binary Interface"]
tags: [se]
status: "developed"
---

# ABI

> **Branch:** [[08 - Software Engineering|Software Engineering]]
> **Also known as:** Application Binary Interface

The binary-level contract between compiled components — calling conventions, data type sizes and alignment, struct layout, name mangling — so separately compiled code can link and run together.

**Context.** Why you can swap a shared library (.so/.dll) without recompiling, as long as the ABI is stable. ABI breaks are nastier than API breaks: code compiles fine and then corrupts memory at runtime. C's stable ABI is why it's the universal FFI lingua franca.

## See also

- [[API]]
- [[Shared Library]]
- [[Calling Convention]]
- [[FFI]]
- [[Name Mangling]]

## Further reading

- [Wikipedia: Application binary interface](https://en.wikipedia.org/wiki/Application_binary_interface)
