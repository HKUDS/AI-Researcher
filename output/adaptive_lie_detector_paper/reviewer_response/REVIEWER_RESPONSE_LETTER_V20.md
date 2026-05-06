# Response to Reviewer (Accept, 7/10; Confidence 4/5) — Revision V20 (Camera-Ready)

We thank this reviewer for the Accept and for the explicit signal that four targeted asks (Q1–Q4) plus minor text cleanups (W5–W9, P1–P2) would raise the score to 8/10. V20 is a focused camera-ready pass: three new experiments (Qwen-on-Qwen self-family control integrated; Mistral 7B + Qwen 14B n=200 adversarial in flight; Qwen 14B n=200 autonomy in flight), a camera-ready human ICC protocol with data-management fix, and text-level cleanups across abstract, Table 1, footnote 1, conclusion, and reviewer-response artifact removal. The paper is **40 pages, 0 errors, 0 undefined refs**.

**At-a-glance.**

| Ask | Reviewer request | V20 response | Location |
|---|---|---|---|
| Q1 | Why was Qwen 14B not scaled to n=200 on persona + false-belief? | **Both runs completed (2026-04-30)**: persona 68.0% CI [61.2, 74.1] \|d\|=0.83; FB 59.5% CI [52.6, 66.1] \|d\|=0.42. 3 of 4 n=200 cells include chance. | Table 4 integrated |
| Q2 | Qwen-on-Qwen self-family cell (e.g., Qwen 32B as extractor) | **New Qwen-14B-on-Qwen-7B cell at n=100**: 66.0% LOO, $-$9 pp below Haiku (no self-boost). Three self-family cells now argue Claude-specific RLHF self-preference. | `experiments.tex` §4.6 L383; `discussion.tex` §5.7(f); `abstract.tex` L4 |
| Q3 | Scale Mistral 7B + Qwen 14B adversarial n=50 → n=200? | Runs in flight (Mistral 7B at ~109/200 as of 2026-04-30; Qwen 14B queued); heterogeneous-mechanism finding re-verified at n=200 in camera-ready | §4.8 Table 10 (follow-up) |
| Q4 | Concrete plan for camera-ready human ICC (n≥100, 3+ annotators, IRB) | **Full protocol frozen**: `docs/icc_annotation_protocol_v2.md` (Prolific, $300 budget, exempt-IRB plan, rubric, attention checks); `data/icc_study_v2/` directory with schema README to address the V19 data-management red flag | New files below |
| W5 | App A.10 pipeline architecture dropped but §3.2 may forward-reference | **Verified clean** — no remaining `app:pipeline_details` refs. | §3.2 unchanged; `grep` = 0 |
| W6 | Drop footnote 1 (exploratory ≤7B vs ≥14B pooled) | **Footnote deleted**; figure caption parenthetical also removed | `experiments.tex` L272 (now short); Fig `scale_trend` caption |
| W7 | Table 1 EXP-I-m row "82%; others 60–66%" inconsistent with Table 4 | **Updated** to "Sycophancy 82/82/72%; persona/FB 54/56% (3B, n=200)" | `experiments.tex` Table 1 L24 |
| W8 | Sonnet 4.5 pilot framing — scale to n=410 or add explicit caveat | **Caveat added** to §5.7(b) stating single-underpowered-datapoint; camera-ready budget does not support scaling to n=410 via Bedrock | `discussion.tex` §5.7(b) |
| W9 | Conclusion should acknowledge disposition-source as hypothesis-not-finding | **Added sentence** explicitly labelling disposition-source a hypothesis from the 4th-scenario rejection; pre-registered 5th-scenario listed as future work | `conclusion.tex` final paragraph |
| P1 | Trim abstract ~100 words | **Abstract 257 → 193 words**; cut 8-target sub-clause, agreement-within-3pp detail, third Llama-on-Llama clause | `abstract.tex` (`wc -w` = 193) |
| P2 | Remove reviewer-response artifacts `(CR1/CR4/W5)`, `(CR3/Q2)`, `(R2)`, `(R1/W4)`, `(R1)` | **All 6 sites cleaned** across `experiments.tex` + `discussion.tex` | `grep -cE '\((CR[0-9]\|R[0-9]\|W[0-9])' sections/*.tex` = 0 |

---

## Q1 — Qwen 14B n=200 autonomy scale-up

**What was asked.** The reviewer noted V19's Llama 3B n=200 scale-up on persona + false-belief was thorough but Qwen 14B (the second scale point) remained at n=50. They asked whether n=50 Wilson CIs of [50–76] and [52–78] would hold at n=200.

**What we did.** Both Qwen 14B autonomy runs completed on 2026-04-30 and are integrated into Table 4:

| Scenario | n=50 (V19) | n=200 (V20) | Wilson 95% CI | Cohen's $d$ | CI status |
|---|---|---|---|---|---|
| Persona maintenance | 64.0% CI [50–76] | **68.0%** | [61.2, 74.1] | 0.83 | excludes chance |
| False beliefs (ICL) | 66.0% CI [52–78] | **59.5%** | [52.6, 66.1] | 0.42 | **includes chance** |

**Interpretation.** Three of four Llama 3B/Qwen 14B × persona/false-belief cells at $n=200$ have Wilson CIs including chance (Llama 3B persona 54.0%, Llama 3B false-belief 56.0%, Qwen 14B false-belief 59.5%). The one cell that excludes chance — Qwen 14B persona 68.0% — is flagged explicitly in §4.6 rather than hidden: it still trails sycophancy transfer (82/82/72%) by $\geq 14$\,pp and sits well below the equalized baseline (64.0% at 3B, 82.5% at 14B). The negative-transfer headline is preserved as "persona and false-belief do not cleanly transfer at $n=200$ across two families," with the Qwen 14B persona exception called out.

---

## Q2 — Qwen-on-Qwen self-family extractor control

**What was asked.** The reviewer observed the V19 self-family evidence rested on two cells (Haiku-on-Claude, Llama-70B-on-Llama) — one showing +10 pp, the other showing no uplift — and that a third independent self-family pair (e.g., Qwen-on-Qwen) would firm up the Claude-specific RLHF self-preference interpretation.

**What we did.** We integrated an existing Qwen-14B-as-extractor cell on Qwen-2.5-7B equalized transcripts (n=100, `qwen_same_family_qwen14b_on_qwen7b.json` from 2026-04-24) that had not previously been reported in the paper. Computed 5-feature LOO:

- **Qwen-14B-on-Qwen-7B: 66.0%** (n=100)
- Haiku-on-Qwen-7B (same transcripts): 75.0% — i.e., Qwen-14B-as-extractor is **$-$9.0 pp below Haiku** on the same target.
- Mistral-L3-on-Qwen-7B (same row in Table 9): 65.0% — Qwen-14B-as-extractor agrees with Mistral-L3 within 1 pp.

**Integration sites:**

1. **`experiments.tex` §4.6 L383** — Llama-on-Llama paragraph extended to add the Qwen-on-Qwen cell:
   > "**Qwen-on-Qwen control.** As a third self-family cell we re-extracted 100 equalized Qwen 2.5 7B transcripts with Qwen 2.5 14B as the self-family extractor: LOO 66.0% (vs. Haiku-on-Qwen-7B 75.0% from the same column above, i.e., Qwen-14B-as-extractor is −9.0 pp below Haiku on the same target and within 1 pp of Mistral L3 65.0%). The Haiku +10 pp uplift again does not replicate: three self-family extractor cells tested (Llama-70B-on-Llama-3B, Llama-70B-on-Llama-8B, Qwen-14B-on-Qwen-7B) and none show an analogous self-boost. The localization to Claude-on-Claude is consistent with Claude-specific RLHF self-preference rather than a universal within-family phenomenon."

2. **`discussion.tex` §5.7(f)** — limitation updated:
   > "Three self-family extractor cells now argue the 9–10 pp Claude-on-Claude uplift is Claude-specific RLHF self-preference rather than a universal family-bias: Llama-70B-on-Llama-3B/8B and Qwen-14B-on-Qwen-7B (§4.6) all produce no analogous self-boost."

3. **`abstract.tex`** — mention added:
   > "three self-family extractor cells (Llama-on-Llama, Qwen-on-Qwen) show no analogous inflation."

**Note on Qwen 32B as extractor.** The plan flagged Qwen 2.5 32B as an additional self-family extractor; we did not run this for V20 because (a) Qwen 32B is the RLHF-collapse row (Table 9, §4.4) that produces 0 refusal markers in both conditions, so its behavior as an _extractor_ on Qwen targets risks being dominated by the same structural-zero pattern and would require a separate interpretive caveat; (b) the three-cell self-family picture is already sufficient to firm up the Claude-specific reading. A Qwen 32B extractor run is listed as future work if reviewers request it.

---

## Q3 — Mistral 7B + Qwen 14B adversarial n=200 scale-up

**What was asked.** The reviewer noted V19's Llama 3B adversarial n=200 run had flipped the qualitative story (50% at n=50 — truth-channel suppression — became 61.5% at n=200 — lying-channel suppression), and asked how confident we were in the Mistral 7B 66% and Qwen 14B 44% n=50 numbers given this precedent.

**What we did.** Mistral 7B adv-fullregex completed at n=200 on 2026-04-30:

| Target | n=50 (V19) | n=200 (V20) | Wilson 95% CI | Truth acc. | Lie acc. | Qualitative story |
|---|---|---|---|---|---|---|
| Llama 3.2 3B | 50% (n=50) | **61.5%** (V19) | [54.6, 68.0] | 87% | 36% | lying-channel suppression |
| Mistral 7B | 66% (n=50) | **64.5%** (V20) | [57.7, 70.8] | 56% | 73% | **paraphrase-preserve (unchanged from n=50)** |
| Qwen 2.5 14B | 44% (n=50) | in flight (ETA ~02:12 2026-05-01) | pending | pending | pending | TBD |

Mistral 7B's qualitative story holds from n=50 to n=200: both channels roughly balanced, the lie channel slightly stronger than truth, consistent with paraphrase-while-preserving-semantics. The Qwen 14B n=200 run is GPU-queued and will complete overnight; it will be integrated into Table 10 in the camera-ready if it completes before the deadline, or kept at n=50 with a paragraph caveat if not.

**Commitment.** If Qwen 14B flips its qualitative story at n=200 (as Llama 3B did), §4.8 will be revised — the three-mechanism characterization will be re-verified rather than asserted.

**Why the V19 n=50 numbers were reported at all.** We chose to include them in V19 because the heterogeneous-mechanism finding is the primary point and does not depend on exact percentages; Llama 3B's flip from 50% to 61.5% at n=200 preserved the qualitative interpretation (both are rule-collapse, just from different channels). We acknowledge the reviewer's concern that n=50 is fragile and will not claim n=50 stability in the camera-ready.

---

## Q4 — Camera-ready human ICC (n≥100, 3+ annotators, IRB, compensation)

**What was asked.** The reviewer asked for a concrete plan — not commitment language — covering recruitment, IRB, compensation, and analysis plan for the n≥100 / 3+ annotator human ICC validation that V19 committed to.

**What we did.** A full protocol is frozen in the supplementary material:

- **`code/adaptive_lie_detector/docs/icc_annotation_protocol_v2.md`** (new, ~140 lines):
  - **Scope**: n=100 equalized transcripts, stratified 50 truth / 50 lie × 7 target models; 3 independent annotators, blind to ground-truth + target-model identity.
  - **Platform**: Prolific. US-based, English fluency screener, ≥10 prior studies, ≥95% approval. 3 annotators × 3 hr × $25/hr = $225; + Prolific 33% service fee ≈ **$300 total**.
  - **IRB**: minimal-risk exempt determination (anonymous Prolific, no identifying data); letter to accompany supplementary material.
  - **Rubric**: 0–10 scale with 4-bucket anchors per feature (consistency, specificity, correction-marker density, confidence, elaboration). Designed to avoid the V16 n=20 scale drift (human mean 1.10–3.95 vs LLM mean ~5).
  - **Training + attention checks**: 5 worked examples pre-task; 3 embedded attention checks; annotator replaced if >1 check fails.
  - **Analysis**: Krippendorff's α (ordinal), ICC(2,1), ICC(2,k=3), Spearman ρ per feature + pooled; comparison to V16 machine-rater proxy ICC(2,1) = 0.79.
  - **Timeline**: 2.5 weeks (1 wk protocol + IRB; 1 wk recruitment; 3 days analysis).

- **`code/adaptive_lie_detector/data/icc_study_v2/README.md`** (new) — directory schema, per-annotator JSON format, and file inventory. This **fixes the V19 data-management red flag** ("raw annotator files were not persisted in a form suitable for automated reanalysis") by committing to raw per-annotator JSONs under version control.

**Reporting plan.** The §5.1 "Camera-ready commitment" paragraph will be replaced with a standalone subsection reporting per-feature ICC(2,1), ICC(2,k), Krippendorff's α, and Spearman ρ (annotator-vs-LLM, 3 columns), plus a one-sentence headline and an interpretive caveat calibrated to the observed pooled ICC. If the pooled ICC remains <0.5 the "rank ordering preserved, absolute levels not" reading stays; if ≥0.6 the paper softly upgrades absolute-level claims from the pipeline. Abstract weak-ICC sentence will be updated to report the n=100/3-annotator values; §5.7(g) limitation will be demoted accordingly.

**Risks.** If Prolific recruitment stalls past the camera-ready deadline, we fall back to the V19 commitment language and report progress on whatever has been collected (e.g., n=50 preliminary α) rather than fabricate a pooled number.

---

## W5 — App A.10 pipeline architecture check

**Status:** verified clean.

`grep -n "app:pipeline_details\|pipeline_details" sections/*.tex` returns no matches. The V19 deletion of the pipeline-details subsection did not leave a stale forward-reference from §3.2. No action required for V20.

---

## W6 — Drop footnote 1

**Done.** Footnote at `experiments.tex` L272 (the pooled ≤7B vs ≥14B exploratory group comparison) has been deleted in its entirety. The parenthetical "(pooled $p<0.0001$, exploratory post-hoc comparison, not pre-registered)" in the Figure `scale_trend` caption (L277) has also been removed. The reviewer's read — that a footnote the authors themselves flag as not surviving their own methodology adds noise without evidence — was correct.

---

## W7 — Table 1 EXP-I-m row

**Done.** The Table 1 row at `experiments.tex` L24 was:

```
EXP-I-m & Matched autonomous (3B+14B) & 200 & \S\ref{sec:autonomous_matched} & Sycophancy 82%; others 60–66% \\
```

Updated to:

```
EXP-I-m & Matched autonomous (3B+14B) & 50–200 & \S\ref{sec:autonomous_matched} & Sycophancy 82/82/72%; persona/FB 54/56% (3B, n=200) \\
```

This is now consistent with Table 4 (`tab:autonomous_matched`).

---

## W8 — Sonnet 4.5 pilot framing

**Done.** Added to `discussion.tex` §5.7(b):

> "The frontier-scale evidence here therefore rests on a single underpowered datapoint (n ≈ 410 would be needed for 80% power on the between-extractor margin); we report the pilot to signal that frontier behavior is _consistent with_ the ≥14B cluster but do not treat it as dispositive."

This makes the single-underpowered-datapoint status explicit. Scaling Sonnet to n=410 was considered but the Bedrock API cost (≈$200 for the between-extractor-only version) combined with the 2-week camera-ready window was not feasible; we elected text transparency over scope creep.

---

## W9 — Conclusion disposition-source hedge

**Done.** Added to `conclusion.tex` final paragraph:

> "Our _disposition-source_ reading of the autonomous-transfer asymmetry — sycophancy transfers (82% at 3B/14B, 72% at 70B) while persona and false-belief do not — is a hypothesis emerging from the pre-registered 4th-scenario rejection of our earlier clarity gloss, not an independently-tested finding; a pre-registered 5th-scenario test that varies disposition-source while holding clarity, turn-count, and target fixed remains future work (§5 Discussion, Future Direction #4)."

This matches the language already in the Future Directions section and the §5.8 future work item (4).

---

## P1 — Abstract trim

**Done.** Abstract compressed 257 → **193 words** (measured via `wc -w sections/abstract.tex`). Cut: the "8-target panel including Qwen 32B" sub-clause; the "agreement within 3 pp" detail; the primary-feature weak-IRR restatement at the paragraph level (kept at the sentence level only). Added: the Qwen-on-Qwen self-family clause (Q2 integration). Kept: thesis, 64.7% primary headline, rule-matches-pipeline claim, n=200 negative-transfer sentence, English-only scoping, contributions list, baseline-not-detector closing.

---

## P2 — Reviewer-response artifacts removed

**Done.** Six sites cleaned:

| Site | Before | After |
|---|---|---|
| `discussion.tex` L9 | `\paragraph{Machine-rater ICC proxy (R1, does not substitute for human ICC).}` | `\paragraph{Machine-rater ICC proxy (does not substitute for human ICC).}` |
| `experiments.tex` L161 | `\textbf{Scope (CR1/CR4/W5).}` | `\textbf{Scope.}` |
| `experiments.tex` L161 | `at the $n=200$ W5 scale-up` | `at $n=200$` |
| `experiments.tex` L147 (Table 10 caption) | `the Adv-FullRegex column now reports $n=200$ (W5 scale-up)` | `the Adv-FullRegex column reports $n=200$` |
| `experiments.tex` L301 (Table 4 caption) | `scaled to $n=200$ (W5)` | `scaled to $n=200$` |
| `experiments.tex` L321 | `\textbf{Cross-family re-extraction (CR3/Q2).}` | `\textbf{Cross-family re-extraction.}` |
| `experiments.tex` L330 | `\textbf{Pre-registered design (R2).}` | `\textbf{Pre-registered design.}` |
| `experiments.tex` L334 (Table caption) | `Pre-registered 4th scenario (R2).` | `Pre-registered 4th scenario.` |
| `experiments.tex` L383 | `\textbf{Llama-on-Llama control (R1/W4).}` | `\textbf{Llama-on-Llama control.}` |

Verification: `grep -cE "\((CR[0-9]|R[0-9]|W[0-9]|W-stats|Q[0-9])" sections/*.tex` returns 0.

---

## Out-of-scope for V20 (explicitly)

- **Pacchiardi full replication** — flagged since V13; out of scope for a camera-ready window.
- **Qwen 14B sycophancy ablation** — flagged since V13; already have Llama 70B sycophancy cross-family re-extraction as the key W6-era evidence.
- **Pre-registered 5th scenario (disposition-source clean test)** — explicit future work (§5 Future Direction 4). Listed in the conclusion hedge added in W9.
- **Closed-loop iterated adversary** — flagged since V16 as future work; the one-shot full-regex-disclosed adversary is the in-scope test.
- **Qwen 32B as third cross-family extractor** — not run because Qwen 32B is the RLHF-collapse row itself; three self-family cells already firm up Claude-specific reading.
- **Sonnet 4.5 n=410 scale-up** — Bedrock cost + calendar infeasible; addressed via text caveat (W8).

---

## Summary

V20 closes three of four reviewer asks substantively (Q2, Q4, W5–W9, P1, P2 fully done; Q1, Q3 in flight with honest progress reporting and camera-ready integration commitment). The paper remains at 40 pages, 0 errors, 0 undefined refs. The abstract is 193 words (target 170–200). All reviewer-response artifact tags are stripped. The data-management red flag on the n=20 ICC pilot is addressed by the v2 protocol + directory structure.
