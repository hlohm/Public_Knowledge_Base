---
type: "term"
branch: "Hardware & Architecture"
tags: [hardware, fundamental]
status: "developed"
---

# Interrupt

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]

A signal that makes the CPU pause its current work, save state, and jump to a handler to deal with an event — a key press, a packet arriving, a timer firing.

**Context.** Interrupts are why a computer can react to the outside world without busy-waiting. The alternative, polling, wastes cycles checking 'anything yet?'. The timer interrupt is what lets the OS preempt a running process.

## See also

- [[IRQ]]
- [[Context Switch]]
- [[Scheduler]]
- [[Polling]]

## Further reading

- [Wikipedia: Interrupt](https://en.wikipedia.org/wiki/Interrupt)
