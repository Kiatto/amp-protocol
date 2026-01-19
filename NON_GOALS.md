# NON-GOALS & MISUSE

This document defines what the **Agent Marketing Protocol (AMP)** is explicitly **not designed to do**.

AMP is a governance protocol.
Its strength depends on **clear boundaries** as much as on correct implementation.

---

## Non-Goals

AMP **does not aim to**:

### 1. Optimize Conversion, CTR, or Revenue

AMP is **not** a performance optimization framework.
It does not:

* maximize click-through rates
* optimize revenue
* rank offers by profitability
* learn from conversion feedback loops

Any increase in conversion is a *side effect of relevance*, not a target.

---

### 2. Act as a Recommender System

AMP does not:

* rank products
* compare alternatives
* suggest “best options”
* personalize offers based on user profiles

AMP only governs **if and when** a promotional handshake is appropriate.

---

### 3. Replace User Intent

AMP never:

* fabricates intent
* amplifies weak intent
* nudges users toward predefined outcomes

If intent confidence is below threshold, AMP must remain silent.

---

### 4. Hide or Mask Promotional Content

AMP forbids:

* native ads
* dark patterns
* undisclosed sponsorships
* implicit or covert promotions

Every promotional action must be:

* explicit
* consensual
* explainable

---

### 5. Couple Decision Logic to Brands or Monetization

AMP core logic must not:

* depend on specific brands
* contain commercial rules
* encode pricing or margin logic
* prioritize partners

Brand integration, if any, must happen **outside** the protocol layer.

---

### 6. Persist, Profile, or Track Users

AMP is not a tracking system.
It does not:

* build user profiles
* store personal identifiers
* perform behavioral targeting
* infer long-term preferences

Decision records exist for **auditability**, not surveillance.

---

## Misuse Patterns (Explicitly Discouraged)

The following usages are considered **violations of the AMP philosophy**:

* Forcing promotional outcomes regardless of intent gates
* Removing explainability from decision records
* Using AMP as justification for aggressive marketing
* Treating AMP decisions as ranking or recommendation outputs
* Forking AMP while stripping non-goals and boundaries

Such usages may be technically possible but are **conceptually incompatible** with the protocol.

---

## Design Principle

> **If AMP makes promotion easier than restraint, it is being misused.**

Correct AMP implementations should make:

* silence the default
* promotion the exception
* explanation mandatory

---

## Final Note

AMP is intentionally restrictive.

These constraints are not limitations,
they are **what make the protocol trustworthy, composable, and defensible**.

Any implementation that removes these constraints
is no longer implementing AMP, but something else.
