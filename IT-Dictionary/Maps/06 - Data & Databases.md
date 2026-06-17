---
type: "map"
tags: [map, data]
---

# Data & Databases

> Persisting, querying and modelling information — relational, NoSQL, transactions, consistency.

## Terms in this branch (25)

- [[ACID]] — The four guarantees of a reliable transaction: Atomicity (all-or-nothing), Consistency (valid state to valid state), Isolation (concurrent transactions don't corrupt each other), Durability (committed data survives crashes).
- [[B-tree]] — A self-balancing, multi-way search tree that keeps data sorted and supports search, insert, and delete in logarithmic time — designed so each node is one disk page.
- [[BASE]] — The consistency philosophy of many distributed NoSQL systems: Basically Available, Soft state, Eventual consistency — accept temporary inconsistency in exchange for availability and partition tolerance.
- [[CAP Theorem]] — In a distributed data store, when a network Partition happens you can keep Consistency or Availability but not both — you can have at most two of consistency, availability, and partition tolerance.
- [[Database]] — An organised collection of structured data, managed by a DBMS (database management system) that handles storage, querying, concurrency, and durability.
- [[Denormalization]] — Deliberately duplicating data or pre-joining tables — violating [[Normalization]] — to make reads faster by avoiding joins at query time.
- [[Eventual Consistency]] — A consistency model guaranteeing that, absent new writes, all replicas will eventually converge to the same value — but a read may return stale data in the meantime.
- [[Foreign Key]] — A column referencing the primary key of another table, enforcing referential integrity — you can't reference a row that doesn't exist.
- [[Index]] — An auxiliary data structure (usually a B-tree) that lets the engine find rows by a key without scanning the whole table — trading write speed and disk space for read speed.
- [[Isolation Level]] — How much a running [[Transaction]] is allowed to see of others' concurrent work.
- [[Join]] — An operation combining rows from two or more tables on a related column — inner (matches only), left/right outer (keep unmatched on one side), cross (cartesian product).
- [[MVCC]] — A concurrency technique where writes create new versions of rows rather than overwriting, so readers see a consistent snapshot without blocking writers (and vice versa).
- [[Normalization]] — Structuring a relational schema to eliminate redundancy by decomposing tables so each fact is stored exactly once, governed by a series of normal forms (1NF, 2NF, 3NF, BCNF…).
- [[NoSQL]] — An umbrella for non-relational stores — key-value, document, column-family, and graph — that trade the relational model and often strict consistency for scale, flexible schemas, or specific access patterns.
- [[OLAP]] — Workloads dominated by large aggregating queries over historical data — reporting, dashboards, analytics — typically on a data warehouse.
- [[OLTP]] — Workloads dominated by many small, fast read/write transactions — order entry, banking, the operational database behind an app.
- [[ORM]] — A library that maps database rows to objects in your programming language, letting you query and persist data without writing raw SQL.
- [[Primary Key]] — The column(s) uniquely identifying each row in a table — non-null, unique, and the row's stable identity.
- [[Query Optimizer]] — The database component that turns declarative SQL into an execution plan — choosing indexes, join order, and join algorithms by estimating costs from table statistics.
- [[RDBMS]] — A database organising data into relations (tables of rows and columns) with enforced schemas and relationships, queried with SQL.
- [[Replication]] — Maintaining copies of data on multiple nodes for availability, read scaling, and durability — synchronous (wait for replicas) or asynchronous (don't).
- [[Sharding]] — Horizontally partitioning a dataset across multiple machines by a shard key, so each node holds a subset — the main way to scale writes beyond one server.
- [[SQL]] — The declarative language for querying and manipulating relational data — you state what you want and the engine's query planner decides how to fetch it.
- [[Strong Consistency]] — The guarantee that every read sees the most recent committed write, system-wide — the distributed system behaves as if there were a single copy of the data.
- [[Transaction]] — A unit of work executed as a single atomic, isolated operation — it either fully commits or fully rolls back, leaving the database consistent either way.

---
← Back to [[_Home]]
