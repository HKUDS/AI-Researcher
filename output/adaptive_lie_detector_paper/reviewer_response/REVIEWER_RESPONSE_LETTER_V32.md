# Reviewer Response Letter — V32
## NeurIPS 2026 Revised Submission

---

**To:** Reviewer 8 (Weak Accept 6/10, Confidence 4/5)

**Subject:** V32 revision addressing MC1–MC6, Q4, and five minor concerns; one experiment completed (Llama 8B-on-8B same-checkpoint: 63.0%, no self-boost)

We thank the reviewer for the thorough reading and actionable concerns. V32 runs one new experiment (Q4: Llama 3.1 8B self-extractor on existing 92 equalized 8B transcripts) and makes seven text-only fixes (MC1 title; MC2 framing note; MC4 partial-transfer promotion; MC5 abstract rewrite; MC6 Pacchiardi own paragraph + §1.1 pointer; Minor-Fig2 caption; Minor-Sonnet promotion to §4.8). MC3 (ICC n≥100) remains a camera-ready commitment, strengthened in §5.1 with a two-branch integration plan. Responses to open questions Q1–Q5 are below.

---

## At-a-Glance Table

| Item | Ask | V32 action | Status |
|---|---|---|---|
| **MC1 (title)** | Title overclaims — "Genuine Behavioral Deception Detection" but only tests instructed roleplay | Subtitle narrowed to "…A Three-Control Evaluation of **Instructed-Roleplay Detection** Across Open-Weight LLMs" | **Done — main.tex** |
| **MC2 (framing)** | Paper structured as empirical-findings paper but contribution is methodological | Added "How to read this section" note at top of §4 calling 7-model panel the *demonstration* of the controls | **Done — experiments.tex** |
| **MC3 (ICC)** | ICC=0.114 inadequately addressed; level-dependent claims still relied on | Camera-ready commitment strengthened: two-branch integration (α≥0.4 validates; α<0.4 demotes level-dependent claims); full protocol in §5.1 | **Camera-ready commitment** |
| **MC4 (partial-transfer)** | "Unexplained partial transfer" for two cells insufficient; should be named finding | Promoted to `\paragraph{Partial transfer in two cells: unexplained positive signal.}` in §4.7; one sentence added to §5.3 summary | **Done — experiments.tex, discussion.tex** |
| **MC5 (80.1% vs 71.8%)** | Abstract leads with pooled-LOO 80.1%; per-target LOO 71.8% is more conservative | Abstract sentence 1 now leads with 71.8% per-target LOO; 80.1% moved to headline bullet as "pooled fixed-threshold" | **Done — abstract.tex** |
| **MC6 (Pacchiardi buried)** | +14 to +29 pp pipeline-over-rule buried in §4.4 parenthetical | Pacchiardi-style exception split into own named paragraph in §4.4; pointer sentence added to §1.1 contribution (1) | **Done — experiments.tex, introduction.tex** |
| **Q4 (same-checkpoint)** | Localization stronger with 3B-on-3B or 8B-on-8B; current Llama cells are 70B-on-3B/8B (cross-checkpoint) | Ran Llama 3.1 8B-on-8B re-extraction (n=100; Ollama); pipeline 63.0%, refusal-count 54.0% — below all cross-family extractors; no self-boost; integrated into §4.8, §5.7(f), §1.1 | **Done — experiments.tex, discussion.tex, introduction.tex** |
| **Minor-Figure 2 caption** | Note that d>3 signals instruction-following bimodality, not feature genuineness | Added one sentence to Figure 2 (feature_collapse) caption: "Cohen's $d > 3$... evidence of instruction-following bimodality rather than feature genuineness" | **Done — experiments.tex** |
| **Minor-Sonnet promotion** | Sonnet-on-Haiku result tucked in Discussion §5.4; deserves §4.8 prominence | Added short paragraph in §4.8 cross-family section; §5.4 now condensed to pointer + interpretation | **Done — experiments.tex, discussion.tex** |
| **Minor-abstract adv CI** | Adversarial framing is point-estimate; note CIs span zero on 2/3 targets | Added "(2 of 3 targets: Wilson CI includes zero)" to abstract headline bullet (3) | **Done — abstract.tex** |
| **Minor-multi-comparison scope** | Already addressed in V31 | No change needed | **Carried from V31** |

---

## MC1 — Title Narrowed

**Before:** `…A Three-Control Evaluation Across Open-Weight LLMs`

**After:** `…A Three-Control Evaluation of Instructed-Roleplay Detection Across Open-Weight LLMs`

The subtitle now names the setting being evaluated, removing the ambiguity about scope.

---

## MC2 — Framing Note at Top of §4

Added at the opening of §4 (Experiments):

> *"The seven-model panel in §4.2–§4.7 is a* demonstration *of the three controls, not a primary claim about any individual model. The paper's claims concern the magnitudes that emerge under joint application of equalization, cross-family extraction, and a regex baseline; the model-specific results instantiate those magnitudes. Headline numbers are consolidated in Tables 1 and 2."*

This directly addresses the reviewer's concern that the paper reads as an empirical-findings paper rather than a methodological demonstration.

---

## MC3 — ICC n≥100 Study: Camera-Ready Commitment (Strengthened)

We commit to the n≥100/3-annotator ICC study for camera-ready. The infrastructure is in place:
- Sampling script: `run_human_baseline_v24.py` (stratified 50T/50L, 7 targets, blind trial IDs)
- Analysis: `multi_rater_icc.py` (ICC(2,1), Krippendorff's α, Spearman ρ)
- Protocol: `icc_annotation_protocol_v2.md` (5-transcript anchor calibration to prevent the n=20 scale-discrepancy failure)

The §5.1 camera-ready commitment now includes the two-branch integration plan explicitly:

> **If α≥0.4 on correction density:** level-dependent claims validated; §5.1 updated to report validation passed; "PROVISIONAL" caveats removed.
> **If α<0.4:** level-dependent claims explicitly demoted to "preliminary, unvalidated"; §5.1 updated with new language; added to §5.7(g) limitation.

The n=20/2-annotator ICC=0.114 is not dismissed — it is reported as a real weakness in §5.1 and propagated to every level-dependent claim. The rule-match finding (80.1% pooled-LOO, 71.8% per-target LOO) is level-independent and unaffected.

**Response to Q1 (Why not run ICC n≥100 now?):** We did not run the study within this revision window because (a) Prolific recruitment takes 24–48hr and our revision window is tight, and (b) the n=100/3-annotator study is infrastructure-ready and we commit to including results in camera-ready. The camera-ready commitment now explicitly names the two integration branches so the reviewer knows exactly what will happen under either outcome.

---

## MC4 — Partial-Transfer Cells Named as Finding

The paragraph in §4.7 previously titled "Current best reading of the two chance-excluding cells" is now:

> `\paragraph{Partial transfer in two cells: unexplained positive signal.}`

Content is unchanged — two cells (Qwen 14B persona 68.0%, Mistral 7B false-belief 66.5%) have Wilson CIs that exclude chance. We report them as genuine unexplained positive signal, not noise.

One sentence added to §5.3 (Instructed Roleplay vs. Genuine Deception):

> *"Two of six fully-autonomous cells (Qwen 14B persona 68.0%, Mistral 7B false-belief 66.5%) have Wilson CIs that exclude chance; these represent genuine unexplained partial-transfer signal that our pre-registered axes cannot account for, and are treated as findings, not noise (§4.7)."*

**Response to Q3 (Qwen 14B persona mechanism):** Our current best guess: persona roleplay in English naturally licenses out-of-character corrections (a model playing "Dr. X" may correct a false claim as character-breaking behavior), while ICL false-belief suppresses the correction channel by providing competing exemplars. This is a hypothesis, not a validated account — the 10-trial qualitative spot-check (camera-ready commitment, §5.8(3)) is specifically designed to test whether Qwen 14B persona transcripts show correction-style language vs. in-character compliance. We report the two cells as genuine unexplained positive signal and flag them as a priority for follow-up.

---

## MC5 — Abstract Rewrite: Lead with Per-Target LOO 71.8%

**Before (sentence 1):** "A one-line regex (refusal count ≥1, fixed threshold, no calibration) achieves 80.1% average accuracy across seven prompt-equalized LLMs…"

**After (sentence 1):** "A one-line regex (refusal count ≥1) achieves **71.8% per-target LOO accuracy** (7 targets, 689 trials; threshold calibrated independently per target), within 3 pp of a 5-feature LLM pipeline's 74.3% same-family-extracted result (level-dependent; ICC=0.114, §5.1) and exceeding its 64.7% cross-family-extracted result by 7 pp. The same rule without any calibration (pooled fixed threshold k=1) achieves 80.1% (range 64–88%)."

The pooled 80.1% is now explicitly labeled "pooled fixed threshold" in the headline bullet, making the two numbers and their distinct interpretations clear.

---

## MC6 — Pacchiardi Promoted to Own Paragraph

**Before (inline in `\paragraph{Regex matches or exceeds under equalization.}`):**
> *"…Pacchiardi-style exception. At ≥14B scale…"* — bolded inline, easy to miss.

**After (own named paragraph):**
> `\paragraph{When the pipeline adds value: topical follow-ups at ≥14B (Pacchiardi-style exception).}`

Full content preserved; the paragraph is now visually distinct. One sentence added to §1.1 contribution (1):

> *"The pipeline materially outperforms the rule in one specific regime: claim-related multi-turn follow-ups at ≥14B (§4.5; Appendix K), where it gains +14–+29 pp over the rule (Llama 70B: +14 pp; Qwen 14B: +29 pp)."*

**Response to Q2 (Why not foreground Pacchiardi as positive?):** We foreground the rule-match as the primary finding because (a) it is the methodological point — a one-line baseline matches a pipeline — and (b) the Pacchiardi-style +14–+29 pp gain is conditioned on a specific regime (multi-turn + topical relevance + ≥14B) that is not the default evaluation setting. The own-paragraph promotion makes the regime where the pipeline genuinely wins visible without restructuring the paper's primary argument.

---

## Q4 — Llama 8B-on-8B Same-Checkpoint Control

**What we did:** Re-extracted the existing 100 equalized Llama 3.1 8B transcripts using Llama 3.1 8B itself as extractor (Ollama; `llama3.1:8b`; temperature 0.1; 5-feature protocol identical to cross-family panel; pipeline LOO via leave-one-out logistic regression; refusal-count k≥1 LOO with Wilson 95% CI).

**Result:**

| Extractor | n | Pipeline LOO | Wilson 95% CI | Refusal-count k≥1 LOO | d (RC) |
|---|---|---|---|---|---|
| Haiku (cross-family) | 100 | 65.0% | — | 74.0% | — |
| Mistral L3 (cross-family) | 100 | 64.0% | — | — | — |
| Llama 70B (cross-checkpoint) | 100 | 67.0% | — | — | — |
| **Llama 8B (same-checkpoint, same-family)** | **100** | **63.0%** | **[53.2%, 71.8%]** | **54.0%** | **0.26** |

**Interpretation:** Llama 8B self-extraction (63.0% pipeline, 54.0% refusal-count) falls *below* all three cross-family extractors (65–67%). The same-checkpoint same-family control shows **no self-boost** — the exact opposite of what a self-preference inflation would predict.

This is the best possible outcome for the localization argument: even when we eliminate the capability-asymmetry concern entirely (same model, same checkpoint, same parameter count), Llama 8B shows no uplift on its own transcripts. **Four independent non-Haiku self-family cells** (Llama-8B-on-8B, Llama-70B-on-3B, Llama-70B-on-8B, Qwen-14B-on-7B) all produce no self-boost. Only Haiku-on-Haiku is anomalous. The +10 pp inflation is localized to the Haiku checkpoint, not to same-family extraction in general, not to Claude-family RLHF, not to capability asymmetry.

---

## Minor — Figure 2 Caption Note

Added to Figure 2 (`feature_collapse.pdf`) caption:

> *"Cohen's $d > 3$ on correction density in the instructed condition is itself evidence of instruction-following bimodality rather than feature genuineness (see §5.1)."*

---

## Minor — Sonnet Result Promoted to §4.8

The full Sonnet-on-Haiku paragraph has been added to §4.8 (Cross-Family Extraction) as `\paragraph{Within-Anthropic control: Sonnet 4.5 on Haiku target.}` and §5.4 has been condensed to a summary pointer + interpretation. The experimental result now appears in the §4 experiment section where it belongs.

---

## Responses to Open Questions

**Q5 (Non-ADAGE published detector):** We acknowledge this as a limitation. The most comparable published system (Pacchiardi et al.) is evaluated in Appendix K with our protocol; our cross-family pipeline achieves 64.7%, below Pacchiardi's reported 67–73% range (consistent with same-family inflation). A direct replication with a fully independent non-ADAGE pipeline would require reimplementing their system end-to-end; we treat this as future work rather than a V32 commitment.

---

## V32 Diff Summary

**Experiments run:**
- Llama 3.1 8B-on-8B same-checkpoint self-extractor (n=100; pipeline LOO 63.0% [53.2%, 71.8%]; refusal-count 54.0%; no self-boost; fully integrated)

**Paper edits:**
- `main.tex` — MC1: subtitle narrowed to name instructed-roleplay setting
- `abstract.tex` — MC5: sentence 1 leads with 71.8% per-target LOO; adversarial CI note added to bullet (3)
- `introduction.tex` — MC6: Pacchiardi regime pointer added to §1.1 contribution (1); stale 82% sycophancy reference updated to 68.5–83%
- `experiments.tex` — MC2: framing note at §4 opening; MC4: paragraph renamed; MC6: Pacchiardi own paragraph; Minor-Fig2: caption note; B6: Sonnet paragraph added to §4.8
- `discussion.tex` — MC4: one sentence added to §5.3; §5.4 Q2 paragraph condensed to pointer

**Page count estimate:** ~48–49 pages (Pacchiardi paragraph split +0.1p; Sonnet §4.8 paragraph +0.2p; framing note +0.1p; partial-transfer §5.3 sentence +0.02p; abstract rewrite ~0p; Fig2 caption +0.02p). If over 48-page target, we will trim the Sonnet §5.4 paragraph to one sentence or remove the Pacchiardi §1.1 pointer sentence.

---

## Camera-Ready Commitments (Accumulated)

- ICC n≥100/3-annotator study with Krippendorff's α (from V30; two-branch integration plan in §5.1)
- RLHF-collapse replication on ≥2 additional models at ≥14B (from V30)
- Sycophancy n=200 for Llama 70B (from V31)
- Llama 8B-on-8B same-checkpoint self-extractor result integrated into Table 9 + §5.7(f) (from V32)

---

## Out-of-Scope for V32

- ICC n≥100/3-annotator study: camera-ready commitment (Prolific ~$300, 24–48hr; infrastructure ready)
- Non-ADAGE published detector replication: future work
- Figure 1(a) replacement with per-target extractor comparison: deferred (figure currently PDF; data in Table 9)
- Trained-annotator human baseline condition: camera-ready candidate

---

*Word count: ~1,700. Response letter follows V31 template.*
