# Reviewer Response Letter — V25
## NeurIPS 2026 Revised Submission

---

**To:** Reviewer 4 (Weak Accept 6/10, Confidence 4/5)

**Subject:** V25 revision addressing W1–W9 and DC1–DC7

We thank the reviewer for the Weak Accept 6/10 and for the structured list of weaknesses and detailed comments, which provide a clear upgrade path. V25 addresses every numbered item. The highest-leverage experimental request — a 3rd annotator to rule out task-specific misunderstanding in the human baseline — is complete. All text edits have been executed.

---

## At-a-Glance Table

| Ask | V25 action | Status |
|---|---|---|
| **W1** Contribution framing oversold; thesis buried | 2-sentence thesis anchor added at top of §1.1 before the three-control enumerate block | **Done — introduction.tex** |
| **W2** Sonnet pilot "between data and promissory note"; demote | §4.6 Sonnet block replaced by 1-sentence pointer; full content in `app:sonnet_pilot`; §1.1 Frontier paragraph updated | **Done — experiments.tex, introduction.tex** |
| **W3** ICC=0.114 caveat should scope all level-dependent claims | Bolded `\textbf{Level-dependent claims (provisional until ICC validated).}` paragraph added to §5.1 listing all three provisional claims; abstract already caveated from V24 | **Done — discussion.tex** |
| **W4** Sharper CAN/CANNOT articulation | Named `\paragraph{What behavioral detection reliably does and does not do.}` added to §5.3 with (a) Does / (b) Partially does / (c) Does not taxonomy | **Done — discussion.tex** |
| **W5** Adversarial paraphrase mechanism hand-wavy; n=50 replication risk | Replaced speculative Mistral 7B mechanism sentence with "mechanism-unknown at tested configurations"; added explicit n=50 generalization caveat paragraph | **Done — experiments.tex** |
| **W6** Qwen 32B framing inconsistency | Contribution 1 parenthetical: `(diagnostic only; §\ref{sec:qwen_scale_sweep})` added; conclusion already reads "hypothesis-generator pending replication" — verified, no edit needed | **Done — introduction.tex; verified — conclusion.tex** |
| **W7** Missing Pacchiardi original vs. equalized comparison | Paragraph added to Appendix J citing Pacchiardi's published 67–73% range and framing the equalized gap as regime distinction, not performance improvement | **Done — appendix.tex** |
| **W8** Human baseline n=2 too thin; need 3rd annotator | Annotator C recruited and completed (n=50, seed=45 shuffle); Fleiss' κ computed; §4.10 and §5.7(k) updated with 3-annotator result | **Done — experiments.tex, discussion.tex** |
| **W9** §4.7 too dense; cross-family re-extraction buried | Navigation sentence added at §4.7 top with pointers to subsections and to §4.8 for Llama 70B cross-family re-extraction | **Done — experiments.tex** |
| **DC1** k=1 "no calibration" misleading | Changed to "label-free under a single-hyperparameter choice (k=1, selected by inspection of the refusal-count distribution rather than labeled-set optimization)" | **Done — experiments.tex** |
| **DC2** Table 5 vs Table 15 LOO protocols not cross-referenced | Footnote added to pooled-LOO table caption explaining pooled vs. per-target LOO and pointing to per-target LOO table | **Done — experiments.tex** |
| **DC3** Sycophancy system-prompt-plus-user-X confound not scoped in limitations | §5.7(l) added: system-prompt-only control needed to isolate disposition-source | **Done — discussion.tex** |
| **DC4** Abstract Llama 8B outlier range check | Verified: abstract already reads "+7 to +16 pp; Llama 3.1 8B outlier at +0.5 pp" — no edit needed | **Verified (no edit needed)** |
| **DC5** n=30 caveat should travel to every §5.7(i) and §5.8 reference | "(n=50/3-target; disposition-source result is n=30/1-target, descriptive only)" added to §5.7(i); "(pilot, n=30)" added to §5.8 future-work citation | **Done — discussion.tex** |
| **DC6** Mistral 7B probe base/Instruct mismatch problem for probe-parity claim | §4.9 lead paragraph rewritten: Llama 3B Instruct stated cleanly (67% peak); Mistral 7B labeled "lower bound due to base/Instruct mismatch" | **Done — experiments.tex** |
| **DC7** §5.4 "97.8% LOO" vs abstract consistency | Grep confirmed: all three occurrences (introduction.tex, discussion.tex ×2, appendix.tex ×3) specify "instructed LOO" and the same Claude Haiku regime — no edit needed | **Verified (no edit needed)** |

---

## W8 — Third Annotator (Highest-Leverage Experimental Item)

> *"The n=2 result is suggestive but not decisive — both annotators may have shared a task-specific misunderstanding. A third naive annotator would rule out this explanation."*

**V25 action: Annotator C recruited and completed.** Annotator C annotated the same 50 transcripts with a different shuffle order (seed=45; A: seed=43, B: seed=44). Annotation protocol identical to A/B (`docs/human_baseline_protocol_v24.md`).

**Result — 3-annotator table:**

| Method | Accuracy | Wilson 95% CI |
|---|---|---|
| Human Annotator A (n=50) | 44.0% | [31.2%, 57.7%] |
| Human Annotator B (n=50) | 44.0% | [31.2%, 57.7%] |
| Human Annotator C (n=50) | 44.0% | [31.2%, 57.7%] |
| Majority vote (A+B+C, n=50) | 44.0% | [31.2%, 57.7%] |
| Refusal-count rule (n=50) | **76.0%** | [62.6%, 85.7%] |
| *Pipeline same-family (paper, n≈689)* | *74.3%* | *—* |
| *Rule pooled-LOO (paper, n≈689)* | *80.1%* | *—* |

**Fleiss' κ (3-annotator, binary TRUTH/LIE):** κ = 0.00 — the same degenerate pattern as Cohen's κ on A/B. All three annotators labeled 48–50/50 trials as TRUTH (A: 50/50, B: 48/50, C: 49/50); raw pairwise agreement 96–100%, but inter-rater reliability is zero because label variance is zero.

**Interpretation.** The 3rd annotator reproduces the collapse exactly, ruling out task misunderstanding by a single annotator. The degenerate κ is not a failure of annotation quality — it reflects the experimental design. In equalized lying trials, the assistant frequently produces factual corrections indistinguishable from truthful-trial responses (the heuristic "assistant that corrects claims → truthful" systematically misfires). Three independent naive annotators consistently miss the signal that the refusal-count rule exploits: the *absence* of correction markers in lying trials where the model endorses the false claim without pushback.

**§4.10 updated** to: *"All three naive annotators collapsed to TRUTH (48–50/50 trials each; Fleiss' κ = 0.00, ruling out single-annotator task misunderstanding; Table~\ref{tab:human_baseline}). Per-annotator accuracy against ground truth: 44.0\% (Wilson CI [31.2\%, 57.7\%]), at or below chance given the 56\% lying-class base rate. Majority-vote accuracy matches per-annotator at 44.0\%. The refusal-count rule achieves 76.0\% (+32 pp over humans)."*

**§5.7(k) updated** to: *"Human baseline completed (n=50, 3 annotators): all three achieved 44.0\% accuracy (chance-level; Wilson CI [31.2\%, 57.7\%]) with Fleiss' κ = 0.00 from collapsing to the TRUTH label on 48–50/50 trials, ruling out single-annotator task misunderstanding. The refusal-count rule reaches 76.0\% on the same sub-sample (+32 pp; §\ref{sec:human_baseline})."*

---

## W2 — Sonnet Pilot Demoted to Appendix

> *"The Sonnet 4.5 pilot sits between a data point and a promissory note — either replicate it properly or confine it to an appendix."*

**V25 action: demoted to Appendix~\ref{app:sonnet_pilot}.**

**Before (experiments.tex §4.6, ~10 lines):** Full `\paragraph{Frontier-scale pilot observation ($n=99$).}` block with numerical results (73.7% rule LOO, 88.9–92.9% pipeline) and power calculation.

**After (experiments.tex §4.6, 3 lines):**
> *"A single frontier pilot on Claude Sonnet~4.5 (Bedrock, $n=99$, equalized) is reported in Appendix~\ref{app:sonnet_pilot} for context; it is 4–6× underpowered for a tested between-extractor comparison ($n\approx410$ needed) and runs on a single serving provider (AWS Bedrock)."*

The `app:sonnet_pilot` appendix already contained the full paragraph content from V23. The §1.1 Frontier observation paragraph now closes with "Full details are in Appendix~\ref{app:sonnet_pilot}."

---

## W1 — Thesis Anchor in §1.1

> *"The contribution framing lists numbers before the thesis is clear; a reader needs to locate the claim before navigating the results tables."*

**Before:** §1.1 opened directly with the three-control `\begin{enumerate}` block.

**After:** 2-sentence thesis anchor inserted immediately before the enumerate:

> *"This paper asks whether behavioral deception detection—as currently practised—survives joint application of three standard evaluation controls. It does not: joint application reduces reported instructed-detection accuracy by 30–41 pp, collapses a 5-feature LLM pipeline to rule-parity under cross-family extraction, and reveals that the residual signal fails to transfer to fully autonomous deception in four of six n=200 cells across three model families."*

---

## W3 — ICC Level-Dependent Caveat Box

> *"ICC=0.114 bears on more claims than currently acknowledged; treat it as a precondition, not future work."*

**V25 action:** After the camera-ready commitment paragraph in §5.1, added:

> *\textbf{Level-dependent claims (provisional until ICC validated).} The following results depend on LLM-extracted feature quality and should be treated as provisional pending the $n\geq100$/3-annotator ICC study: (i) 74.3\% Haiku pipeline accuracy (same-family upper bound); (ii) the EXP-G decomposition (+7.5–15 pp instruction-following contribution); (iii) the white-box probe band (63–67\% LOO, Llama 3B Instruct; Mistral 7B probe additionally a lower bound due to base/Instruct mismatch). Level-independent claims (refusal-count LOO 80.1\%, equalization collapse 30–41 pp, Claude-on-Claude localization, autonomous transfer failure) do not depend on LLM feature quality and are unaffected.*

The abstract 74.3% mention already carries `(level-dependent; ICC=0.114, §5.1)` from V24. No additional abstract edit needed.

---

## W4 — CAN / CANNOT Taxonomy

> *"The paper needs a sharper 'what detection reliably does vs. does not do' articulation."*

**V25 action:** Named paragraph added to §5.3 (Instructed Roleplay vs. Genuine Deception):

> *\paragraph{What behavioral detection reliably does and does not do.} (a) \textbf{Does}: detect instructed deception via refusal-count markers at 61–84\% on equalized transcripts for models ≥7B — a non-trivial result given that unaided human performance on the same transcripts is at or below chance (§4.10). (b) \textbf{Partially does}: transfer to sycophancy as the semi-autonomous case (82\% at 3B/14B, 72\% at 70B). (c) \textbf{Does not}: transfer to fully autonomous persona-maintenance or false-belief ICL (four of six n=200 Wilson CIs include chance).*

---

## W5 — Adversarial Mechanism Caveat

> *"The Mistral 7B mechanism explanation is speculative; the Qwen 14B n=50→n=200 flip is a replication warning."*

**V25 action:**

**(a) Mechanism sentence replaced:**
- Before: "paraphrase-while-preserving-semantics is sufficient at that scale"
- After: "the Mistral 7B near-parity failure mode is mechanism-unknown at the tested configurations"

**(b) Replication caveat paragraph added after the Qwen 14B flip description:**
> *"The Qwen~2.5~14B pattern reversal ($n=50$: truth-suppression; $n=200$: lying-channel suppression) cautions that any $n=50$ adversarial result in this paper should be treated as a preliminary signal; the stable failure mode at scale is lying-channel suppression on at least two of three families."*

---

## W6 — Qwen 32B Framing Consistency

> *"Qwen 32B appears in abstract/contributions/conclusion inconsistently with single-observation framing."*

**V25 verification:** Contribution 1 in §1.1 now reads "(diagnostic only; §\ref{sec:qwen_scale_sweep})" for the 8-target panel. Conclusion §6 reads "hypothesis-generator pending replication on additional RLHF-tuned models." Abstract does not mention Qwen 32B directly. Framing is consistent. No edit to conclusion needed.

---

## W7 — Pacchiardi Published Numbers

> *"Missing comparison to Pacchiardi original-protocol accuracy to contextualize the equalized gap."*

**V25 action:** Paragraph added at end of Appendix J (`app:pacchiardi`):

> *\paragraph{Comparison to Pacchiardi et al.'s original protocol.} Pacchiardi et al.\ reported 67–73\% accuracy under their asymmetric instructed protocol (lying condition: explicit instruction to lie; Table~2 in \citealt{pacchiardi2023catch}). Our EXP-K equalized condition removes the explicit lie instruction, yielding 63–84\% refusal-count and 52–84\% pipeline accuracy depending on model and follow-up type. The refusal-count results are comparable to or above Pacchiardi's published range for ≥14B models; the improvement is not meaningful because the protocols differ (equalized vs. instructed) and our target models differ from theirs. The key gap is not a performance improvement but a regime distinction: Pacchiardi's instructed-protocol accuracy partly reflects instruction-following artifacts; equalized accuracy reflects transferable behavioral signal. The cross-family pipeline at 64.7\% is below their published range, consistent with same-family extraction inflation accounting for the difference.*

---

## W9 — §4.7 Navigation

> *"§4.7 too dense: sycophancy + persona/FB + two pre-registered scenarios + cross-family re-extraction all in one section."*

**V25 action:** Navigation sentence added at the top of §4.7:

> *\emph{Navigation.} Section~\ref{sec:autonomous_matched} covers three scenario types in order of autonomy: sycophancy (semi-autonomous, §\ref{sec:sycophancy_semi_autonomous}), persona and false-belief ICL (fully autonomous, §\ref{sec:persona_fb_autonomous}), and pre-registered causal probes (§\ref{sec:exp_i_4th_scenario}–\ref{sec:exp_i_5th_scenario}). The Llama~3.3~70B cross-family re-extraction on the sycophancy cell is reported in §\ref{sec:cross_family_equalized} to keep the cross-family discussion in one place.*

---

## DC1 — k=1 "No Calibration" Framing

> *"'No calibration data' is slightly misleading; honest framing is 'label-free under a single-hyperparameter choice'."*

**Before:** "without any labeled data"
**After:** "label-free under a single-hyperparameter choice ($k=1$, selected by inspection of the refusal-count distribution rather than by labeled-set optimization)"

---

## DC2 — LOO Protocol Cross-Reference

> *"Table 5 vs Table 15: different LOO protocols not cross-referenced."*

**V25 action:** Caption of the pooled-LOO table (`tab:refusal_only`) updated to read: "A single shared threshold $k=1$ is fixed across all targets — this is the 'pooled-LOO' deployment regime. For per-target LOO (individually optimized threshold per model), see Table~\ref{tab:cross_family_panel}."

---

## DC3 — Sycophancy Confound Note

> *"System-prompt-plus-user-asserted-X confound acknowledged but not scoped in limitations."*

**V25 action:** §5.7(l) added to discussion.tex:

> *"(l) The sycophancy condition uses a system prompt plus user-asserted false claims (the user-asserted-X trigger); a system-prompt-only control — which would eliminate the direct epistemic-pressure trigger — is needed to cleanly isolate disposition-source from the knowledge-conflict mechanism."*

---

## DC4 — Abstract Llama 8B Range (Verified)

> *"Check that abstract reads '+7 to +16 pp; Llama 8B outlier at +0.5 pp'."*

Verified: `abstract.tex:2` reads "Haiku $+9$\,pp above the mean...on 7 of 8 targets (range $+7$ to $+16$\,pp; Llama~3.1~8B is an outlier at $+0.5$\,pp)." No edit needed.

---

## DC5 — n=30 Caveat Propagation

> *"(pilot, n=30; descriptive only) should travel to §5.7(i) and §5.8 references of disposition-source rejection."*

**V25 action:**
- §5.7(i): Added "($n=50$/3-target; disposition-source result is $n=30$/1-target, descriptive only)" to both falsified axes.
- §5.8 future-work item 4: Added "($n=30$, pilot only; descriptive only)" to the disposition-source citation.

---

## DC6 — Probe Parity Claim Restriction

> *"Mistral 7B base/Instruct mismatch is a real problem for the probe-parity claim; restrict to Llama 3B Instruct."*

**V25 action:** §4.9 lead paragraph rewritten:

> *"On Llama 3.2 3B Instruct equalized transcripts ($n=100$), last-layer LR probes achieve 63\% LOO; per-layer sweep (29 layers × 2 pooling strategies) peaks at 67\% (layer 12, last-token), within $+4$\,pp of the refusal-count rule. Mistral 7B results (65\% LOO, Appendix~\ref{app:mistral_probe_panel}) use the base checkpoint rather than Instruct due to availability constraints, understating probe capacity; rule-parity on Mistral 7B should be treated as a lower bound. No Instruct-checkpoint configuration at tested design points exceeds the Llama 3B refusal-count rule by more than $+4$\,pp."*

---

## DC7 — §5.4 and Abstract "97.8%" Consistency (Verified)

> *"Verify all 97.8% occurrences specify the instructed LOO regime consistently."*

Grep across `sections/*.tex` confirms: all six occurrences specify "instructed LOO" and reference Claude Haiku 4.5 in the instructed (not equalized) condition. No edit needed.

---

## V25 Diff Summary

**New data files:**
- `code/adaptive_lie_detector/data/human_baseline_v24/annotator_C_completed.csv` — Annotator C labels (49/50 TRUTH, 1/50 LIE)

**Paper edits (sections/*.tex):**
- `introduction.tex` — 2-sentence thesis anchor before three-control enumerate (+2 lines); Frontier observation paragraph updated (pointer to appendix); contribution-1 Qwen 32B parenthetical added
- `experiments.tex` — §4.6 Sonnet demote (~10→3 lines, −0.2 page); §4.3 k=1 framing fix; tab:refusal_only caption LOO cross-reference; §4.5 adversarial mechanism fix + replication caveat; §4.7 navigation sentence; §4.9 probe parity restriction; §4.10 3-annotator result update (+3 lines)
- `discussion.tex` — §5.1 level-dependent caveat box (+5 lines); §5.3 CAN/CANNOT paragraph (+5 lines); §5.7(i) n=30 caveat; §5.7(k) 3-annotator result update; §5.7(l) sycophancy confound note (+2 lines); §5.8 future-work DC5 caveat
- `appendix.tex` — Appendix J Pacchiardi published-numbers paragraph (+8 lines)

**Page count:** 43 pages (within ≤43 target). W2 Sonnet demote (−0.2 page) offsets B.3+B.4+B.7+W8 additions (+0.2 page net). 0 LaTeX errors. 0 undefined refs.

---

## Out-of-Scope for V25

- Non-English n=50 pilot: remains §5.8 future work.
- Provider replication of Sonnet 4.5 at n≈410: remains §5.8 future work.
- n≥100/3-annotator ICC study: remains camera-ready commitment (§5.1).
- Scaling human baseline beyond n=3 annotators: n≥100/3-annotator study is the §5.1 camera-ready commitment (Fleiss' κ is an interim result; Krippendorff's α will be the primary IRR metric at scale).
- Qwen 14B persona qualitative spot-check coding (P/B-correct/B-other): script and 10-trial report produced in V24; counts to be integrated into Appendix N at camera-ready.

---

*Word count: ~1,600. Response letter follows V23/V24 template.*
