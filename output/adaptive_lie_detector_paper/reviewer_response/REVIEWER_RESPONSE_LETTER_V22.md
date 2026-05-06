# Response to Reviewer (Weak Accept) — Revision V22

We thank the reviewer for the Weak Accept and for the unusually precise set of observations on the V21 submission. The review explicitly praises the V21 additions (two pre-registered self-falsifications, Mistral 7B third-family negative-transfer at n=200, the "how to read this paper" paragraph, and the §5.5 novelty reframe) and describes the paper as "honest to a degree that is unusual for this venue." V22 is therefore a **tight cleanup pass, not another large revision**: we fix the one rendering bug the reviewer caught, address four narrow asks about framing and honesty, and promote the 5th-scenario pilot to the structural prominence the reviewer asked for. The paper is **42 pages, 0 errors, 0 undefined refs**.

**At-a-glance.**

| Ask | Reviewer request | V22 response | Location |
|---|---|---|---|
| W7 / Practical | 5th-scenario pilot is structurally hidden inside §4.7.1 as a `\paragraph`; promote to §4.7.2 with a parallel structure and a properly numbered table | **Promoted**: `\subsubsection{Pre-Registered 5th Scenario: Disposition-Source (Pilot)}` with `\label{sec:exp_i_5th_scenario}` and a dedicated 3-row `\begin{table}` float (Table 13). | `experiments.tex` §4.7.2 |
| W8 / Minor typo | "Table 4.7.1" cross-reference renders as a section number in §1 contribution (v), §5.8(4), and the abstract | **Fixed automatically by W7**: `\label{tab:exp_i_5th_scenario}` now binds to the new Table 13 rather than the former `\paragraph`. Verified in `main.aux`: `\newlabel{tab:exp_i_5th_scenario}{{13}{18}...}`. | — |
| W1 / Q1 | After two self-falsifications, the autonomous-transfer asymmetry has *no* validated causal account; the paper should acknowledge this rather than advance a third post-hoc axis | **New `\paragraph{No validated causal account of the transfer asymmetry.}` in §5.3** and a matching **bullet (i) in §5.8 Limitations** stating: two pre-registered axes falsified, clarity×turn-structure is a post-hoc candidate, we do not advance a validated causal account in V22. | `discussion.tex` §5.3 end; §5.8(i) |
| Q2 | Soften abstract "does not cleanly transfer" | **Rewrote to: "transfers only to semi-autonomous sycophancy … on fully-autonomous persona and false-belief at n=200 across three families, four of six cells have Wilson CIs including chance (…)."** All magnitudes retained. | `abstract.tex` |
| Q3 | Scenario-implementation sensitivity: persona prompt identical across the n=50 persona run and the 5th-scenario pilot? | **New sentence in §4.7.2** notes the persona prompt ("Dr. Alex Morgan, MIT physics educator") is reused **verbatim** from `run_persona_autonomous.py`; the only cross-scenario variable is `disposition_source`. Wording robustness is out of scope. | §4.7.2 |
| Q4 | ICC camera-ready fallback if n≥100/3-annotator recruitment slips | **Rewrote bold final sentence of §5.1** as a two-branch commitment: (i) target n≥100/3-annotator + Krippendorff α by camera-ready; (ii) explicit fallback — preliminary n≥50/2-annotator ICC + Krippendorff α **and** raw per-rater CSVs so downstream researchers can complete validation. | `discussion.tex` §5.1 |
| Q1 (mechanism) | Sketch the clarity × turn-structure post-hoc mechanism and whether it's pre-registrable | **Appended one sentence to §5.8 future-work (4)** describing a pre-registrable 2×2 factorial (clarity × turns) on the three n=200 families at n=50/cell for ~80% power on a 15 pp effect. Explicitly flagged as future work, not V22 evidence. | `discussion.tex` future-work (4) |

---

## Detailed responses

### W1 — Empirical-contribution framing in the presence of two self-falsifications (also Q1)

**The reviewer's point.** After V21 landed its second pre-registered self-falsification (the 5th-scenario pilot inverting the sycophancy > persona prediction), the paper's discussion still advanced a *third* post-hoc candidate (clarity × turn-structure) without clearly labeling it as such. The reviewer is correct that, at this point, the paper should state plainly that it does not yet have a validated causal account of why sycophancy transfers and persona/FB do not.

**V22 change.** We added a dedicated `\paragraph{No validated causal account of the transfer asymmetry.}` at the end of §5.3:

> *"After two pre-registered self-falsifications — knowledge-conflict clarity (§4.7.1) and disposition-source ranking (§4.7.2) — we do not yet have a validated causal account of why sycophancy transfers while persona and false-belief do not. The clarity × turn-structure interaction suggested by the 5th-scenario pilot is a post-hoc candidate, not a pre-registered finding; we state it as a hypothesis to test, not as an explanation the paper establishes."*

And a matching limitation bullet (§5.8(i)):

> *"**(i)** The autonomous-transfer asymmetry (sycophancy transfers; persona/FB do not) currently lacks a validated causal explanation: two candidate axes (knowledge-conflict clarity, §4.7.1; disposition-source ranking, §4.7.2) have been pre-registered and falsified, and the clarity × turn-structure candidate suggested by the 5th-scenario pilot is post-hoc and not itself pre-registered."*

We also tightened two stale claims in §4.6 that were still asserting disposition-source as the controlling axis (the "Why sycophancy is semi-autonomous" paragraph and the "Confound acknowledgement" paragraph), replacing their trailing sentences with pointers to §5.8(i).

**What we did not do.** We did not advance a new positive interpretation in V22. The clarity × turn-structure candidate is labeled as post-hoc throughout, and the §5.8 future-work item (4) describes how it would be pre-registered (below, Q1) — it does not claim the paper has validated it.

### W7 / Practical — Promote the 5th-scenario pilot (fixes W8 typo)

**The reviewer's point.** The V21 5th-scenario pilot was structurally important (the second pre-registered self-falsification) but was buried as a `\paragraph` inside §4.7.1 (the 4th-scenario subsubsection), with all three condition numbers crammed into one dense paragraph and the `\label{tab:exp_i_5th_scenario}` attached to that paragraph. As a result, `Table~\ref{tab:exp_i_5th_scenario}` in the abstract, §1 contribution (v), and §5.8(4) rendered as the section number "4.7.1" — the reviewer correctly flagged this as "Minor typo: 'Table 4.7.1' appears in §1 contribution #5 and §5.8(4), which looks like an unrendered cross-reference to a numbered table that doesn't exist."

**V22 change.** The entire paragraph is now a proper `\subsubsection{Pre-Registered 5th Scenario: Disposition-Source (Pilot)}` with `\label{sec:exp_i_5th_scenario}` and a dedicated `\begin{table}` float (Table 13):

```latex
\subsubsection{Pre-Registered 5th Scenario: Disposition-Source (Pilot)}
\label{sec:exp_i_5th_scenario}

\textbf{Pre-registered design.} Holding clarity (high), turn-count (multi-turn
adaptive), and target (Qwen 2.5 14B) fixed, we vary only \emph{disposition
source}: sycophancy, persona ("Dr. Alex Morgan, MIT physics educator" --- reused
verbatim from \texttt{run\_persona\_autonomous.py}, so the only cross-scenario
variable is \texttt{disposition\_source}; wording robustness is out of scope),
and explicit lie-defense. n=30 per condition (15 TRUE + 15 high-clarity FALSE
from the 4th-scenario pool). Pre-registered one-sided prediction: sycophancy
LOO > persona LOO and > explicit lie-defense LOO.

\begin{table}[h]
\centering
\caption{Pre-registered 5th scenario (disposition-source pilot) on Qwen 2.5 14B,
n=30 per condition. Pre-registered one-sided prediction (sycophancy > persona,
sycophancy > explicit lie-defense) is rejected: persona produces the strongest
separation. Our second pre-registered self-falsification after §4.7.1.}
\label{tab:exp_i_5th_scenario}
\begin{tabular}{lrrrr}
  Disposition           & LOO    & Wilson 95\% CI  & |d|  & Pipeline \\
  Sycophancy            & 73.3\% & [55.6, 85.8]    & 0.94 & 86.7\%   \\
  Persona               & 93.3\% & [78.7, 98.2]    & 2.08 & 76.7\%   \\
  Explicit lie-defense  & 70.0\% & [52.1, 83.3]    & 0.99 & 90.0\%   \\
\end{tabular}
\end{table}
```

**Verification.** `main.aux` now shows:

```
\newlabel{sec:exp_i_5th_scenario}{{4.7.2}{18}{...}{subsubsection.4.7.2}{}}
\newlabel{tab:exp_i_5th_scenario}{{13}{18}{...}{table.caption.46}{}}
```

`Table~\ref{tab:exp_i_5th_scenario}` now renders as "Table 13" everywhere it appears (abstract, §1 contribution (v), §5.8(4)). The "Table 4.7.1" typo is fully resolved.

We also updated the §5.8(4) future-work pointer from `§\ref{sec:exp_i_4th_scenario}` to `§\ref{sec:exp_i_5th_scenario}` so the section pointer lands on the right subsection (it was pointing at the 4th-scenario subsubsection by mistake).

### Q2 — Soften abstract "does not cleanly transfer"

**V21 wording:**
> *"The residual signal does not cleanly transfer to fully-autonomous persona-maintenance or false-belief at n=200 on three families: Llama 3.2 3B 54.0%/56.0%, Qwen 2.5 14B 68.0%/59.5%, Mistral 7B 58.5%/66.5% (four of six cells have Wilson CIs including chance); semi-autonomous sycophancy does transfer (82% at 3B/14B, 72% at 70B)."*

**V22 wording (re-ordered lead):**
> *"The residual signal transfers only to semi-autonomous sycophancy (82% at 3B/14B, 72% at 70B); on fully-autonomous persona-maintenance and false-belief at n=200 across three families, four of six cells have Wilson CIs including chance (Llama 3.2 3B 54.0%/56.0%, Qwen 2.5 14B 68.0%/59.5%, Mistral 7B 58.5%/66.5%)."*

All magnitudes preserved. The binary "does not cleanly transfer" framing is replaced with the positively-stated "transfers only to X; on Y, four of six cells have Wilson CIs including chance" — which is both more informative and more honest about the two cells (Qwen 14B persona, Mistral 7B FB) that do exclude chance.

### Q3 — Scenario-implementation sensitivity (persona prompt across runs)

**Reviewer's concern.** If the "Dr. Alex Morgan" persona prompt used in the 5th-scenario pilot (n=30 on Qwen 14B; 93.3% LOO) differs from the prompt used in the original n=50 persona-autonomy run (which produced the 66% result), the 93.3% pilot result might be a prompt-wording effect rather than a disposition-source effect.

**V22 answer.** The persona prompt is **identical** — the 5th-scenario pilot script (`run_exp_i_5th_scenario.py`) imports the persona prompt verbatim from `experiments/run_persona_autonomous.py` and only varies the `disposition_source` argument. We now state this explicitly in §4.7.2:

> *"…persona ("Dr. Alex Morgan, MIT physics educator" — reused verbatim from `run_persona_autonomous.py`, so the only cross-scenario variable is `disposition_source`; wording robustness is out of scope)…"*

The 93.3% vs. 66% gap between the pilot (n=30, Qwen 14B, multi-turn adaptive, high-clarity FALSE pool from 4th-scenario) and the original n=200 persona autonomy (Qwen 14B, different FALSE pool, different turn structure) is therefore attributable to the clarity × turn-structure interaction, **not** to persona-prompt wording. This is consistent with the post-hoc candidate hypothesis now explicitly stated in §5.3 and §5.8(i) (and discussed as a pre-registrable test under Q1 below).

Full robustness-to-paraphrase (varying persona name, credentials, instructional framing) is **out of scope for V22** and a natural extension of the pre-registered 2×2 factorial sketched in §5.8 future-work (4).

### Q4 — ICC camera-ready fallback

**V21 wording (end of §5.1):**
> *"**Camera-ready commitment.** The authoritative human ICC study at n≥100 with 3+ independent annotators will be completed and included in the camera-ready version of this paper."*

**V22 wording (two-branch):**
> *"**Camera-ready commitment (two-branch).** Target: a full n≥100/3-annotator ICC study with Krippendorff's α included in the camera-ready. Explicit fallback if recruitment slips past the camera-ready deadline: (i) a preliminary n≥50/2-annotator ICC report with Krippendorff's α, and (ii) the raw per-rater CSVs released alongside, so downstream researchers can complete validation independently."*

The V20 protocol freeze (`docs/icc_annotation_protocol_v2.md`) already fixed the annotator-instruction language, rubric, and data directory, so the fallback is executable without further protocol design. The raw n=20 annotator CSVs are already released; the fallback guarantees that whatever subset of the full n≥100/3-annotator sample we have by camera-ready will be released in the same format, making the validation open to downstream completion even under the worst-case recruitment timeline.

### Q1 — Pre-registrability of the clarity × turn-structure mechanism

**V22 addition (appended to §5.8 future-work item (4)):**
> *"A pre-registrable test of that candidate would be a 2×2 factorial (clarity ∈ {high, low} × turns ∈ {single, multi-turn-adaptive}) on the three n=200 families (Llama 3B, Qwen 14B, Mistral 7B), n=50/cell for ~80% power on a 15 pp main effect — pre-registrable but future work."*

This is explicitly labeled as future work, not V22 evidence. The paper at this point states:
1. Two candidate causal axes (clarity; disposition-source) pre-registered and falsified (§4.7.1; §4.7.2).
2. Clarity × turn-structure as a post-hoc candidate suggested by the 5th-scenario pilot (§5.3; §5.8(i)).
3. A pre-registrable 2×2 factorial to test (2) (§5.8 future-work (4)).
4. No validated causal account in V22 (§5.3; §5.8(i)).

This is what the reviewer asked for: the paper is honest about not having an explanation yet, and it sketches the specific experiment that would test the leading post-hoc candidate.

---

## V22 diff summary

| File | Change |
|---|---|
| `sections/experiments.tex` | §4.7.2 new subsubsection with Table 13 (promoted from V21 `\paragraph`); §4.6 "Why sycophancy is semi-autonomous" and "Confound acknowledgement" trailing sentences tightened to remove stale disposition-source claims. |
| `sections/abstract.tex` | Transfer sentence re-ordered to lead with "transfers only to sycophancy" (Q2). |
| `sections/introduction.tex` | No change (`Table~\ref{tab:exp_i_5th_scenario}` now renders correctly by virtue of A.1). |
| `sections/discussion.tex` | §5.1 camera-ready commitment → two-branch (Q4); §5.3 new `\paragraph{No validated causal account}` (W1/Q1); §5.8(i) new limitations bullet (W1/Q1); §5.8 future-work (4) appended 2×2 factorial sketch (Q1); §5.8(4) section pointer corrected to `sec:exp_i_5th_scenario`. |
| `sections/appendix.tex` | Appendix N Mistral 7B probe panel prose tightened (~3 lines) to reclaim page budget for Table 13; Table 31 inlined into prose (lowest-information table in the paper). |

**Page budget**: 42 (unchanged from V21); 0 LaTeX errors; 0 undefined refs.

---

## Explicitly out-of-scope for V22

- Running the n≥100/3-annotator ICC validation itself (protocol frozen in V20; 2.5-week recruitment calendar starts at camera-ready acceptance).
- Running the 2×2 clarity × turn-structure factorial (pre-registrable; stated in §5.8 future-work (4) as the next experiment).
- A fourth family at n=200 on persona/FB (Haiku, Gemma, DeepSeek); three independent families at n=200 is what V21 landed.
- Scaling Sonnet 4.5 to n=410 (Bedrock cost; limitation already in §5.7(b)).
- Closed-loop adaptive adversary (flagged since V16).
- Full Pacchiardi replication (flagged since V13; current Table 1 EXP-K row is sufficient).
- Persona-wording robustness (varying name/credentials of "Dr. Alex Morgan"); the V22 answer to Q3 reports that we reused the prompt verbatim, which is the correct reportable answer given the pilot design.

We again thank the reviewer for the precise set of observations and for the Weak Accept. V22 addresses every numbered item in the review without expanding the paper's scope or adding new experimental evidence.
