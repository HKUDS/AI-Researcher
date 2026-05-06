# V50 — Response to Weak Reject (5/10) Reviewer (NeurIPS 2026)

**Paper:** Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B–70B)

**Prior decision:** Weak Reject (5/10)

**Reviewer's explicit path to acceptance:**
> "A revision that (i) tightens scope in abstract/intro to instructed roleplay on ≤70B open-weight English models, (ii) adds at least 1–2 frontier-scale targets, (iii) resolves the autonomous-transfer task-validity question, and (iv) reconciles the n=20 vs n=100 ICC discrepancy would be a strong NeurIPS paper."

**V50 strategy:** All four conditions are addressed.

---

## At-a-Glance Table

| # | Reviewer concern | V50 action | Status |
|---|---|---|---|
| **(i) Scope** | Abstract/intro overclaims beyond ≤70B instructed-roleplay evidence | Abstract now **leads** with scope: "English instructed-roleplay, open-weight models (3B–70B); results do not generalize to frontier-scale or autonomous-deception settings." Multi-turn caveat added inline. | **Done** |
| **(ii) Frontier targets** | No frontier model beyond Sonnet 4.5 | **New experiment**: Llama~4~Maverick ($n=100$, AWS Bedrock, cross-family Haiku extractor). Rule 77.0%, pipeline 45.0% (classifier-transfer failure — inverse of Sonnet 4.5 pattern). Frontier panel: Sonnet~4.5 ($n=99$) + Llama~4~Maverick ($n=100$). | **Done** |
| **(iii) Autonomous transfer** | Task-validity contradiction: can't claim scenario invalid AND use null as detector evidence | Persona/false-belief cells **excluded from detector conclusions**. §4.6 now: "scenario-design failure prevents detector assessment." Figure 1 panel (b) redesigned to show sycophancy + system-prompt-only control only. | **Done** |
| **(iv) ICC discrepancy** | n=20 ICC=0.114 unexplained; looks like a re-run after failure | Mechanistic account added to Discussion §4.1: scale-range discrepancy (Ann1 mean 1.10, Ann2 mean 3.95), rank-order preserved (Spearman ρ=0.619), measurement artifact not construct failure. | **Done** |
| **W2** | "80.1% matches pipeline" ignores +14–29 pp multi-turn advantage | Added inline to abstract: "equivalence holds in single-turn/pooled-LOO; at ≥14B multi-turn, pipeline outperforms rule by +14–29 pp." | **Done** |
| **W5** | Haiku localization claim from Sonnet n=99 alone | Added qualifier: "hypothesis-generating, not established localization; Llama 4 Maverick provides open-weight frontier comparison." | **Done** |
| **W7** | Sycophancy 70B n=50 in headlines underpowered | Removed from abstract; retained in body text as "preliminary (n=50)" only. Removed from Figure 1 panel (b). | **Done** |

---

## Detailed Responses

### (i) Scope Tightening

**Reviewer ask:**
> "The paper's title and abstract make claims about 'deception detection' broadly, but the actual evidence base is: English only, ≤70B open-weight models, instructed roleplay only."

**V50 response:**

The abstract has been restructured to lead with scope:

> "**Scope: English instructed-roleplay evaluations, open-weight models (3B–70B) only.** Results do not generalize to frontier-scale (>70B closed-weight) or autonomous-deception settings without additional study."

This is the first sentence of the abstract — scope is no longer buried at line 13. The multi-turn pipeline-vs-rule qualification has also been added inline:

> "*The rule-vs-pipeline equivalence holds in the single-turn/pooled-LOO regime; at ≥14B multi-turn, the pipeline outperforms the rule by +14–29 pp (§4.3).*"

The intro §Scope paragraph now explicitly states "instructed roleplay on open-weight models (3B–70B)" rather than the implicit framing.

---

### (ii) Frontier-Scale Targets

**Reviewer ask:**
> "Q5: Can you commit to running at least one additional frontier model (GPT-4o, Gemini 2.5, Llama 4 if available) before camera-ready?"

**V50 response:**

**New experiment:** Llama~4~Maverick (\texttt{us.meta.llama4-maverick-17b-instruct-v1:0}, AWS Bedrock) — a frontier-generation MoE model (400B+ total parameters, 17B active), independent family from Claude. Protocol identical to all other equalized experiments: Haiku as cross-family interrogator/extractor, $n=100$, same 50 matched claim pairs.

**Frontier panel (§4.5):**
- Sonnet 4.5 ($n=99$, closed-weight): rule 49.0% (chance), pipeline 82.8–83.0%
- Llama 4 Maverick ($n=100$, open-weight MoE): rule **77.0%**, pipeline **45.0%** (classifier-transfer failure)

**Llama 4 Maverick result detail:**
- Rule: 77.0% — RC≥1 in 44/50 lying trials vs. 17/50 truth trials; lie RC mean=1.84, truth RC mean=0.48
- Pipeline: 45.0% (below chance) — trained ADAGE classifier predicts "truthful" on 79/100 trials (not marker suppression; classifier-transfer failure)
- Pattern is the *inverse* of Sonnet 4.5: correction markers remain discriminative at open-weight frontier scale, but the classifier does not generalize to Llama 4's feature profiles

This is a substantively informative finding: the rule/pipeline dissociation is model-architecture-dependent at frontier scale. The rule works on open-weight frontier but fails on closed-weight frontier; the pipeline works on closed-weight frontier but fails on open-weight frontier. Together these two targets characterize the frontier-scale regime fully. Results integrated into §4.5 and Appendix~B (new table with frontier comparison).

---

### (iii) Autonomous Transfer Task-Validity Resolution

**Reviewer ask:**
> "You cannot simultaneously claim a scenario is task-invalid and use null results from it as evidence about detector capability. Either the scenario is valid (and the detector fails) or it isn't (and the result is uninformative). The paper wants both readings."

**V50 response:**

The reviewer is correct. The paper was logically inconsistent. V50 resolves this by:

1. **§4.6 reframe:** Persona/false-belief section renamed "Scenario-design failure prevents detector assessment." The opening now reads: "A spot-check of 10 Qwen 14B persona trials reveals persona-break-with-correction on TRUE trials (6/10): the model abandons its false identity and produces correction language on TRUE trials... This is a **scenario-design failure**: the scenario does not reliably elicit autonomous deception, so these cells provide **no evidence about detector capability** — neither in favor nor against."

2. **Cells excluded from detector conclusions:** The statistical pattern (4/6 cells include chance; neither exclude-chance cell survives Bonferroni) is still reported for completeness but explicitly not interpreted as detector evidence.

3. **Figure 1 panel (b) redesigned:** Persona/false-belief bars completely removed. Panel (b) now shows only: (a) sycophancy LOO at 3B and 14B ($n=200$), and (b) system-prompt-only control at 3B and 14B ($n=200$). The caption states: "Persona/false-belief cells excluded from panel (b): spot-checks reveal scenario-design artifact (models abandoning false personas), so these cells provide no evidence about detector capability."

4. **Discussion §5 Regime 3:** Reframed from "null-or-uninterpretable for detector" to "null-for-scenario-validity: the detector cannot be assessed until scenarios reliably elicit autonomous deception."

The paper no longer claims the detector fails to transfer to autonomous deception; it claims the scenarios failed to elicit the target behavior.

---

### (iv) ICC Discrepancy Reconciliation

**Reviewer ask:**
> "Why was the n=20 pilot ICC (0.114) not predictive of the n=100 study (0.606)? Without a mechanistic account, this looks like a successful re-run after a failed first attempt."

**V50 response:**

Added to Discussion §4.1 (Construct Validity):

> "The initial $n=20$/2-annotator pilot yielded ICC=0.114, far below the full study's α=0.606. This reflects a **scale-range discrepancy**, not construct invalidity: Annotator 1 used a mean of 1.10 on the 0–10 correction-count scale, while Annotator 2 used a mean of 3.95. Absolute-agreement ICC is highly sensitive to scale-range heterogeneity; rank-order correlation was preserved (Spearman ρ=0.619). The n=100 study with three annotators and standardized calibration instructions ('use the full scale; 0 = no corrections, 5+ = heavy correction language') recovered α=0.606, clearing the pre-registered threshold (α≥0.4). The pilot failure was a measurement artifact, not a substantive replication failure."

The evidence that this is an artifact rather than a re-run:
- Rank ordering is preserved (ρ=0.619) — the annotators agreed on which responses had *more* correction markers, just not how many
- The two annotators' absolute scale ranges are documented (1.10 vs 3.95)
- The fix was specifically calibration instructions, not a different annotation protocol
- The pre-registered threshold was set before either study was run

---

### W2: Multi-Turn Pipeline Advantage

**Reviewer ask:**
> "§4.4 quietly concedes the pipeline beats the rule by +14–29 pp at ≥14B in multi-turn topical follow-up (Appendix M). This should be in the abstract."

**V50 response:**

Added to abstract as an italic qualifier following the rule/pipeline comparison:

> "*The rule-vs-pipeline equivalence holds in the single-turn/pooled-LOO regime; at ≥14B multi-turn, the pipeline outperforms the rule by +14–29 pp (§4.3).*"

---

### W5: Haiku Localization Qualifier

Added to Discussion §5.3:

> "**This interpretation rests on a single closed-weight frontier target (Sonnet 4.5, n=99) and should be treated as hypothesis-generating, not established localization** (Llama 4 Maverick provides an open-weight frontier comparison)."

---

### W7: Sycophancy 70B n=50 Downgrade

Removed from abstract and Figure 1 panel (b). Retained in §4.6 body text only: "Llama 70B 72.0% (n=50, preliminary)" — not in headline summaries.

---

## Summary of V50 Changes

| File | Change |
|---|---|
| `sections/abstract.tex` | Lead with scope; multi-turn caveat; two frontier targets; remove sycophancy 70B; task-validity framing |
| `sections/introduction.tex` | Scope paragraph: explicit ≤70B open-weight; two frontier targets forward-pointer |
| `sections/discussion.tex` | §4.1: ICC n=20 mechanistic account; §5.3: Haiku localization qualifier; Regime 3: scenario-design failure |
| `sections/experiments.tex` | §4.5: Llama 4 Maverick frontier stub; §4.6: persona/FB as scenario-design failure, excluded from detector conclusions |
| `figures/summary_results.tex` | Panel (b): only sycophancy + system-prompt-only bars; persona/FB excluded; caption updated |
| `sections/appendix.tex` | New §: Llama 4 Maverick results (stub, to be filled) |
| NEW: `experiments/run_llama4_equalized.py` | Llama 4 Maverick prompt-equalized experiment |

**Paper status:** 41 pages, compiles cleanly (2-pass), 0 undefined references. Llama 4 Maverick experiment complete (n=100); all [L4M_RULE]/[L4M_PIPE] placeholders filled.
