---
type: "map"
tags: [map, se]
---

# Software Engineering

> Building software with other humans over time: version control, testing, architecture, process.

## Terms in this branch (28)

- [[ABI]] — The binary-level contract between compiled components — calling conventions, data type sizes and alignment, struct layout, name mangling — so separately compiled code can link and run together.
- [[API]] — The defined contract through which one piece of software is used by another — function signatures, endpoints, data formats.
- [[Branch]] — A divergent line of development.
- [[CI]] — The practice of merging all developers' work to a shared mainline frequently, with each integration automatically built and tested.
- [[Cohesion]] — How focused a single module is — high cohesion means its parts all serve one well-defined purpose.
- [[Commit]] — A recorded snapshot of changes with a message, author, timestamp, and pointer to its parent(s) — the atomic unit of history.
- [[Coupling]] — The degree of interdependence between modules — how much one must know about another.
- [[Dependency]] — External code your project relies on.
- [[Dependency Injection]] — Supplying a component's dependencies from outside (via constructor or setter) rather than having it construct them itself — a form of inversion of control.
- [[Design Pattern]] — A named, reusable solution to a recurring design problem — a shared vocabulary (Singleton, Observer, Factory, Strategy) rather than copy-paste code.
- [[DRY]] — The principle that every piece of knowledge should have a single, authoritative representation in a system — avoid duplicating logic.
- [[Event-driven Architecture]] — Systems built around producers emitting events (facts: 'order placed') that interested consumers react to asynchronously, usually via a broker — instead of services calling each other directly.
- [[Feature Flag]] — A runtime conditional that turns functionality on or off without redeploying — per user, percentage, or environment.
- [[Framework]] — A reusable scaffold that defines the structure of your application and calls your code at the points it specifies — inversion of control.
- [[Git]] — The dominant distributed version control system — a content-addressed store of immutable snapshots, where branches are cheap movable pointers into a commit DAG.
- [[Inversion of Control]] — Flipping who calls whom: instead of your code driving and calling libraries, a framework drives and calls your code at defined points.
- [[Library]] — A collection of reusable code you call from your program — you control the flow and call into it.
- [[Merge]] — Combining divergent branches, reconciling their changes — automatically where they don't overlap, with a merge conflict to resolve where they do.
- [[Microservices]] — An architectural style structuring an application as a suite of small, independently deployable services communicating over the network, each owning its data.
- [[Mock]] — A stand-in test object replacing a real dependency (database, API, clock) so a unit test runs fast, deterministic, and isolated.
- [[Monolith]] — An application built and deployed as a single unit, with all functionality in one codebase and process.
- [[Property-Based Testing]] — Asserting invariants over generated input classes instead of hand-picked examples, with failing cases automatically shrunk to a minimal counterexample.
- [[Rebase]] — Reapplying a branch's commits onto a new base commit, producing a linear history as if you'd branched from the new point.
- [[Semantic Versioning]] — A versioning convention MAJOR.MINOR.PATCH: bump MAJOR for breaking changes, MINOR for backward-compatible features, PATCH for backward-compatible fixes.
- [[SOLID]] — Five OOP design principles: Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion.
- [[TDD]] — A discipline of writing a failing test first, then the minimal code to pass it, then refactoring — the red-green-refactor loop.
- [[Unit Test]] — An automated test exercising one small unit (a function/class) in isolation, fast and deterministic, verifying behaviour against expectations.
- [[Version Control]] — A system that records changes to files over time so you can recall any version, branch, merge, and collaborate without overwriting each other's work.

---
← Back to [[_Home]]
