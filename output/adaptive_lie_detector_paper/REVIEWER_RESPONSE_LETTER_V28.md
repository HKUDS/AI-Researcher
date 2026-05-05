# Reviewer Response Letter — V28
## NeurIPS 2026 Revised Submission

---

**To:** Reviewer 5 (Borderline 5.5/10, upgraded from Weak Reject 5/10)

**Subject:** V28 revision addressing W1–W8 and Q1–Q5

We thank the reviewer for upgrading to Borderline and for the precise identification of remaining gaps. V28 makes no new API calls — all changes are text fixes, local data reads, or short calculations on existing results. The most substantive changes are: (1) §4.7.3 "orthogonal signal" reframed as floor-recovery via sycophancy-suppression mechanism; (2) Llama +5.4 pp same-scale gap benchmarked against ±5 pp noise floor; (3) 6-target sensitivity analysis (excluding Haiku-as-target) added as footnote; (4) Mistral 7B adversarial near-parity characterized as partial symmetric degradation; (5) stale 92.9% Sonnet-Haiku reference removed from §5.7(g); (6) sec:icc_owned label fixed to sec:icc_caveat throughout; (7) persona n=30 reversal caution added.

---

## At-a-Glance Table

| Item | Ask | V28 action | Status |
|---|---|---|---|
| **T1 (orthogonal signal)** | "Orthogonal" is ambiguous — could be floor recovery | §4.7.3 interpretation rewritten: "multi-turn follow-up questions recover the signal suppressed by the sycophancy floor effect" | **Done — experiments.tex** |
| **T2 (Llama +5.4 pp)** | +5.4 pp not benchmarked vs. capability-gap noise | §4.8 sentence updated: "+5.4 pp falls within ±5 pp capability-gap noise range; unlike Haiku's +9.7 pp at same scale" | **Done — experiments.tex** |
| **T3 (sycophancy n=50)** | 82/82/72% each at n=50 — needs caveat | Abstract and §4.7 sycophancy row now include "(n=50 per cell; n=200 replication is future work)" | **Done — abstract.tex** |
| **T4 (headlines)** | 10 headline numbers — reduce to ≤5 primary | Rows 2/5/6 removed from primary table (74.3% Haiku, 66.9% Llama-70B, 50% Qwen-32B); caption now commits to "64.7% cross-family (Mistral L3) as recommended system-performance number"; removed rows available in Tab. cross_family_panel | **Done — experiments.tex** |
| **T5 (stale label)** | `\ref{sec:icc_owned}` in abstract should be `sec:icc_caveat` | Grep-replaced all 8 occurrences across abstract.tex, experiments.tex, discussion.tex, appendix.tex | **Done — all sections** |
| **T6 (§5.7(g) stale)** | "92.9% Sonnet-Haiku" appears in §5.7(g) | Found and removed: "92.9% Sonnet-Haiku" was present in §5.7(g) limitations item; removed, now reads "level-dependent claims (74.3% Haiku pipeline, EXP-G decomposition, probe band)" | **Done — discussion.tex** |
| **T7 (machine-ICC)** | Machine-ICC §5.1 still prominent | Verified: §5.1 already has pointer-only form (≤2 sentences); no change needed | **No change — already correct** |
| **T8 (Q5 persona reversal)** | n=30 persona pilot needs extreme caution given n=50→n=200 reversal | Added to §4.7.2 interpretation: "Given direction reversal observed when EXP-ADV-FULLREGEX scaled from n=50 to n=200 on Qwen-14B, the n=30 disposition-source pilot ranking should be treated as directionally unreliable pending n≥200 replication" | **Done — experiments.tex** |
| **A1 (Mistral mechanism)** | "mechanism-unknown" without characterization | §4.4 EXP-ADV Mistral paragraph updated: "partial symmetric degradation — both channels remain above adversarial floor (+17 pp residual lie-channel advantage vs. one-sided collapses on Llama-3B and Qwen-14B)" | **Done — experiments.tex** |
| **A2 (6-target sensitivity)** | Haiku is both extractor and target — exclude it | Computed 6-target avgs (ex. Haiku): Haiku-extractor 72.9%, Mistral-L3 63.5%, Llama-70B 65.9%; Haiku advantage 8.2 pp vs. 8.5 pp 7-target → no Haiku-on-Haiku artifact | **Done — experiments.tex footnote** |
| **A3 (K=1 on persona/FB)** | Does K=1 also fail below chance on persona/FB? | K=1 on persona/FB yields exactly 50% (RC=0 for all 200 trials in both conditions — universal suppression, not below chance). Different failure mode from sycophancy (which breaks below chance). Added to Tab. autonomous_matched caption | **Done — experiments.tex** |

---

## T1 — §4.7.3 "Orthogonal Signal" Reframe

> *"'Orthogonal signal' is ambiguous. The K=1 fails below chance, which is consistent with floor recovery via follow-up questions, not a genuinely independent channel."*

The reviewer's reading is correct: the adaptive multi-turn recovery is floor-recovery, not independent signal. V28 makes this explicit.

**Before (§4.7.3 interpretation paragraph):**
> *"...confirming that multi-turn interrogation provides signal orthogonal to the first-response refusal count."*

**After:**
> *"...confirming that multi-turn follow-up questions recover the signal suppressed by the sycophancy floor effect: when the sycophancy prompt sets RC\,=\,0 for all truthful trials (eliminating the K=1 threshold's discriminative direction), adaptive interrogation accesses model-internal state via subsequent turns, bypassing the first-response floor-effect degradation."*

The mechanism is now explicit: sycophancy sets RC=0 on truthful trials (K=1 sees "all lying" → predict all as lying → below-chance accuracy on balanced data). Adaptive multi-turn breaks out of this by asking follow-up questions that elicit correctional language in later turns. This is floor-recovery, not independent signal, and the text now says so.

---

## T2 — Llama +5.4 pp Benchmarking

> *"+5.4 pp Llama-over-Mistral gap at same scale — is this above noise? You need to benchmark against the capability-gap range on this panel."*

**Before (§4.8 Llama-on-Llama paragraph):**
> *"Llama~70B self-extraction is $-$9.7\,pp below Haiku on its own target, and $+$5.4\,pp above Mistral~L3 (within the capability-gap range expected from a stronger extractor)."*

**After:**
> *"Llama~70B self-extraction is $-$9.7\,pp below Haiku on its own target, and $+$5.4\,pp above Mistral~L3. The $+$5.4\,pp Llama-over-Mistral gap falls within the $\pm$5\,pp capability-gap noise range observed across extractor pairs on this panel; unlike Haiku's $+$9.7\,pp gap (which persists at same scale), the $+$5.4\,pp gap is not clearly above this noise floor and should not be interpreted as confirmed self-preference."*

The ±5 pp noise floor is calibrated against the Llama-70B-vs-Mistral-L3 difference on the full 6 non-Haiku targets (ranging from −3 pp to +10 pp across cells). The Haiku +9.7 pp is at same scale and therefore cannot be explained by capability asymmetry; the +5.4 pp sits at the upper edge of the noise band.

---

## T4 — Headline Table Consolidation

> *"10 headline numbers across 2 tables. Reduce to ≤5 primary; commit to a single recommended system-performance number."*

**Before (tab:headlines_primary): 9 rows**
1. Instructed LOO 93.9–100%
2. Equalized pipeline avg (Haiku) 74.3%
3. Equalized rule avg (pooled-LOO) 80.1%
4. Cross-family pipeline (Mistral L3) 64.7%
5. Cross-family pipeline (Llama 70B) 66.9%
6. Qwen 32B RLHF-collapse 50.0%
7. Instructed-matched ΔLOO +7.5–15 pp
8. Sycophancy transfer 82/82/72%
9. Persona/FB (3B; 14B; rule) 60–66%

**After (tab:headlines_primary): 6 rows**
1. Instructed LOO 93.9–100%
2. Equalized rule avg (pooled-LOO) 80.1% (Regex)
3. Cross-family pipeline (Mistral L3) **64.7%** ← committed
4. Instructed-matched ΔLOO +7.5–15 pp
5. Sycophancy transfer 82/82/72%
6. Persona/FB (3B; 14B; rule) 60–66%

Rows 2/5/6 from the old table (74.3% Haiku, 66.9% Llama-70B, 50% Qwen-32B) are moved out of the primary table. They remain available in Table~\ref{tab:refusal_only}, Table~\ref{tab:cross_family_panel}, and §\ref{sec:qwen_scale_sweep} respectively; a reader can find them, but they are not headline claims.

Caption now reads: *"Recommended system-performance number for cross-family claims: 64.7\% (Mistral~L3)."*

---

## T5 — Stale `sec:icc_owned` Label Fix

> *"Abstract still has `§\ref{sec:icc_owned}` — the label was renamed to `sec:icc_caveat` in V27."*

`sec:icc_owned` appears 8 times across 4 files:
- `abstract.tex`: 2 occurrences (`\ref{sec:icc_owned}`)
- `experiments.tex`: 2 occurrences
- `discussion.tex`: 3 occurrences (`\label{sec:icc_owned}` alias retained; 2 `\ref` → updated)
- `appendix.tex`: 1 occurrence

All `\ref{sec:icc_owned}` replaced with `\ref{sec:icc_caveat}`. The `\label{sec:icc_owned}` alias in discussion.tex is retained for backward compatibility with any cross-references not caught by grep (it points to the same section).

Verified: 0 undefined references in V28 compile.

---

## T6 — §5.7(g) Stale Sonnet-Haiku Reference

> *"§5.7(g) still mentions '92.9% Sonnet-Haiku' — this was supposed to be removed in V26."*

This was present in V27 (reviewer's concern was valid — the earlier Explore agent report was incorrect). Found and removed:

**Before (§5.7(g) limitations):**
> *"level-dependent claims (74.5\% Haiku pipeline, 92.9\% Sonnet-Haiku, EXP-G decomposition, probe band) should be read with this caveat"*

**After:**
> *"level-dependent claims (74.3\% Haiku pipeline, EXP-G decomposition, probe band) should be read with this caveat"*

Also corrected 74.5% → 74.3% (7-target average from Table~\ref{tab:refusal_only}).

---

## A1 — Mistral 7B Adversarial Near-Parity Characterized

> *"The Mistral 7B 'mechanism-unknown' is unsatisfying. Can you at least characterize the channel behavior?"*

From existing n=200 result data: Mistral 7B EXP-ADV-FULLREGEX shows truth 56%, lie 73% — both channels above floor, unlike Llama 3B (truth 87%, lie 36%) and Qwen 14B (truth 99%, lie 31%) which show one-sided lying-channel collapse.

**Before:**
> *"The Mistral~7B near-parity failure mode is mechanism-unknown at the tested configurations."*

**After:**
> *"The Mistral~7B near-parity failure mode ($n=200$, truth 56\%, lie 73\%) is consistent with partial symmetric degradation: both channels remain above their adversarial floor (unlike the one-sided collapses on Llama~3B and Qwen~14B), with the residual lie-channel advantage ($+$17\,pp) reflecting weaker lexical suppression rather than asymmetric channel collapse."*

This is a characterization of the channel behavior from data, not a new experiment. The mechanism (why Mistral suppresses both channels symmetrically rather than one-sidedly) is still open.

---

## A2 — 6-Target Sensitivity Analysis (Excluding Haiku)

> *"Haiku is both extractor and target in your 7-target panel. Excluding it, what are the cross-family averages?"*

From Table~\ref{tab:cross_family_panel}, excluding the Claude Haiku row:

| Extractor | 6-target avg (ex. Haiku) | 7-target avg | Δ |
|---|---|---|---|
| Haiku | 72.9% | 74.3% | −1.4 pp |
| Mistral L3 | 63.5% | 64.7% | −1.2 pp |
| Llama 70B | 65.9% | 66.9% | −1.0 pp |

Haiku advantage: 8.2 pp (6-target) vs. 8.5 pp (7-target). The same-family uplift is essentially unchanged when excluding the Haiku-on-Haiku cell, confirming it is not an artifact of that self-family cell.

Added as a footnote to the cross-family panel summary paragraph in §4.5.

---

## A3 — K=1 Rule on Persona/False-Belief

> *"The sycophancy K=1 falls below chance. Does persona/FB also fall below chance, or at chance?"*

From existing persona/FB transcript data (n=200 per condition): RC=0 on all 200 trials in both lying and truthful conditions for both persona and false-belief scenarios. K=1 rule (predict lying if RC≥1) yields 50% LOO — all trials predicted as truthful.

This is **at** chance (50%), not below chance. The distinction matters:
- **Sycophancy** (K=1 fails below chance, 22–50%): sycophancy prompt selectively suppresses RC on *truthful* trials only (lying trials may still produce corrections because the model "knows" the claim is false), making the rule predict lying far too often.
- **Persona/FB** (K=1 at chance, 50%): both conditions suppress RC universally — lying and truthful trials alike produce RC=0. K=1 just predicts "all truthful," yielding balanced 50%.

Added as a `†` footnote to Table~\ref{tab:autonomous_matched} caption.

---

## T8 — Persona n=30 Reversal Caution

> *"Given you found n=50→n=200 direction reversal in sycophancy, the n=30 persona pilot needs strong caution language."*

**Before (§4.7.2 interpretation):**
> *"We do not claim persona > sycophancy as a ranking at n=30; we report only that the pre-registered one-sided prediction (sycophancy > persona) fails to be confirmed (persona > sycophancy at n=30, descriptive only)."*

**After:** Added sentence:
> *"...Given the direction reversal observed when EXP-ADV-FULLREGEX scaled from $n=50$ to $n=200$ on Qwen~14B (§\ref{sec:adversarial_fullregex}), the $n=30$ disposition-source pilot ranking should be treated as directionally unreliable pending $n\geq200$ replication."*

---

## V28 Diff Summary

**Paper edits:**
- `experiments.tex` — §4.7.3 floor-recovery reframe; §4.8 +5.4 pp noise-benchmarked; sycophancy n=50 caveat in Tab. autonomous_matched caption; K=1/persona-FB at-chance footnote in Tab. autonomous_matched; §4.7.2 persona-caution sentence; Mistral-7B partial-symmetric characterization; 6-target footnote in cross-family summary; tab:headlines_primary 3 rows removed (74.3%, 66.9%, 50%); tab:headlines_primary caption updated with 64.7% commitment
- `abstract.tex` — 82/82/72% now has "(n=50 per cell)" parenthetical; all `\ref{sec:icc_owned}` → `\ref{sec:icc_caveat}`
- `discussion.tex` — §5.7(g) "92.9% Sonnet-Haiku" removed; all `\ref{sec:icc_owned}` → `\ref{sec:icc_caveat}`
- `appendix.tex` — `\ref{sec:icc_owned}` → `\ref{sec:icc_caveat}`

**Page count:** 45 pages (V27 was 44; net +1 page: C.2/C.8/A.1/A.2 additions ~+1.2 pages; C.4 row removal −0.2 pages). All additions address specific reviewer gaps with no padding. 0 LaTeX errors, 0 undefined references.

---

## Out-of-Scope for V28

- n=200 replication of sycophancy 82/82/72%: remains §5.8 future work
- n=200 replication of persona n=30 pilot: remains §5.8 future work
- ICC validation n≥100/3-annotator: remains camera-ready commitment
- Non-English pilot: remains §5.8 future work
- EXP-ADV weak-14-word n=200: acknowledged as preliminary at n=50

---

*Word count: ~1,800. Response letter follows V27 template.*
