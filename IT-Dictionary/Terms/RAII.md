---
type: "term"
branch: "Programming Languages"
aliases: ["Resource Acquisition Is Initialization"]
tags: [pl]
status: "developed"
---

# RAII

> **Branch:** [[07 - Programming Languages|Programming Languages]]
> **Also known as:** Resource Acquisition Is Initialization

A C++ idiom (also Rust's core model) where a resource's lifetime is tied to an object's scope — acquired in the constructor, released deterministically in the destructor when the object goes out of scope.

**Context.** The deterministic alternative to garbage collection: no collector, no pauses, and cleanup happens exactly when scope ends — covering memory, file handles, locks, sockets. Rust's ownership generalises this into a compile-time guarantee.

## See also

- [[Garbage Collection]]
- [[Ownership]]
- [[Destructor]]
- [[Scope]]
- [[Memory Safety]]

## Further reading

- [Wikipedia: Resource acquisition is initialization](https://en.wikipedia.org/wiki/Resource_acquisition_is_initialization)
