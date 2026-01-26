# Agent Marketing Protocol (AMP)

AMP is an **open protocol for governing promotion inside AI agents**.

It defines **when**, **why**, and **how** a promotional action may occur,
with the explicit goal of making such decisions **explainable, consensual, and auditable**.

AMP is not a recommender system.
AMP is not an advertising engine.
AMP is a **decision governance layer**.

---

## Why AMP Exists

As AI agents become interfaces for decision-making,
promotion is no longer a UI problem but a **behavioral one**.

Today, most systems either:

* inject promotions opaquely, or
* avoid them entirely due to trust and compliance concerns.

AMP addresses this gap by introducing:

* explicit intent gates
* decision thresholds
* explainable outcomes
* user-consensual handshakes

---

## Core Principles

AMP is built on four non-negotiable principles:

1. **Silence First**
   Promotion is never the default behavior.

2. **Intent Before Exposure**
   Promotional actions are allowed only when user intent is explicit and confident.

3. **Explainability by Construction**
   Every decision must be explainable through a structured decision record.

4. **Separation of Concerns**
   Decision logic is isolated from brands, monetization, and delivery channels.

---

## What AMP Is

* A protocol for promotional decision governance
* A set of deterministic gates and thresholds
* A producer of explainable decision records
* Brand-agnostic and LLM-agnostic by design
* Suitable for AI agents, assistants, and autonomous systems

---

## What AMP Is NOT

AMP explicitly defines what it does **not** aim to do.

Before using or extending AMP, **read this first**:

👉 **[NON-GOALS & Misuse](./NON_GOALS.md)**

This document is part of the protocol and defines its boundaries.

---

## High-Level Architecture

At a high level, AMP operates as follows:

1. User input is analyzed for intent and context
2. Intent gates and thresholds are evaluated
3. A decision outcome is produced:

   * `NEUTRAL`
   * `INSIGHT_ONLY`
   * `HANDSHAKE_ALLOWED`
4. A structured **Decision Record** is generated
5. External systems decide whether and how to act on the decision

AMP itself never:

* triggers promotions
* logs data autonomously
* persists user information

---

## Decision Record

Every AMP decision produces a **Decision Record**, containing:

* the final outcome
* a summarized representation of inputs
* a structured explanation of why gates passed or failed

Decision Records exist to enable:

* auditability
* debugging
* compliance
* trust

---

## Example Usage

A minimal end-to-end example is available in:

```
examples/
└── simple_flow.py
```

The example demonstrates:

* a neutral user interaction
* an evaluated intent
* a generated decision record
* optional external logging

No brands or marketing content are involved.

---

## Status

AMP is an **experimental but stable protocol**.

* APIs may evolve
* principles and boundaries are stable
* backward compatibility is not guaranteed pre-1.0

---

## License

This project is released under an open license.

Use, fork, and extend responsibly,
and respect the boundaries defined in the protocol documentation.

---

## Final Note

AMP is intentionally restrictive.

If an implementation makes promotion easier than restraint,
it is no longer implementing AMP.
