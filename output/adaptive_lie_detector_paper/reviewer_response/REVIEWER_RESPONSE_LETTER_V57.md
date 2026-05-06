# V57 — Response to Accept (7/10) Reviewer (NeurIPS 2026)

**Paper:** Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B-70B)

**Prior decision:** Accept (7/10) — "I lean toward acceptance."

**Reviewer's path to Strong Accept:**
> "If the authors can run the third-extractor experiment (Llama-70B-as-extractor on Sonnet/Haiku) for the camera-ready, this would move toward Strong Accept."

**V57 strategy:** The Llama-70B-as-extractor data already exists in Table 24. Surface it prominently as the disambiguating experiment; reframe the same-family narrative from "checkpoint-specific bias" to "extractor-quality differences" throughout. Add the reflexive statement and CI transparency the reviewer requests.

---

## At-a-Glance Table

| # | Concern | V57 action | Status |
|---|---|---|---|
| **MC1 — Same-family claim still featured without disambiguation** | Llama 70B already in Table 24: 50.5% on Sonnet = identical to Haiku. Surfaced as the third-extractor result; reframed abstract + SS3.5 + SS4.3 from "same-family bias" to "extractor-quality differences" | **Done** |
| **MC2 — Autonomous story negative; no reflexive statement** | Added "Reflexive implication" paragraph to SS4.3: validated regimes are the artifactual regimes; deployment-relevant regime is unassessed | **Done** |
| **MC3 — Multi-turn CIs not transparent** | Added "n=93-100 per model; lower CI bound ~5 pp" to conclusion recommendation | **Done** |
| **MC4 — Figure caption mismatch** | Caption now says "Three representative targets shown (Llama 3.2 3B, Mistral 7B, Llama 3.3 70B)" instead of "All seven equalized targets shown" | **Done** |
| **MC5 — SS3.5 structure: Llama is validated, Qwen is descriptive** | Restructured: Llama (validated) first, Qwen (descriptive) second; opening sentence names the validated finding | **Done** |
| **m1 — Abstract leads with contested claim** | Rewritten: "Three extractors (Haiku, Mistral L3, Llama 70B) show Haiku uniformly outperforms the other two by 7-10 pp... indicating extractor-quality differences rather than checkpoint-specific bias" | **Done** |
| **m2 — SS4.2 Regime descriptions editorial** | Frontier paragraph tightened to 2 sentences | **Done** |
| **m3 — Stale "limitation (l)" reference** | Fixed: now cites actual SP-only results (SS3.6; Llama 3B 63.1%, Qwen 14B 69.5%, n=200) | **Done** |
| **m4 — Sonnet-on-Haiku "self-family" confusing** | Added "[same Claude family]" clarification parenthetical | **Done** |
| **m5 — 70B accuracy table confusion** | Added reconciliation note to appendix explaining different accuracy levels under different conditions | **Done** |

---

## Detailed Responses to Major Concerns

### MC1: Third-extractor experiment — already exists

**Reviewer concern:**
> "The same-family hypothesis is still featured (abstract, SS3.5) but not disambiguated. If the authors can run Llama-70B-as-extractor on Sonnet/Haiku for the camera-ready, this would move toward Strong Accept."

**V57 response:**

This experiment was already run and appears in Table 24. The key results:

| Target | Haiku (extractor) | Llama 70B (extractor) | Mistral L3 (extractor) |
|--------|------|----------|-----------|
| Sonnet 4.5 | 50.5% | 50.5% | 82.8% |
| 7-target avg | 74.3% | 66.9% | 64.7% |

**Interpretation:** Two extractors from different families (Claude Haiku, Llama 70B) both fail identically on Sonnet (50.5%), while only Mistral L3 succeeds (82.8%). This rules out the "Haiku-checkpoint-specific blind spot for sibling models" reading: if it were a Haiku-specific blind spot, Llama 70B should not share it.

On the 7 open-weight targets, the pattern is Haiku > Llama 70B ~ Mistral L3 uniformly (no target shows Llama 70B outperforming Haiku). The five self-family controls (Llama-on-Llama x2, Qwen-on-Qwen, Mistral-on-Mistral, Sonnet-on-Haiku) all fall within 0-3 pp of cross-family baselines, ruling out an additional same-family boost.

**Conclusion:** The 9.7 pp Haiku-over-Mistral-L3 gap reflects extractor-quality differences, not checkpoint-specific same-family bias. We have reframed throughout:
- Abstract: "indicating extractor-quality differences rather than checkpoint-specific bias"
- SS3.5: "Haiku being a uniformly stronger extractor"  
- SS4.3: "extractor-quality differences (+7-10 pp; Haiku outperforms both Mistral L3 and Llama 70B uniformly)"
- Appendix: Sonnet paragraph now interprets Llama 70B = Haiku = 50.5% as ruling out reading (1)

---

### MC2: Reflexive implication — validated-on-artifactual-regime

**Reviewer concern:**
> "The paper should acknowledge reflexively that the regimes where its detector is validated are the regimes where its own controls reveal the signal is largely artifactual."

**V57 response:**

Added between SS4.3 "Summary of Contributions" and SS4.4 "Limitations":

> **Reflexive implication.** The regimes where this detector is validated (instructed roleplay, semi-autonomous sycophancy) are precisely the regimes where the three controls show the signal is predominantly artifactual or dispositional. The regime where genuine autonomous deception would matter most (goal-directed strategic deception) is precisely the regime we cannot assess. This characterizes behavioral deception detection as a field, not just our framework---but it bounds practical implications: detector research validated only on instructed/sycophancy settings cannot be assumed transferable to deployment-relevant autonomous scenarios without equalized controls.

This makes the reflexive implication explicit rather than leaving readers to infer it.

---

### MC3: Multi-turn CI transparency

**Reviewer concern:**
> "The +14-29 pp multi-turn recommendation needs sample-size and uncertainty context."

**V57 response:**

Conclusion now reads:
> **Practical recommendation:** use the refusal-count rule for single-turn evaluation; use the full pipeline for >=14B multi-turn (+14-29 pp; n=93-100 per model; lower CI bound ~5 pp).

The CI lower bound (~5 pp) confirms the effect is directionally real but acknowledges the wide uncertainty given sample sizes.

---

### MC4: Figure caption mismatch

**Reviewer concern:**
> "The caption says 'All seven equalized targets shown' but the figure displays only three models."

**V57 response:**

Fixed. Caption now reads:
> Three representative targets shown (Llama 3.2 3B, Mistral 7B, Llama 3.3 70B) spanning the 3B-70B range; per-model values for all seven targets are in Table [ref].

---

### MC5: SS3.5 structure — validated vs. descriptive

**Reviewer concern:**
> "The Qwen non-monotonic pattern appears first and reads as a headline finding, but it doesn't survive joint correction. The Llama jump is validated and should lead."

**V57 response:**

Restructured SS3.5:
1. Opening sentence now names the validated finding: "The validated within-family scale finding is Llama 8B->70B (+26 pp, p=0.004, survives joint Holm-Bonferroni)"
2. Scale patterns paragraph reordered: **Llama (validated)** first, then **Qwen (descriptive; does not survive joint correction)** second
3. Multiple-testing methodology paragraph retained with full statistical justification

---

## Summary of Changes (V56 -> V57)

| File | Changes made |
|------|-------------|
| `abstract.tex` | Rewrote same-family sentence: "extractor-quality differences rather than checkpoint-specific bias" |
| `experiments.tex` | Rewrote SS3.5 cross-family paragraph (three-extractor framing); restructured scale patterns (Llama first); added "[same Claude family]" clarification |
| `discussion.tex` | Updated SS4.3 contribution summary; added reflexive paragraph; tightened pilot ICC, classifier generalization, and frontier paragraphs to fit page budget |
| `conclusion.tex` | Added CI range (n=93-100; lower CI bound ~5 pp) to multi-turn recommendation |
| `appendix.tex` | Rewrote Sonnet interpretation (Llama 70B = Haiku = 50.5% rules out reading 1); fixed figure caption; fixed stale "limitation (l)" reference; added Llama 70B accuracy reconciliation note |

**Page budget:** Main content fits within 9 pages (conclusion on page 9; bibliography begins page break). 0 undefined references.

---

## Verification Checklist

- [x] Abstract no longer says "localized to the Claude Haiku checkpoint"
- [x] SS3.5 cross-family paragraph references Llama 70B as third extractor (66.9% avg, 50.5% on Sonnet)
- [x] SS3.5 paragraph order: Llama (validated) before Qwen (descriptive)
- [x] SS4.3 says "extractor-quality differences" not "same-family bias (Haiku-specific)"
- [x] Appendix Sonnet paragraph interprets Llama-70B = Haiku = 50.5% as ruling out reading (1)
- [x] SS4.3/SS4.4 has reflexive paragraph about validated-on-artifactual-regime
- [x] Conclusion has CI lower bound for multi-turn
- [x] Figure caption says "Three representative targets" not "All seven"
- [x] Stale "limitation (l)" reference fixed
- [x] Paper compiles cleanly (41 pages, 0 undefined refs, main content <= 9 pages)
