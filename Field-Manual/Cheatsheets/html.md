---
type: cheatsheet
area: writing
aliases: [HTML, HTML5]
tags: [cheatsheet, html, web, writing]
status: working
---

# html

> **Area:** [[Writing & Docs]]
> The structural markup of the web. Pairs with [[css]] for presentation; this note covers modern HTML5, semantics first.

## 1. Document skeleton

```html
<!DOCTYPE html>                      <!-- without it browsers enter quirks mode -->
<html lang="en">                     <!-- lang helps screen readers & translation -->
<head>
    <meta charset="utf-8">           <!-- first thing in head, before any text -->
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Page title</title>        <!-- the tab label and search-result headline -->
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- content -->
    <script src="app.js" defer></script>  <!-- defer: run after parse, keep in head or end of body -->
</body>
</html>
```

## 2. Semantic structure

```html
<header>...</header>                 <!-- page or section intro -->
<nav>...</nav>                       <!-- primary navigation -->
<main>...</main>                     <!-- exactly one per page -->
<article>...</article>               <!-- self-contained, syndicatable unit -->
<section>...</section>               <!-- thematic grouping, should have a heading -->
<aside>...</aside>                   <!-- tangential content, sidebars -->
<footer>...</footer>
<div>...</div>                       <!-- last resort: no meaning, styling hook only -->
```

Semantics buy accessibility, SEO, and reader modes for free — reach for `<div>` only when nothing meaningful fits.

## 3. Text

```html
<h1>...</h1> ... <h6>...</h6>        <!-- one h1 per page; don't skip levels -->
<p>paragraph</p>
<strong>important</strong>           <!-- semantic; <b> is purely visual -->
<em>stressed</em>                    <!-- semantic; <i> is purely visual -->
<code>inline code</code>
<pre><code>block of code</code></pre> <!-- pre preserves whitespace -->
<blockquote cite="https://example.com">quote</blockquote>
<small>fine print</small>
<mark>highlight</mark>
<br>                                 <!-- line break; if you need two, you want a <p> -->
<hr>                                 <!-- thematic break -->
```

## 4. Links, images & media

```html
<a href="https://example.com">text</a>
<a href="#section-id">jump link</a>
<a href="mailto:you@example.com">mail</a>
<a href="https://example.com" target="_blank" rel="noopener">new tab</a>  <!-- rel=noopener: security -->

<img src="photo.jpg" alt="what the image shows" width="600" height="400">
<!-- alt is mandatory: accessibility + shown on broken load. width/height prevent layout shift -->

<figure>
    <img src="chart.png" alt="Sales by quarter">
    <figcaption>Q1–Q4 sales.</figcaption>
</figure>

<video src="clip.mp4" controls></video>
<audio src="sound.mp3" controls></audio>
```

## 5. Lists & tables

```html
<ul><li>unordered</li></ul>
<ol start="3"><li>ordered</li></ol>
<dl><dt>term</dt><dd>definition</dd></dl>

<table>
    <thead><tr><th scope="col">Header</th></tr></thead>   <!-- scope aids screen readers -->
    <tbody><tr><td>cell</td></tr></tbody>
</table>
```

Tables are for tabular data — never for layout; that's what [[css]] grid/flexbox are for.

## 6. Forms

```html
<form action="/submit" method="post">
    <label for="email">Email</label>            <!-- label+for: click target & a11y -->
    <input id="email" name="email" type="email" required>
    <input type="password" name="pw" minlength="8">
    <input type="checkbox" id="ok" name="ok"> <label for="ok">Agree</label>
    <select name="choice">
        <option value="a">A</option>
    </select>
    <textarea name="msg" rows="4"></textarea>
    <button type="submit">Send</button>          <!-- default type is submit; be explicit -->
</form>
```

Input `type` (`email`, `number`, `date`, `url`…) buys native validation and the right mobile keyboard.

## 7. Attributes worth knowing

```html
class="a b"                          <!-- many per element, the CSS/JS hook -->
id="unique"                          <!-- one per page, anchor target -->
data-user-id="42"                    <!-- your own data, read via dataset.userId -->
hidden                               <!-- boolean attributes need no value -->
title="tooltip"
aria-label="close"                   <!-- a11y name when no visible text -->
loading="lazy"                       <!-- on img/iframe: defer offscreen loads -->
```

## 8. Escaping

```html
&lt; &gt; &amp; &quot;               <!-- < > & " — must escape & and < in content -->
```

## 9. Interactive & modern elements

```html
<details>                            <!-- native disclosure, no JS -->
    <summary>Show more</summary>     <!-- the always-visible label -->
    <p>Hidden until toggled.</p>
</details>

<dialog id="dlg">                    <!-- native modal: dlg.showModal() / dlg.close() -->
    <form method="dialog"><button>OK</button></form>
</dialog>

<progress value="70" max="100"></progress>   <!-- determinate progress bar -->
<meter value="0.6">60%</meter>                <!-- a measurement within a range -->
<time datetime="2026-07-14">today</time>      <!-- machine-readable date -->
```

## 10. Responsive images

```html
<!-- srcset + sizes: browser picks the best file for the viewport & DPR -->
<img src="small.jpg"
     srcset="small.jpg 400w, medium.jpg 800w, large.jpg 1200w"
     sizes="(max-width: 600px) 100vw, 600px"
     alt="...">

<!-- picture: art direction or format fallback (AVIF/WebP with JPEG fallback) -->
<picture>
    <source srcset="hero.avif" type="image/avif">
    <source srcset="hero.webp" type="image/webp">
    <img src="hero.jpg" alt="...">   <!-- the <img> is the required fallback -->
</picture>
```

## 11. Metadata & SEO

```html
<head>
    <meta name="description" content="One-sentence summary — the search snippet.">
    <link rel="canonical" href="https://example.com/page">  <!-- dedupe duplicate URLs -->

    <!-- Open Graph: how the link looks when shared (social, chat) -->
    <meta property="og:title" content="Page title">
    <meta property="og:description" content="Summary for the card">
    <meta property="og:image" content="https://example.com/card.png">
    <meta property="og:type" content="article">
</head>
```

## 12. Accessibility essentials

```html
<a href="#main" class="skip-link">Skip to content</a>   <!-- first focusable element -->
<button aria-expanded="false" aria-controls="menu">Menu</button>
<nav aria-label="Primary">...</nav>                      <!-- name repeated landmarks -->
<div role="alert">Saved.</div>                           <!-- announced by screen readers -->
<img src="deco.svg" alt="">                              <!-- empty alt = decorative, skip it -->
```

Native elements come with roles, focus, and keyboard behavior for free; reach for ARIA only to fill gaps, never to reinvent a `<button>` from a `<div>`.

## Daily workflows

```html
<!-- Minimal comment syntax -->
<!-- this is a comment -->

<!-- Validate before shipping: https://validator.w3.org -->
```

## Gotchas / Golden rules

- **Always `alt` on images** — empty `alt=""` for purely decorative ones, never missing.
- **Semantics over divs:** if there's an element for it, use it; a11y and SEO are downstream of markup.
- **One `<h1>`, one `<main>`** per page; heading levels form the document outline — don't skip.
- **Void elements** (`img`, `br`, `input`, `meta`, `link`, `hr`) take no closing tag.
- **`target="_blank"` without `rel="noopener"`** hands the opener window to the target page.
- **Don't nest interactive elements** (a link inside a button, a button inside a link) — behavior is undefined.
- **Attribute values in quotes**, lowercase tag names — legal without, unreadable without.
- **HTML is not XML:** unknown tags don't error, they silently become inline elements — typos hide well.
- **`<picture>`/`<source>` need the `<img>` fallback** — without it, nothing shows on unsupported browsers.
- **ARIA is a last resort:** a real `<button>`/`<a>`/`<input>` beats `role="button"` on a `<div>` every time — don't reinvent native behavior.
- **`<dialog>` without `showModal()`** isn't modal — the backdrop and focus-trap only come from the JS call.

## Further reading

- [MDN: HTML elements reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Element) — every element, authoritative
- [MDN: HTML forms guide](https://developer.mozilla.org/en-US/docs/Learn/Forms) · [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [W3C Markup Validator](https://validator.w3.org/) — catch malformed markup before shipping
