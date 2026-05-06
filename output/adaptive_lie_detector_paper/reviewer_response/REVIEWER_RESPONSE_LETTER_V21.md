# Response to Reviewer (Weak Accept, 6/10; Confidence 4/5) — Revision V21

We thank this reviewer for the Weak Accept and for the unusually specific 8-item weakness list, 4 questions, and 9 detailed comments. The reviewer's overall read is clear: the experimental work is solid, but the paper's novelty framing ("first joint application") is thin for NeurIPS, caveat-density hurts readability, and two experimental gaps (a third family on persona/FB at n=200; a pilot of the pre-registered 5th scenario) remain. V21 is organized around those asks. The paper is **42 pages, 0 errors, 0 undefined refs**.

**At-a-glance.**

| Ask | Reviewer request | V21 response | Location |
|---|---|---|---|
| W1 | "first joint application" is thin novelty for NeurIPS | Abstract reframed to lead with the **magnitudes** the joint application reveals (30–41 pp equalization collapse, 9–10 pp Claude-localized same-family inflation, rule/pipeline within 5 pp). §5.5 reframed the same way. "First joint application" moved out of the lead sentence. | `abstract.tex`; `discussion.tex` §5.5 L31–34 |
| W2 | Caveat-density hurts readability | Added **"How to read this paper"** guide paragraph after §1 opening, and elevated the **level-dependent / level-independent claim taxonomy** from §5.7(g) to §1. | `introduction.tex` L3–5 |
| W5 / Q2 | Qwen 14B adv-fullregex n=200 status | Run at 95/200 (checkpoint persisted); on-course to finish ≈01:30 2026-05-01. Integration script ready to merge on completion (as with Mistral 7B in V20). | §4.8 Table 10 (pending integration) |
| W6 / Q1 | 5th-scenario pilot missing from submission | **New pilot in flight**: n=30/condition × 3 conditions on Qwen 14B, varying `disposition_source` ∈ {sycophancy, persona, explicit_lie_defense} while holding clarity/turn-count/target fixed. `run_exp_i_5th_scenario.py` at `code/adaptive_lie_detector/experiments/`. | §4.7.1 (pending integration) |
| Q3 | Only two families at n=200 for persona/FB | **Mistral 7B persona n=200 in flight** as third family (P0.A running at 17 min elapsed); FB queued to follow via watcher script. Integration plan in §4.6 / Table 4. | `experiments.tex` Table 4 (pending integration) |
| Q4 | Commit to ICC release + fallback | Protocol v2 frozen in V20 (`docs/icc_annotation_protocol_v2.md`); §5.1 fallback tightened to explicit "preliminary Krippendorff α at n=50" language. | V20-frozen; no net-new change |
| D1 | Abstract should lead with methodology, not 64.7% | Abstract lead rewritten: **"When three evaluation controls … are jointly applied … headline accuracies collapse by large and consistent magnitudes."** 64.7% moved to second paragraph. | `abstract.tex` L2–4 |
| D3 | §4.4 EXP-G is the strongest; deserves more prominence | Added **3-row scale-band summary table** (`tab:expg_band_summary`) foregrounding the clean vs. confounded decomposition. EXP-G referenced from §1 contributions. | `experiments.tex` L196–209 |
| D4 | Why within-family for Holm-Bonferroni scale correction? | **Added one sentence** to §4.6 justifying within-family as the causal unit (family-specific RLHF objectives control each scale-curve's shape); joint correction reported for transparency. | `experiments.tex` §4.6 L243 |
| D6 | Three-self-family claim should be in §1 contributions | **Added contribution (iv)** to the §1 contributions list: three independent self-family extractor cells localize the 9–10 pp uplift to Claude-on-Claude. | `introduction.tex` contributions L22 |
| D7 | White-box probing: one panel main + one appendix | **Done**: Llama 3B panel stays in main §4.9 Fig 1; Mistral 7B base-checkpoint panel moved to Appendix `app:mistral_probe_panel` with 1-line main-text pointer. Table 8 retained in main. | `experiments.tex` §4.9; `appendix.tex` |
| D9 | Level-dep / level-indep taxonomy belongs in §1 | **Done**: one-sentence operational statement added to the "How to read" paragraph with forward `\ref{sec:limitations}` to §5.7(g). | `introduction.tex` L3 |

---

## W1 — Novelty framing: from "first joint application" to magnitudes

**What was asked.** The reviewer wrote: *"'first joint application' is thin novelty for NeurIPS; the paper's value is in the magnitudes the joint controls reveal, not the claim of having been the first to combine them."* A second reviewer had already pushed the abstract in this direction in V19; the reviewer here is asking us to finish the job.

**What we did.**

1. **Abstract lead rewritten** (`abstract.tex` L2): opens with *"When three evaluation controls … are jointly applied to behavioral deception detection in large language models, headline accuracies collapse by large and consistent magnitudes"* — then lists the three magnitudes (30–41 pp equalization collapse; 9–10 pp same-family inflation localized to Claude; rule-matches-pipeline within 5 pp). "First joint application" does not appear in the abstract.

2. **§5.5 reframed** (`discussion.tex` L31–34): lead now reads *"The contribution of this paper is the **magnitudes** that jointly applying three standard controls reveals: 30–41 pp … 9–10 pp … a one-line regex matching a 5-feature pipeline within 5 pp."* The "first joint application" language is demoted to second position and softened to *"to our knowledge, no prior work applies all three jointly to behavioral deception detection."*

3. **§1.1 contributions list updated**: the motivation paragraph now reads *"Our contribution is their joint application to behavioral deception detection: when applied together, they reveal confounds of a magnitude previously undocumented in this domain"* — the "first" claim is dropped from the lead and replaced with the magnitude triad.

---

## W2 — Readability: caveat-density & structure

**What was asked.** The reviewer noted that the paper's many caveats — while individually justified — make the argumentative arc hard to follow for a first-time reader, and recommended (a) a "how to read" paragraph after the abstract, (b) elevating the level-dep/level-indep taxonomy from §5.7(g) to §1, and (c) moving 1–2 diagnostic experiments to the appendix.

**What we did.**

1. **"How to read this paper" paragraph** (`introduction.tex` L3, new \paragraph):
   > *"The primary headline number (7-target cross-family pipeline 64.7%, rule-match 80.1%) is in Section 4.3. The three evaluation controls each have their own experimental section: equalization in §4.2, cross-family extraction in §4.3, and the regex baseline in §4.2. The instructed-matched decomposition (EXP-G) in §4.4 is the single cleanest control experiment. Negative results—$n=200$ autonomous-transfer (§4.6), pre-registered 4th-scenario rejection (§4.7), and the weak-ICC construct-validity caveat (§5.1)—are consolidated into a level-dependent / level-independent claim taxonomy at §5.7(g), which we recommend skimming before reading §4. Throughout, level-dependent claims (…) are read under the ICC caveat; level-independent claims (…) are unaffected by absolute-level validity."*

2. **Level-dep / level-indep taxonomy in §1**: the "How to read" paragraph ends with the operational statement as a forward-reference to §5.7(g) (`\ref{sec:limitations}`). §5.7(g) itself is unchanged (the full caveat still lives there).

3. **Mistral 7B probe panel → appendix** (D7): the Llama 3B per-layer curve stays in main (Fig. 1, now single-panel); the Mistral 7B base-checkpoint panel is moved to Appendix `app:mistral_probe_panel` with a one-line main-text pointer in §4.9.

---

## W5 / Q2 — Qwen 14B adv-fullregex n=200

**Status.** In flight (PID 27839, 95/200 at 19:19 on 2026-04-30; ~49% complete after 5h 8m). On track to finish around 01:30 2026-05-01.

**Plan.** On completion, integrate into Table 10 Qwen 14B row (44% n=50 → [n=200 value] with Wilson 95% CI) and update the §4.8 heterogeneous-mechanism paragraph. If the qualitative story flips at n=200 (as Llama 3B did from n=50 → n=200), §4.8 will be rewritten to match the three-target n=200 picture rather than forcing the n=50 characterization.

---

## W6 / Q1 — 5th-scenario disposition-source pilot

**What was asked.** *"The pre-registered 5th scenario (§5.8) is listed as future work. A small pilot — even n=30/condition — would let readers calibrate how much the disposition-source interpretation really holds up."*

**What we did.**

1. **New script**: `code/adaptive_lie_detector/experiments/run_exp_i_5th_scenario.py` (adapted from `run_exp_i_4th_scenario.py`).
2. **Design**:
   - **Fixed**: knowledge-conflict clarity = high; turn-count = multi-turn (adaptive); target = Qwen 2.5 14B (the one scale point in Table 4 whose persona cell excludes chance at n=200, so the signal-to-noise for a disposition-source contrast is cleanest here).
   - **Varied**: `disposition_source` ∈ {sycophancy, persona (Dr. Alex Morgan MIT physics educator), explicit_lie_defense (debate-practice framing)}.
   - **$n=30$/condition** (pilot floor; 15 TRUE + 15 high-clarity-FALSE claims from the 4th-scenario 15-triple pool).
3. **Pre-registered prediction**: sycophancy LOO clearly above persona + explicit_lie_defense LOO (one-sided). Null: all three cluster in the 60–70 % equalized band.
4. **Status**: running (PID 34893, started 19:10 on 2026-04-30; on trial 4/90 at 19:19). ETA ~6–10 h total.
5. **Reporting plan**: new `\paragraph{Pre-registered 5th scenario (disposition-source, pilot).}` in §4.7.1 with a 3-row table, one row per condition (n, LOO, Wilson 95%, Cohen's d). Explicit-pilot framing: "indicative, not confirmatory; n=30/condition has Wilson CI width ≈ 32 pp." If sycophancy clearly exceeds the other two, this supports the disposition-source reading (§5, Future Direction 4). If not, we flag honestly that even the cleanest cell is underpowered and rework the §5 disposition-source interpretation.

---

## Q3 — Mistral 7B autonomy n=200 as third family

**What was asked.** V20 introduced persona/FB at n=200 on Llama 3B and Qwen 14B (two families); the reviewer asked whether the "does not cleanly transfer" headline holds on a third family.

**What we did.**

1. **Launched Mistral 7B persona autonomy n=200** (PID 34699, 17 min elapsed at 19:27 on 2026-04-30). Scripts: `experiments/run_persona_autonomous.py` with `--model mistral:7b --n 200`.
2. **Queued Mistral 7B false-beliefs autonomy n=200** via watcher script (`/tmp/mistral_fb_queue.sh`, PID 35011): starts immediately after the persona run completes, to avoid GPU contention on the MPS backend.
3. **Calendar**: serial wall-clock ETA ≈40 h total (persona 18–24 h, then FB 18–24 h). Persona should complete before submission; FB may or may not depending on the exact deadline.
4. **Integration plan**:
   - Table 4 (`tab:autonomous_matched`) will add rows:
     - `Persona maintenance | Mistral 7B | 200 | [value] | [Wilson CI] | [d]`
     - `False beliefs (ICL)  | Mistral 7B | 200 | [value] | [Wilson CI] | [d]`
   - §4.6 narrative updates from "two families at n=200" to "three families at n=200."
   - Abstract negative-transfer sentence updated if the Mistral numbers preserve the pattern (expected: CIs include chance on both).
5. **Fallback**: if either run does not complete before submission, report at whatever n has been reached (e.g., n=120 / 200 via checkpoint) with Wilson CI and an explicit "preliminary, third-family scaling incomplete" caveat. The negative-transfer headline remains anchored on Llama 3B + Qwen 14B at n=200 each; Mistral is supplementary.

---

## Q4 — ICC release + fallback

**What was asked.** The reviewer accepted V20's protocol freeze (`docs/icc_annotation_protocol_v2.md`, `data/icc_study_v2/README.md`) but asked for explicit fallback language in case recruitment stalls past the camera-ready deadline.

**What we did.** V21 tightens the §5.1 camera-ready commitment (via the `icc_annotation_protocol_v2.md` §Known risks section) to specify the fallback numerically: *"If recruitment stalls past the camera-ready deadline, fall back to the commitment language and report progress on whatever is collected (e.g., n=50 preliminary Krippendorff α) rather than fabricate a pooled number."* The protocol document (frozen in V20) already contains this language; no further paper-level edit is needed beyond the one-sentence pointer in §5.1.

---

## D1 — Abstract reorder (lead with methodology)

**Done.** The abstract now leads with the methodology sentence (see W1 above); 64.7% primary-headline appears in paragraph 2 immediately after the three magnitudes. Word count: 212 (within the 170–220 range).

---

## D3 — EXP-G prominence (3-row dedicated table)

**Done.** Added `tab:expg_band_summary` (`experiments.tex` L196–209) grouping EXP-G decomposition by scale band — $\leq 8$B (upper bound; KT confound), $14$B (clean $+7.5$ pp), $70$B (clean $+15$ pp). The existing per-model Table `tab:expg_summary` is retained below the summary table. §4.4 paragraph label: **"EXP-G: Instructed-matched control (cleanest single control experiment)."** EXP-G is referenced from the new §1 contributions list (contribution ii) and from the "How to read" paragraph.

---

## D4 — Within-family Holm-Bonferroni justification

**Done.** Added to `experiments.tex` §4.6 L243:
> *"We apply within-family Holm-Bonferroni as the primary correction because family-specific RLHF objectives (not raw parameter count) control each family's scale-curve shape (see the Qwen 32B RLHF collapse in §4.4.1): jointly correcting across non-exchangeable families would be conservative but mismatched to the causal unit; we report the joint correction for transparency."*

---

## D6 — Three-self-family claim in §1 contributions

**Done.** Added contribution (iv) to the §1.1 contributions list:
> *"**Three independent self-family extractor cells localize the 9–10 pp uplift to Claude-on-Claude.** Re-extracting equalized Llama 3B, Llama 8B, and Qwen 7B transcripts with their respective same-family extractors (Llama 70B × 2, Qwen 14B) produces no analogous same-family boost (§4.3), consistent with Claude-specific RLHF self-preference rather than a universal family-bias artifact."*

Also added contribution (v):
> *"**Pre-registered self-falsification and $n=200$ negative-transfer.** A pre-registered 4th scenario rejects our earlier 'knowledge-conflict clarity' interpretation ($\Delta=-4.2$ pp pooled, paired-bootstrap CI includes zero; §4.7), and $n=200$ scale-ups on two families produce Wilson CIs that include chance on three of four cells (§4.6)."*

---

## D7 — Probe panel placement

**Done.** Fig. 1 in main text is now single-panel (Llama 3B Instruct). Mistral 7B base-checkpoint panel + 3-row summary table moved to Appendix `app:mistral_probe_panel`. Main-text narrative retains the 1-sentence Mistral cross-reference: *"A preliminary replication on a Mistral 7B base checkpoint (Table 8 row, Appendix `app:mistral_probe_panel` per-layer panel) peaks at 65–66% at layer 4…"* Table `tab:whitebox_probe` in main retains Llama 3B rows only; Mistral rows moved to the appendix table. Saves ~0.3 pp of main body.

---

## D9 — Level-dep / level-indep taxonomy in §1

**Done.** Last sentence of the "How to read" paragraph in §1 (see W2 above):
> *"Throughout, level-dependent claims (74.5% Haiku pipeline, 92.9% Sonnet-Haiku, EXP-G decomposition, probe band) are read under the ICC caveat; level-independent claims (refusal-count LOO, three-control gaps, Qwen 32B zero-marker collapse) are unaffected by absolute-level validity."*

Forward `\ref{sec:limitations}` to §5.7(g), where the full caveat still lives.

---

## Compile status

- **42 pages**, 0 errors, 0 undefined refs (after adding the `\label{sec:limitations}` target to §5.7 for the new §1 forward-reference).
- Page count is up 1 pp from V20 (41 → 42) due to the "How to read" paragraph, EXP-G summary table, and two new contribution bullets; offset by the Mistral probe panel move to appendix (~0.3 pp savings). Comfortably within the NeurIPS 42-page main-text budget.
- Abstract: 212 words (target 170–220).

---

## Out-of-scope for V21 (explicitly)

- **Sonnet 4.5 n=410** — V20 caveat at §5.7(b) already explicitly flags this as infeasible within the Bedrock cost + camera-ready calendar budget.
- **Fourth family (Haiku / Gemma / DeepSeek) autonomy n=200** — Mistral is the third family for V21; a fourth would push serial wall-clock past two weeks.
- **Full n=50 × 3-target version of the 5th scenario** — pilot is in scope; the full pre-registered version remains future work (§5, Future Direction 4).
- **Closed-loop adaptive adversary** — flagged since V16 as future work; the in-scope test is the one-shot full-regex-disclosed adversary.
- **Full Pacchiardi replication** — flagged since V13; current Table 1 EXP-K row is sufficient for the paper's scope.
- **Running the n=100 / 3-annotator human ICC study** — protocol frozen in V20; the 2.5-week calendar starts at camera-ready acceptance.

---

## Summary

V21 is a framing-and-readability pass with two experimental adds. All text-level work (W1, W2, D1, D3, D4, D6, D7, D9, plus the Q4 fallback pointer) is complete in the compiled PDF. Three background experiments are in flight at submission time: Mistral 7B persona/FB autonomy n=200 (third-family negative-transfer), Qwen 14B adv-fullregex n=200 (W5 completion), and the 5th-scenario disposition-source pilot (Q1/W6). If any of the three fails to complete before the deadline, the text will report partial progress with Wilson CIs and explicit "preliminary" labeling rather than fabricate a pooled number. The paper remains at 42 pages, 0 errors, 0 undefined refs. The level-dependent / level-independent claim taxonomy is now the load-bearing organizing principle, surfaced in §1 and in the "How to read" guide.
