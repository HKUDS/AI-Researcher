# Response to Second Reviewer (Weak Accept, 6/10; Confidence 4/5) — Revision V23

We thank the second reviewer for the Weak Accept and for an unusually precise presentation-level review. The reviewer explicitly endorses the V22 controls and honesty ("honest almost to a fault") and the core empirical content; their asks are concentrated on *presentation*: the paper hands the reader four or five candidate headline numbers and does not pick one per claim, the front-matter under-weights the ICC=0.114 caveat, over-weights the Qwen 32B single-datapoint, advances a frontier-scale claim on a single n=99 pilot, and under-engages with the one regime where the pipeline genuinely beats the rule (Pacchiardi-style at ≥14B). V23 is therefore a **second tight cleanup pass, not a revision**: no new experiments, one new decision-tree paragraph in §1.1, two narrow demotions in the front-matter, six targeted main-text reframings, and four added limitations / future-work items. The paper remains **42 pages, 0 errors, 0 undefined refs**. Two experimental adds the reviewer tagged "would strengthen" (W8 non-English n=50 pilot; W9/Q1 human baseline n=50/2-annotator) are explicitly out-of-scope for V23 and are added to §5.8 future work.

**At-a-glance.**

| Ask | Reviewer request | V23 response | Location |
|---|---|---|---|
| W1 | Abstract: lead with rule 80.1% (extractor-independent); demote 74.3% Haiku pipeline | **Rewritten abstract lead** — rule first as label-free; pipeline 74.3% labeled as same-family upper bound; 64.7% as cross-family estimate. | `abstract.tex` |
| W2 / D1 | Decision tree "if claim X, cite Y" across the 4–5 candidate headlines | **New `\paragraph{Which number to report, by claim}` with a 5-row tabular in §1.1** (promoted from the buried parenthetical in V22 contribution (i)). | `introduction.tex` §1.1 |
| W3 | Frontier-scale Sonnet claim in contributions is unsupported at n=99 | **Demoted from contribution (iii)** to a standalone `\paragraph{Frontier observation (single pilot).}` labeling the n=99 pilot "a single measurement, not a tested frontier-scale claim." | `introduction.tex` §1.1 |
| W4 | Acknowledge single-persona-prompt limitation in main limitations list | **New §5.8 bullet (j)**: "5th-scenario persona condition tests a single persona prompt ('Dr. Alex Morgan'); wording-robustness untested." | `discussion.tex` §5.8 |
| W5 | Pacchiardi (§J) shows pipeline adds +14/+29 pp at scale; engage honestly in §4.5 | **New sentence in §4.5 "Regex matches or exceeds under equalization"** — explicit Pacchiardi-style exception at ≥14B (Llama 70B +14 pp, Qwen 14B +29 pp), with cross-pointer to Appendix J. | `experiments.tex` §4.5 |
| W6 / Q2 | Within-family Holm-Bonferroni feels post-hoc; strengthen | **New named `\paragraph{Multiple-testing correction: within-family vs.\ joint.}` in §4.6** with the unit-of-analysis argument (RLHF lineage) and the non-exchangeability demonstration (Qwen 32B RLHF collapse not replicated on Llama). | `experiments.tex` §4.6 |
| W7 | Demote Qwen 32B RLHF-collapse from front-matter primary claims | **Removed from §1 "How to read" level-independent list**; still retained in Table 1, §4.6, §4.8 footnote `$\ddagger$`. | `introduction.tex` §1 |
| W8 | Small non-English pilot (n=50 Spanish or Mandarin) would strengthen | **Out of scope for V23**; added as §5.8 future-work item (ii) under the reviewer-surfaced direction (5). | `discussion.tex` §5.8 |
| W9 / Q1 | Human baseline (n=50, 2 annotators) on equalized transcripts | **Out of scope for V23**; new §5.8 limitations bullet (k) plus future-work item (iii) under reviewer-surfaced direction (5). | `discussion.tex` §5.8 |
| D2 | §4.3 Table 2: k=1 fixed row first, LOO second | **Reordered §4.3** — `EXP-J-fixed` (k=1, label-free) is now the first paragraph (the label-free claim); `EXP-J` (LOO) second as calibration-comparison. | `experiments.tex` §4.3 |
| D3 | §4.4 EXP-G +26/+31 pp rows should flag KT confound visibly | **Verified** — abstract and §1.1 contribution (ii) already carry "upper bound conflating instruction-following with knowledge transfer"; Table 5 caption already carries "KT confound" Note column. No edit needed. | — |
| D4 | §4.6 Sonnet 92.9% — dual caveats (same-family + n=99) | **Covered by W3**: the contribution-list demotion also carries the dual caveats explicitly. | — |
| D5 | §4.7.2 Table 13 at n=30 invites overreading | **Bolded "Pilot, n=30 — descriptive, not confirmatory"** at the start of Table 13 caption; interpretation paragraph hardened to a bolded sentence: "We do not claim persona > sycophancy as a ranking at n=30; we claim only that the pre-registered one-sided prediction (sycophancy > persona) fails." | `experiments.tex` §4.7.2 |
| D6 | §4.8 "9–10 pp" framing ignores Llama 8B outlier | **Replaced** "systematic +9–10 pp" with "7 of 8 targets in +7 to +16 pp range (mean +9.4 pp); Llama 8B is the exception at +0.5 pp and is discussed separately." | `experiments.tex` §4.8 |
| D7 | §4.9 white-box "equalized regime is hard" over-claims from n=2 architectures | **Reframed** to "at the four pooling/layer configurations tested per target (two targets × four configurations), probe accuracy is within ±4 pp of the rule; we do not claim the equalized regime is hard for white-box methods in general." | `experiments.tex` §4.9 |
| D8 | Promote Appendix L truth-distribution numbers to main text | **Inlined** into §4.3 EXP-ADV-FULLREGEX interpretation: "lying 84%→48%→16% vs. truth 46%→8%→4% symmetric collapse; rule fails because lying collapse (68 pp) exceeds truth collapse (42 pp) — lexical-channel suppression, not semantic correction failure." | `experiments.tex` §4.3 |
| D9 | Verify cross-pointers (no stale labels, no "Table N.M" artifacts) | **Verified** — `main.aux` clean; `\newlabel{tab:exp_i_5th_scenario}{{13}...}` resolves; grep for "Table [0-9]\.[0-9]" returns nothing. | compile |
| Q3 | Qwen 14B persona 68% qualitative inspection | **Out of scope for V23**; added as §5.8 future-work item (iv) under reviewer-surfaced direction (5). | `discussion.tex` §5.8 |
| Q4 | Sonnet via Bedrock — reproducibility across providers | **Added one-line scope caveat** to §4.6 Sonnet pilot paragraph and to Appendix M: "single serving provider (AWS Bedrock); provider-replication (e.g., via Anthropic direct) is future work." | `experiments.tex` §4.6; `appendix.tex` §M |
| Q5 | ICC camera-ready fallback — flag in abstract | **Inline parenthetical in abstract**: "(ICC=0.114, n=20, 2 annotators; camera-ready is two-branch: full n≥100/3-annotator with Krippendorff's α, or fallback n≥50/2-annotator plus raw per-rater CSVs, §5.1)." | `abstract.tex` |

---

## Detailed responses

### W1 / Q5 — Abstract: lead with the extractor-independent rule; bind ICC to §5.1

**The reviewer's point.** V22's abstract led with the 30–41 pp equalization collapse and named 64.7% as the primary headline, but the first sentence still cited 74.3% (Haiku-same-family pipeline) as if it were a comparably robust anchor. The reviewer observed that (a) the one claim the paper can genuinely make label-free is rule 80.1% (k≥1, pooled-LOO, no calibration), and (b) the ICC=0.114 caveat is load-bearing for any pipeline-absolute claim and should be named at the abstract level, not just §5.1.

**V23 change.** Rewrote the abstract lead to put the rule first and label the two pipeline numbers by what they mean:

> *"A one-line regex (refusal count ≥ 1, fixed threshold, no calibration) achieves 80.1% average accuracy across seven prompt-equalized LLMs (689 trials; range 64–88%; 75–88% on models ≥7B), matching a 5-feature LLM pipeline's 74.3% same-family-extracted result within 5 pp and exceeding its 64.7% cross-family-extracted result by 15 pp."*

Added an inline parenthetical in the second paragraph binding the ICC caveat to §5.1's two-branch camera-ready commitment (Q5):

> *"ICC caveat on LLM-extracted features: 0.114 (n=20, 2 annotators; camera-ready is two-branch: full n≥100/3-annotator with Krippendorff's α, or fallback n≥50/2-annotator plus raw per-rater CSVs, §5.1)."*

Both changes are within the existing 2-paragraph abstract budget and preserve all magnitudes.

### W2 / D1 — Decision tree in §1.1: "which number to report, by claim"

**The reviewer's point.** The paper reports five candidate headlines (74.3% Haiku pipeline, 80.1% rule pooled-LOO, 71.8% rule per-target, 64.7% cross-family pipeline, 64.2% 8-target). Without explicit per-claim guidance, a reader cannot tell which to cite when, and the buried parenthetical in V22 contribution (i) was easy to miss.

**V23 change.** Promoted the recommendation to a standalone `\paragraph{Which number to report, by claim}` immediately after the §1.1 contributions list, as a compact 5-row tabular:

| If you are making this claim… | Cite… | Source |
|---|---|---|
| Label-free detection capability | rule 80.1% (k=1, pooled-LOO) | Table 2 |
| Rule accuracy under per-target calibration | rule 71.8% (7-target per-target LOO) | Table 9 |
| Pipeline same-family upper bound | 74.3% (Haiku extractor, 7 targets) | Table 9 |
| Pipeline cross-family estimate | 64.7% (Mistral L3; Llama 70B within 3 pp) | Table 9 |
| "With structural-zero" diagnostic | 64.2% (8-target, incl. Qwen 32B) | Table 9 |

The row ordering matches the reviewer's thesis: robustness-first, calibration-dependence second, extractor-sensitivity third, structural-zero diagnostic last.

### W3 / D4 — Demote Sonnet 4.5 frontier pilot from contributions list

**The reviewer's point.** V22 contribution (iii) advanced the Sonnet 4.5 pipeline (88.9–92.9%) as a headline on n=99, which the between-extractor CI analysis already flagged as 4–6× underpowered (n≈410 needed).

**V23 change.** Removed the Sonnet sentence from contribution (iii) and placed it into a standalone `\paragraph{Frontier observation (single pilot).}` between the contributions list and the "Scope" paragraph:

> *"A single equalized pilot on Claude Sonnet 4.5 (AWS Bedrock, n=99) reports refusal-count LOO 73.7% and pipeline 88.9–92.9% (Haiku / Llama 70B); 4–6× underpowered between-extractor (n≈410 needed; §4.6). A single measurement, not a tested frontier-scale claim."*

§4.6 and Appendix M retain the full pilot table and the single-provider caveat (Q4). The sentence no longer reads as a contribution, only as a "consistent-with" observation.

### W4 — Single-persona-prompt limitation, in main limitations list

**V23 change.** New §5.8 bullet (j):

> *"(j) The 5th-scenario persona condition (§4.7.2) tests a single persona prompt ('Dr. Alex Morgan, MIT physics educator', reused verbatim from run_persona_autonomous.py); wording-robustness (varying name, credentials, instructional framing) is untested."*

### W5 — §4.5 "Regex matches or exceeds" now engages with the Pacchiardi exception

**The reviewer's point.** V22 §4.5 stated the pipeline is redundant under equalization (regex matches on 6 of 7). Appendix J (Pacchiardi-style related vs. unrelated follow-ups) shows that at ≥14B scale the 5-feature pipeline gains +14 pp on Llama 70B (66%→80%) and +29 pp on Qwen 14B (52%→81%) when moving from unrelated to claim-related follow-ups. The paper did not engage with this exception in the main text.

**V23 change.** New sentence at the end of §4.5's "Regex matches or exceeds under equalization" paragraph:

> *"**Pacchiardi-style exception.** At ≥14B scale (Appendix J, Table 30), moving from unrelated to claim-related follow-ups lifts the 5-feature pipeline +14 pp on Llama 70B (66%→80%) and +29 pp on Qwen 14B (52%→81%); refusal-count is already saturated at the first response (±2 pp). The pipeline materially outperforms the rule only when multi-turn and topical relevance combine at ≥14B."*

This is the one regime we document where the pipeline genuinely adds value over the rule, and it is now stated in the main text with the magnitude and the scope.

### W6 / Q2 — Within-family Holm-Bonferroni, named paragraph in §4.6

**V23 change.** Replaced the V22 2-sentence justification with a named paragraph:

> *"**Multiple-testing correction: within-family vs. joint.** We apply within-family Holm-Bonferroni as the primary correction and report joint correction for transparency. Each RLHF lineage (Llama-family, Qwen-family) is a distinct unit of analysis: scale increments within a family vary parameter count while holding training objective, reward model, and safety tuning constant, but increments across families covary on multiple dimensions at once. The Qwen 32B RLHF agreeableness collapse (0 refusal markers under RLHF, §4.6) is not replicated on Llama at any scale, confirming the cross-family-exchangeability assumption that joint correction would require does not hold. Within-family: Qwen 3B→7B Fisher p=0.014 < α/3=0.017 and Llama 8B→70B p=0.004 < α/2=0.025 both survive. Joint (all 5 adjacent increments, α/5=0.01): only Llama 8B→70B survives. We do not claim joint-corrected Qwen effects; the strongest Qwen claim is within-family significance."*

The unit-of-analysis argument (RLHF lineage) and the non-exchangeability demonstration (Qwen 32B collapse absent on Llama) answer the reviewer's Q2 directly.

### W7 — Remove Qwen 32B RLHF-collapse from §1 level-independent list

**V23 change.** §1 "How to read this paper" previously listed "refusal-count LOO, three-control gaps, Qwen 32B zero-marker collapse" as level-independent claims. Qwen 32B is a single-model datapoint and belongs in diagnostics, not primary claims. We removed it from the list; the row is retained in Table 1, §4.6 scale sweep, and §4.8 Table `$\ddagger$` footnote as a "structural-zero" diagnostic.

### W8 / W9 / Q1 / Q3 — Reviewer-surfaced experimental directions (out of scope)

**The reviewer's asks.** Four experiment-level "would strengthen" requests: (i) provider-replication of the Sonnet pilot on a second API (Q4), (ii) non-English n=50 pilot (W8), (iii) human baseline n=50/2-annotator (W9/Q1), (iv) Qwen 14B persona 68% qualitative spot-check (Q3).

**V23 position.** All four are out of scope for V23 (a text-only cleanup pass). We added:

- **§5.8 limitations bullet (k)**: "No human baseline: the paper compares the 5-feature LLM pipeline against the regex rule but does not report how well human annotators classify the same equalized transcripts. An n=50/2-annotator human baseline would contextualize the 61–84% equalized band and is listed as future work."
- **§5.8 future-work item (5) "Reviewer-surfaced additional directions"** consolidating (i)–(iv): "Four additional directions surfaced in the NeurIPS 2026 reviews are future work, not V23 evidence: (i) provider-replication of the Sonnet 4.5 pilot on a second API (e.g., Anthropic direct) to rule out Bedrock-specific serving effects; (ii) a small n=50 non-English pilot (Spanish or Mandarin) with localized claim pairs and a language-appropriate refusal-lexeme inventory to test the English-only scope boundary empirically; (iii) an n=50/2-annotator human baseline on the equalized transcripts to contextualize the 61–84% pipeline band; (iv) a 10-trial qualitative read of the Qwen 14B persona cell (the only fully-autonomous persona/FB cell excluding chance at n=200, 68.0%) coded for persona-maintenance / direct-correction / other, to distinguish signal from persona-prompt leakage."

### D2 — §4.3 paragraph reorder (k=1 first, LOO second)

**V23 change.** Reordered §4.3 so the `EXP-J-fixed` paragraph (k=1, label-free, no calibration) is first and `EXP-J` (LOO, calibration-optimized) second. The first sentence of §4.3 now reads: "The central methodological finding is that a single regex feature (refusal/correction count, fixed threshold k≥1, no calibration) achieves 80.1% average accuracy across seven equalized models, matching the 5-feature pipeline on 6 of 7." Table 2 is unchanged; the text now matches the reviewer's preferred order of importance.

### D5 — §4.7.2 Table 13 and interpretation: bolded "descriptive, not confirmatory"

**V23 change.** Prepended to Table 13 caption: "**Pilot, n=30 per condition — descriptive, not confirmatory.**" Interpretation paragraph hardened to: "**We do not claim persona > sycophancy as a ranking at n=30; we claim only that the pre-registered one-sided prediction (sycophancy > persona) fails.**" Both are bolded to prevent the pilot being read as a confirmatory ranking.

### D6 — §4.8 "9–10 pp" softening

**V23 change.** Replaced "Haiku produces a systematic +9 to +10 pp uplift" with "Haiku is above the mean of the two non-Anthropic extractors on 7 of 8 targets, with per-target gap ranging +7 to +16 pp (mean +9.4 pp); Llama 8B is the exception at +0.5 pp and is discussed separately below." Abstract and §1.1 contribution (i) already used per-target ranges (not "consistent 9–10"); grep-verified.

### D7 — §4.9 white-box probes: reframe from "equalized regime is hard" to "rule-parity at tested configurations"

**V23 change.** Replaced "preliminary evidence that the equalized regime remains hard for simple white-box LR probes at this scale across the full depth of both networks" with "is a consistent pattern at the four pooling/layer configurations tested per target (two targets × four configurations); across these eight configurations probe accuracy is within ±4 pp of the refusal-count rule. We do not claim the equalized regime is hard for white-box methods in general — only that simple last-layer and mid-layer LR probes at this scale do not exceed the refusal-count rule in any tested configuration." Dropped the "consistent with representation-level difficulty" speculative tail. Azaria & Mitchell-style stronger probes remain flagged as future work.

### D8 — Inline Appendix L truth-distribution into §4.3

**V23 change.** The truth 46%→8%→4% vs. lying 84%→48%→16% symmetric-collapse pattern (previously only in Appendix L) is now inlined into §4.3's EXP-ADV-FULLREGEX interpretation: "On Llama 3B the lying-condition marker fraction collapses 84%→48%→16% across baseline / 14-word / full-regex disclosure, while truth drops symmetrically 46%→8%→4% (Appendix L). The rule fails because the lying-channel collapse is larger in absolute terms (68 pp vs. 42 pp), so surviving marker-bearing trials are no longer enriched in lies — lexical-channel suppression, not semantic correction failure." Appendix L retained as the home for the histogram.

### Q4 — Sonnet single-provider caveat

**V23 change.** One sentence appended to §4.6 Sonnet pilot paragraph: "The pilot runs on a single serving provider (AWS Bedrock); provider-replication (e.g., via Anthropic direct) is future work." Covered again by §5.8 future-work item (5)(i).

---

## V23 diff summary

| File | Change |
|---|---|
| `sections/abstract.tex` | Lead rewritten (W1): rule 80.1% first; 74.3%/64.7% labeled by regime; per-claim headline list; ICC inline parenthetical (Q5) binding to §5.1 two-branch commitment. |
| `sections/introduction.tex` | §1 "How to read" level-independent list: Qwen 32B removed (W7); §1.1 new `\paragraph{Which number to report, by claim}` with 5-row tabular (W2/D1); contribution (iii) Sonnet sentence demoted to new `\paragraph{Frontier observation (single pilot).}` (W3/D4). |
| `sections/experiments.tex` | §4.3 paragraphs reordered — k=1 fixed first (D2); §4.3 inline Appendix L truth-collapse numbers (D8); §4.5 new "Pacchiardi-style exception" sentence (W5); §4.6 new `\paragraph{Multiple-testing correction}` (W6/Q2); §4.6 Sonnet single-provider caveat (Q4); §4.7.2 Table 13 caption bolded "Pilot, n=30 — descriptive" + hardened interpretation (D5); §4.8 "9–10 pp" → "7 of 8 targets" + Llama 8B outlier (D6); §4.9 white-box reframe (D7). |
| `sections/discussion.tex` | §5.8 new limitations bullets (j) single-persona-prompt (W4) and (k) no human baseline (W9/Q1); §5.8 future-work item (5) "Reviewer-surfaced additional directions" consolidating (i)–(iv) (W8, Q3, Q4, W9). |
| `sections/appendix.tex` | Appendix L compressed (D8 numbers now inlined in §4.3); Appendix M Sonnet pilot prose tightened to reclaim page budget. |
| `REVIEWER_RESPONSE_LETTER_V23.md` | New file. |

**Page budget**: 42 (unchanged from V22); 0 LaTeX errors; 0 undefined refs; `\newlabel{tab:exp_i_5th_scenario}` still resolves to `{13}`.

---

## Explicitly out-of-scope for V23

- Running the non-English n=50 pilot (W8): requires localized claim pairs and a language-appropriate refusal-lexeme inventory. Now §5.8 future-work (5)(ii).
- Running the human baseline n=50/2-annotator study (W9/Q1): 1-week recruitment; now §5.8 limitations (k) + future-work (5)(iii).
- Running the Qwen 14B persona qualitative spot-check (Q3): now §5.8 future-work (5)(iv). Data file (`persona_autonomous_qwen2.5_14b_n200_final.json`) is released so downstream researchers can run this directly.
- Provider-replication of the Sonnet 4.5 pilot (Q4): Bedrock cost; now §5.8 future-work (5)(i).
- Scaling Sonnet 4.5 to n=410 for adequately-powered between-extractor comparison (Bedrock cost; §5.7(b)).
- The n≥100/3-annotator ICC validation itself (protocol frozen in V20; recruitment calendar triggered at camera-ready acceptance; two-branch fallback in §5.1).
- The 2×2 clarity × turn-structure factorial (pre-registrable; §5.8 future-work (4)).
- Closed-loop adaptive adversary (flagged since V16).
- Full Pacchiardi replication on Qwen 32B and frontier models.

We again thank the second reviewer for the precision of the asks and for the Weak Accept. V23 addresses every numbered item (W1–W9, D1–D9, Q1–Q5) without running new experiments or expanding the paper's scope.
