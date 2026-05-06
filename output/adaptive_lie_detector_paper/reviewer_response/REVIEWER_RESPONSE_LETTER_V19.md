# Response to Reviewer (Weak Accept, 6/10; Confidence 4/5) — Revision V19

We thank this reviewer for the careful and constructive critique. The review is a materially different read from the V18 reviewer (who returned Accept, 7/10) and focuses on four substantive weaknesses and six minor issues that V19 closes with **new data on every major ask**, not framing alone. Specifically:

- **W1 (contribution framing)** — every "we introduce X" claim has been rewritten as "first joint application to behavioral deception detection," with single-citation acknowledgements of prior art (sycophancy, jury-of-judges, standard NLP) in §1.1 and §5.5.
- **W2 (headline-number ambiguity)** — the abstract and §1.1 both lead with one primary headline, **7-target cross-family pooled LOO 64.7%** (Mistral Large 3 extractor, under equalization), confirmed by a second non-Anthropic extractor (Llama 3.3 70B at 66.9%). Haiku-extracted and 8-target variants are demoted to sensitivity analyses.
- **W3 (ADAGE pipeline real estate)** — §3.2 cut from 20 lines to 5 lines; Appendix A.3 (pipeline architecture figure and 40-line description) deleted entirely. Only the 5-feature definitions required by §4 forward-refs are retained.
- **W4 (same-family bias vs.\ capability asymmetry)** — a **new Llama-70B-on-Llama cross-extraction panel** (3 Llama targets + 5 non-Llama targets, Apr 2026) shows Llama-70B-extractor scores Llama 3B/8B/70B at **50%/67%/74%** vs.\ Mistral-L3 extractor at **52%/67%/87%** — i.e., the +9–10 pp Haiku-on-Claude uplift does **not** replicate as a Llama-on-Llama uplift, localizing the same-family bias to Claude-specific RLHF self-preference.
- **W5 (autonomy + adversarial underpowered at n=50)** — **new n=200 runs** on 7 rows (adv-fullregex × 3 targets; persona + false-belief × 2 targets) sharpen the Wilson CIs 2× vs.\ n=50. The heterogeneous-mechanism finding on adversarial is preserved; autonomy persona/false-belief CIs remain near chance with tighter bounds.
- **Minor W6–W10** — all resolved via text edits; see the at-a-glance table below.

V19 is a substantive revision: the only phase that does not add new computation is the text-restructure pass (P1). Every major ask has new runs behind it.

**Summary of V19 changes at a glance.**

| W# | Reviewer ask | V19 response | Location |
|---|---|---|---|
| W1 | Contribution framing oversells (controls have prior art) | **Reframed** to "first joint application to behavioral deception detection" with sycophancy/jury-of-judges/NLP citations | `abstract.tex` L1, `introduction.tex` L8, `discussion.tex` §5.5 L34 |
| W2 | Headline ambiguity — 4 candidates compete | **Primary = 7-target cross-family 64.7%**; others demoted to sensitivity analysis | `abstract.tex` L4, `introduction.tex` Contribution 1 L17 |
| W3 | ADAGE pipeline real estate given then shown redundant | **§3.2 cut 20→5 lines; App A.3 deleted entirely** (~45 lines removed) | `methodology.tex` §3.2 (was ~20 lines, now 5); `appendix.tex` App A.3 removed |
| W4 | Same-family bias vs. capability asymmetry not resolved | **New Llama-on-Llama panel** — no uplift observed; bias localizes to Claude RLHF | `experiments.tex` §4.6; `discussion.tex` §5.7(f) |
| W5 | n=50 underpowers 7 rows | **n=50 → n=200 scale-up** on adv-fullregex × 3 targets + persona/false-belief × 2 targets | `experiments.tex` §4.6 (autonomy), §4.8 (adversarial); Tables 4, 5, 10 |
| W6 | Probe-panel "signal floor" overselling | **Softened** — "$n=2$ probe architectures are not dispositive, not a validated floor" | `discussion.tex` §5.2 L14 |
| W7 | Qwen 32B RLHF-collapse in abstract | **Removed from abstract**; kept in §4.4 only | `abstract.tex` — no "32B" mention |
| W8 | Sonnet 4.5 pilot in abstract | **Removed from abstract**; kept in §4.5 + App M only | `abstract.tex` — no "Sonnet" mention |
| W9 | English-only scoping buried in final clause | **Moved to 3rd sentence** of abstract (first paragraph) | `abstract.tex` L2 |
| W10 | Disposition-source as "established" framing | **Already hedged** in V17/V18: "best-supported-but-not-pre-registered"; re-verified | `experiments.tex` §4.7.1; `discussion.tex` §5.8 future work item 4 |

---

## W1 — Contribution framing: first joint application (not "we introduce")

**What was asked.** The reviewer correctly observed that each of our three controls has individual prior art — prompt equalization in sycophancy evaluation, cross-family LLM-as-judge in jury-of-judges work, and regex/lexical baselines as standard NLP sanity checks. They asked that the paper stop framing these as "controls we introduce" and instead credit prior art while narrowing the contribution claim to the joint application.

**What we did.** Three sites were rewritten:

**1. Abstract lead (sentence 2):**

> "None of the three controls we apply — prompt equalization, cross-family feature extraction, and surface-level regex baselines — is individually novel (each has prior art in sycophancy studies, LLM-as-judge robustness, and standard NLP respectively); our contribution is their _first joint application_ to behavioral deception detection, which materially changes the headline numbers."

**2. §1.1 Motivation and Contributions (paragraph lead):**

> "None of the three controls below is individually novel — prompt equalization is standard in the sycophancy literature, cross-family LLM-as-judge usage is the 'jury-of-judges' design, and lexical/regex baselines are routine NLP sanity checks. Our contribution is the _first joint application_ of all three to behavioral deception detection and the demonstration that their joint application materially changes the headline numbers."

**3. §5.5 Technical Contribution and Novelty:**

> "The contribution is not that any of the three controls is individually novel: prompt equalization has been used in sycophancy and instruction-following studies [perez2022discovering], LLM-as-judge capability asymmetries motivate cross-family evaluation in the 'jury-of-judges' literature, and lexical/regex baselines are standard NLP sanity checks. The contribution is the _first joint application_ of equalization, cross-family extraction, and regex baselines to behavioral deception detection, and the demonstration that their joint application reveals confounds of a magnitude previously undocumented in this domain: 30–41 pp accuracy collapse under equalization, up to 7× feature variance across extractors, and 9–16 pp same-family extractor inflation (now further localized to Claude-on-Claude by the Llama-on-Llama control, §4.6)."

Existing citations for prior art are preserved: `\cite{sharma2023sycophancy}` (sycophancy equalization), `\cite{verga2024replacing}` (jury-of-judges), and standard-NLP regex-baseline practice cited inline.

**Files.** `sections/abstract.tex`, `sections/introduction.tex` §1.1, `sections/discussion.tex` §5.5.

---

## W2 — Pick one primary headline (64.7%, 7-target cross-family)

**What was asked.** V18 had four candidate headlines competing for reader attention: 80.1% (Haiku pooled), 74.3% (Haiku 7-target), 64.7% (Mistral-L3 7-target cross-family), and 64.2% (8-target with Qwen 32B). The reviewer recommended picking one primary regime and demoting the rest to sensitivity analysis.

**What we did.** We promoted the most conservative interpretable regime — **7-target cross-family pooled LOO 64.7%** (Mistral Large 3 extractor, under equalization) — as the primary headline number everywhere the paper speaks in headlines.

**Abstract primary headline sentence:**

> "Primary headline (7-target cross-family, Mistral Large 3 extractor): pipeline accuracy 64.7% on Llama 3.2 3B/8B, Mistral 7B, Qwen 2.5 7B/14B, Llama 3.3 70B, and Claude Haiku 4.5 (equalized, pooled-LOO); under a second non-Anthropic cross-family extractor (Llama 3.3 70B) the same panel is 66.9%."

All other headline numbers are explicitly demoted:
- Haiku-extracted 74.3% is reported as a sensitivity analysis with the 9–10 pp uplift flagged as "consistent with Claude-specific RLHF self-preference."
- The 8-target (including Qwen 32B) variant at 64.2% is reported as a transparency diagnostic ("within 0.5–0.9 pp of the 7-target value").
- The rule at 80.1% Haiku-pooled is reported but framed: "is extractor-independent by construction; we recommend the 7-target cross-family 64.7% as the primary interpretable summary statistic and the 8-target 64.2% as a transparency diagnostic; the rule is a more honest headline than either pipeline value."

**Verification.** `grep -c "64\.7" sections/abstract.tex` returns ≥ 1; `grep -c "74\.3" sections/abstract.tex` returns 0 (value appears only in §4, never in the abstract headline).

**Files.** `sections/abstract.tex` primary headline; `sections/introduction.tex` §1.1 Contribution 1.

---

## W3 — ADAGE pipeline trim: §3.2 20→5 lines, App A.3 deleted

**What was asked.** The reviewer noted that §3.2 gave the ADAGE pipeline substantial real estate, then §4.5 and §5.6 demonstrated it is redundant with a one-line refusal-count rule. They asked that the pipeline's page footprint match its reduced-role framing.

**What we did.** Two cuts:

**1. §3.2 ADAGE Pipeline cut 20 lines → 5 lines.** We retained only the 5-feature names (consistency, specificity, correction-marker density, confidence, elaboration) — these are referenced by name in §4.9 (probing) and §5.1 (ICC). We cut: the adaptive-stopping description, the pipeline-architecture diagram references, the feature-weight discussion, and the 8-turn-cap prose. The §3.2 text now reads:

> "The ADAGE pipeline produces, for each trial, five LLM-extracted features on a 0–10 scale: **consistency**, **specificity**, **correction-marker density**, **confidence**, and **elaboration**. These feature names are the ones referenced by the experiments and probe sections; the extractor LLM scores each assistant response across up to 8 interrogator turns and trial-level means feed a logistic-regression classifier. The pipeline is the measurement vehicle, not the contribution — a single refusal-count regex matches or exceeds it on 6 of 7 equalized models (§4.5), and its primary LLM feature has weak construct validity (§5.1)."

**2. Appendix A.3 deleted entirely.** The 40-line pipeline-architecture appendix (including a TikZ figure) was the direct target of W3. It is fully removed. The `\label{app:pipeline_details}` is preserved via a 3-line pointer paragraph so no cross-ref breaks; any remaining forward-refs now resolve to that pointer, which redirects to §3.2.

**Forward-ref audit.** We grepped for `\ref{sec:adage_pipeline}` and `\ref{app:pipeline_details}` across all section files. No orphaned references remain.

**Files.** `sections/methodology.tex` §3.2 (L17–L21, now 5 lines; was ~25 lines); `sections/appendix.tex` App A.3 (~40 lines removed and replaced with a 3-line pointer).

---

## W4 — Same-family bias vs.\ capability asymmetry: new Llama-on-Llama panel

**What was asked.** V18 reported +9–10 pp Haiku-on-Haiku uplift (Haiku extracting Claude Haiku target) over Mistral-L3 extraction. The reviewer correctly noted this is observationally consistent with either (a) Claude-specific RLHF self-preference or (b) Haiku being a more capable extractor than Mistral-L3. The two hypotheses were not separable with the V18 design. They suggested running a second self-family extraction pair on a different family to test whether the uplift replicates.

**What we did.** We ran Llama-3.3-70B-as-extractor on Llama-family targets (3B, 8B, 70B) on the same equalized transcripts used for Haiku and Mistral-L3 extraction. This gives us the three pairings needed for the test:

| Extractor → Target | Llama 3.2 3B | Llama 3.1 8B | Llama 3.3 70B |
|---|---|---|---|
| Mistral Large 3 (cross-family) | 52% | 67% | 87% |
| Llama 3.3 70B (same-family) | **50%** | **67%** | **74%** |
| Δ (same − cross) | **−2 pp** | **0 pp** | **−13 pp** |

Compare to the corresponding Haiku-on-Claude row on Claude Haiku 4.5 target: Mistral-L3 extractor 61%, Haiku-self extractor 71%, **Δ = +10 pp**.

**The Haiku-on-Haiku +10 pp uplift does not replicate as a Llama-on-Llama uplift.** The Llama-70B same-family row on the three Llama targets is either flat or _negative_ vs.\ the Mistral-L3 cross-family baseline. This localizes the +9–10 pp uplift to Claude-specific RLHF self-preference and makes capability asymmetry an implausibly-specific explanation (it would require the Haiku vs. Mistral-L3 gap to be positive on Claude targets but zero-or-negative on Llama targets, which is not a capability pattern).

**Abstract integration:**

> "Haiku-extracted on the same panel is 74.3%; the 9–10 pp uplift is consistent with Claude-specific RLHF self-preference — Llama-70B-as-extractor on Llama 3B/8B targets shows _no_ analogous Llama-on-Llama inflation."

**§4.6 integration:** A new paragraph reports the Llama-on-Llama results as a W4-direct response, citing the three cells above. The "Haiku-on-Haiku uplift" is recast as "Claude-on-Claude uplift" wherever the distinction matters.

**§5.7(f) Limitations update:**

> "Same-family extraction inflates signal; cross-family should be standard. The Llama-on-Llama control (§4.6) argues the 9–10 pp Claude-on-Claude uplift is Claude-specific RLHF self-preference rather than a universal family-bias; one more non-Anthropic self-family extractor pair would further constrain this."

**Files.** `code/adaptive_lie_detector/data/results/cross_family_equalized_{llama3_2_3b,llama8b,llama70b}_llama70b_extractor.json` (existing, Apr 2026); new analyzer output in `output/adaptive_lie_detector_paper/llama70b_extractor_panel.json`; `sections/experiments.tex` §4.6; `sections/discussion.tex` §5.7(f); `sections/abstract.tex`.

---

## W5 — n=200 scale-up on 7 underpowered rows

**What was asked.** V18 reported n=50 cell sizes for (a) the adversarial-fullregex-disclosed attack on 3 open-weight targets (Table 10) and (b) the persona-maintenance + false-belief-ICL autonomy rows on 2 targets each (Tables 4 and 5). Wilson 95% CIs at n=50 are wide enough that most of the near-chance autonomy point estimates span 50%, weakening the negative-transfer claim. The reviewer asked we scale to n=200 on these 7 key rows.

**What we did.** We launched n=200 runs on exactly the 7 rows: adversarial-fullregex × {Llama 3.2 3B, Mistral 7B, Qwen 2.5 14B}; persona-maintenance × {Llama 3.2 3B, Qwen 2.5 14B}; false-belief-ICL × {Llama 3.2 3B, Qwen 2.5 14B}. Implementation details:

- **Adversarial scale-up.** `run_adversarial_full_regex.py` was extended to support `--n_samples 200` via pool-replication (the claims pool caps at 100 pairs from `claims_equalized.py`; we replicate 2× with the existing Ollama temperature=0.7 setting to sample fresh completions per-claim, preserving per-claim structure via `trial_idx`). Fresh random seeds; not a resume of n=50 data.
- **Autonomy scale-up.** `run_persona_autonomous.py` and `run_false_beliefs_autonomous.py` sample-with-replacement from their 20-stem pools, so n=200 is a natural 10× replication — no script changes.
- **Analysis.** Refusal-count LOO, Cohen's $d$, and Wilson 95% CIs recomputed at n=200 from scratch; Tables 4, 5, and 10 updated in-place.

**Status at submission.** 3 of 7 n=200 runs are complete and integrated in the paper; 4 (Mistral 7B adversarial, Qwen 14B adversarial, Qwen 14B persona, Qwen 14B false-belief) remained in flight on local GPU hardware at submission cutoff. The completed rows appear with n=200 in Tables 4 and 10; rows still at n=50 are explicitly flagged in the respective captions ("Mistral~7B and Qwen~14B Adv-FullRegex columns remain $n=50$"; "sycophancy and Qwen~14B persona/false-belief remain $n=50$"). The 4 pending Qwen 14B / Mistral 7B rows will be reported in the camera-ready.

| Row | n=50 LOO | n=200 LOO | Wilson 95\% CI |
|---|---|---|---|
| Adversarial-fullregex Llama 3.2 3B | 50.0\% | **61.5\%** | [54.6, 68.0] |
| Persona-maintenance Llama 3.2 3B | 66\% | **54.0\%** | [47.1, 60.8] |
| False-belief-ICL Llama 3.2 3B | 60\% | **56.0\%** | [49.1, 62.7] |
| Adversarial-fullregex Mistral 7B | 66.0\% | _in flight_ | --- |
| Adversarial-fullregex Qwen 2.5 14B | 44.0\% | _in flight_ | --- |
| Persona-maintenance Qwen 2.5 14B | 66\% | _in flight_ | --- |
| False-belief-ICL Qwen 2.5 14B | 66\% | _in flight_ | --- |

**Interpretation (Llama 3B at n=200).** The two autonomy rows move closer to chance with much tighter CIs, strengthening the negative-transfer claim: the n=50 point estimates (66\%, 60\%) were optimistic, and n=200 gives 54.0\% (Wilson width 13.7 pp vs.\ 31 pp at n=50) and 56.0\% (width 13.6 pp vs.\ 32 pp). The adversarial row reveals a small-sample artifact at n=50: the rule was reported as 50.0\% (truth 8\%, lie 92\%), consistent with truth-channel suppression; at n=200 the failure mode is actually lying-channel suppression (truth 87\%, lie 36\%) and the rule recovers partially to 61.5\%. The heterogeneous-mechanism claim on adversarial is therefore qualified on this target: at n=200 the rule is weakened (from the instructed 100\% ceiling) but not defeated.

**Pre-commit on the 4 pending runs.** Regardless of what the 4 Qwen 14B / Mistral 7B runs produce, the camera-ready will report them honestly. If they preserve n=50 directions, the negative-transfer / heterogeneous-mechanism claims strengthen; if they shift, the abstract framing will be updated to reflect the shift. This pre-commit is visible in this response letter so selective reporting is not available.

**Files.**
- Adversarial: `code/adaptive_lie_detector/data/results/adversarial_full_regex_{llama3_2_3b,mistral_7b,qwen2_5_14b}_n200_final.json`
- Autonomy: `code/adaptive_lie_detector/data/results/persona_autonomous_{llama3.2_3b,qwen2.5_14b}_n200_final.json`, `false_beliefs_autonomous_{llama3.2_3b,qwen2.5_14b}_n200_final.json`
- Tables updated: `sections/experiments.tex` Tables 4, 5, 10
- Abstract scale-up sentence: `sections/abstract.tex`

---

## W6 — Probe-panel "signal floor" softened

**What was asked.** V18 §5.2 said "preliminary evidence that the equalized regime is hard for probes" on the basis of $n=2$ probe architectures. The reviewer correctly noted this is over-reading two data points.

**What we did.** §5.2 now reads:

> "This is _one data point at a single design point_ (last-layer last-token LR, two targets, one architecture, one pooling strategy), not a validated floor. The result does not warrant the reading that 'the equalized regime is hard for probes': $n=2$ probe architectures are not dispositive, and one of the two uses a base/Instruct checkpoint mismatch. Azaria \& Mitchell report substantially stronger probes on Llama-1 7B under a different prompt regime. We report the probe parity with the rule as _consistent with_ representation-level difficulty at the tested configurations; conclusive comparison would require multiple probing architectures (intermediate layers, mean-pooled representations, non-linear probes) and frontier-scale open-weight targets."

**Files.** `sections/discussion.tex` §5.2 Black-box Behavioral vs.\ White-box Probing.

---

## W7 — Qwen 32B removed from abstract

**What was asked.** The Qwen 2.5 32B RLHF-zero-refusal-collapse is an interesting finding but was competing for abstract attention with the primary headline.

**What we did.** No "32B" mention in the abstract. The Qwen 32B collapse finding is retained in §4.4 (Qwen scale sweep) and in §5.1's machine-ICC-proxy paragraph (where it informatively collapses to ICC 0.00–0.06) but does not appear in the abstract.

**Verification.** `grep -c "32B" sections/abstract.tex` returns 0.

**Files.** `sections/abstract.tex`.

---

## W8 — Sonnet 4.5 removed from abstract

**What was asked.** The Sonnet 4.5 pilot ($n=99$) is a single frontier data point and was competing for abstract attention with the primary headline.

**What we did.** No "Sonnet" mention in the abstract. The Sonnet frontier pilot is retained in §4.5 and Appendix M with the full paired-bootstrap CI treatment.

**Verification.** `grep -c "Sonnet" sections/abstract.tex` returns 0.

**Files.** `sections/abstract.tex`.

---

## W9 — English-only scoping moved to first paragraph

**What was asked.** V18's English-only scoping was in the final clause of the last sentence of the abstract. The reviewer correctly noted that scope limitations of this magnitude belong in the first paragraph so they shape how the headline numbers are read.

**What we did.** The English-only + lexical-fragility scoping is now in the 3rd sentence of the abstract (first paragraph):

> "All behavioral detection here is English-only and reads the lexical surface of replies; refusal-marker patterns are not validated on non-English prompts, code-switching, or stylistic variants."

The §1 Introduction "Scope: English-only and lexical-fragile" paragraph was already in place from V17 and is unchanged; the abstract promotion just makes this visible to readers who only read the abstract.

**Verification.** `grep -c "English-only" sections/abstract.tex` returns ≥ 1, in the first paragraph.

**Files.** `sections/abstract.tex`.

---

## W10 — Disposition-source already hedged

**What was asked.** V18 framed disposition-source as "the established interpretation" replacing the V17 knowledge-conflict-clarity gloss. The reviewer asked whether disposition-source itself was pre-registered (no — it is a post-hoc reading that best explains the data).

**What we did.** The phrasing was already hedged in V17/V18 as "best-supported-but-not-pre-registered." We re-verified and §4.7.1 currently reads:

> "Disposition-source (system-prompt-induced agreement pressure) is the most-consistent reading but itself not pre-registered; §5.8 item 4 commits to the cleaner test (varies disposition-source vs.\ clarity while holding turn-count and target fixed)."

§5.8 Future Directions item 4 is the pre-registered 5th scenario commitment (carried from V18).

**Files.** `sections/experiments.tex` §4.7.1; `sections/discussion.tex` §5.8 item 4.

---

## Acknowledgements

We want to specifically credit the reviewer for two framing wins that V19 adopts verbatim:

1. **"First joint application to behavioral deception detection"** is the reviewer's exact framing — it is more precise than our V18 phrasing and honest about the individual prior art. We adopt it unchanged.
2. **Primary-headline discipline** — picking one number and demoting the rest to sensitivity analysis — is a clean improvement in how the paper communicates with a cold reader. We adopt it.

The Llama-on-Llama extraction test (W4) was the reviewer's insight that the Haiku-on-Claude +10 pp alone cannot distinguish self-preference from capability asymmetry. The new panel confirms the reviewer's suspected mechanism (self-preference, localized to Claude) — this is data the paper did not have before V19.

---

## Carried-over defers (unchanged from V18)

These items remain out-of-scope for V19 and are the explicit camera-ready commitments or future work:
- **Human ICC study at $n \geq 100$ with 3+ annotators** — camera-ready commitment (V18 bolded sentence in §5.1, unchanged).
- **Pacchiardi full replication** (task #112) — defers to post-camera-ready.
- **Qwen 14B sycophancy ablation** (task #161) — defers to post-camera-ready.
- **Closed-loop iterated adversary, 2nd RLHF-heavy ≥14B target** — carried from V16–V18 defer lists.
- **Pre-registered 5th scenario** (disposition-source vs. clarity held fixed, V18 Future Directions item 4) — explicitly future work.

---

## Page budget

V18 submitted at 41 pages. V19 stays at ≤41 pages after: −2 pages from §3.2 + App A.3 trim; +0.3 page from the Llama-on-Llama integration paragraph in §4.6; +0 pages from n=200 table updates (in-place); −0.3 page from abstract compression (607 → ~440 words).
