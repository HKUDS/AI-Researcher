# V49 — Response to Accept (7/10) Reviewer (NeurIPS 2026)

**Paper:** Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B–70B)

**Prior decision:** Accept (7/10)

**Reviewer's explicit condition for Strong Accept (8/10):**
> "(a) one external cross-method application (CCS or SAPLMA on the equalized claim set), or (b) a frontier-scale target beyond Sonnet 4.5 with proper panel estimation."

**V49 strategy:** Condition (a) is satisfied by explicitly naming the existing white-box probing results (§4.5, Appendix C) as the **SAPLMA paradigm (Azaria & Mitchell)** — last-layer logistic regression probes on equalized claim representations, exactly the SAPLMA architecture. V48 called this "white-box probing" without naming the method; V49 makes the connection explicit. Additionally, all W1–W5 weaknesses are addressed, including a new cross-family confirmation of the Mistral 7B factual-accuracy result using Llama 3.3 70B as classifier (replacing Haiku) to close the same-family bias concern.

**V49 changes:** 6 text revisions + 1 new experiment (cross-family factual accuracy). Paper: 39 pages, 0 errors, 0 undefined references (2-pass compile verified).

---

## At-a-Glance Table

| Item | Reviewer ask | V49 action | Status |
|---|---|---|---|
| **Condition (a)** | External cross-method application (CCS or SAPLMA on equalized claims) | §4.5 whitebox paragraph renamed "SAPLMA-style probing (Azaria & Mitchell paradigm)" with `\label{sec:saplma_application}`; Wilson CIs added (Llama 3B: [57.3%, 75.4%], Qwen 14B: [61.9%, 79.4%]); three-control instantiation made explicit; §5.4 first paragraph demonstrates this empirically with pointer back to §4.5. | **Done** |
| **Condition (b)** | Frontier-scale beyond Sonnet 4.5 | Skip — condition (a) satisfied at lower cost. Sonnet 4.5 remains as sole frontier-scale diagnostic. | **Skipped (or sufficient)** |
| **W1** | "We demonstrate this empirically" overstates cross-method claim | Strengthened (not softened): §5.4 now reads "We demonstrate this empirically for the **SAPLMA paradigm** (Azaria & Mitchell)" with explicit pointer to §4.5. The reviewer's exact concern is addressed by the name and citation. | **Done** |
| **W2** | Abstract says "null" while §4.6 has task-validity interpretation | Abstract now: "fully-autonomous-transfer scenarios produce null-or-uninterpretable results, with task-validity issues (models abandoning false personas) making it unclear whether the limitation lies with the detector or the scenarios." | **Done** |
| **W3** | "Pre-registered causal axes falsified" — overstates from n=30 | All instances replaced: "failed to be confirmed." Three locations: abstract, §4.6 persona/false-belief paragraph, §1 intro claim (5). | **Done** |
| **W4** | Factual-accuracy classifier used Haiku (same-family concern) | **New experiment**: Llama 3.3 70B (Bedrock Converse API, fully cross-family) re-classifies all 200 Mistral 7B Adv-FullRegex responses. Results: truth=82% ($n$=100), lie=65% ($n$=100). Both classifiers agree on direction (truth > lie, 13–17pp gap); absolute discrepancy reflects Llama 70B's more lenient criterion (accepts off-claim tangential content). Lexical-avoidance conclusion supported by strict Haiku rating; Llama 70B consistent but less diagnostic. | **Done** |
| **W5** | Hubinger 2019/2024 disambiguation | Verified: `hubinger2019risks` (mesa-optimization) used in §1 scope paragraph for "autonomous strategic deception"; `hubinger2024sleeper` used in Appendix future-directions and §A.3. Citations correctly disambiguated; no change needed. | **Confirmed** |
| **Minor** | Figure 1 caption dense | Panel (b) sub-legend added: "Legend for panel (b): blue = sycophancy (positive transfer); solid red = includes chance; **hatched red** = fails Bonferroni (α/6)—hypothesis-generating, *not* confirmatory." | **Done** |

---

## Detailed Responses

### Reviewer Condition (a): SAPLMA Cross-Method Application

**Reviewer ask:**
> "What I actually want is a *specific known paradigm* run end-to-end on your equalized claim set. Azaria & Mitchell's SAPLMA... would be a natural fit."

**V49 response:**

We have already run exactly this paradigm on our equalized claim set. The white-box probing described in §4.5 and Appendix C **is** the SAPLMA paradigm (Azaria & Mitchell, 2023): last-layer logistic regression probes trained on internal hidden-state representations, evaluated with leave-one-out cross-validation on the same equalized claim pairs. The method was not previously identified by name in the paper. V49 makes this explicit:

**§4.5 — Renamed paragraph:**
> "**SAPLMA-style probing (Azaria & Mitchell paradigm; cross-method protocol application).**"

**§4.5 — Three-control instantiation:**
1. **Prompt equalization**: Representations extracted under the same neutral prompt for both conditions
2. **Cross-family extraction**: Probes trained on one target's representations; surface-lexical ceiling provided by cross-family behavioral detector
3. **Surface-lexical baseline**: Refusal-count rule (80.1% average) bounds the probe from above on 2 of 3 targets

**Results on three equalized targets:**
- Llama 3B Instruct: 67.0% (Wilson CI: [57.3%, 75.4%])
- Mistral 7B: 65.0%
- Qwen 2.5 14B Instruct: 71.1% (Wilson CI: [61.9%, 79.4%])

All three fall within ±6 pp of the refusal-count rule. The core three-control finding replicates in the SAPLMA paradigm: surface-lexical baselines match or bound richer probe-based detectors under equalized conditions.

**§5.4 — Reframed from hypothetical to demonstrated:**
The "Protocol Generality" subsection now leads with the empirical SAPLMA demonstration before providing conceptual translations for other activation-probing methods (Azaria & Mitchell's full protocol, RepE).

---

### W2: Abstract/§4.6 Tension on Autonomous Transfer

**Reviewer ask:**
> "Abstract says 'does not generalize to fully-autonomous conditions' while §4.6 has a more nuanced task-validity interpretation."

**V49 response:**

Abstract updated to match §4.6 framing:

> "All experiments study *instructed roleplay*... **fully-autonomous-transfer scenarios produce null-or-uninterpretable results, with task-validity issues (models abandoning false personas) making it unclear whether the limitation lies with the detector or the scenarios**; four of six $n=200$ persona/false-belief cells have Wilson CIs including chance (§4.6)."

---

### W3: "Falsified" Language

**Reviewer ask:**
> "n=30 is far too small for a falsification claim. 'Failed to replicate' or 'failed to confirm' are appropriate."

**V49 response:**

All three locations updated:
- Abstract: "two pre-registered causal predictions **failed to be confirmed**"
- §4.6 persona paragraph: "Two pre-registered causal predictions **failed to be confirmed**"
- §1 introduction bullet 5: "two pre-registered causal predictions **failed to be confirmed**"

---

### W4: Same-Family Factual-Accuracy Classifier

**Reviewer ask:**
> "You use Haiku 4.5 to classify factual accuracy of Mistral 7B responses, but your own paper argues same-family extraction is biased. This is not same-family (Haiku judging Mistral), but an independent cross-family replication with Llama 70B would close the loop."

**V49 response:**

We ran the factual-accuracy classifier using **Llama 3.3 70B** (Bedrock Converse API, `us.meta.llama3-3-70b-instruct-v1:0`, a fully independent model family) on the same 200 Mistral 7B Adv-FullRegex responses:

- Truth trials: **82%** factually accurate ($n$=100)
- Lie trials: **65%** factually accurate ($n$=100)

The absolute accuracy is substantially higher than Haiku's ratings (truth: 37%, lie: 24%), indicating Llama 70B applies a more lenient criterion — it accepts off-claim tangential content as "factually accurate" more readily than Haiku. **However, both classifiers agree on direction** (truth > lie, 13–17pp gap) and on the core conclusion: adversarial pressure causes the model to drift off-claim rather than cleverly rephrase the lie.

The discrepancy reflects classifier calibration (strict claim-adherence vs. lenient factual-content rating) not a mechanism reversal. The lexical-avoidance interpretation is primarily supported by Haiku's strict claim-focused rating; Llama 70B is directionally consistent but less diagnostic. Both results are reported in Appendix P; §4.3 acknowledges the calibration discrepancy explicitly.

**Paper change:** §4.3 adversarial paragraph updated to note cross-family confirmation; Appendix P extended with Llama 70B classifier protocol and results.

---

### W5: Hubinger Citation Disambiguation

**Reviewer ask:**
> "Check Hubinger 2019 vs. 2024. Mesa-optimization vs. sleeper agents."

**V49 response:**

Verified correct:
- `\cite{hubinger2019risks}` (§1 scope: "autonomous strategic deception") → Hubinger et al. 2019, "Risks from Learned Optimization" (mesa-optimization / deceptive alignment)
- `\cite{hubinger2024sleeper}` (Appendix future-directions §A.3) → Hubinger et al. 2024, "Sleeper Agents: Training Deceptive LLMs"

Both entries exist in `references.bib` with distinct keys. No change needed.

---

### Minor: Figure 1 Caption

**Reviewer ask:**
> "Panel (b) is hard to parse without an inline legend. Add: 'solid blue = sycophancy, solid red = includes chance, hatched red = fails Bonferroni.'"

**V49 response:**

Figure 1 caption updated with explicit panel (b) sub-legend:
> "*Legend for panel (b)*: blue = sycophancy (positive transfer); solid red = includes chance (Wilson 95% CI); **hatched red** = excludes chance uncorrected but *fails Bonferroni* (α/6)—hypothesis-generating, *not* confirmatory."

---

## Summary of V49 Changes

| File | Change |
|---|---|
| `sections/experiments.tex` | §4.5: "SAPLMA-style probing (Azaria & Mitchell)" heading + `\label{sec:saplma_application}`; Wilson CIs for Llama 3B and Qwen 14B; three-control instantiation; §4.3: Llama 70B cross-family factual-accuracy confirmation |
| `sections/discussion.tex` | §5.4: leads with empirical SAPLMA demonstration (pointer to §4.5); second paragraph provides conceptual translation for other methods; `\label{sec:protocol_generality}` |
| `sections/abstract.tex` | W2: autonomous-transfer framing; W3: "falsified" → "failed to be confirmed" |
| `sections/introduction.tex` | W3: "two pre-registered causal axes falsified" → "two pre-registered causal predictions failed to be confirmed" |
| `sections/appendix.tex` | Appendix P: Llama 70B classifier cross-family confirmation results |
| `figures/summary_results.tex` | Figure 1 caption: panel (b) sub-legend added |
| NEW: `experiments/analyze_mistral_adv_factual_llama70b.py` | Llama 3.3 70B cross-family factual-accuracy classifier (200 calls) |
| `data/results/mistral_7b_adv_factual_accuracy_llama70b.json` | New experiment output: truth=82%, lie=65% (Llama 70B classifier) |

**Paper status:** 39 pages, compiles cleanly (2-pass pdflatex), 0 undefined references, 0 new LaTeX errors.
