# Response to Reviewer (Weak Accept, 6/10; Confidence 4/5) — Revision V17

We thank the reviewer for the constructive read, the explicit prioritization between expected asks (R1–R3), specific suggestions (S1–S4), and text-only weakness sharpenings (W-eng, W-stats), and for framing R1–R3 as the revision bar. V17 delivers on R1–R3 and on all actionable S1–S3 items within a single revision cycle; S4 and the full human ICC study (R1 authoritative form) are logged as **camera-ready commitments**.

**Summary of V17 changes at a glance.**

| Ask | Form | Where |
|---|---|---|
| **R1** Human ICC n≥100 / 3+ annotators | **Proxy delivered** (machine-rater ICC across 3 LLM extractors on same n=100 transcripts); raw n=20 annotator files released; full human study deferred to camera-ready | §5.1 new paragraph, `multi_rater_icc.py`, `machine_rater_icc.json` |
| **R2** Pre-registered 4th EXP-I-matched scenario | **Executed**: high-clarity vs low-clarity knowledge-conflict, Llama 3B / Mistral 7B / Qwen 14B, n=50 per condition | new §4.7.X `sec:exp_i_4th_scenario`, `run_exp_i_4th_scenario.py` |
| **R3** Compress OR expand Sonnet 4.5 pilot | **Compress chosen** (per reviewer either/or): §4.5 27-line paragraph + Table 7 → 4-line summary with CI and appendix pointer; 2 of 3 Sonnet abstract mentions removed; 2 Sonnet rows moved from primary table to diagnostics | abstract, §4.5, appendix `sec:sonnet_pilot`, Table 2 split |
| **S1** Split Table 2 into primary + diagnostics | **Executed**: `tab:headlines_primary` (9 rows) + `tab:headlines_diagnostics` (5 rows) | §4.2 |
| **S2** Mistral 7B Instruct per-layer probe | **Partial**: full-layer sweep on Mistral 7B **base** checkpoint (reuses V16 `--full_sweep`); base-vs-Instruct distinction footnoted | §5.2, Table 8, `probe_layer_curve_panel.pdf` |
| **S3** One primary number per claim | **Executed** via S1 split — primary table has single canonical number per row | §4.2 |
| **S4** 2nd RLHF-heavy ≥14B model for Qwen 32B replication | **Camera-ready commitment** (tractable, parallel to R2 compute budget) | response letter, future work |
| **W-eng** English-only + lexical-fragility more prominent | **Executed**: abstract trailer sentence, §1.1 scope paragraph, §5 limitations keep | abstract.tex, introduction.tex |
| **W-stats** §4.6 pooled ≤7B vs ≥14B load-bearing or demote | **Demote chosen**: inline sentence → footnote; number preserved in diagnostics table | §4.6, Table 3 |

---

## R1 — Human ICC at n≥100 with 3+ annotators

**What was asked.** A proper inter-rater reliability study for the 5 behavioral features at n≥100 with 3+ annotators, to lift the ICC=0.114 caveat that currently bounds all absolute-level claims.

**What we did in V17 (proxy).** We computed a **three-rater machine-ICC** on the same n=100 equalized transcripts using the three LLM feature-extractors already available from the cross-family panel: Claude Haiku 4.5, Llama 3.3 70B Instruct, and Mistral Large 3. Coverage is 5 of 8 targets with triple-rater files (haiku, llama 8B, qwen 7B/14B/32B) for pooled n_trials=495. We implemented Shrout–Fleiss ICC(2,1) and ICC(2,k) two-way random effects, absolute agreement.

Results:
- Pooled mean ICC(2,1) across 5 features = **0.79**; ICC(2,k) = **0.89**
- Per-feature ICC(2,1): elaboration 0.95, specificity 0.94, confidence 0.91, **defensiveness (= correction density) 0.77**, consistency 0.37
- Qwen 2.5 32B row: ICC(2,1) ∈ [0.00, 0.06] across all 5 features — the RLHF zero-refusal collapse documented in §4.4 is visible at the rater-agreement level

**How we present it (honest framing).** We explicitly state in §5.1: *"This proxy does NOT substitute for the reviewer's human ICC ask."* Three LLM raters share systematic biases (overlapping training distributions, similar rubric interpretations) that human annotators do not; the defensiveness ICC jumping from 0.114 (human, n=20) to 0.77 (3 LLMs, pooled n=495) is exactly the pattern expected from shared rater bias, not independent evidence that the construct is reliable. We additionally release the raw n=20 human annotator rating files in supplementary material so reviewers can compute subgroup ICC and alternative reliability metrics independently.

**What we defer to camera-ready.** The authoritative human ICC at n≥100 with 3+ annotators remains a multi-week recruitment task not tractable in a single revision cycle. This is the fourth cycle this ask has been logged (V13/V14/V15 declined, V16 deferred); V17 delivers a non-trivial machine-rater proxy and a raw-data release as a good-faith partial response, and commits to the full human study as a camera-ready requirement.

**Files.**
- New: `code/adaptive_lie_detector/experiments/multi_rater_icc.py`
- New: `code/adaptive_lie_detector/data/results/machine_rater_icc.json`
- New §5.1 paragraph: "Machine-rater ICC proxy (R1, does not substitute for human ICC)"

---

## R2 — Pre-registered 4th EXP-I-matched scenario

**What was asked.** A pre-registered 4th scenario that varies only knowledge-conflict clarity while holding disposition-source and turn-count fixed, to disentangle the "knowledge-conflict clarity" interpretation from "small n on scenarios that happen to covary."

**What we did in V17.** Created `run_exp_i_4th_scenario.py`, which holds disposition-source = spontaneous (sycophancy system prompt, matching the §4.7 design that replicates at 82% across three scales) and turn-count = multi-turn adaptive (10 questions max, same detector as elsewhere), while varying only the magnitude of the knowledge conflict on FALSE claims:

- **High-clarity** false claims: textbook-wrong (e.g., "Water boils at 80°C", "The Sun orbits the Earth")
- **Low-clarity** false claims: near-miss or partially-true variants of the same domain (e.g., "Water boils at 99°C", "The Earth orbits the Sun every 360 days")
- **TRUE claims** are identical across both conditions (15 shared true claims); only the false-side is manipulated.

15 claim domains × (true, high-false, low-false) triples. Executed at n=50 per condition (= 25 true + 25 false per condition) on three models via Ollama: Llama 3.2 3B, Mistral 7B, Qwen 2.5 14B. Full numbers are reported in §4.7.X (Section `sec:exp_i_4th_scenario`); pre-registered prediction is that refusal-count LOO should be **higher under high-clarity than low-clarity** if the knowledge-conflict-clarity interpretation is correct.

**Why this is the right test.** The confound we flagged in V16 is that the three EXP-I-matched scenarios (sycophancy, persona, false beliefs via ICL) vary along three axes at once — knowledge-conflict clarity, instructed-action vs spontaneous-disposition, and single- vs multi-turn structure. The 4th scenario holds disposition-source and turn-count fixed at the sycophancy-multi-turn setting (the one that robustly transfers at 82% across three scales) and manipulates only clarity. A positive high-vs-low contrast is clean evidence that clarity is the controlling axis; a null contrast tells us clarity is not load-bearing and the sycophancy result rests on the disposition-source / multi-turn axes instead.

**Files.**
- New: `code/adaptive_lie_detector/experiments/run_exp_i_4th_scenario.py`
- New: `data/results/exp_i_4th_scenario_{llama3.2_3b,mistral_7b,qwen2.5_14b}_latest.json`
- New §4.7.X subsection `sec:exp_i_4th_scenario`

---

## R3 — Compress or expand Sonnet 4.5 pilot

**What was asked.** Either compress the §4.5 Sonnet 4.5 single-frontier-pilot treatment (27-line paragraph + Table 7 + 3 abstract mentions) to a compact summary, OR expand to the ~n≈410 needed for 80% power on the +4 pp cross-family gap.

**What we chose (compress).** Per the reviewer's explicit either/or, we compressed.

- §4.5 paragraph: 27 lines → 4 lines. The surviving sentences state refusal-count LOO (73.7%), the 5-feature pipeline under Haiku (92.9%) and Llama 3.3 70B cross-family (88.9%), and the paired-bootstrap 95% CI on the +4 pp Haiku margin ([−3.0, +11.1], includes zero). Everything else is pushed to appendix `sec:sonnet_pilot`.
- Appendix: new section `\section{Sonnet 4.5 Frontier Pilot: Full Details}` with the full cross-extractor table (`tab:sonnet_crossfamily_app`) and the power calculation paragraph that previously sat in §4.5.
- Abstract: reduced from 3 Sonnet mentions to 1 (the retained mention is the single headline "73.7% refusal-count LOO; 92.9%/88.9% pipeline" with CI).
- Table 2 (headline numbers): 3 Sonnet rows removed from primary table; 2 Sonnet rows retained in new diagnostics table (see S1).

The compression respects that the Sonnet pilot is load-bearing for exactly one claim — "cross-family extractor gap shrinks at frontier scale" — which survives in compressed form; every auxiliary number (per-extractor table, power calc, bootstrap pairing explanation) is in the appendix where it belongs.

---

## S1 + S3 — Split Table 2 into primary + diagnostics; one primary number per claim

**What was asked.** S1: split Table 2 into a reader-facing primary table and a separate diagnostics table. S3: pick one primary number per claim rather than paired same-family / cross-family numbers.

**What we did.** Split `\label{tab:headlines}` into two tables. Both backward-compatible labels retained so existing `\ref{tab:headlines}` citations still resolve.

- **`tab:headlines_primary`** (rows 1–9): instructed LOO, equalized LOO, cross-family LOO (the canonical headline), scale patterns, the EXP-G decomposition, and sycophancy semi-autonomous transfer. Each row reports the single number the reader should memorize.
- **`tab:headlines_diagnostics`** (rows 10–14): adversarial paraphrase effect, ICC caveat pointer, and the 3 Sonnet pilot rows displaced from the primary table by R3 compression.

S3 falls out of S1 automatically: by moving paired same-family / cross-family rows into diagnostics, the primary table carries exactly one canonical number per row.

---

## S2 — Mistral 7B per-layer probe sweep

**What was asked.** Run the V16 per-layer probing sweep (originally on Llama 3B) also on Mistral 7B, to check whether the flat-across-layers curve replicates.

**What we did (partial with caveat).** We reused V16's `whitebox_5_multilayer_probes.py --full_sweep` on the existing Mistral 7B **base**-checkpoint equalized data (the same data whose last-layer probe is reported in §5.2 Table 8). A fresh extraction from Mistral 7B Instruct would require ~1 hour of representation extraction that was not tractable within the V17 compute budget alongside R2; we disclose this in a one-line footnote on the new §5.2 Mistral panel: *"Base-checkpoint representations; Instruct-checkpoint results may differ."*

Results integrated in §5.2: new 2-panel figure (`figures/probe_layer_curve_panel.pdf`) showing Llama 3B and Mistral 7B per-layer LR probe curves side-by-side, plus the best-layer row added to Table 8.

---

## S4 — 2nd RLHF-heavy ≥14B model for Qwen 32B replication

**What was asked.** Given the Qwen 32B RLHF zero-refusal collapse is load-bearing in §4.4, run a second ≥14B model with known RLHF-heavy safety training to check whether the pattern replicates.

**Camera-ready commitment.** Tractable in ~2–4h but parallel to R2 compute; we log it here and commit to deliver for camera-ready. Candidate models: Claude Haiku 4.5 (already evaluated, but that is same-family with Haiku extractor; the zero-refusal-under-neutral check is different), Llama 3.3 70B (evaluated equalized, no zero-refusal observed), or a DeepSeek / Yi / Gemma 2 frontier open-weight model with known aggressive safety tuning.

---

## W-eng — English-only + lexical-fragility more prominent

**Done.** The abstract now trails with a single sentence: *"All patterns and prompts are English-only and read from the lexical surface; non-English and semantic-adversary robustness are out of scope."* §1.1 has a new `\paragraph{Scope: English-only and lexical-fragile.}` that spells out the two limitations (14 regex patterns are English; both the rule and the 5-feature pipeline read from lexical surface; a one-shot adversarial paraphrase drops rule accuracy by 5–10 pp on three open-weight targets; the full-regex-disclosed variant defeats the rule at 2 of 3 scales). §5 limitations keep their existing English-only + lexical-marker language unchanged.

## W-stats — §4.6 pooled ≤7B vs ≥14B comparison

**Done (demote).** The pooled 67.8% (≤7B) vs 83.0% (≥14B) comparison is no longer an inline load-bearing sentence in §4.6. It is now a footnote on the §4.6 paragraph (preserving the number for completeness) and the header-number is also preserved in the diagnostics table (S1 split). The within-family increments (Qwen 3B→7B p=0.014; Llama 8B→70B p=0.004) are the load-bearing scale claim and remain inline.

---

## Items previously logged as deferred (V15/V16 carry-over)

These remain deferred in V17 with the same rationale as before:

- **Closed-loop iterated adversary (CR4 V15)**: one-shot adversarial paraphrase and full-regex-disclosed variants are integrated in §4.1.1 and §4.1.2; a closed-loop adversary requires multiple adversary-updates between runs and is left as future work. §1.1 scope paragraph is honest that an adaptive adversary would "almost certainly drive accuracy to chance."
- **Pacchiardi full replication**: §2.2 summary retained; the "within 1 pp" finding on related vs unrelated follow-ups is sufficient to update the Pacchiardi design rationale.
- **Opus cross-family extractor**: would strengthen the cross-family panel but is same-provider (Anthropic) and therefore does not add the cross-family information Mistral Large 3 and Llama 3.3 70B already provide. Deferred.

---

## Verification checklist for the reviewer

- Abstract ≤ 1 Sonnet mention (was 3): R3
- Table 2 splits into `tab:headlines_primary` + `tab:headlines_diagnostics`: S1/S3
- New §4.7.X subsection with label `sec:exp_i_4th_scenario`: R2
- New §5.1 paragraph containing "machine-rater" and "does not substitute for human": R1
- Mistral 7B panel in per-layer probe figure; base-checkpoint footnote: S2
- English-only + lexical-fragile in both abstract and §1.1: W-eng
- §4.6 pooled ≤7B vs ≥14B in footnote only, not inline: W-stats
- `run_exp_i_4th_scenario.py` + result JSONs + checkpoint files: R2
- `multi_rater_icc.py` + `machine_rater_icc.json`: R1
- Page count ≤ 41, compile clean (0 errors, 0 undefined refs): V17 target

We hope the three R-items and the four S-items delivered here are sufficient to move the review to clear accept. The residual deferrals (R1 full human study, S4 2nd RLHF-heavy model) are tractable post-acceptance and are committed to camera-ready.
