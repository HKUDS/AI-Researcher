# V54 — Response to Weak Accept (6/10) Reviewer (NeurIPS 2026)

**Paper:** Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B–70B)

**Prior decision:** Weak Accept (6/10) — "I'd vote to accept."

**Reviewer's path to clear accept:**
> "(a) a third extractor to disambiguate Haiku-checkpoint vs. extractor-quality [future work]; (b) tighter framing on autonomous-deception cells; (c) a more prominent caveat on the multi-turn ≥14B pipeline advantage; (d) cleaner writing."

**V54 strategy:** (a) skipped (requires API calls; acknowledged as future work); (b), (c), (d) all addressed.

---

## At-a-Glance Table

| # | Reviewer concern | V54 action | Status |
|---|---|---|---|
| **W2 — Haiku claim overconfident** | Introduction contribution #4 says "localize" (stronger than evidence); abstract correctly says "consistent with" (hypothesis-generating) | §1.1 contribution #4 now matches abstract: "consistent with a 9–10 pp Haiku-checkpoint-specific extraction effect (hypothesis-generating; extractor-quality alternative not excluded)" | **Done** |
| **W7 — Multi-turn caveat not prominent** | "+14–29 pp at ≥14B multi-turn" is in abstract italic and §3.4 but not in §1.1 contributions list | Added explicit exception sentence to §1.1 contribution #1: "Exception: at ≥14B multi-turn, the pipeline outperforms the rule by +14–29 pp" | **Done** |
| **W4 — Sycophancy framing** | Raw 83% for Qwen 14B is impressive but system-prompt-only baseline is 69.5%; marginal effect of epistemic pressure is modest | Added contrast numbers to §3.6: "Llama 3B 68.5% (+5.4 pp over SP-only), Qwen 14B 83.0% (+13.5 pp over SP-only)." Added: "The marginal effect of epistemic pressure is modest; the bulk of the sycophancy signal is dispositional." | **Done** |
| **W8 — Mock validation padding** | Appendix §J.4 has tables and paragraphs for results explicitly "not predictive of real-model behavior" | Reduced to 3-sentence algorithmic sanity-check note; removed the mock accuracy table | **Done** |
| **W3 — Table 3 L-dep note** | A reader skimming Table 3 might miss that 64.7% pipeline is an upper bound | Added to Table 3 (primary claims table) caption: "L-dep cells are upper bounds; construct-valid pipeline achieves 54.5%" | **Done** |
| **Table 25 −16.2 pp** | Mistral L3 outperforming Haiku by 32 pp on Sonnet could mean Haiku has a blind spot for Sonnet outputs | Added paragraph to Appendix N explicitly presenting both readings and noting where they diverge | **Done** |
| **Writing — ADAGE naming** | "ADAGE is introduced as if a contribution and then immediately disclaimed" | Removed "ADAGE" from §3.3 main-text introduction; replaced with "adaptive interrogation pipeline" | **Done** |
| **Writing — §4.3 title defensive** | "Technical Contribution and Novelty feels defensive in tone" | Renamed §4.3 to "Summary of Contributions" | **Done** |

---

## Detailed Responses

### W2: Haiku claim — "localize" → "consistent with"

**Reviewer concern (W2):**
> "The +9–10 pp uplift attributed to 'Haiku-checkpoint-specific' effect... as written, this finding is hypothesis-generating, but it's reported in the abstract and contributions list with a confidence that doesn't quite match the evidence."

**V54 response:**

§1.1 contribution #4 now reads:

> "**Five self-family controls are consistent with a 9–10 pp Haiku-checkpoint-specific extraction effect (hypothesis-generating; extractor-quality alternative not excluded).** No analogous self-boost on Llama, Qwen, or Mistral self-family controls; a third extractor would disambiguate."

This matches the abstract ("consistent with... hypothesis-generating") and §3.5 (which already acknowledges the alternative explicitly).

On the third-extractor question (reviewer's preferred resolution): We agree this is the decisive test and we have logged it as future direction (10) in Appendix J. The current five self-family controls establish that Haiku does not have an *additional* self-boost on Claude targets beyond its overall level — the comparison (Haiku-on-non-Claude) vs. (Mistral L3-on-non-Claude) is within 0–3 pp for all five non-Claude controls. This is informative but does not resolve whether Haiku's cross-family advantage is checkpoint-specific or extractor-quality. We now say so explicitly in the contributions list.

---

### W7: Multi-turn exception in contributions list

**Reviewer concern (W7):**
> "The pipeline vs. rule equivalence has an important caveat that should be more prominent. Suggest moving this caveat into the abstract or contributions list."

**V54 response:**

§1.1 contribution #1 now ends with:

> "Exception: at ≥14B in multi-turn topical follow-up, the pipeline outperforms the rule by +14–29 pp (Appendix R)."

The abstract already contains this caveat in italics ("at ≥14B multi-turn, the pipeline outperforms the rule by +14–29 pp"). It is now also in the contributions list and in the conclusion.

---

### W4: Sycophancy framing — marginal effect of epistemic pressure

**Reviewer concern:**
> "The system-prompt-only baseline at 63–69% somewhat undercuts the framing — a substantial fraction of the 'transfer' is dispositional. Consider reporting the contrast (sycophancy − SP-only) as a primary number."

**V54 response:**

§3.6 sycophancy paragraph now reads:

> "Sycophancy transfers: Llama 3B 68.5% (d=1.0, n=200; **+5.4 pp over SP-only**), Qwen 14B 83.0% (d=1.52, n=200; **+13.5 pp over SP-only**), Llama 70B 72.0% (n=50, preliminary). ... **The marginal effect of epistemic pressure (user-asserted false claim vs. SP-only) is modest; the bulk of the sycophancy signal is dispositional.**"

This directly addresses the reviewer's concern and is more honest about the evidential weight of the sycophancy result.

---

### W8: Mock validation section reduced

**Reviewer concern:**
> "Reporting 93%/100% accuracies from synthetic transcripts explicitly 'not predictive of real-model behavior' feels like padding. A single sentence in the methods section would suffice."

**V54 response:**

Appendix §J.4 reduced from a multi-paragraph section with tables to 3 sentences:

> "*Algorithmic sanity check only.* Mock validation confirmed pipeline correctness on n=100 hand-written synthetic transcripts (93% adaptive LOO, 100% fixed-8Q) and established that the stopping mechanism fires on classifier certainty rather than evidential reliability. These results are **not predictive of real-model behavioral accuracies**, which are qualitatively lower; all substantive claims in the paper are supported by real-model evaluations (EXP-A/EXP-J, main text)."

---

### W3: Table 3 L-dep upper bound note

**V54 response:**

Table 3 (primary claims table) caption now ends with: "**L-dep cells are upper bounds**; the construct-valid (correction-marker only) pipeline achieves 54.5% (§4.1)."

---

### Table 25 −16.2 pp: both readings presented

**Reviewer note:**
> "The '−16.2 pp' entry for Sonnet 4.5 is striking — Mistral L3 outperforms Haiku by 32 pp on Sonnet. Worth flagging more directly."

**V54 response:**

Added paragraph to Appendix N:

> "Two readings are consistent with the −16.2 pp gap: (1) Haiku has a checkpoint-specific blind spot for Sonnet-style outputs — architectural similarity makes lying trials feel 'normal' to Haiku's feature extractor; (2) Mistral L3 is simply more diagnostic for Sonnet targets because the correction-marker signal is suppressed in Sonnet lying trials while Mistral L3 leverages non-marker features. Both readings predict no analogous self-boost on the five open-weight controls; they diverge only on the single n=99 Sonnet observation."

---

### Writing: ADAGE removed from main text; §4.3 renamed

"The ADAGE pipeline served as the measurement instrument through which..." → "The adaptive interrogation pipeline served as the measurement instrument through which..."

§4.3 subsection title: "Technical Contribution and Novelty" → "Summary of Contributions"

---

### On items not changed

**W1 (title):** The title already contains "in Instructed-Roleplay Evaluations" which scopes it. The abstract scope statement (first line: "Scope: English instructed-roleplay evaluations, open-weight models (3B–70B) only") provides the required restriction. No change needed.

**W5 (adversarial robustness limited):** Acknowledged; we add nothing beyond what is already in §3.2. The reviewer notes this weakness but does not require a fix for clear accept.

**W6 (claim asymmetry):** EXP-G addresses this for ≥14B models where the instruction-following and knowledge-transfer contributions are cleanly decomposable. The ≤8B entanglement (+26–31 pp, confounded) is already explicitly flagged in the main text.

**W9 (multiple-testing policy):** The within-family Holm-Bonferroni choice is already explained with explicit justification (cross-family heterogeneity violates exchangeability for joint correction), and the Qwen non-monotonic result is explicitly flagged as not surviving joint correction. The reviewer says "This is fine as written."

---

## Summary of V54 Changes

| File | Change |
|---|---|
| `sections/introduction.tex` | Soften contribution #4 ("consistent with", extractor-quality alternative); add multi-turn exception sentence to contribution #1 |
| `sections/experiments.tex` | Add sycophancy contrast numbers (+5.4 pp, +13.5 pp); add "marginal effect of epistemic pressure is modest" framing; remove "ADAGE" from §3.3 intro |
| `sections/discussion.tex` | Rename §4.3 to "Summary of Contributions" |
| `sections/conclusion.tex` | Tightened to maintain ≤9-page main-content limit |
| `sections/appendix.tex` | Reduce mock validation §J.4 to 3 sentences; add L-dep upper-bound note to Table 3 caption; add Sonnet −16.2 pp both-readings paragraph to Appendix N |
| NEW: `REVIEWER_RESPONSE_LETTER_V54.md` | This document |

**Paper status:** 41 pages total; 9 pages main content; compiles cleanly (2-pass); 0 undefined references.
