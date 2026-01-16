# AMP Architecture

## Purpose of This Document

This document explains **where AMP lives in a system**, **what it is responsible for**, and—just as important—**what it must never control**.

AMP is not an application, not a model, and not a recommendation engine.
It is a **decision-layer protocol**.

---

## High-Level Positioning

AMP sits **between understanding and response generation**.

```text
User Input
   ↓
[ Understanding Layer ]
(Intent, entities, context)
   ↓
[ AMP Decision Layer ]
(Should promotion be allowed?)
   ↓
[ Response Composition Layer ]
(Language, UX, tone)
   ↓
User Output
```

AMP never generates text and never selects products.
It only answers one question:

> *Is it legitimate to propose a brand-related resource in this moment?*

---

## Core Architectural Principles

### 1. Deterministic Decisions

All AMP decisions must be:

* reproducible
* explainable
* auditable

No stochastic component is allowed in the final decision gate.

---

### 2. Separation of Concerns

AMP enforces strict boundaries:

| Layer         | Responsibility                | AMP Access        |
| ------------- | ----------------------------- | ----------------- |
| LLM / NLP     | Interpret intent and language | Read-only input   |
| AMP           | Decide promotion eligibility  | Full control      |
| UI / Response | Phrase the answer             | No policy control |

This separation prevents hidden persuasion and brand-driven bias.

---

### 3. Silence Is a Valid Output

AMP explicitly supports **no-action outcomes**.

If conditions are not met, AMP must return a neutral or insight-only decision.
This is considered a *successful execution*, not a failure.

---

## AMP as a Policy Engine

AMP should be implemented as one of the following:

* an in-process library
* a stateless microservice
* a shared internal policy module

In all cases, AMP:

* receives structured inputs
* returns a structured decision
* does not mutate external state

Example decision output:

```json
{
  "decision": "HANDSHAKE_ALLOWED",
  "pes": 0.73,
  "reason": "Intent and gap exceed thresholds"
}
```

---

## Boundary With LLMs

LLMs may assist with:

* intent detection
* gap hypothesis generation
* natural language phrasing

LLMs must never:

* override thresholds
* select brands
* decide promotion timing
* optimize for conversion

All promotion decisions must remain outside the model.

---

## Brand Isolation

Brands are treated as **external resources**, never as actors.

Rules:

* brands cannot influence scoring
* brands cannot access user data
* brands cannot trigger AMP

Brand eligibility is evaluated *after* a promotion decision is allowed.

---

## Deployment Scenarios

### AI Assistants

AMP acts as a guardrail before any brand mention.

### Decision Support Tools

AMP evaluates whether optional resources may be proposed.

### Multi-Agent Systems

AMP serves as a shared compliance layer across agents.

---

## What AMP Intentionally Does Not Do

* generate recommendations
* rank products
* personalize pricing
* track user behavior
* optimize funnels

These responsibilities belong elsewhere.

---

## Architectural Non-Goals

If AMP is used to:

* increase promotion frequency
* bypass user consent
* optimize revenue directly

Then it is being misapplied.

---

## Summary

AMP is a **decision constraint**, not a growth tool.

Its value emerges when it limits behavior, not when it expands it.

Systems that respect this boundary gain trust, clarity, and long-term leverage.
