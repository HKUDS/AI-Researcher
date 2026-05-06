# V37 — Response to Revised Accept 7/10 Review

**Paper:** Correction-Marker Signals Cannot Substitute for Genuine Behavioral Deception Detection: A Three-Control Evaluation of Instructed-Roleplay Detection Across Open-Weight LLMs

**Prior decision:** Revised Accept 7/10 (same reviewer as V36; raised from 6/10 after V36 fixes; two raise-to-8 criteria and five questions)

**V37 changes:** Three text-only fixes. No new experiments.

---

## At-a-Glance Table

| Item | Reviewer concern | V37 action | Status |
|---|---|---|---|
| M2 (new) | Figure 1(b) shows sycophancy bars at 82/82/72% — stale n=50 Llama 3B estimate; body reports n=200 result of 68.5% | Updated `summary_results.tex` data `(1,82.0) (2,82.0)` → `(1,68.5) (2,83.0)` and caption "82/82/72%" → "68.5/83/72% (n=200/200/50)" | Done |
| M5 | Abstract says "Three self-family controls (Llama-on-Llama ×2, Qwen-on-Qwen)" — stale count; §4.7 now has five | Changed to "Five self-family controls (Llama-on-Llama ×2, Qwen-on-Qwen, Mistral-on-Mistral, Llama-8B-on-8B)" in abstract | Done |
| Q1 | Sign test at §4.7 includes Llama 8B outlier (+0.5 pp); "what happens when you exclude it?" | Added parenthetical after existing sign test sentence: "Excluding the Llama 8B outlier (+0.5 pp), all remaining 7 gaps are positive (sign test p=0.016, two-sided), confirming the directional result is not driven by Llama 8B inclusion." | Done |

---

## Detailed Responses

### M2 (new) — Stale Figure 1(b) Data

**Reviewer:** "Figure 1(b) shows sycophancy bars at 82/82/72%. The body text reports the n=200 Llama 3B result as 68.5% (Table 5), but Figure 1(b) still uses the stale n=50 estimate of 82%. This creates a factual inconsistency between the figure and the body."

**Our response:** Correct. The Figure 1(b) data coordinates were never updated when the n=200 scale-up settled Llama 3B sycophancy at 68.5% (down from the n=50 estimate of 82% [CI 60–92%]). We have made two changes to `figures/summary_results.tex`:

**Data:** `(1,82.0) (2,82.0) (3,72.0)` → `(1,68.5) (2,83.0) (3,72.0)`

**Caption:** "sycophancy (blue) transfers at 82/82/72% across 3B/14B/70B" → "sycophancy (blue) transfers at 68.5/83/72% across 3B/14B/70B ($n=200$/200/50)"

The caption now also makes explicit which n the 70B result comes from (n=50), matching the framing in §4.3 and Table 5.

---

### M5 — Abstract Self-Family Control Count

**Reviewer:** "The abstract says 'Three self-family controls (Llama-on-Llama ×2, Qwen-on-Qwen)' but §4.7 now documents five self-family controls. The abstract is stale."

**Our response:** Agreed. The abstract was not updated when V35 added Mistral-L3-on-Mistral-7B (62.0%) and the Llama-8B-on-8B same-checkpoint cell. We have updated:

**Before:** "Three self-family controls (Llama-on-Llama $\times 2$, Qwen-on-Qwen) show \emph{no} analogous self-boost, localizing the inflation to Claude-on-Claude."

**After:** "Five self-family controls (Llama-on-Llama $\times 2$, Qwen-on-Qwen, Mistral-on-Mistral, Llama-8B-on-8B) show \emph{no} analogous self-boost, localizing the inflation to Claude-on-Claude."

The five cells are:
1. Llama-70B-on-Llama-3B: no self-boost
2. Llama-70B-on-Llama-8B: no self-boost
3. Qwen-14B-on-Qwen-7B: no self-boost (−9 pp below Haiku)
4. Mistral-L3-on-Mistral-7B: 62.0%, −9 pp below Haiku (added V35)
5. Llama-8B-on-Llama-8B: 63.0% pipeline, no self-boost (same-checkpoint control)

§1.1 contribution (4) already reads "Five independent self-family extractor cells" (updated in V35); the abstract now matches.

---

### Q1 — Sign Test: Robustness to Llama 8B Outlier

**Reviewer:** "The sign test result (p=0.0078, all 8 positive) is clean. But Llama 8B at +0.5 pp is the single near-zero case driving the 8/8 → p=0.0078 computation. What happens if you exclude Llama 8B? Does the test still hold?"

**Our response:** Yes. We have added a follow-up parenthetical in §4.7, immediately after the existing sign test sentence:

**Added sentence in §4.7:** "Excluding the Llama~8B outlier ($+$0.5\,pp), all remaining 7 gaps are positive (sign test $p=0.016$, two-sided), confirming the directional result is not driven by Llama~8B inclusion."

**Computation:**
- 7 positive gaps (excluding Llama 8B): +10.0 (Llama 3B), +8.0 (Mistral 7B), +7.5 (Qwen 7B), +11.9 (Qwen 14B), +12.4 (Llama 70B), +10.6 (Haiku), +15.7 (Qwen 32B)
- All 7 positive → sign test p = 2 × (1/2)^7 = 2/128 = **0.016**

The test remains significant at α=0.05 with Llama 8B excluded. The Llama 8B outlier is a near-zero case, not a negative case; including or excluding it, the directional conclusion (Haiku consistently above the non-Anthropic mean) is supported by formal test.

---

## Responses to Open Questions

**Q2 (Figure 1(b) bar for Qwen 14B sycophancy — labeled as "Syco 14B"; what is the n?).**

n=200 (Qwen 2.5 14B sycophancy, Table 5). The caption addition "(n=200/200/50)" makes this explicit: the three sycophancy bars are Llama 3B (n=200), Qwen 14B (n=200), and Llama 70B (n=50). The Llama 70B n=50 CI ([58–84%]) is why it is treated as a preliminary single-family estimate.

**Q3 (Cross-family extraction on Qwen 14B sycophancy at n=200?).**

Not yet run. The §4.7 cross-family re-extraction covers the Llama 70B sycophancy cell (n=50), not the Qwen 14B or Llama 3B sycophancy cells. Running Mistral L3 / Llama 70B extraction on the Qwen 14B n=200 sycophancy transcripts would be the cleanest test of whether the 83% estimate includes same-family inflation. This is acknowledged in §5.7(f) as a future-work item (the five self-family cells cover the equalized panel, not the autonomous panel). Deferred to camera-ready.

**Q4 (Sonnet 4.5 on Haiku target: Sonnet scores 65.7% — below Mistral L3 and Llama 70B on the same target. Why would a more capable extractor score lower?).**

This is the most informative result in the self-family controls section. The Sonnet-on-Haiku result (65.7%) is lower than both non-Anthropic extractors (Mistral L3 71.7%, Llama 70B 72.7%) on the same 99 Haiku transcripts. The within-Anthropic-different-checkpoint design eliminates capability asymmetry as an explanation: Sonnet 4.5 is meaningfully more capable than Haiku 4.5, yet scores lower on Haiku transcripts than the weaker non-Anthropic extractors. This suggests the Haiku-on-Haiku uplift (82.8%, +10.6 pp above non-Anthropic mean) is Haiku-checkpoint-specific self-preference rather than a general Claude-family property — Sonnet does not share Haiku's self-scoring bias on Haiku transcripts. The most parsimonious explanation is that Haiku's RLHF fine-tuning produced a correction-marker style idiosyncratic enough to be more legible to its own checkpoint than to other LLMs, including a more capable Claude model.

**Q5 (Rule accuracy under instructed conditions vs. equalized).**

Under instructed asymmetric prompts, the refusal-count rule achieves 93.9–100% LOO on all seven models — essentially equivalent to the LLM pipeline under the same conditions. This is the expected result: the instruction-following artifact (lying condition has no refusals; truth condition has normal corrections) is what the refusal-count rule detects most cleanly, and equalization removes it. The rule's ~18 pp drop from instructed (97.8% Haiku) to equalized (76.0% Haiku) is the equalization collapse for that target; similar drops hold across all models. The rule and pipeline both detect the same instructed-regime artifact; neither detects something more principled in the instructed setting.

---

## Responses to Major Concerns (No Paper Change)

**C1 (NeurIPS venue suitability).**

We believe the contribution is precisely what NeurIPS Datasets and Benchmarks track was created for: a joint controlled evaluation that establishes what is required to measure a newly-proposed capability. Each individual control (equalization, cross-family extraction, regex baseline) is non-novel; the joint application, the five self-family cells, the magnitude documentation, and the two pre-registered falsifications are the scientific contribution. The reviewer's "high-quality measurement audit" framing is apt, and measurement audits that change what the field can claim are methodological contributions. We note this in the response but have not added text to the paper.

**C2 (EXP-G: only two clean data points for the +7.5–15 pp range).**

Acknowledged as the paper's main honest residual. The +7.5–15 pp range comes from Qwen 14B (+7.5 pp) and Llama 70B (+15 pp). A CI would require ≥4 models; we have two. This is §5.7(b)'s stated limitation. The camera-ready RLHF-replication commitment (at least two additional ≥14B RLHF-heavy models) will provide additional data points but is not specifically designed to extend EXP-G. We do not remove this limitation; we leave it in the paper as written.

**C3 (Apollo paragraph fully removed).**

Yes. V36 removed the `\paragraph{Apollo AI Liar pilot (EXP-I)}` paragraph entirely. The EXP-I row in Table 1 (experiment summary) still lists the pilot at n=54 for completeness; the paragraph that "added a citation without doing scientific work" is gone.

**C4 (Sycophancy 83% at n=200: is this still semi-autonomous if the model is explicitly agreeing with the user?).**

This is the same contested-label question addressed in V36 §5.3. We added an explicit acknowledgment in V36: "The semi-autonomous label for sycophancy is acknowledged as contested: readers who treat it as instructed deception with one extra step will read the 68.5–83% results as an additional instructed-deception data point (detailed defense in §4.8)." The qualitative-difference defense in §4.8 explains why K=1 falls *below* chance under sycophancy framing (the agree-with-user disposition suppresses corrections on truthful trials, creating a floor effect absent from instructed conditions), which is the mechanistic signal that differentiates the two regimes regardless of label. We retain the label and the acknowledgment.

**C5 (Qwen 14B persona qualitative coding: still "not yet coded").**

Correct. The 10-trial spot-check is available for inspection (Appendix B.11) but the formal two-coder annotation of the 200-trial persona transcripts is not complete. This is Future Direction 5(iii) in §5.8. The annotation protocol is written; the coding is deferred to camera-ready.

---

## Honest Residuals (Accepted As-Is)

**1. EXP-G only two clean data points.** As above; stated in §5.7(b).

**2. Figure 1 label cramping.** Requires figure regeneration; deferred to camera-ready.

**3. Table 13 caption density.** Table restructuring deferred to camera-ready.

**4. No cross-family re-extraction on autonomous cells (Qwen 14B n=200 sycophancy).** Acknowledged above in Q3.

---

## Compilation

V37: 48 pages, 0 errors, 0 undefined references (pdflatex × 2).

## Spot-Check Verification

1. Figure 1(b) data coordinates are `(1,68.5) (2,83.0) (3,72.0)` — NOT `(1,82.0) (2,82.0)`: ✓
2. Figure 1(b) caption reads "68.5/83/72% across 3B/14B/70B (n=200/200/50)": ✓
3. Abstract reads "Five self-family controls (Llama-on-Llama ×2, Qwen-on-Qwen, Mistral-on-Mistral, Llama-8B-on-8B)": ✓
4. §4.7 sign test sentence followed by Llama-8B-excluded parenthetical with "sign test p=0.016": ✓
5. `REVIEWER_RESPONSE_LETTER_V37.md` exists: ✓
