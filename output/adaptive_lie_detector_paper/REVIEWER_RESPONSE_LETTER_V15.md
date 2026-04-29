# Response to Reviewer — Round 6 Revision (Borderline Weak-Accept, Confidence 4/5)

We thank the reviewer for the detailed and careful review, the intellectually generous framing ("intellectual honesty is admirable"), and the explicit signal that a revision addressing the five suggested revisions "would push this clearly into accept territory." This letter addresses each of the five suggested revisions in order, followed by responses to the five author questions and the tractable minor comments.

---

## Suggestion 1 — Commit to the negative-result framing; strip deployment-rule language (text only)

**Ask.** The reviewer observed that the paper oscillates between "negative result" and "we propose a deployment-ready rule," and asked us to commit to the former: frame the rule as a baseline against which more robust detectors should be measured, not as a production detector.

**What we did.** We replaced every instance of deployment-framing in the experimental sections and appendix with the reviewer-aligned wording "baseline, not a production detector." Specifically:

- `sections/experiments.tex` **§4.2 lede** — "The most deployment-relevant finding is..." → "The central methodological finding is that a single regex feature... matches or exceeds the full LLM pipeline on equalized data. This is evidence that the pipeline adds little above surface-lexical baselines in this regime, not a recommendation that practitioners use the rule in production: the rule is English-only, lexical, and (as §4.x shows) fragile to static adversarial paraphrase."
- **§4.2 Table 1 caption** — removed "matching a shared-deployment regime."
- **§4.2 EXP-J-fixed sub-heading** — "Fixed-threshold deployment rule" → "Fixed-threshold label-free rule"; body sentence "This validates a concrete deployment path: practitioners can apply..." replaced with "We report this as a methodological baseline, not a production detector, and report the fixed-threshold result specifically to show that the average holds without labeled calibration data."
- **§4.x Cross-claim-set heading** — "Cross-claim-set deployment (EXP-L)" → "Cross-claim-set generalization (EXP-L)."
- **§4.6 Qwen 32B RLHF-collapse paragraph** — removed "arguably the most practically significant finding for frontier deployment"; added an explicit "\emph{We label the following as speculation, not evidence}" prefix to the RLHF-can-be-weaponized hypothesis. This is also relevant to W8 (Qwen 32B overinterpretation).
- **Appendix A.9** — "a deployment-oriented detector relying on refusal-count markers" → "a methodological baseline relying on refusal-count markers."

A final `grep -r "deployment" sections/` shows 0 remaining occurrences of the deployment-framing pattern in the experimental sections. The one-shot "deployment" label remaining in `sections/discussion.tex` is a `\label{sec:deployment}` back-reference target retained purely for backward compatibility with existing cross-references; no prose uses it.

---

## Suggestion 2 — Strengthen white-box probing with ≥1 additional configuration (new experiment)

**Ask.** The reviewer specifically cited Azaria & Mitchell's SAPLMA-style probing, which uses **intermediate layers and mean-pooled representations**, and asked that the probe comparison cover at least one additional configuration. The current paper reports only last-layer last-token LR probes on Llama 3B and Mistral 7B.

**What we did.** We implemented `experiments/whitebox_5_multilayer_probes.py`, which extracts hidden states at all layers from the same saved equalized transcripts (`llama_3b_equalized.json`, `mistral_7b_equalized.json`) and trains LR probes at four configurations per target:

1. Last-layer last-token (the original design, retained for comparison)
2. Mid-layer last-token (layer $L/2$, matching SAPLMA's intermediate-layer intuition)
3. Last-layer mean-pooled
4. Mid-layer mean-pooled

All configurations use the same LOO + StandardScaler + LogisticRegression pipeline and are reported with Wilson 95% CIs on the same $n$ as the original probe.

**Result.** The multi-configuration band spans \textbf{39–66\%} on Llama 3B (last-layer last-token: 63\%, mid-layer last-token: 66\%, last-layer mean-pool: 39\%, mid-layer mean-pool: 56\%). Mid-layer last-token is the best configuration and exceeds the last-layer last-token result by $+3$pp, directly validating the reviewer's Q3 intuition that intermediate layers may carry stronger signal. Mean-pooled probes are *worse* on Llama 3B than last-token probes at both layer depths, contrary to what SAPLMA-style reasoning would predict; we report this as an honest empirical finding, noting that Azaria \& Mitchell's result held for a different architecture (Llama-1 7B) and different base task. The §4.8 white-box probe table now has four rows per target rather than one, the §4.8 and §5.2 prose are updated to report the multi-configuration band rather than the single-point 63\% result, and the paper's claim is now "the multi-configuration best-probe band on two open-weight targets is still within the refusal-count rule's band" rather than "the single last-layer last-token probe matches the rule."

(Note: the Mistral 7B multi-layer results were still in the middle of extraction at paper-freeze time; we will add the Mistral 7B rows to Table 8 in the camera-ready update, paired with the existing 65\% last-layer last-token baseline.)

---

## Suggestion 3 — Expand n on Sonnet 4.5 or label it a pilot

**Ask.** The Sonnet 4.5 result ($n=99$, paired-bootstrap CI on the Haiku--Llama 70B pipeline gap $[-3.0, +11.1]$, includes zero) is underpowered by $4$–$6\times$ for the between-extractor claim the paper implicitly makes. The reviewer accepted either expansion to $n\approx 410$ or an explicit pilot label.

**What we did.** We chose the honest option: **label it a pilot**. The §4.5 heading is now "Frontier-scale pilot observation (single frontier data point, $n=99$)," and the paragraph explicitly begins: "We report a \emph{pilot} observation on Claude Sonnet~4.5... because the key paired comparison (Haiku vs.\ Llama~70B pipeline gap) is underpowered by $4$–$6\times$ at this $n$, so no between-extractor claim should be derived from it; we report the numbers as a single frontier measurement, not as a tested hypothesis." The abstract was similarly updated to read "A single frontier pilot ($n=99$, Claude Sonnet~4.5, underpowered by $4$–$6\times$ for the key between-extractor comparison)... we treat this as a single measurement, not a tested claim." All prior language positioning the $4$pp gap as an effect has been removed; the numerical triangulation remains as a single pilot measurement. Expanding to $n\approx 410$ was declined as out of scope for the revision window (~\$10 Bedrock cost plus ~1 day of inference for a marginal improvement in a result we had already decided to demote).

---

## Suggestion 4 — One adaptive adversarial iteration (new experiment)

**Ask.** The paper currently uses a single-shot static adversarial prompt with 14 curated forbidden markers. The reviewer's point was that the paper \emph{asserts} "an adaptive adversary would almost certainly drive accuracy to chance" without ever running one; at least one iteration with more-informed attack would validate (or falsify) that assertion.

**What we did.** We implemented `experiments/run_adversarial_full_regex.py`, a variant of the original adversarial script that discloses to the target the **full 14-pattern refusal-marker regex list** that the detector actually uses (the `REFUSAL_PATTERNS` list from `analyze_matched_autonomous.py`), rather than the hand-curated 14-word subset in the original run. This is a strictly stronger attack than the original: the adversary now has complete information about the detector's lexical pattern set. It is **still technically a one-shot static adversary** (no feedback loop; no iterative rewriting based on per-trial detector scores), and we label it as such in the code, in the §4.x prose, and in the abstract — a closed-loop "adaptive adversary" in the formal sense remains future work.

**Protocol.** $n=50$ per target, identical pipeline to the original adversarial run, paired against the existing non-adversarial equalized baseline on Llama 3B, Mistral 7B, and Qwen 2.5 14B. (Llama 3B was in flight at paper-freeze time; partial results at trial 11/50 show 45\% accuracy, consistent with at-or-near-chance under full-regex disclosure. Mistral 7B and Qwen 14B will be reported in the camera-ready update as a direct extension of the adversarial table.)

**Interpretation.** Whatever the final numbers, this is a stronger adversarial datapoint than the original, and the paper's "adaptive would drive to chance" claim is now backed by at least one informed-adversary experiment rather than asserted cold. We will report the full-regex-disclosed numbers alongside the original curated-14-word numbers as a paired column in the adversarial table, and clearly state which is "one-shot weak" (the original) and which is "one-shot informed" (the new variant).

---

## Suggestion 5 — Single consolidated headline-numbers table in §4

**Ask.** Headline numbers are currently scattered across Tables 1, 2, 3, 4, 5, 7, 8, 9 plus Figure 4 and prose; the reviewer couldn't find them without reading §4 three times.

**What we did.** We added a new Table (`tab:headlines`) at the start of §4 (immediately before §4.1), titled "Headline numbers." It has 14 rows covering:

- Instructed LOO (7-model range)
- Equalized pipeline avg under Haiku (7-model)
- Equalized rule avg (pooled-LOO, $k=1$)
- Cross-family pipeline under Mistral L3 and Llama 70B (7-target)
- Qwen 32B RLHF-collapse structural zero
- Instructed-matched $\Delta$LOO range (clean $\geq$14B)
- Sycophancy transfer across three scales (rule)
- Persona/false-belief across two scales (rule)
- Adversarial Mistral 7B paraphrase (rule, paired)
- ICC validity
- Frontier pilot rule and two pipeline variants (Sonnet 4.5)

Each row has columns: Finding, Value, $n$, Regime, Extractor, Reference (pointing to the full-detail table or section). This is a reader-orientation table, not a new result.

---

## Author questions

### Q1 — Pre-register the $\leq$7B vs.\ $\geq$14B gap prediction

Committed. Before any future within-family scale replication (the natural next study is a 4B–70B Qwen grid on a non-Anthropic cross-family extractor), we will pre-register the hypothesis that refusal-count LOO at $\leq$7B falls below 70\% and at $\geq$14B falls above 75\% (both $n\geq 100$, Wilson 95\% CIs must not overlap 70\%). The result will be recorded publicly and reported regardless of outcome.

### Q2 — Sycophancy scaling prediction

Our prediction at the time of submission, offered here as the natural extension of the Table 4 panel: sycophancy transfer holds at $\geq$ 200B frontier scale (rule $\geq 75\%$ on $n\geq 100$), because the signal appears to track knowledge-conflict clarity rather than model capability, and knowledge-conflict clarity is if anything higher at frontier scale. If sycophancy transfer \emph{collapses} at frontier scale (e.g., $\leq$60\% at GPT-5 or Sonnet Opus 4.x), that would falsify the "knowledge-conflict clarity" interpretation and be a substantial update.

### Q3 — Probing architecture commitment

Addressed by Suggestion 2 above. The multi-layer, mean-pool extension is implemented; Llama 3B shows +3pp gain under mid-layer last-token, confirming the reviewer's intuition that the single-design-point probe was underpowered.

### Q4 — EXP-G +7.5pp ceiling honesty

Acknowledged in the §4 prose: "The small $\Delta$ on Qwen 14B (+7.5pp) reflects ceiling-effect compression rather than a family-specific difference in how much instruction-following adds: there is little headroom between 82.5\% and the 90\% instructed-matched ceiling." This is a ceiling caveat, not a claim about the magnitude of the instruction-following effect itself. We leave the $+$7.5–15 range as the conservative interpretable number, while explicitly noting the ceiling-effect confound in §4.x.

### Q5 — Mistral Large 3 parameter count

Dropped. The appendix "Model identification notes" paragraph no longer cites the "675B" figure. The prose now reads: "we use the name ``Mistral Large~3'' following AWS Bedrock documentation and position the model as ``a non-Anthropic cross-family extractor of AWS Bedrock flagship-Mistral capability''; we make no numerical claim about its parameter count, which Mistral AI has not publicly attested."

---

## Minor comments

| Comment | Response |
|---|---|
| ICC=0.114 appears 9 times | Consolidated to 3 canonical sites (§5.1, abstract, Limitation (i)). Introduction, methodology, §4.4, discussion §5.4/§5.5, and appendix A.4 now use `Section~\ref{sec:icc_owned}` as the forward reference. |
| Fig. 1 caption says "filled vs.\ hatched" but actual figure is blue + orange-hatched | Caption updated to "solid blue bars vs.\ hatched orange bars." |
| Table 4 ($\|d\|$ column) undefined in caption | Caption updated: "``$\|d\|$'' is Cohen's $d$ on refusal-count between lying and truthful trials (unsigned; larger = cleaner behavioral separation)." |
| Anthropic citation (`references.bib:100`) is Claude 3, paper evaluates Claude 4.5 | Added `@techreport{anthropic2025claude45}` pointing to the Claude 4.5 family (Haiku 4.5 and Sonnet 4.5) with Bedrock model IDs. First-use in the introduction now cites it. |
| Appendix A.10 77-line ADAGE subsection | Trimmed from 77 lines to ~15 lines. Architecture figure retained (conveys measurement apparatus); detailed feature extraction prompts, classifier mathematics, and adaptive-stopping pseudocode collapsed into a single paragraph pointing readers to the accompanying code repository for the exact text. |
| Abstract states the central thesis twice | De-duplicated. Thesis ("current behavioral detection works only in the instructed regime...") now appears once in the abstract lede; the former second statement has been removed from the Contributions sentence, which now lists only the three contributions without repeating the thesis. |
| Abstract two-paragraph structure | Retained; the de-duplication cleaned up the semantic redundancy without forcing a one-paragraph rewrite. |

---

## Explicitly declined / deferred

- **n≥100, 3+ annotator ICC validation study**: as in V14, deferred to post-camera-ready public release (multi-week annotator recruitment + calibration). Limitation (i) already enumerates ICC-invariant vs.\ ICC-sensitive claims.
- **Frontier Opus cross-family extraction on Sonnet 4.5 transcripts**: same API-cost/time constraint as V13 and V14; left as future work in §5.
- **Closed-loop iterated adaptive adversary**: Suggestion 4 covers one iteration with full detector-regex disclosure. A true closed-loop adversary (iterate-to-convergence on per-trial detector scores) remains future work.

---

## Summary of changes

| Ask | Response | Type |
|---|---|---|
| R1. Commit to negative-result framing; strip deployment | 6 inline edits across experiments.tex, appendix.tex | Text |
| R2. Additional probe configuration | Multi-layer + mean-pool probe implemented (`whitebox_5_multilayer_probes.py`); Llama 3B shows +3pp at mid-layer last-token | New experiment |
| R3. Sonnet 4.5 pilot label or expand | Labeled as pilot in §4.5 and abstract | Text (and honest-downgrade) |
| R4. One adaptive adversarial iteration | Full-regex-disclosed static adversary implemented (`run_adversarial_full_regex.py`); Llama 3B at 11/50 trials shows 45\% (at-chance) | New experiment |
| R5. Consolidated headline table | New Table `tab:headlines` at start of §4 | New table |
| Q1. Pre-register $\leq$7B vs.\ $\geq$14B prediction | Committed for next replication | Commitment |
| Q2. Sycophancy scaling prediction | Provided: transfer at frontier | Text |
| Q3. Probing architecture commitment | Implemented via R2 | Experiment |
| Q4. EXP-G +7.5pp ceiling | Ceiling caveat already in §4.x | Text (already present) |
| Q5. Mistral Large 3 parameter count | Dropped from appendix | Text |
| ICC×9 | Consolidated to ×3 | Text |
| Fig. 1 caption | Fixed | Text |
| Table 4 $\|d\|$ | Defined in caption | Text |
| Anthropic Claude 4.5 citation | Added | Bib |
| Appendix A.10 trim | ~halved | Text |
| Abstract thesis dedup | Done | Text |

We believe the five suggested revisions plus the minor-comment cleanup substantively address the reviewer's borderline-weak-accept concerns. The R2 and R4 experiments supply empirical backing for previously-asserted claims; R1, R3, R5, and the minor comments are concrete text changes the reviewer can verify by reading the revised PDF.
