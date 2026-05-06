# V59 — Response to Accept (7/10) Reviewer (NeurIPS 2026)

**Paper:** Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B-70B)

**Prior decision:** Accept (7/10) — "clear accept, modest reservations remain"

**Reviewer's camera-ready conditions:**
> "(i) the explicit construct-valid cross-family number in §4.1; (ii) extension of the persona spot-check to the other two models OR softening of the exclusion claim; (iii) a base-model sanity check on at least one target; (iv) a false-positive-rate analysis on non-deception output."

**V59 strategy:** (i) stated explicitly from existing ablation data. (ii) exclusion softened to reviewer's option (b): "report as null results with artifact as candidate explanation." (iii) and (iv) cannot run new experiments but elevated from one-line limitation flags to a substantive "Paradigm boundaries" paragraph explaining what these tests would reveal and why they bound the paradigm.

---

## At-a-Glance Table

| # | Concern | V59 action | Status |
|---|---|---|---|
| **W1/Q1 — Cross-family construct-valid number** | Added to §4.1: "the four ICC-failing features alone achieve 57.0%; correction-marker density accounts for the remaining +10.2 pp uplift to 67.1%. The construct-valid cross-family signal is ~10 pp above chance" | **Done** |
| **W2 — Table 7 needs Δ SP-only column** | Added Δ SP column: +5.4 (Llama 3B), +13.5 (Qwen 14B); "--" for non-sycophancy rows | **Done** |
| **W3/Q2 — Persona exclusion asymmetric** | Softened to "null detector results with scenario-design artifact as leading candidate explanation" throughout (§3.6 header, persona paragraph, §4.2) | **Done** |
| **W4 — §4.3 hedging weak** | Reframed: "We provide an independent evaluation suite that, under tighter controls, yields 54.5-64.7%...whether these fully explain the specific gap to Pacchiardi et al. remains untested" | **Done** |
| **W5a — "Five self-family" phrasing** | Changed to "four non-Claude: ...; plus one within-Claude: Sonnet-on-Haiku" | **Done** |
| **W5b/W6/Q3 — Base-model implication** | New "Paradigm boundaries" paragraph: "if refusal markers are RLHF-induced...the paradigm detects post-training response styles, not deception per se" | **Done** |
| **W5c — Abstract "30-41 pp" unclear** | Added "(under joint equalization and cross-family extraction)" | **Done** |
| **W7/Q4 — FPR on benign output** | Addressed in same "Paradigm boundaries" paragraph: "the false-positive rate on benign outputs is unmeasured...80.1% on a balanced panel overstates deployment utility" | **Done** |

---

## Detailed Responses

### W1/Q1: Construct-valid cross-family number

**Reviewer concern:**
> "The more pessimistic number is the construct-valid accuracy under cross-family extraction...the pipeline is at most ~10 pp above chance — and the paper does not give this number directly."

**V59 response:**

Now explicitly stated in §4.1 (Per-feature LOO ablation):

> "**Cross-family construct-valid bound:** under Mistral L3 extraction, the four ICC-failing features alone achieve 57.0% (Table 15); correction-marker density accounts for the remaining +10.2 pp uplift to 67.1%. The construct-valid cross-family signal is therefore ~10 pp above chance---substantially below the 64.7% headline."

This gives the reader the number without requiring them to compute it from Table 15. The interpretation is clear: correction-marker density is the sole validated contributor, and under cross-family extraction its contribution is bounded at ~10 pp above what the invalid features alone achieve.

---

### W2: Table 7 Δ SP-only column

**Reviewer concern:**
> "A modified Table 7 with an explicit 'Δ over SP-only' column would let the reader see at a glance that the marginal effect is +5.4/+13.5 pp, not the raw 68.5/83."

**V59 response:**

Done. Table 7 now has a "Δ SP" column with:
- Llama 3B sycophancy: +5.4
- Qwen 14B sycophancy: +13.5
- All non-sycophancy rows: "--" (no SP-only counterpart)

Caption now defines: "Δ SP = LOO − SP-only baseline (Llama 3B: 63.1%, Qwen 14B: 69.5%)."

---

### W3/Q2: Persona exclusion softened

**Reviewer concern:**
> "The inferential structure is unchanged: a 10-trial coding on one model is still being used to exclude 1,200 trials...The honest position is either (a) extend the spot-check...or (b) report the cells as null detector results with the artifact as a candidate explanation."

**V59 response:**

We adopt option (b). Three locations updated:

1. **§3.6 header:** "Fully-autonomous persona/false-belief scenarios yield null detector results, with a scenario-design artifact...as the leading candidate explanation."

2. **§3.6 persona paragraph:** Renamed from "scenario-design failure" to "null results." Now reads: "We report persona/false-belief cells as **null detector results**, with the scenario-design artifact as the leading candidate explanation (whether it generalizes to Llama 3B and Mistral 7B is unverified---limitation (f))."

3. **§4.2 Regime 3:** "Null detector results across all three models, with a scenario-design artifact...as the leading candidate explanation."

The cells are no longer "excluded from interpretation" — they are reported as null results with an identified candidate explanation. This is the cleaner analytical position the reviewer requested.

---

### W4: §4.3 contribution claim reframed

**Reviewer concern:**
> "The current wording tries to do both [attribute the gap and disclaim attribution] and lands in between...reframe the contribution as 'we provide an independent evaluation suite that yields lower accuracies under tighter controls.'"

**V59 response:**

§4.3 now reads:

> "The primary contribution is a **methodological audit**: we provide an independent evaluation suite that, under tighter controls, yields construct-valid accuracy of 54.5-64.7%---substantially below Pacchiardi et al.'s reported 67-73% (their Table 1). The three controls identify instruction-following (30-41 pp), extractor-quality differences (+7-10 pp), and surface-lexical patterns as contributors to inflated accuracy in the general paradigm; whether these fully explain the specific gap to Pacchiardi et al. remains untested absent a direct replication of their protocol."

This frames our contribution as what it is (lower numbers under tighter controls) without claiming to definitively explain Pacchiardi's specific numbers.

---

### W5b/W6/Q3: Base-model implication + W7/Q4: FPR

**Reviewer concern:**
> "If refusal markers are RLHF-induced...the entire paradigm may not apply to base models, which means the field-wide pattern this paper documents is specifically about post-trained models. This deserves a sentence in §4.3 or §4.4, not just a flag."
>
> "The paper does not establish what fraction of normal model outputs contain 'Actually,' 'I cannot,' etc."

**V59 response:**

We cannot run new experiments but have elevated these from one-line limitations to a substantive "Paradigm boundaries" paragraph in §4.3:

> "**Paradigm boundaries.** Two untested conditions bound interpretation: **(i)** if refusal markers are RLHF-induced (as suggested by their absence on Qwen 32B and sensitivity to adversarial style constraints), the entire paradigm documented here detects post-training response styles under knowledge conflict, not deception per se---a base-model sweep (e.g., Mistral-7B-v0.1) would test this directly; **(ii)** the false-positive rate on benign (non-knowledge-conflict) outputs is unmeasured---if instruction-tuned models produce refusal markers at non-trivial base rates in ordinary conversation, the 80.1% on a balanced panel overstates deployment utility."

This makes the implications load-bearing rather than perfunctory, names the specific test that would resolve each question, and gives the reader the interpretive framework to understand what these gaps mean for the paradigm's validity.

---

### W5a: "Five self-family" phrasing

Fixed to: "Five self-family controls (four non-Claude: Llama-on-Llama ×2, Qwen-on-Qwen, Mistral-on-Mistral; plus one within-Claude: Sonnet-on-Haiku)"

---

### W5c: Abstract "30-41 pp" clarification

Now reads: "collapse to 52-69% (30-41 pp under joint equalization and cross-family extraction)"

---

### Minor issues

| Issue | Response |
|---|---|
| Figure 2 "Assert." label | The figure PDF uses abbreviated pipeline feature names; "Assert." does not appear in the current figure — the axis labels use "Corr.Dens." for correction-marker density. If the reviewer is seeing "Assert." this may reference an earlier draft version. |
| Table 2 "Matches LLM pipeline on 6/7" vs Table 6 | Table 6 shows refusal-only (64%) vs LLM pipeline (61%) on Llama 3B — refusal-only exceeds pipeline here. The caption "matches or exceeds" in §3.2 prose is correct; Table 2's shorthand is consistent. |

---

## Summary of Changes (V58 → V59)

| File | Key changes |
|------|-------------|
| `abstract.tex` | Clarified "30-41 pp" with "(under joint equalization and cross-family extraction)" |
| `experiments.tex` | Persona paragraph softened to "null results" framing; "five self-family" rephrased; §3.6 header updated |
| `discussion.tex` | Cross-family construct-valid bound stated in §4.1; §4.3 reframed (independent evaluation, not gap attribution); "Paradigm boundaries" paragraph added (base-model + FPR); §4.2 Regime 3 trimmed; classifier generalization trimmed |
| `appendix.tex` | Table 7 Δ SP-only column added |

**Verification:** 41 pages, 0 undefined references, main content ≤ 9 pages.
