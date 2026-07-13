---
type: cheatsheet
area: writing
aliases: [LaTeX, TeX, latexmk]
tags: [cheatsheet, latex, writing, typesetting]
status: draft
---

# latex

> **Area:** [[Writing & Docs]]
> Typesetting for documents where structure and math matter. Covers document anatomy, everyday commands, math mode, and compiling. Obsidian and most markdown renderers borrow the math syntax (§5) inside `$...$`.

## 1. Document anatomy

```latex
\documentclass[11pt,a4paper]{article}   % article | report | book | beamer (slides)

% ---- preamble: packages & settings only, no text ----
\usepackage[utf8]{inputenc}             % omit on modern LuaLaTeX/XeLaTeX
\usepackage{amsmath, amssymb}           % the math essentials
\usepackage{graphicx}                   % \includegraphics
\usepackage{hyperref}                   % clickable refs & links — load last
\title{Title}
\author{A.\ Author}
\date{\today}

\begin{document}
\maketitle
\tableofcontents                        % needs two compile passes
% ...content...
\end{document}
```

## 2. Structure

```latex
\section{Name}                          % numbered, in ToC
\subsection{Name}
\subsubsection{Name}
\section*{Name}                         % starred: unnumbered, not in ToC
\paragraph{Name}                        % run-in heading

\label{sec:intro}                       % put right after the heading
\ref{sec:intro} on page \pageref{sec:intro}
\autoref{sec:intro}                     % hyperref: prints "Section 1" for you
```

## 3. Text & spacing

```latex
\textbf{bold} \textit{italic} \emph{context-aware emphasis}
\texttt{monospace} \underline{underlined}
\verb|raw text with \special #chars|

% paragraphs: blank line = new paragraph; \\ = line break, not a paragraph
``quotes''                              % backticks + apostrophes, not "
10\,\%  50\,km                          % thin space between number and unit
~                                       % non-breaking space: Fig.~3, p.~12
\ldots                                  % … not three periods

% reserved characters must be escaped:
\% \$ \& \# \_ \{ \} \textbackslash
```

## 4. Lists

```latex
\begin{itemize}
    \item bullet
    \item[--] custom marker
\end{itemize}

\begin{enumerate}
    \item numbered
\end{enumerate}

\begin{description}
    \item[Term] definition text
\end{description}
```

## 5. Math mode

```latex
$e^{i\pi} + 1 = 0$                      % inline
\[ \int_0^\infty e^{-x^2}\,dx = \frac{\sqrt{\pi}}{2} \]   % display, unnumbered
\begin{equation}\label{eq:euler}        % display, numbered & referencable
    e^{i\pi} + 1 = 0
\end{equation}

% building blocks
x^2  x_{ij}  \frac{a}{b}  \sqrt[3]{x}  \sum_{i=1}^n  \prod  \lim_{x \to 0}
\alpha \beta \gamma \Delta \Omega       % greek
\leq \geq \neq \approx \in \subseteq \to \implies \forall \exists
\mathbb{R} \mathcal{L} \mathbf{v}       % blackboard, calligraphic, bold
\left( \frac{a}{b} \right)              % auto-sized brackets
\text{plain words inside math}

% aligned multi-line (amsmath): & marks the alignment column
\begin{align}
    f(x) &= (x+1)^2 \\
         &= x^2 + 2x + 1
\end{align}
```

## 6. Figures & tables

```latex
\begin{figure}[htbp]                    % placement *suggestions*: here/top/bottom/page
    \centering
    \includegraphics[width=0.8\textwidth]{plot.pdf}   % pdf/png; relative widths scale
    \caption{What the figure shows.}
    \label{fig:plot}                    % label AFTER caption, or refs break
\end{figure}

\begin{table}[htbp]
    \centering
    \begin{tabular}{lrc}                % l/r/c per column; add | for vertical rules
        \toprule                        % booktabs package: publication-quality rules
        Item & Qty & OK \\
        \midrule
        Foo  & 42  & yes \\
        \bottomrule
    \end{tabular}
    \caption{Caption above tables by convention.}
    \label{tab:items}
\end{table}
```

## 7. Citations

```latex
\usepackage[style=numeric]{biblatex}    % modern route (vs classic bibtex)
\addbibresource{refs.bib}
As shown in \cite{knuth1984} ...
\printbibliography
```

```bibtex
@book{knuth1984,
    author = {Knuth, Donald E.},
    title  = {The {TeX}book},          % braces protect capitalization
    year   = {1984},
    publisher = {Addison-Wesley}
}
```

## 8. Compiling

```bash
# latexmk runs the right number of passes (refs, ToC, bib) automatically
latexmk -pdf main.tex
latexmk -pdf -pvc main.tex       # watch mode: recompile on save
latexmk -c                       # clean aux files, keep pdf

pdflatex main.tex                # single manual pass — refs need 2-3 passes
```

## Files & locations

```
main.tex          # source
refs.bib          # bibliography database
main.pdf          # output
main.aux .log .toc .bbl ...     # regenerable build files — gitignore them
```

## Gotchas / Golden rules

- **Compile twice** (or use `latexmk`) — cross-references and the ToC resolve on the second pass; `??` in output means one more pass.
- **`\label` after `\caption`**, never before, or the reference points at the section instead of the figure.
- **Blank line = new paragraph**, including inside math-adjacent text; an accidental blank line inside an equation environment is an error.
- **Escape `%` in text** — an unescaped `%` silently comments out the rest of the line, including your closing brace.
- **`[htbp]` is a suggestion**, not a command; fighting float placement is normal — write text as if figures float, referencing them by number.
- **Use `\emph{}` not `\textit{}`** for emphasis — it nests correctly (italic inside italic flips upright).
- **Straight quotes `"` come out wrong** — use ``` `` ``` and `''`.
- **Error messages point past the real error** — read the *first* error, fix, recompile; later errors are usually cascade.
- **The log is noisy** but `grep -n "Warning\|Error" main.log` finds what matters.
