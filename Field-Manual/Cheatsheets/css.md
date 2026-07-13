---
type: cheatsheet
area: writing
aliases: [CSS, CSS3, stylesheet]
tags: [cheatsheet, css, web, writing]
status: draft
---

# css

> **Area:** [[Writing & Docs]]
> Presentation layer for [[html]]. Selectors, the box model, and the two layout systems that replaced all the old hacks: flexbox and grid.

## 1. Applying CSS

```css
/* external file — the normal case */
/* <link rel="stylesheet" href="style.css"> in <head> */

selector {
    property: value;                 /* declarations end with ; */
}
```

Inline `style=""` attributes win over everything and can't be overridden without `!important` — avoid both.

## 2. Selectors & specificity

```css
p                { }                 /* element */
.card            { }                 /* class — the workhorse */
#header          { }                 /* id — high specificity, use sparingly */
p.note           { }                 /* element with class */
.card .title     { }                 /* descendant, any depth */
.card > .title   { }                 /* direct child only */
.a, .b           { }                 /* group: same rules for both */
a:hover          { }                 /* pseudo-class: state */
li:first-child   { }
p::first-line    { }                 /* pseudo-element: part of element */
[type="email"]   { }                 /* attribute selector */
.card:has(img)   { }                 /* parent selector — modern browsers */
```

Specificity: inline > id > class/attribute/pseudo-class > element. Later rules win ties. If you're reaching for `!important`, your selectors are fighting — flatten them.

## 3. Box model

```css
.box {
    box-sizing: border-box;          /* width includes padding+border — set globally */
    width: 300px;
    padding: 1rem;                   /* inside the border */
    border: 1px solid #ccc;
    margin: 1rem auto;               /* outside; auto left/right centers block */
}

/* shorthand order: top right bottom left (clockwise) */
margin: 1px 2px 3px 4px;
margin: 1rem 2rem;                   /* vertical | horizontal */

* { box-sizing: border-box; }        /* the universal reset everyone starts with */
```

Vertical margins between siblings *collapse* to the larger of the two — the classic "where did my spacing go".

## 4. Layout: flexbox (one dimension)

```css
.row {
    display: flex;
    flex-direction: row;             /* or column */
    justify-content: space-between;  /* main axis: start|center|end|space-* */
    align-items: center;             /* cross axis */
    gap: 1rem;                       /* spacing without margin hacks */
    flex-wrap: wrap;
}
.row > .grow { flex: 1; }            /* child takes remaining space */
```

## 5. Layout: grid (two dimensions)

```css
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);          /* three equal columns */
    grid-template-columns: 200px minmax(0, 1fr);    /* sidebar + fluid main */
    gap: 1rem;
}
.grid .wide { grid-column: 1 / -1; }                /* span full width */

/* auto-responsive without media queries: */
grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
```

Rule of thumb: flexbox for a line of things, grid for a layout of things.

## 6. Typography & color

```css
body {
    font-family: system-ui, sans-serif;   /* always end with a generic fallback */
    font-size: 1rem;                 /* rem = root-relative; respects user settings */
    line-height: 1.5;                /* unitless: scales with font size */
    color: #333;
}
h1 { font-size: 2rem; font-weight: 700; }

color: #1a2b3c;                      /* hex */
color: rgb(26 43 60 / 0.5);          /* with alpha */
color: hsl(210 40% 17%);             /* easiest to reason about */
```

Use `rem` for font sizes and spacing, `em` for things relative to local font size, `px` only for borders and hairlines.

## 7. Custom properties (variables)

```css
:root {
    --brand: #0066cc;                /* define once at the root */
    --space: 1rem;
}
.button {
    background: var(--brand);
    padding: var(--space);
}
```

## 8. Responsive design

```css
/* mobile-first: base styles are the small screen, override upward */
@media (min-width: 768px) {
    .sidebar { display: block; }
}
@media (prefers-color-scheme: dark) {
    :root { --bg: #111; }
}
```

## 9. Position & stacking

```css
position: static;                    /* default, in flow */
position: relative;                  /* in flow, but children's absolute anchor */
position: absolute;                  /* out of flow, vs nearest positioned ancestor */
position: fixed;                     /* vs viewport */
position: sticky; top: 0;            /* in flow until it hits the edge */
z-index: 10;                         /* only works on positioned elements */
```

## Daily workflows

```css
/* Debug layout: outline everything (outline doesn't shift layout, border does) */
* { outline: 1px solid red; }

/* Center anything, the modern way */
.parent { display: grid; place-items: center; }

/* Truncate text with ellipsis */
.trunc { overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
```

## Gotchas / Golden rules

- **Set `box-sizing: border-box` globally** — the intuitive box model; padding stops changing widths.
- **Margin collapse** merges adjacent vertical margins; padding or `gap` never collapses — prefer `gap`.
- **Specificity wars end with flat class selectors** (`.card-title`, not `#main div.card h2 span`).
- **`z-index` is not global** — it competes only within the same stacking context; a parent's `z-index: 1` caps all children.
- **Mobile-first media queries** (`min-width`) compose; desktop-first (`max-width`) fight each other.
- **`height: 100%` needs every ancestor sized** — usually you want `min-height: 100vh` or flexbox.
- **Prefer classes over ids for styling** — ids are for anchors and JS.
- **Unitless `line-height`**; `line-height: 24px` breaks on nested font-size changes.
