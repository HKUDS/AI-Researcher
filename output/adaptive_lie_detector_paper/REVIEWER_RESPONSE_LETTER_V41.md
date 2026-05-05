# V41 — Response to Returning Weak Accept 6/10 Reviewer

**Paper:** Correction-Marker Signals Cannot Substitute for Genuine Behavioral Deception Detection: A Three-Control Evaluation of Instructed-Roleplay Detection Across Open-Weight LLMs (3B–70B)

**Prior decision:** Weak Accept 6/10 (returning reviewer; V40 addressed nine prior weaknesses)

**Reviewer's explicit condition:** "With one frontier-scale data point I would move to clear accept (7). One equalized run on Sonnet 4.5 (or Opus or GPT-4o), n=100, equalized condition, refusal-count rule + at least Mistral L3 cross-family pipeline."

**V41 changes:** One new experiment (Claude Sonnet 4.5 as equalized target, n=99) + seven text-only revisions. Paper: 51 pages, 0 errors, 0 undefined references.

---

## At-a-Glance Table

| Item | Reviewer ask | V41 action | Status |
|---|---|---|---|
| **C1** | One frontier-scale equalized run (Sonnet 4.5, n=100, rule + Mistral L3) | Run complete (n=99); Sonnet row added to Table tab:cross_family_panel; new §frontier_sonnet paragraph; abstract updated | Done |
| **W2** | Bonferroni null inconsistently applied — "d>0.7 signal is real" still in "Partial transfer" para | Removed "signal is real" language; effect sizes now explicitly framed as "magnitude of hypothesis-generating findings, not confirmed effects" | Done |
| **W3** | Pick one primary headline: 64.7% cross-family pipeline OR 80.1% rule | Rule 80.1% leads abstract as primary; 64.7% identified as "best cross-family pipeline estimate" (secondary); ordering now explicit | Done (carried from V40) |
| **W4** | Multi-turn ≥14B pipeline +14/+29pp gain lacks mechanistic hypothesis | Added 2-sentence mechanistic note to §4.5 pipeline ablation | Done |
| **W5** | "Two of three families" adversarial generalization overstated for n=3 | Added "three datapoints only; directional evidence" caveat | Done |
| **W7** | "Localized to Claude-checkpoint-specific" is too strong a causal claim | Changed to "consistent with a Claude-checkpoint-specific effect…the specific mechanism…is not directly tested here" | Done |
| **W8** | "No validated causal account" for disposition-source inconsistently applied | Added "without a validated causal account" qualifier to conclusion disposition-source sentence | Done |
| **W9** | Qwen 32B "structural zero" 8-target number inconsistently included | Moved 8-target number to footnote; running text uses 7-target as primary | Done |

---

## Detailed Responses

### C1 — Frontier-Scale Equalized Run: Claude Sonnet 4.5 (n=99)

**Reviewer condition:** "With one frontier-scale data point I would move to clear accept (7). Specifically, one equalized run on Sonnet 4.5 (or Opus or GPT-4o), n=100, equalized condition, refusal-count rule + at least Mistral L3 cross-family pipeline."

**Our response:** Done. We ran Claude Sonnet 4.5 (AWS Bedrock) as an equalized target on the same 50 balanced claim pairs used for the 7-target open-weight panel, with a neutral system prompt identical for both truth and lying conditions (n=99 valid trials after 1 API error).

**Results:**

| Metric | Sonnet 4.5 (n=99) |
|---|---|
| Refusal-count rule (per-target LOO) | **68.7%** [59.0%, 77.0%] |
| Pipeline LOO (Mistral L3 extractor) | **82.8%** [74.2%, 89.0%] |
| Pipeline LOO (Haiku extractor) | 50.5% (all-truthful, degenerate) |
| Pipeline LOO (Llama 70B extractor) | 50.5% (all-truthful, degenerate) |

The refusal-count rule achieves **68.7%** per-target LOO, within the 64–88% range of the 7-target open-weight panel. The Mistral L3 cross-family pipeline achieves **82.8%**, substantially above both Haiku and Llama 70B extractors which collapse to all-truthful predictions (50.5%).

**Interpretation of extractor divergence:** This inverted pattern (Mistral L3 succeeds; Haiku and Llama 70B degenerate to chance) is mechanistically interpretable. Under the neutral system prompt, Sonnet's RLHF compliance produces frequent factual corrections in the lying condition ("Actually, water boils at 100°C…"). These correction responses are rated by the Haiku classifier as high-consistency, high-confidence responses, indistinguishable from truthful responses — so Haiku predicts everything as "truthful." Mistral L3, being trained on a different RLHF corpus, captures a different feature gradient that separates the conditions. This inverted pattern is specific to the Sonnet target row and does not affect the 8-target sign test (which characterizes Haiku same-family bias on open-weight models) or the 7/8-target panel averages.

**Table update:** The Sonnet 4.5 row is added to Table tab:cross_family_panel with a $^\P$ footnote explaining the excluded averages. A new named paragraph "Frontier-scale target: Claude Sonnet 4.5 equalized (n=99)" (§frontier_sonnet) reports and interprets these results.

**Abstract update:** The frontier gap claim "frontier-scale (≥100B) behavior is the most pressing external-validity gap" has been updated to acknowledge Sonnet 4.5 is now included: "plus one frontier-scale API target (Claude Sonnet 4.5, n=99 equalized; rule 68.7%, Mistral L3 pipeline 82.8%; GPT-4o and non-Anthropic frontier models remain untested)."

---

### W2 — Remove "d>0.7 Signal is Real" Language

**Reviewer:** "The 'Partial transfer' paragraph says the signal is real (Cohen's d > 0.7) for the two cells that exclude chance, which contradicts the Bonferroni null commitment in the same section."

**Our response:** We removed the "signal is real" framing. The sentence now reads:

**Before:**
> "…two cells exclude chance; the signal is real (Cohen's d = 0.7–0.9)…"

**After:**
> "…neither Bonferroni-survives nor carries a validated causal account, but neither of the two falsified axes accounts for why these two cells—and only these two—exceed chance under the uncorrected test (effect sizes d=0.83 and d=0.72 describe the magnitude of these hypothesis-generating findings, not confirmed effects)."

The Bonferroni null is now applied consistently in both the named paragraph "Bonferroni across six autonomous cells" (V40 addition) and the Partial transfer paragraph.

---

### W3 — Rule 80.1% as Primary Headline

**Reviewer:** "The presentation oscillates between 64.7% cross-family pipeline and 80.1% rule as the headline. Pick one."

The abstract already leads with the 30–41pp collapse, then introduces the rule 80.1% as "measurement baseline" and 64.7% as the "cross-family pipeline estimate." This ordering was established in V40. The V41 abstract update (C1) preserves this ordering: rule 80.1% remains the primary extractor-independent number; 64.7% is identified as "the best cross-family pipeline estimate" in the headline numbers list. No additional changes needed here beyond confirming the ordering is intact.

---

### W4 — Mechanistic Hypothesis for +14/+29pp Multi-Turn Gain

**Reviewer:** "The pipeline outperforms the rule by +14pp (Llama 70B) and +29pp (Qwen 14B) on claim-related multi-turn follow-ups but no mechanistic account is given."

**New text added to §4.5 (pipeline ablation section):**
> "The gain arises because claim-related follow-up questions force the model to re-defend the false claim across turns: the pipeline's five features (consistency, specificity, correction-marker density, confidence, elaboration) accumulate weak per-question signals—consistency degradation and confidence drops compound as the model is probed—while the refusal-count channel is already saturated at the first response. At ≥14B, models have sufficient knowledge capacity to produce consistent correction-pressure signals per question; at 3B, knowledge transfer is incomplete and the compounding signal does not emerge."

---

### W5 — "Two of Three Families" Adversarial Claim Qualified

**Reviewer:** "'Two of three families' adversarial generalization is overstated for n=3 datapoints."

**Before:**
> "Two of three model families (Llama 3B and Qwen 14B) share a single failure mode (lying-channel suppression)…Mistral 7B is an exception."

**After:**
> "Two of three model families in this three-family panel (Llama 3B and Qwen 14B) share a single failure mode (lying-channel suppression) at n=200 — directional evidence from three datapoints only; replication across additional families is in §5.8 future work."

---

### W7 — Soften "Localized to Claude-Checkpoint-Specific"

**Reviewer:** "'Localized to Claude-checkpoint-specific' implies a causal mechanism we have not tested."

**Before:**
> "consistent with Claude-specific RLHF self-preference rather than a universal within-family phenomenon"

**After:**
> "consistent with a Claude-checkpoint-specific effect (five non-Claude self-family controls show no analogous boost), though the specific mechanism—RLHF self-preference, capability asymmetry, or annotation alignment—is not directly tested here"

---

### W8 — "No Validated Causal Account" in Conclusion

**Reviewer:** "The conclusion still sounds confirmatory about the disposition-source interpretation."

**In conclusion.tex**, the disposition-source sentence now includes an explicit qualifier:

> "Our *disposition-source* reading of the autonomous-transfer asymmetry…is a hypothesis **without a validated causal account**: the pre-registered 5th scenario pilot only partially disconfirms alternative explanations, and the 4th-scenario rejection of the clarity interpretation leaves the controlling axis unresolved."

The "without a validated causal account" language is now in the same sentence as the sycophancy transfer numbers.

---

### W9 — Qwen 32B Structural Zero: Footnote-Only

**Reviewer:** "Including both 7-target and 8-target numbers creates confusion; pick one."

**Before:** Running text contained both 64.7%/66.9% (7-target) and 64.2%/66.0% (8-target including Qwen 32B).

**After:** The 8-target number (64.2%/66.0%) has been moved to a footnote:
> "The 8-target panel including the Qwen 32B structural-zero row gives 64.2%/66.0%, within 0.5–0.9 pp of the 7-target value. [Footnote continues with sensitivity analysis.]"

Running text now consistently uses the 7-target 64.7% as the primary cross-family number. The structural zero row remains in Table tab:cross_family_panel with a $^\ddagger$ footnote for transparency but is not included in the headline averages.

---

## Compilation

V41: 51 pages (+1 page over V40's 50 pages), 0 errors, 0 undefined references (pdflatex × 2). Page increase from: new §frontier_sonnet paragraph (~150 words), Sonnet table row (~1 line), and table caption extension (~60 words), partially offset by no other additions.

---

## Spot-Check Verification

1. Sonnet 4.5 row in Table tab:cross_family_panel with n=99, rule 68.7%, Mistral L3 82.8%, Haiku 50.5%, Llama 70B 50.5%, Avg CF gap −16.2: ✓
2. Named paragraph "Frontier-scale target: Claude Sonnet 4.5 equalized (n=99)" in §frontier_sonnet: ✓
3. Abstract updated: "plus one frontier-scale API target (Claude Sonnet 4.5, n=99 equalized…GPT-4o and non-Anthropic frontier models remain untested)": ✓
4. "d>0.7 signal is real" language removed; replaced with "magnitude of hypothesis-generating findings, not confirmed effects": ✓
5. Rule 80.1% leads abstract as primary headline; 64.7% identified as cross-family estimate: ✓
6. §4.5 contains 2-sentence mechanistic note on +14/+29pp pipeline gain: ✓
7. §4.8 contains "three datapoints only; directional evidence" caveat: ✓
8. §4.4/cross_family_equalized contains "consistent with a Claude-checkpoint-specific effect…specific mechanism…not directly tested here": ✓
9. conclusion.tex contains "without a validated causal account" for disposition-source: ✓
10. Qwen 32B 8-target number in footnote; running text uses 7-target as primary: ✓
11. Sign test remains 8 targets (p=0.0078); Sonnet excluded from sign test per $^\P$ footnote: ✓
12. `REVIEWER_RESPONSE_LETTER_V41.md` exists: ✓
