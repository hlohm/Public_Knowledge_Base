---
type: "map"
tags: [map, pl]
---

# Programming Languages

> How we tell machines what to do, and the ideas that distinguish languages: types, paradigms, memory models.

## Terms in this branch (35)

- [[AST]] — A tree representation of source code's structure, produced by the parser, abstracting away syntactic noise (parentheses, semicolons) into the essential grammar.
- [[Async-Await]] — Language syntax for writing asynchronous, non-blocking code that reads like sequential code — await suspends until a result is ready without blocking the thread.
- [[Bytecode]] — A compact, portable intermediate instruction set for a virtual machine — between human-readable source and native machine code.
- [[Closure]] — A function bundled together with the variables it captured from its surrounding scope — it 'closes over' that environment and can use those variables later, even after the enclosing function has returned.
- [[Compiler]] — A program that translates source code in one language into another (usually machine code or bytecode) ahead of execution, typically performing optimisation along the way.
- [[Concurrency]] — Structuring a program as multiple independent tasks that can make progress in overlapping time periods — about dealing with many things at once, even on one core.
- [[Coroutine]] — A function that can suspend and resume its execution, preserving local state across suspensions — cooperative, lightweight, and not tied to an OS thread.
- [[Dereference]] — Following a pointer or reference to access the value it points to.
- [[Dynamic Typing]] — Type checking performed at runtime — a variable's type is a property of its current value, not a fixed declaration.
- [[Functional Programming]] — Programming with [[Pure Function]]s and immutable data: computation as expression evaluation rather than state mutation.
- [[Garbage Collection]] — Automatic reclamation of memory no longer reachable by the program, freeing the developer from manual free()/delete and the bugs that come with it.
- [[Generics]] — Writing code parameterised over types — a List<T> or Vec<T> that works for any element type while staying type-safe.
- [[Inheritance]] — An OOP mechanism where a class derives fields and behaviour from a parent class, modelling an 'is-a' relationship.
- [[Interface]] — A named contract of operations without implementation: anything providing these methods can be used here.
- [[Interpreter]] — A program that executes source code directly, translating and running it statement by statement rather than compiling to machine code first.
- [[JavaScript]] — The language of the web, standardized as ECMAScript: dynamically typed, prototype-based, single-threaded with an event loop — and via Node.js, V8, and WASM hosts, long since escaped the browser.
- [[JIT Compilation]] — Compiling bytecode to native machine code at runtime, often guided by profiling of which paths are actually hot — blending interpretation's flexibility with compilation's speed.
- [[Lambda]] — A function defined inline without a name, often passed as an argument — x => x + 1.
- [[Lexer]] — The first stage of a compiler: turns the raw character stream into tokens (identifier count, operator +=, literal 42), discarding whitespace and comments.
- [[Memory Safety]] — The property that a program cannot access memory incorrectly — no buffer overflows, use-after-free, null dereferences, or data races on memory.
- [[Null Pointer]] — A pointer that points to nothing — a sentinel meaning 'no value'.
- [[Parallelism]] — Actually executing multiple computations simultaneously, on multiple cores or machines — about doing many things at once for speed.
- [[Parser]] — The compiler stage that assembles the lexer's token stream into a structured [[AST]] according to the language's grammar — and reports syntax errors when the stream doesn't fit.
- [[Pointer]] — A value holding the memory address of another value.
- [[Polymorphism]] — Code that operates on values of multiple types.
- [[Pure Function]] — A function whose output depends only on its inputs and which has no side effects — same input always yields same output, and nothing observable changes outside it.
- [[RAII]] — A C++ idiom (also Rust's core model) where a resource's lifetime is tied to an object's scope — acquired in the constructor, released deterministically in the destructor when the object goes out of scope.
- [[Recursion]] — A function that solves a problem by calling itself on smaller subproblems, with a base case to stop.
- [[Reference]] — An alias to a value — a handle that lets you access the original without copying it.
- [[Side Effect]] — Any observable change a function makes beyond returning a value — mutating state, I/O, network calls, writing to a database.
- [[Static Typing]] — Type checking performed at compile time — types are known and verified before the program runs.
- [[Type Inference]] — The compiler deducing types automatically from context, so you get static-typing guarantees without writing every annotation.
- [[Type System]] — The rules by which a language assigns and checks types, catching whole classes of errors and enabling optimisation.
- [[Undefined Behavior]] — Code whose result the language spec leaves entirely unconstrained — the compiler may do anything, including silently miscompile, crash, or appear to work.
- [[Variable]] — A named binding to a storage location or value.

---
← Back to [[_Home]]
