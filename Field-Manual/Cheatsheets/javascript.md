---
type: cheatsheet
area: "Programming Languages"
aliases: [js, typescript, ts]
tags: [javascript, typescript, programming, web, node]
status: working
---

# JavaScript / TypeScript

> **Area:** [[Programming Languages]]

Modern JavaScript (ES2020+) and TypeScript. Covers the language features you use daily in Node.js scripts and web applications. Assumes familiarity with basic syntax.

---

## 1. Variables and types

```js
const x = 1;            // block-scoped, immutable binding (not a deep freeze)
let y = 2;              // block-scoped, mutable
// var is function-scoped and hoisted — avoid it

// Primitives: number, string, boolean, null, undefined, symbol, bigint
typeof null   // "object" — historic bug, null is not an object
typeof undefined  // "undefined"

// Type coercion traps
0 == false      // true  (loose equality)
0 === false     // false (strict equality — always use ===)
null == undefined   // true  (only case where this is expected)
NaN === NaN     // false — use Number.isNaN(x)

// Nullish coalescing (null / undefined → default)
const name = user.name ?? "Anonymous";

// Optional chaining (short-circuits at null/undefined)
const city = user?.address?.city;
const len  = arr?.[0]?.length;
fn?.();   // call fn only if it's defined
```

## 2. Destructuring and spread

```js
// Array destructuring
const [first, second, ...rest] = [1, 2, 3, 4];
const [, second] = [1, 2];        // skip first

// Object destructuring
const { name, age, city = "Unknown" } = person;  // with default
const { name: fullName } = person;                // rename
const { a: { b } } = { a: { b: 1 } };           // nested

// Spread
const merged = { ...defaults, ...overrides };
const copy   = [...original, newItem];
fn(...args);   // spread into function call

// Swap without temp
[a, b] = [b, a];

// Function parameters
function render({ title, content, className = "" }) { ... }
```

## 3. Strings

```js
// Template literals
const msg = `Hello, ${name}! You have ${count} messages.`;

// Tagged template (e.g., for SQL escaping, HTML sanitisation)
const html = sanitize`<div>${userInput}</div>`;

// Common methods
str.trim()                  // strip whitespace
str.split(",")              // → array
str.includes("sub")
str.startsWith("http"), str.endsWith(".png")
str.replace("old", "new")  // first match
str.replaceAll("a", "b")   // all matches
str.padStart(5, "0")       // "00042"
str.padEnd(10, ".")        // "hello....."
str.slice(0, 3)            // first 3 characters
str.at(-1)                 // last character (ES2022)
str.repeat(3)
```

## 4. Arrays

```js
// Non-mutating (return new array):
arr.map(x => x * 2)
arr.filter(x => x > 0)
arr.reduce((acc, x) => acc + x, 0)
arr.flatMap(x => [x, x * 2])    // map + flatten one level
arr.find(x => x.id === id)       // first match or undefined
arr.findIndex(x => x.id === id)  // index or -1
arr.some(x => x > 10)           // true if any match
arr.every(x => x > 0)           // true if all match
arr.slice(1, 3)                  // elements 1 and 2
[...new Set(arr)]                // deduplicate

// Mutating:
arr.push(x), arr.pop()
arr.unshift(x), arr.shift()      // prepend / remove first
arr.splice(index, deleteCount, ...items)
arr.sort((a, b) => a - b)        // numeric sort (mutates!)
arr.reverse()                    // mutates!

// Flat
[1, [2, [3]]].flat()             // [1, 2, [3]]  (one level)
[1, [2, [3]]].flat(Infinity)     // [1, 2, 3]

// Array.from
Array.from({ length: 5 }, (_, i) => i)   // [0, 1, 2, 3, 4]
Array.from("abc")                          // ["a", "b", "c"]
Array.from(nodeList)                       // DOM NodeList → Array
```

## 5. Objects

```js
// Shorthand
const x = 1, y = 2;
const point = { x, y };          // { x: 1, y: 2 }

// Computed property names
const key = "dynamic";
const obj = { [key]: 42 };       // { dynamic: 42 }

// Object methods
Object.keys(obj), Object.values(obj), Object.entries(obj)
Object.assign({}, defaults, overrides)   // shallow merge
Object.freeze(obj)                       // prevents modification
Object.fromEntries([["a", 1], ["b", 2]])  // { a: 1, b: 2 }

// Check property
"key" in obj          // true for own + inherited
obj.hasOwnProperty("key")         // own only
Object.hasOwn(obj, "key")         // ES2022 preferred

// Deep clone (simple, no functions/special types)
const clone = structuredClone(obj);   // ES2022 / Node 17+
```

## 6. Async / await

```js
// async function always returns a Promise
async function fetchUser(id) {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();   // returns Promise<User>
}

// Error handling
async function main() {
    try {
        const user = await fetchUser(1);
        console.log(user.name);
    } catch (err) {
        console.error("Failed:", err.message);
    }
}

// Parallel execution
const [userA, userB] = await Promise.all([fetchUser(1), fetchUser(2)]);

// Race / timeout pattern
const result = await Promise.race([
    fetchUser(1),
    new Promise((_, reject) => setTimeout(() => reject(new Error("timeout")), 5000))
]);

// Promise.allSettled — don't fail-fast; get all results
const results = await Promise.allSettled([fetch(a), fetch(b)]);
results.forEach(r => {
    if (r.status === "fulfilled") use(r.value);
    else console.error(r.reason);
});

// Promise creation
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
```

## 7. Modules (ES Modules)

```js
// Named exports
export const PI = 3.14;
export function greet(name) { return `Hello, ${name}`; }
export default class App { ... }    // one default export per file

// Import
import App, { PI, greet } from "./app.js";
import * as math from "./math.js";
import "./side-effect.js";          // run for side effects

// Dynamic import (lazy loading)
const module = await import("./heavy.js");
```

## 8. Error handling patterns

```js
// Custom error
class AppError extends Error {
    constructor(message, code) {
        super(message);
        this.name = "AppError";
        this.code = code;
    }
}

// instanceof check
try {
    await doSomething();
} catch (err) {
    if (err instanceof AppError) {
        console.error(`App error ${err.code}: ${err.message}`);
    } else {
        throw err;   // re-throw unexpected errors
    }
}
```

## 9. TypeScript essentials

```ts
// Basic types
let n: number = 42;
let s: string = "hello";
let b: boolean = true;
let ns: null = null;
let u: undefined = undefined;

// Union and literal types
type Status = "pending" | "done" | "error";
type ID = string | number;

// Interfaces vs type aliases
interface User {
    id: number;
    name: string;
    email?: string;   // optional
}

type Point = { x: number; y: number };

// Generics
function first<T>(arr: T[]): T | undefined {
    return arr[0];
}

// Utility types
Partial<User>          // all fields optional
Required<User>         // all fields required
Pick<User, "id" | "name">
Omit<User, "email">
Record<string, number>  // { [key: string]: number }
Readonly<User>

// Type guards
function isString(x: unknown): x is string {
    return typeof x === "string";
}

// Non-null assertion (use sparingly)
document.getElementById("app")!.innerHTML = "";

// as const
const config = { env: "prod", port: 8080 } as const;
// config.port is type 8080 (literal), not number
```

---

## Daily workflows

### "Transform an array of objects into a map by id"
```js
const byId = Object.fromEntries(users.map(u => [u.id, u]));
// Access: byId[42]

// Or with Map:
const map = new Map(users.map(u => [u.id, u]));
map.get(42);
```

### "Remove duplicates from an array of objects by key"
```js
const unique = [...new Map(items.map(i => [i.id, i])).values()];
```

### "Group an array by a property"
```js
const grouped = items.reduce((acc, item) => {
    (acc[item.category] ??= []).push(item);
    return acc;
}, {});
```

## Gotchas / Golden rules

1. **`===` always, `==` never** — loose equality `==` coerces types in surprising ways; `[] == false` is `true`.
2. **`Array.sort()` is lexicographic by default** — `[10, 9, 2].sort()` gives `[10, 2, 9]`; always pass a comparator for numbers.
3. **`const` does not freeze objects** — only the binding is immutable; the object's properties can still change. Use `Object.freeze()` for shallow immutability.
4. **Floating point arithmetic is not exact** — `0.1 + 0.2 !== 0.3`; use integer cents/basis-points for money.
5. **`await` inside `.forEach()` does not work as expected** — `forEach` is not async-aware; use `for...of` or `Promise.all(arr.map(...))` instead.
