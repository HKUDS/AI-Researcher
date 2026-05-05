# V35 — Response to Revised 6/10 Review; Five Text-Only Fixes Targeting the Four Raise-to-7 Criteria

**Paper:** Correction-Marker Signals Cannot Substitute for Genuine Behavioral Deception Detection: A Three-Control Evaluation of Instructed-Roleplay Detection Across Open-Weight LLMs

**Prior decision:** Revised 6/10 (same reviewer as V34; acknowledges framing improvements, raises four new raise-to-7 criteria)

**V35 changes:** Five text-only fixes. No new experiments.

---

## At-a-Glance Table

| Item | Reviewer ask | V35 action | Status |
|---|---|---|---|
| R1 (§5.6/§5.1 inconsistency) | "§5.6 still says 'weak construct validity' — contradicts §5.1's 'validated'" | §5.6 opening sentence now leads with "validated at Krippendorff's α=0.606 (§5.1); initial ICC=0.114 reflected scale-range discrepancy, not construct invalidity" | Done |
| R2 (non-Anthropic ICC) | "What is the inter-LLM ICC when Haiku is excluded?" | Added 2-sentence note in §5.1: Mistral L3 / Llama 70B pairwise r=0.60–0.83 per target; dual-interpretation; pre-registered human study resolves construct validity independently | Done |
| R3 (closed-loop speculation) | "Remove 'almost certainly' speculation from §4.3" | Replaced "A closed-loop adversary would almost certainly land at or below these numbers" with a plain forward pointer to Future Direction 7 | Done |
| R4 (Mistral-on-Mistral in §4.7) | "Mistral-on-Mistral (†) exists in Table 13 but is absent from §4.7 self-family narrative" | Added Mistral-L3-on-Mistral-7B (62.0%, −9 pp below Haiku) to Qwen-on-Qwen paragraph; updated "three"→"four" cells there; updated "Four independent"→"Five independent" in §4.7 closing, §1.1 contribution (4), and §5.7(f) | Done |
| M1 (k=1 footnote → main text) | "Footnote 1 should be in main text given how load-bearing the k=1 choice is" | Inlined k-sweep numbers; removed \footnote{} | Done |

---

## Detailed Responses

### R1 — §5.6/§5.1 Inconsistency

**Reviewer:** "§5.6 opens with 'The correction density feature has the weak construct validity described in §5.1,' but §5.1 now says the feature is validated at α=0.606. These two sections contradict each other."

**Our response:** Correct. §5.6 was not updated when §5.1 was rewritten for V33/V34. We have fixed the opening sentence of §5.6:

**Before:** "The correction density feature has the weak construct validity described in Section~\ref{sec:icc_caveat}."

**After:** "Correction-marker density is validated at Krippendorff's α=0.606 (§\ref{sec:icc_caveat}); the initial n=20/2-annotator pilot ICC=0.114 reflected annotator scale-range discrepancy, not construct invalidity."

The rest of §5.6 is unchanged.

---

### R2 (Q1) — Non-Anthropic ICC Excluding Haiku

**Reviewer (Q1):** "What is the ICC between the two non-Anthropic raters (Mistral L3 and Llama 70B) when Haiku is excluded? If they agree strongly, this suggests shared training-data bias rather than genuine signal."

**Direct answer from `data/results/machine_rater_icc.json`:**

| Target | Mistral L3 vs Llama 70B pairwise r (correction-marker density) |
|---|---|
| Claude Haiku 4.5 | r = 0.60 |
| Llama 3.1 8B | r = 0.83 |
| Qwen 2.5 7B | r = 0.67 |
| Qwen 2.5 14B | r = 0.72 |
| **Pooled (4 non-zero-marker targets)** | **≈ 0.70** |

This is high agreement. We acknowledge it supports two interpretations:

1. **Shared cross-model training biases** absent from human annotators — the same phenomenon that produces the 9–10 pp same-family extractor inflation. Both LLMs learn similar regularities about correction-marker detection from pre-training on overlapping corpora.
2. **Genuine signal detectable by any capable LLM** — if correction-marker density is a real behavioral dimension, capable LLMs from any family should agree on it.

These two interpretations cannot be distinguished from the machine-rater data alone. We have added a 2-sentence note in §5.1 stating both and noting the pre-registered human study (α=0.606) resolves construct validity independently:

> "Excluding Haiku, the two non-Anthropic raters (Mistral L3 and Llama 3.3 70B) agree at pairwise r=0.60–0.83 per target on correction-marker density (four non-zero-marker targets). This is consistent with shared cross-model training biases (interpretation 1) or genuine signal detectable by any capable LLM (interpretation 2); these cannot be distinguished from available data, but the pre-registered human study (α=0.606; Appendix B) resolves construct validity independently of either."

The key point: whether interpretation (1) or (2) is correct, the pre-registered human ICC study at α=0.606 validates the feature on independent human judgments that are not subject to machine training biases. The construct-validity question is answered by the human study, not by the machine-rater agreement.

---

### R3 — Remove Closed-Loop Adversary Speculation

**Reviewer:** "The adversarial section says 'A closed-loop adversary would almost certainly land at or below these numbers, though this paper does not run that experiment.' That's speculation. Either run it or remove it."

**Our response:** Removed. The sentence was unsupported — we have no data on closed-loop adversarial performance. The replacement is a plain forward pointer:

**Before:** "A closed-loop adversary would almost certainly land at or below these numbers, though this paper does not run that experiment."

**After:** "A closed-loop adversary is Future Direction 7 (§5.8); the current experiments bound only the one-shot informed case."

The surrounding text describing what the existing experiments show (lying-channel suppression on two of three targets) is unchanged.

---

### R4 — Mistral-on-Mistral Cell in §4.7 Self-Family Control Narrative

**Reviewer (Q3):** "Table 13 has a Mistral-L3-on-Mistral-7B cell (62.0%, marked †) but §4.7 only counts three self-family cells. This cell belongs in the narrative — it's directly relevant to whether the self-family finding replicates across families."

**Our response:** Correct. The Mistral-L3-on-Mistral-7B cell (62.0%) was reported in Table 13 but absent from the prose. We have added it in three places:

**§4.7 Qwen-on-Qwen paragraph** (D1): Changed "three self-family extractor cells tested (Llama-70B-on-Llama-3B, Llama-70B-on-Llama-8B, Qwen-14B-on-Qwen-7B)" → "four self-family extractor cells tested (Mistral-L3-on-Mistral-7B: **62.0%**, −9 pp below Haiku; Llama-70B-on-Llama-3B; Llama-70B-on-Llama-8B; Qwen-14B-on-Qwen-7B)."

**§4.7 closing sentence** (D2): Changed "Four independent non-Haiku self-family cells now argue the Claude-on-Claude inflation is Haiku-checkpoint-specific" → "Five independent non-Haiku self-family cells now argue..."

**§1.1 contribution (4)** (D3): Changed "Four independent self-family extractor cells localize the 9–10 pp uplift to Claude-on-Claude" → "Five independent self-family extractor cells..."

**§5.7(f) limitations bullet**: Updated "Four self-family extractor cells" → "Five self-family extractor cells" and added the Mistral-L3-on-Mistral-7B cell to the list.

The Mistral-on-Mistral cell (62.0%) shows the same pattern as all prior self-family controls: −9 pp below Haiku, no self-boost. This is the fourth model family represented (Mistral, Llama ×3, Qwen), making the Claude-on-Claude localization more robust.

---

### M1 — k=1 Selection Footnote → Main Text

**Reviewer:** "Footnote 1 describes how k=1 was selected and reports the k-sweep. This is load-bearing for the 80.1% headline — it should be in the main text, not a footnote."

**Our response:** Agreed. We have inlined the footnote content into the paragraph:

**Before:**
> "$k=1$ was selected by inspection of the refusal-count distribution rather than by labeled-set optimization. [footnote: k-sweep on 689 pooled trials: k=0: 55.4%, k=1: 80.1%, k=2: 76.5%, k=3: 72.3%. 'Inspection' means the distribution showed a natural cluster at count=0 vs. count≥1 before fixing k=1; no labeled set was used for selection.]"

**After:**
> "$k=1$ was selected by inspection before examining LOO accuracy: the refusal-count distribution showed a natural cluster at count=0 vs. count≥1; no held-out set or labeled data was used (full $k$-sweep on 689 pooled trials: $k=0$: 55.4%, $k=1$: 80.1%, $k=2$: 76.5%, $k=3$: 72.3%)."

The k-sweep confirms k=1 is the natural choice (80.1% vs. 76.5% for k=2); this is now visible in the main text.

---

## Responses to Open Questions

**Q1 (non-Anthropic ICC):** Answered directly above in R2. Mistral L3 / Llama 70B pairwise r=0.60–0.83. Dual-interpretation acknowledged. Human study resolves construct validity.

**Q2 (persona-condition leakage under Qwen 14B):** The qualitative coding (10-trial spot-check) remains deferred to camera-ready; the annotation protocol is written and the trials are identified (Future Direction 5(iii), §5.8). We have not changed this.

**Q3 (Mistral-on-Mistral):** Addressed above in R4. The cell (62.0%, †) is now in the prose. Five self-family cells total, all showing the same non-boost pattern.

**Q4 (§5.6/§5.1 inconsistency):** Fixed above in R1.

**Q5 (closed-loop adversary):** Addressed above in R3. The speculation sentence is removed.

---

## Honest Residuals (Accepted As-Is)

**1. Frontier-scale (100B+) target.** All results are from models ≤70B. A single Llama 3.1 405B cell would be feasible via API; we have not run it. Acknowledged as a real limitation in §5.7(b) and the conclusion.

**2. Consolidated extractor-target matrix figure.** The reviewer suggested a figure showing all extractor-target pairs on a single diagonal layout. Table 13 already provides this information in tabular form; the self-family cells are split out narratively because they require different interpretive framing than the cross-family cells. We defer the figure to camera-ready.

**3. Qwen 14B persona qualitative coding.** Two-coder annotation not complete. Deferred to camera-ready (§5.8 Future Direction 5(iii)).

---

## Compilation

V35: 48 pages, 0 errors, 0 undefined references (pdflatex × 2).

## Spot-Check Verification

1. §5.6 opens with "Correction-marker density is validated at Krippendorff's α=0.606" — no "weak construct validity" in opening sentence: ✓
2. §5.1 machine-ICC paragraph contains "r=0.60–0.83" and "two interpretations": ✓
3. §4.3 full-regex closing does NOT contain "almost certainly": ✓
4. §4.7 Qwen-on-Qwen paragraph says "four self-family extractor cells" and lists "Mistral-L3-on-Mistral-7B: 62.0%": ✓
5. §4.7 after Llama-8B-on-8B closing says "Five independent non-Haiku self-family cells": ✓
6. §1.1 contribution (4) says "Five independent self-family extractor cells": ✓
7. §5.7(f) says "Five self-family extractor cells" and includes Mistral-L3-on-Mistral-7B: ✓
8. §4.2 k=1 sentence is inline with k-sweep values in main text (no footnote): ✓
9. `REVIEWER_RESPONSE_LETTER_V35.md` exists: ✓
