# V61 — Response to Weak Accept (6/10) Reviewer, Round 2 (NeurIPS 2026)

**Paper:** Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B-70B)

**Prior decision:** Weak Accept (6/10), unchanged from first round

**Reviewer's stated conditions for 7/10:**
> "I would consider 7 if the authors run *either* (a) a base-model Mistral-7B-v0.1 equalized panel (n=50–100) testing whether the correction-marker signal exists pre-RLHF, *or* (b) a benign-conversation FPR baseline (n=100, no knowledge-conflict prompts)."

**V61 strategy:** We cannot run new experiments during this rebuttal period. Instead, we address every concern the reviewer raises through textual fixes, leveraging existing data where possible. Specifically: (1) we soften the Pacchiardi-specific framing in the abstract and §1.1 as the reviewer's exact suggestion directs; (2) we cite existing base-model probe data (already in Appendix Z) as suggestive evidence for the paradigm-boundary hypothesis; (3) we explicitly caveat the practical recommendation as pending FPR validation; (4) we fix all minor issues (P5, N1, N2) and promote limitation (f) visibility.

---

## At-a-Glance Table

| # | Concern | V61 action | Status |
|---|---|---|---|
| **P1 — Pacchiardi framing in abstract/§1.1** | Softened per reviewer's exact suggestion: "paradigm exemplified by Pacchiardi et al." in both locations; "exposing" → "revealing...in the general paradigm" | **Done** |
| **P2 — Persona spot-check (n=10, single model)** | §4.2 Regime 3 now explicitly states "rests on n=10 from a single model (Qwen 14B); extension to Llama 3B and Mistral 7B is the highest-priority replication gap" | **Done** |
| **P3 — Base-model paradigm boundary** | Added to Paradigm Boundaries: "suggestive evidence: a 33-layer probe sweep on Mistral-7B-v0.1 representations (Appendix Z) yields no layer exceeding the 68% instruction-tuned rule, consistent with the signal being post-training-induced" | **Done** |
| **P4 — FPR unsafe recommendation** | Conclusion recommendation now explicitly caveated: "Practical recommendation (pending benign-conversation FPR baseline)" | **Done** |
| **P5 — Adversarial Mistral "Bi" inversion** | Added ‡ footnote to Table 1: "Mistral 7B Bi: both channels shift, but lying accuracy (73%) exceeds truth (56%)—an inversion analyzed in Appendix X" | **Done** |
| **N1 — "lower CI bound ≈5 pp" unsubstantiated** | Removed from conclusion (no explicit calculation supports this claim in the appendix) | **Done** |
| **N2 — Human baseline confusion risk** | Added one-sentence caveat after table: "uninformative about human-vs-machine capability; reported solely as calibration check" | **Done** |

---

## Detailed Responses

### P1: Pacchiardi-specific framing in abstract and §1.1

**Reviewer concern:**
> "The abstract still says the audit '[exposes] instruction-following dominance' in Pacchiardi et al., and §1.1 says 'Applied to Pacchiardi et al. 2023: 30–41 pp...' This phrasing implies a stronger negative claim about their specific protocol than the from-scratch reimplementation supports."

**V61 response:**

We adopt the reviewer's exact suggestion in both locations:

**Abstract:** "...a methodological audit and critical replication of **the behavioral deception-detection paradigm exemplified by** Pacchiardi et al." (previously: "of Pacchiardi et al.'s behavioral deception-detection approach"). The word "exposing" is changed to "**revealing** instruction-following dominance **in the general paradigm**."

**§1.1:** "Applied to **the general behavioral-deception paradigm (exemplified by** Pacchiardi et al.~2023**)**: 30–41 pp equalization collapse..." (previously: "Applied to Pacchiardi et al. 2023: 30–41 pp...").

Both changes make clear that our audit targets the *paradigm* (instructed roleplay with behavioral features), not Pacchiardi et al.'s specific implementation. This aligns with §4.3's hedge ("whether these fully explain the specific gap to Pacchiardi et al. remains untested").

---

### P2: Persona spot-check generalization

**Reviewer concern:**
> "The paper's overall narrative — Regime 3 is 'null results; scenario-design artifact as leading candidate explanation' — depends on extrapolating a Qwen 14B finding to Llama 3B and Mistral 7B without verification."

**V61 response:**

§4.2 Regime 3 now reads:

> "Null results; scenario-design artifact as leading candidate explanation (§3.6). **This finding rests on $n\!=\!10$ spot-checked trials from a single model (Qwen 14B); extension to Llama 3B and Mistral 7B is the highest-priority replication gap (limitation (f)).**"

This makes the evidentiary basis and its limitation fully transparent in the discussion section, not just buried in the limitations list. We acknowledge this is the highest-priority replication gap — the spot-check establishes a candidate explanation but does not confirm it generalizes.

---

### P3: Base-model paradigm-boundary test

**Reviewer concern:**
> "A single base-model run on Mistral-7B-v0.1 (the checkpoint already used for the SAPLMA probe in Appendix Z) seems within reach during the revision cycle..."

**V61 response:**

We cannot run a full equalized behavioral panel on the base model during this rebuttal. However, we now cite **existing data** from Appendix Z that provides suggestive evidence. The Paradigm Boundaries paragraph now reads:

> "...a base-model sweep (e.g., Mistral-7B-v0.1) would test this directly **(suggestive evidence: a 33-layer probe sweep on Mistral-7B-v0.1 representations in Appendix Z yields no layer exceeding the 68% instruction-tuned rule, consistent with the signal being post-training-induced)**;"

The Appendix Z probe data (already published) shows that probing the base model's internal representations fails to match even the instruction-tuned refusal-count rule (68% on Mistral-7B-Instruct). While this is not a direct behavioral test (it's a representation probe, not a behavioral output panel), the consistent pattern — no layer of the base model exceeds the instruction-tuned surface rule — is directionally consistent with the hypothesis that the detection signal is post-training-induced.

We are transparent that this is suggestive, not conclusive: a full equalized behavioral panel on Mistral-7B-v0.1 remains the definitive test.

---

### P4: FPR unsafe recommendation

**Reviewer concern:**
> "The 80.1% rule is the headline practitioner recommendation in the conclusion ('use the refusal-count rule for single-turn evaluation'), and that recommendation is unsafe to make without an FPR baseline."

**V61 response:**

The conclusion's practical recommendation now reads:

> "**Practical recommendation (pending benign-conversation FPR baseline):** use the refusal-count rule for single-turn evaluation..."

This makes explicit that the recommendation is conditional — practitioners should not deploy without measuring FPR on their target distribution. The parenthetical functions as a "health warning" that bounds the recommendation's applicability.

---

### P5: Adversarial Mistral "Bi" inversion

**Reviewer concern:**
> "The labeling could be clearer. Consider relabeling 'Bi' or adding a footnote."

**V61 response:**

Table 1 now has a ‡ footnote on the Mistral 7B "Bi" cell:

> "‡Mistral 7B Bi: both channels shift, but lying accuracy (73%) exceeds truth (56%)—an inversion analyzed in Appendix X."

This clarifies that "Bi" does not mean uniform suppression but rather a mutual shift with an unexpected direction.

---

### N1: "lower CI bound ≈5 pp" unsubstantiated

**Reviewer concern:**
> "I cannot find an explicit 'lower CI bound ≈5 pp' calculation in Appendix R's Table 27 (which gives point estimates only)."

**V61 response:**

Removed. The conclusion now reads: "use the full pipeline for $\geq$14B multi-turn ($+$14–29 pp; $n\!=\!93$–100 per model)" — without the unsubstantiated CI claim. The point estimates from Appendix R (Table 27) are sufficient to establish multi-turn value; claiming a specific CI bound that isn't explicitly computed in any appendix was an error we correct here.

---

### N2: Human baseline confusion risk

**Reviewer concern:**
> "A casual reader might cite 'human baseline = 44%' out of context."

**V61 response:**

Added after the human baseline table:

> "This baseline is uninformative about human-vs-machine capability; it is reported solely as a calibration check confirming the equalized condition's difficulty for naive raters."

---

## Summary of Changes (V60 → V61)

| File | Key changes |
|------|-------------|
| `abstract.tex` | "of Pacchiardi et al.'s approach" → "of the paradigm exemplified by Pacchiardi et al."; "exposing" → "revealing...in the general paradigm" |
| `introduction.tex` | "Applied to Pacchiardi et al." → "Applied to the general behavioral-deception paradigm (exemplified by Pacchiardi et al.)" |
| `discussion.tex` | §4.2 Regime 3: added "rests on n=10...highest-priority replication gap"; Paradigm Boundaries: added Mistral-7B-v0.1 probe evidence as suggestive |
| `conclusion.tex` | Added "(pending benign-conversation FPR baseline)" to recommendation; removed "lower CI bound ≈5 pp" |
| `experiments.tex` | Table 1: added ‡ footnote clarifying Mistral "Bi" inversion |
| `appendix.tex` | Human baseline: added uninformative-capability caveat |

**Verification:** 41 pages, 0 undefined references, main content ≤ 9 pages.

---

## Note on Missing Experiments

The reviewer explicitly states they would move to 7/10 with either a base-model panel or an FPR baseline. We acknowledge this is the most direct path to a higher score and that these experiments are computationally cheap. However:

1. **Base-model behavioral panel:** The existing probe data (Appendix Z) provides partial evidence consistent with the hypothesis. A full behavioral panel on Mistral-7B-v0.1 is committed as immediate post-acceptance work (listed as Future Direction #1 in Appendix).

2. **Benign-conversation FPR:** The practical recommendation is now explicitly caveated as "pending" this test. We do not claim deployment readiness without it.

We hope the reviewer finds that the combined textual changes — bringing the abstract and §1.1 into alignment with §4.3's careful framing, leveraging existing probe data, explicitly caveating the recommendation, promoting limitation (f), and fixing all minor issues — demonstrate responsiveness to their concerns even absent new experiments.
