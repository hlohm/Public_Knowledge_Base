---
type: cheatsheet
area: "Programming Languages"
aliases: [SQL, postgres, postgresql, mysql, sqlite]
tags: [sql, database, postgres, mysql, sqlite, querying]
status: working
---

# SQL

> **Area:** [[Programming Languages]]

Querying and data manipulation patterns that span PostgreSQL, MySQL/MariaDB, and SQLite. Syntax differences noted where they diverge. Assumes basic SELECT/WHERE knowledge.

---

## 1. SELECT patterns

```sql
-- Aliases
SELECT
    e.first_name || ' ' || e.last_name AS full_name,
    d.name                             AS department,
    e.salary
FROM employees e
JOIN departments d ON d.id = e.department_id
WHERE e.active = true
ORDER BY e.salary DESC
LIMIT 10;

-- DISTINCT
SELECT DISTINCT country FROM users;

-- CASE expression
SELECT
    name,
    CASE
        WHEN score >= 90 THEN 'A'
        WHEN score >= 80 THEN 'B'
        ELSE 'C'
    END AS grade
FROM students;

-- Conditional aggregate
SELECT
    department_id,
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE salary > 80000) AS high_earners,  -- PostgreSQL
    -- MySQL: SUM(CASE WHEN salary > 80000 THEN 1 ELSE 0 END)
    AVG(salary) AS avg_salary
FROM employees
GROUP BY department_id
HAVING COUNT(*) > 5
ORDER BY avg_salary DESC;
```

## 2. JOINs

```sql
-- INNER JOIN: only matching rows
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON o.user_id = u.id;

-- LEFT JOIN: all users, even without orders
SELECT u.name, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.name;

-- RIGHT JOIN: all orders even if user missing (rare; LEFT is preferred)
-- FULL OUTER JOIN: all rows from both (PostgreSQL; not in SQLite/older MySQL)

-- Self join: find employees and their managers
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON m.id = e.manager_id;

-- Cross join: cartesian product (all combinations)
SELECT a.color, b.size
FROM colors a
CROSS JOIN sizes b;
```

## 3. Subqueries and CTEs

```sql
-- Scalar subquery
SELECT name, (SELECT COUNT(*) FROM orders WHERE user_id = u.id) AS order_count
FROM users u;

-- IN subquery
SELECT name FROM users
WHERE id IN (SELECT DISTINCT user_id FROM orders WHERE total > 100);

-- EXISTS (often faster than IN for large tables)
SELECT name FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.user_id = u.id AND o.total > 100
);

-- CTE (WITH clause) — available in PostgreSQL, MySQL 8+, SQLite 3.35+
WITH
    active_users AS (
        SELECT id, name FROM users WHERE active = true
    ),
    user_totals AS (
        SELECT user_id, SUM(total) AS lifetime_value
        FROM orders
        GROUP BY user_id
    )
SELECT u.name, COALESCE(t.lifetime_value, 0) AS ltv
FROM active_users u
LEFT JOIN user_totals t ON t.user_id = u.id
ORDER BY ltv DESC;

-- Recursive CTE (hierarchies / trees)
WITH RECURSIVE org_chart AS (
    SELECT id, name, manager_id, 0 AS depth
    FROM employees
    WHERE manager_id IS NULL          -- root
    UNION ALL
    SELECT e.id, e.name, e.manager_id, oc.depth + 1
    FROM employees e
    JOIN org_chart oc ON oc.id = e.manager_id
)
SELECT depth, name FROM org_chart ORDER BY depth, name;
```

## 4. Window functions

```sql
-- ROW_NUMBER, RANK, DENSE_RANK
SELECT
    name,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rn,
    RANK()       OVER (PARTITION BY department_id ORDER BY salary DESC) AS rnk,
    DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS drnk
FROM employees;

-- Top N per group (common pattern)
SELECT name, salary, department_id
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rn
    FROM employees
) sub
WHERE rn <= 3;

-- LAG / LEAD: previous / next row
SELECT
    date,
    revenue,
    LAG(revenue)  OVER (ORDER BY date) AS prev_revenue,
    LEAD(revenue) OVER (ORDER BY date) AS next_revenue,
    revenue - LAG(revenue) OVER (ORDER BY date) AS change
FROM daily_revenue;

-- Running total
SELECT
    date, amount,
    SUM(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM transactions;

-- Moving average (7-day window)
SELECT
    date, amount,
    AVG(amount) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS avg_7d
FROM transactions;
```

## 5. DML: INSERT, UPDATE, DELETE

```sql
-- INSERT
INSERT INTO users (name, email, created_at)
VALUES ('Alice', 'alice@example.com', NOW());

-- INSERT multiple rows
INSERT INTO tags (name, color)
VALUES ('urgent', 'red'), ('low', 'green'), ('blocked', 'yellow');

-- INSERT … ON CONFLICT (upsert) — PostgreSQL
INSERT INTO settings (user_id, key, value)
VALUES (1, 'theme', 'dark')
ON CONFLICT (user_id, key)
DO UPDATE SET value = EXCLUDED.value;

-- INSERT … IGNORE (MySQL) / ON CONFLICT DO NOTHING (PostgreSQL/SQLite)
INSERT OR IGNORE INTO sessions (token, user_id) VALUES ('abc', 1);  -- SQLite
INSERT INTO sessions (token, user_id) VALUES ('abc', 1) ON CONFLICT DO NOTHING;  -- PG

-- UPDATE
UPDATE users
SET last_login = NOW(), login_count = login_count + 1
WHERE id = 42;

-- UPDATE with JOIN (PostgreSQL)
UPDATE users u
SET group_name = g.name
FROM groups g
WHERE g.id = u.group_id;

-- UPDATE with JOIN (MySQL)
UPDATE users u
JOIN groups g ON g.id = u.group_id
SET u.group_name = g.name;

-- DELETE
DELETE FROM sessions WHERE expires_at < NOW();

-- TRUNCATE — fast delete all rows, no WHERE, not logged per-row
TRUNCATE TABLE audit_log;         -- resets auto-increment in MySQL
TRUNCATE TABLE audit_log RESTART IDENTITY;  -- PostgreSQL
```

## 6. Aggregates

```sql
COUNT(*), COUNT(col)   -- * counts all rows; col skips NULLs
SUM(col), AVG(col), MIN(col), MAX(col)
STRING_AGG(col, ', ')  -- PostgreSQL/SQLite (GROUP_CONCAT in MySQL)
ARRAY_AGG(col)         -- PostgreSQL: aggregate into an array
BOOL_AND(col), BOOL_OR(col)    -- PostgreSQL
JSON_AGG(row), JSON_OBJECT_AGG(key, val)  -- PostgreSQL
```

## 7. NULL handling

```sql
-- NULL comparisons always return NULL (not true/false)
x = NULL    -- always NULL  (use IS NULL)
x IS NULL, x IS NOT NULL

-- COALESCE: first non-NULL argument
COALESCE(discount, 0)
COALESCE(nickname, first_name, 'Unknown')

-- NULLIF: returns NULL if both arguments are equal (useful for divison)
salary / NULLIF(hours, 0)    -- avoids division by zero

-- NULL in aggregates: SUM/AVG ignore NULLs; COUNT(*) counts all rows
-- NULL in ORDER BY: NULLS LAST / NULLS FIRST (PostgreSQL)
ORDER BY score DESC NULLS LAST
```

## 8. Indexes and performance

```sql
-- Create index
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_events_created ON events(created_at DESC);

-- Partial index (only index relevant rows)
CREATE INDEX idx_active_users ON users(email) WHERE active = true;

-- Composite index (order matters: col1 must be in WHERE for index to be used)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- See query plan
EXPLAIN SELECT * FROM orders WHERE user_id = 1;
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 1;  -- actually runs it

-- Common query plan nodes to look for (PostgreSQL):
-- Seq Scan     → no index (may be OK for small tables)
-- Index Scan   → using index
-- Bitmap Scan  → combining multiple indexes
-- Hash Join / Nested Loop → join strategies
```

---

## Files & locations

| File | Purpose |
|---|---|
| `~/.psqlrc` | psql startup config (prompt, timing, pager) |
| `~/.pgpass` | PostgreSQL passwords — `host:port:db:user:pass` |
| `~/.my.cnf` | MySQL client config (`[client]` section) |
| `~/.sqliterc` | SQLite REPL config (`.mode column`, `.headers on`) |

## Gotchas / Golden rules

1. **`COUNT(col)` skips NULLs; `COUNT(*)` counts everything** — pick intentionally.
2. **`GROUP BY` must include all non-aggregate columns in SELECT** — `SELECT name, MAX(salary) FROM ... GROUP BY id` would silently give arbitrary names in MySQL's non-strict mode; PostgreSQL rejects it.
3. **`LIKE 'abc%'` can use an index; `LIKE '%abc'` cannot** — leading wildcards force a full scan.
4. **UPDATE without WHERE deletes all rows** — double-check `WHERE` clauses; run as a SELECT first to preview.
5. **Transactions**: wrap related INSERT/UPDATE/DELETE in `BEGIN; ... COMMIT;` to ensure atomicity; use `ROLLBACK` on error.
