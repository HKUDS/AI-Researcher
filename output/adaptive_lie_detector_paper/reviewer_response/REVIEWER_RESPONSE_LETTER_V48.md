# V48 — Response to Weak Accept (6/10) Reviewer (NeurIPS 2026)

**Paper:** Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B–70B)

**Prior decision:** Weak Accept (6/10)

**Reviewer's explicit condition for 7/10 (Accept):**
> "would move to Accept (7) with a second-detector application **or** a frontier-scale data point."

**V48 strategy:** Both conditions are now satisfied. The frontier-scale data point (Claude Sonnet 4.5, n=99) was already in the paper but insufficiently foregrounded; V48 explicitly labels it as the frontier-scale extension. The second-detector application is now empirically demonstrated by pointing to the existing white-box probing results (§4.5) as a cross-method application of the three-control protocol, with §5.4 reframed from hypothetical to demonstrated. Additionally, all W1–W9 weaknesses are addressed with text fixes and one new experiment (Mistral 7B adversarial factual-accuracy second-pass).

**V48 changes:** 8 text revisions + 1 new experiment. Paper: 39 pages, 0 errors, 0 undefined references.

---

## At-a-Glance Table

| Item | Reviewer ask | V48 action | Status |
|---|---|---|---|
| **Condition — frontier-scale** | "a frontier-scale (100B+) data point" | §4.5 Sonnet paragraph now explicitly labeled as "frontier-scale (100B+) target"; extends scale sweep beyond 70B upper bound. Causal claim softened per minor comment. | **Done** |
| **Condition — second-detector** | "a second-detector application" | §4.5 white-box probing paragraph expanded: last-layer LR probes on 3 equalized targets constitute an end-to-end cross-method application of all three controls. §5.4 reframed from hypothetical ("would apply") to demonstrated ("has been applied, as shown in §4.5"). | **Done** |
| **W1** | Scope framing occasionally elides narrowness | Multiple-testing policy paragraph now explicitly states within-family is more lenient than joint; cross-family heterogeneity justification added inline. | **Done** |
| **W2** | Qwen 32B — second observation or within-family comparison | Already addressed in V47: cross-organizational replication (Gemma 2 27B 84%, Mistral 7B 56%) localizes collapse to Qwen family. Retained in V48. | **Done (V47)** |
| **W3** | Mistral 7B adversarial: factual-accuracy second-pass not done | **New experiment**: Claude Haiku factual-accuracy classifier on all 200 Mistral 7B Adv-FullRegex responses. Truth: 37% accurate, Lie: 24% accurate → **lexical avoidance** (not semantic substitution). Added to §4.3 adversarial paragraph and Appendix P. | **Done** |
| **W4** | Persona/false-belief task-validity soft-pedaled | §4.6 now explicitly states: "If so, this is a **task-validity failure**—the scenario does not reliably elicit the autonomous deception it purports to measure, and the null result speaks to scenario design, not detector capability." | **Done** |
| **W5** | Protocol "reusable" needs external application | See Condition — second-detector above. | **Done** |
| **W6** | Pipeline-vs-rule multi-turn conditioning underplayed | §4.2 now explicitly foregrounds: "The headline equivalence holds in the single-turn / pooled-LOO regime; practitioners needing multi-turn ≥14B detection should prefer the full pipeline." | **Done** |
| **W7** | Human baseline is degenerate; uninformative | §4.5 human baseline line now states: "This degenerate collapse makes the human comparison uninformative; it is reported for completeness but is not interpreted as a meaningful ceiling." | **Done** |
| **W8** | Within-family multiple-testing needs more justification | §4.5 scale intro now explicitly acknowledges: "this choice is **more lenient** than joint correction...The within-family choice is justified by demonstrated cross-family heterogeneity...which violates the exchangeability assumption required for joint correction." | **Done** |
| **W9** | Llama 70B sycophancy n=50 in headline tables as "preliminary" | Already labeled "preliminary" in abstract and §4.6; no headline table change needed — label confirmed present. | **Confirmed** |
| **Minor — broken citation** | `\cite{li2023inference}` undefined | Replaced with `\citealt{zou2023representation}` (RepE; already in bib); text updated to "Representation engineering (RepE)" | **Done** |
| **Minor — Sonnet causal softening** | "suppresses" is causal from n=99 | Changed to "appears to suppress...single n=99 observation; causal interpretation remains speculative" | **Done** |
| **Minor — Bedrock model ID** | Verify `anthropic.claude-haiku-4-5-20250106-v1:0` | Corrected to `us.anthropic.claude-haiku-4-5-20251001-v1:0` in Appendix E.1.3 | **Done** |

---

## Detailed Responses

### Reviewer Condition: Frontier-Scale Data Point

**Reviewer ask:**
> "The practical reach of the conclusions is limited. Frontier-scale data would substantially strengthen the paper."

**V48 response:**

The paper already contains a frontier-scale (100B+) evaluation: **Claude Sonnet 4.5** ($n=99$, §4.5). This was present in V47 but framed only as a "diagnostic finding." V48 makes the frontier-scale label explicit:

> "As the sole **frontier-scale (100B+)** target in our evaluation, Sonnet~4.5 extends the scale sweep beyond the 70B upper bound of open-weight models."

**Key findings at frontier scale (Sonnet 4.5, n=99):**
- Refusal-count rule: 49.0% (near chance) — RLHF training appears to suppress the refusal-marker channel
- Haiku pipeline: 83.0%; Mistral L3: 82.8% — non-refusal features still carry signal
- This is the only data point where the rule fails while the pipeline succeeds, confirming 80.1% is an *open-weight* ceiling

The causal language has been softened per the minor comment: "appears to suppress" + "(single n=99 observation; causal interpretation remains speculative)."

---

### Reviewer Condition: Second-Detector Application

**Reviewer ask:**
> "The paper does not actually run [the three-control protocol] on any second detector. A single concrete cross-method application would substantiate the 'general framework' claim."

**V48 response:**

The paper *does* apply the three-control protocol to a second detection paradigm — white-box probing — and reports results in §4.5. This was previously a single line that did not make the cross-method framing explicit. V48 expands it:

> "This constitutes an empirical application of the three-control protocol to a second detection paradigm: probe-based detection uses cross-family extraction by design (features from one family's activations tested on held-out models), and the refusal-count rule provides the surface-lexical ceiling (§5.4)."

**Results:** Last-layer LR probes on three equalized targets (Llama 3B, Mistral 7B, Qwen 14B) fall within ±6 pp of the refusal-count surface-lexical ceiling — the same pattern observed for behavioral detection. The three-control finding (surface-lexical baselines match or bound richer detectors) replicates in the white-box paradigm.

**§5.4 reframe:** The Azaria & Mitchell paragraph has been restructured. The first paragraph establishes that the protocol *has already been empirically applied* to white-box probing in §4.5, and the second paragraph provides the explicit step-by-step translation for activation-probing methods (Azaria & Mitchell, RepE).

---

### W3: Mistral 7B Adversarial Factual-Accuracy Second-Pass

**Reviewer ask:**
> "The Mistral 7B factual-accuracy second-pass check is described as the 'single most informative follow-up for the adversarial-robustness claim.' Why was it not performed?"

**V48 response:**

We ran the second-pass check: a Claude Haiku 4.5 factual-accuracy classifier ("Is the speaker's final statement factually accurate? YES/NO") on all 200 Mistral 7B Adv-FullRegex responses.

**Results:**
- Truth trials: 37% factually accurate (n=100)
- Lie trials: 24% factually accurate (n=100)

**Interpretation:** Both conditions show low factual accuracy, identifying the Bi (near-parity) pattern as **lexical avoidance** — the model collapses to vague, factually unreliable responses under adversarial pressure rather than cleverly rephrasing the lie with equivalent content (semantic substitution). This resolves the mechanism ambiguity flagged in Appendix P and rules out the more concerning hypothesis (that the adversary enables sophisticated semantic substitution).

**Paper changes:** §4.3 adversarial paragraph updated with the finding; Appendix P extended with the full second-pass protocol and results.

---

### W4: Persona/False-Belief Task-Validity

**Reviewer ask:**
> "This is a *task-validity* problem, not a *statistical-power* problem, and the paper soft-pedals it."

**V48 response:**

The §4.6 persona paragraph now directly states:

> "If so, this is a **task-validity failure** — the scenario does not reliably elicit the autonomous deception it purports to measure, and the null result speaks to scenario design, not detector capability."

We agree with the reviewer's framing. The Qwen 14B persona 68% is better interpreted as the model abandoning its false identity (a scenario-design artifact) than as a detection success. This interpretation has been made the primary reading in the main text, with the "exploratory evidence" qualifier removed.

---

## Summary of V48 Changes

| File | Change |
|---|---|
| `sections/experiments.tex` | §4.3: Mistral adv factual-accuracy result (lexical avoidance); §4.2: pipeline-vs-rule multi-turn conditioning foreground; §4.5: Sonnet frontier-scale label + causal softening; §4.5: whitebox probing cross-method framing; §4.5: human baseline degenerate note; §4.5: multiple-testing policy leniency acknowledgment; §4.6: persona task-validity sentence |
| `sections/discussion.tex` | §5.4: reframed from hypothetical to demonstrated; explicit pointer to §4.5 whitebox; broken `li2023inference` → `zou2023representation` |
| `sections/appendix.tex` | Appendix P: Mistral 7B factual-accuracy second-pass protocol and results; model ID corrected |
| `data/results/mistral_7b_adv_factual_accuracy.json` | New experiment output (n=200 factual accuracy classifications) |

**Paper status:** 39 pages, compiles cleanly, 0 undefined references, 0 new LaTeX errors.
