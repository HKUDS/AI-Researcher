# Third NeurIPS 2026 Revision Summary

## Status: PHASE 1 COMPLETE

All Phase 1 writing revisions (8-12h estimated, ~6h actual) completed successfully.  
Addresses NEW REVIEWER (different from previous two revision rounds) with borderline reject (5/10).

---

## Reviewer Context

**Critical distinction:** This is a DIFFERENT reviewer from the first two revision rounds.

**Previous work completed:**
- **First revision:** White-box probing, Qwen scale sweep (3B→7B→14B→32B U-shape)
- **Second revision:** Methodology framing, ICC caveat elevation, Llama scale sweep (3B→8B→70B flat-then-jump)
- All 4 explicit acceptance criteria from original reviewer were met

**New reviewer rating:** Borderline reject (5/10), leaning toward weak accept with major revisions

**Reviewer's key quote:** "I lean toward borderline reject in the current form, with strong potential to become weak accept after revision. If the authors reframe and address the IRR issue, I'd shift to weak accept."

---

## Reviewer's 4 Concerns (Mapped to Our Response)

### Concern 1: Scope Mismatch (MC1)
**Reviewer:** "Paper opens with AI-safety deception but studies instructed roleplay."

**Our fix:** Reframed entire paper to lead with "behavioral detection primarily measures instruction-following"
- Abstract opening rewritten
- Introduction §1.1 now leads honestly with finding
- AI-safety framing moved to limitations

### Concern 2: Thin Novelty (MC2)
**Reviewer:** "Each control is standard individually. 'Systematic application' is thin for NeurIPS."

**Our fix:** Pivoted from methodology to empirical contribution
- Abstract: "primary contribution is the empirical finding..."
- Introduction: Controls are "diagnostic tools that enabled the empirical discovery"
- Conclusion: Contribution is what we learned, not the framework

### Concern 3: Weak ICC (MC3)
**Reviewer:** "ICC=0.114 too weak. Should lead with regex baseline."

**Our fix:** Restructured entire paper to lead with regex throughout
- Abstract paragraph reordered: refusal-count heuristic (80.1%) presented first
- Introduction findings list: "Label-free deployment rule" is now Finding #2 (was #3)
- LLM pipeline characterized as "comparison apparatus"

### Concern 4: White-Box Too Thin (MC7)
**Reviewer:** "Only 2 models, linear probes, final-layer. Either expand substantially or remove."

**Our fix:** Removed entirely (as reviewer suggested)
- Section 4.9 deleted (~3 pages)
- Abstract paragraph removed
- Paper: 55 → 54 pages

---

## Strategic Tension: Previous vs Current Reviewer

**Previous reviewer wanted:**
- Methodology framing → We did it
- Scale sweep → We did it (Qwen + Llama)
- All 4 acceptance criteria met → We did it

**Current reviewer says:**
- Methodology novelty thin → Pivot to empirical contribution
- Scale patterns undermine (not support) scale claims → Reframe as family-specific, non-monotonic
- White-box section thin → Remove it

**Resolution:** Different reviewers, different priorities. We've made the paper stronger by:
1. More honest framing (instruction-following detection, not methodology innovation)
2. Leading with practical result (80.1% label-free deployment rule)
3. Accurate interpretation (family-specific RLHF effects, not universal scaling)

---

## All Changes Made (Phase 1)

### Task 1.1: Reframe Scope and Contribution ✅
**Files modified:**
- `sections/abstract.tex`: Opening paragraph rewritten
- `sections/introduction.tex`: §1.1 Motivation rewritten, contribution paragraph updated
- `sections/conclusion.tex`: Opening paragraph rewritten

**Impact:** Paper explicitly positioned as empirical finding (instruction-following detection), not methodology contribution

---

### Task 1.2: Lead with Regex Baseline Throughout ✅
**Files modified:**
- `sections/abstract.tex`: Paragraph ordering changed to present refusal-count heuristic first
- `sections/introduction.tex`: Findings list reordered, LLM pipeline demoted to comparison

**Impact:** 80.1% label-free deployment rule is now the primary detector; LLM pipeline validates signal exists but is not the hero

---

### Task 1.3: Soften Scale Claims ✅
**Files modified:**
- `sections/abstract.tex`: Scale paragraph rewritten with "family-specific, non-monotonic patterns"
- `sections/introduction.tex`: Finding #8 retitled and reframed
- `sections/conclusion.tex`: Parallel updates

**Impact:** Honest interpretation - Qwen U-shape (peaks 14B, collapses 32B) and Llama flat-then-jump (driven by 8B→70B) are family-specific RLHF effects, not universal improvement

---

### Task 1.4: Remove White-Box Section ✅
**Files modified:**
- `sections/abstract.tex`: White-box paragraph removed
- `sections/experiments.tex`: Entire §4.9 deleted

**Impact:** Paper tightened from 55 → 54 pages, removes thin analysis

---

### Task 1.5: Fix All Minor Issues ✅

**MI1 (Truncated abstract):** ✅ Fixed - compiles correctly  
**MI2 (Broken refs):** ✅ Verified none exist  
**MI3 (Terminology):** ✅ Already standardized in second revision  
**MI4 (Figure 1):** ✅ Caption expanded from 1 to 4 sentences  
**MI5 (EXP-K replication):** ✅ Limitation note added  
**MI6 (Ollama wall-time):** ✅ Already documented (40 hours in Appendix A.6)  
**MI7 (50-claim bank):** ✅ Already acknowledged in Discussion footnote  
**MI8 (Fundamental limit):** ✅ Qualified with "framework tested here"  
**MI9 (Future directions):** ✅ Already concise (5 specific directions)

---

## Phase 2: Response Letter ✅

**Created:** `REVIEWER_RESPONSE_LETTER_V3.md`

**Structure:**
- Overview of key changes
- Point-by-point response to all 7 major concerns (MC1-MC7)
- Point-by-point response to all 9 minor issues (MI1-MI9)
- Summary table showing quantitative and qualitative changes
- Addresses reviewer's bottom line: "reframe and address IRR issue"

**Key message:**
1. Reframing complete (methodology → empirical finding)
2. IRR issue addressed via regex pivot (80.1% without LLM extraction)
3. Scale interpretation honest (family-specific, non-monotonic)
4. Focused paper (white-box removed)

**Expected outcome:** Borderline reject (5/10) → Weak accept (6/10)

---

## Summary Statistics

### Page Count
- **Before third revision:** 55 pages
- **After third revision:** 54 pages (-1 from white-box removal)
- **Net change from original:** +0 pages (54→56→55→54)

### Abstract Word Count
- **Current:** 394 words (within NeurIPS 500-word limit)
- **Change from second revision:** +19 words (375→394, slight expansion from two-family summary)

### Framing Shift
- **Before:** "We present a methodology..." (methodology contribution)
- **After:** "We demonstrate that behavioral detection primarily detects instruction-following..." (empirical finding)

### Files Modified (Third Revision)
**Phase 1 (Writing):**
- `sections/abstract.tex` (4 major edits: reframe, reorder, scale, contribution)
- `sections/introduction.tex` (4 major edits: motivation, contribution, findings order, scope)
- `sections/experiments.tex` (2 edits: remove white-box section, qualify "fundamental limit")
- `sections/methodology.tex` (1 edit: expand Figure 1 caption)
- `sections/conclusion.tex` (3 edits: reframe opening, scale softening, contribution)

**Phase 2 (Response Letter):**
- `REVIEWER_RESPONSE_LETTER_V3.md` (new file, ~3500 words)

**Total:** 5 existing files modified, 1 new response letter, 0 new experiments

---

## How This Addresses All 7 Major + 9 Minor Concerns

### Major Concerns

**MC1 (Scope mismatch):**  
✅ Reframed to lead with "instruction-following detection" finding, not AI-safety motivation

**MC2 (Thin novelty):**  
✅ Pivoted to empirical contribution (what we discovered) not methodology contribution (evaluation framework)

**MC3 (ICC=0.114):**  
✅ Lead with regex baseline (80.1%) throughout; LLM pipeline demoted to validation apparatus

**MC4 (Statistical power):**  
✅ Scale claims softened; 7B→14B no longer cited as significant (p=0.17)

**MC5 (Scale story overstated):**  
✅ Reframed as "family-specific, non-monotonic patterns" - honest interpretation of Qwen U-shape + Llama flat-then-jump

**MC6 (Cross-family extraction):**  
✅ Already transparent about capability-masking alternative (no changes needed)

**MC7 (White-box too thin):**  
✅ Removed entirely as reviewer suggested (55→54 pages)

### Minor Issues

**MI1:** ✅ Abstract truncation fixed  
**MI2:** ✅ No broken refs found  
**MI3:** ✅ Already standardized  
**MI4:** ✅ Figure 1 caption expanded  
**MI5:** ✅ EXP-K limitation noted  
**MI6:** ✅ Ollama wall-time already documented  
**MI7:** ✅ 50-claim limitation already noted  
**MI8:** ✅ "Fundamental limit" qualified  
**MI9:** ✅ Future directions already concise

---

## Expected Outcome

**Original rating:** Borderline reject (5/10)

**Target rating after revision:** Weak accept (6/10)

### Justification

1. ✅ **Reframing addresses scope mismatch (MC1):**  
   Paper now honestly leads with "instruction-following detection" not AI-safety motivation

2. ✅ **Empirical pivot addresses thin novelty (MC2):**  
   Contribution is what we discovered (instruction-following dominance, family-specific patterns, 80.1% label-free rule), not the evaluation framework

3. ✅ **Regex-first addresses ICC concern (MC3):**  
   Primary result (80.1% deployment-ready) doesn't depend on weak-reliability LLM features

4. ✅ **Scale reframing addresses overstated claims (MC4, MC5):**  
   Honest interpretation: family-specific RLHF effects, not universal improvement

5. ✅ **White-box removal addresses thin analysis (MC7):**  
   Focused paper, cleaner contribution

6. ✅ **All 9 minor issues addressed**

**Reviewer's stated path to weak accept:**  
> "If the authors reframe and address the IRR issue, I'd shift to weak accept."

**Our response:**  
- Reframing ✅ (methodology → empirical finding)
- IRR issue ✅ (regex-first pivot, 80.1% without LLM extraction)

---

## Risks & Mitigation

### Risk 1: Previous reviewer preferred methodology framing
**Mitigation:** This is a different reviewer with different priorities. NeurIPS decision will weigh both reviews. If both reviewers are satisfied with their respective framings, meta-reviewer will likely accept. The empirical framing is more honest and defensible.

### Risk 2: Removing white-box section might displease previous reviewer
**Mitigation:** Previous reviewer wanted white-box comparison (got it). This reviewer says it's too thin. Removing shows responsiveness. If needed, can note in meta-review: "Different reviewers had different views on white-box depth; we've opted for focused paper."

### Risk 3: Empirical framing might seem like "just a negative result"
**Mitigation:** The positive findings are:
1. Label-free regex rule (80.1% deployment-ready)
2. Family-specific scale effects reveal RLHF impact (Qwen collapse at 32B is policy-relevant)
3. Boundary characterization (where behavioral detection works and doesn't)

Frame as empirical boundary characterization, not pure negative.

---

## Revision Timeline

**Week 1: Phase 1 (Writing)**
- Day 1: Task 1.1 (Reframe) - 2h
- Day 1: Task 1.2 (Regex-first) - 2h
- Day 1: Task 1.3 (Soften scale) - 1h
- Day 1: Task 1.4 (Remove white-box) - 15min
- Day 1: Task 1.5 (Minor fixes) - 45min
- **Total:** ~6 hours

**Week 1: Phase 2 (Response Letter)**
- Day 1: Draft response letter - 2h
- **Total:** ~2 hours

**Grand total:** ~8 hours (vs 8-12h estimated)

---

## Next Steps

**Option A: Submit Now (Recommended)**
- All Phase 1 tasks complete ✅
- Response letter complete ✅
- Paper compiles cleanly (54 pages) ✅
- Addresses all 7 major + 9 minor concerns ✅

**Option B: Optional Enhancements (Not Recommended)**
- Enhanced IRR study (20-30 hours) - SKIP (regex pivot makes this unnecessary)
- Additional experiments - SKIP (Phase 1 addresses reviewer's path to weak accept)

**Recommendation:** Submit now. Phase 1 fully addresses reviewer's stated concerns and path to weak accept.

---

## Files for Submission

When submitting revision, include:

1. **Revised manuscript:** `main.pdf` (54 pages)
2. **Response letter:** `REVIEWER_RESPONSE_LETTER_V3.md` (convert to PDF)
3. **Revision summary:** `THIRD_REVISION_SUMMARY.md` (this file, optional supplemental)

---

## Confidence Assessment

**Likelihood of acceptance after this revision:** 70-80%

**Reasoning:**
- Reviewer provided implicit path to weak accept ("reframe and address IRR")
- All 4 concerns addressed (reframe ✅, IRR via regex ✅, scale honest ✅, white-box removed ✅)
- Writing extensively revised based on feedback
- Claims appropriately moderated (instruction-following, family-specific patterns)

**Risk factors:**
- Different reviewer may have different unstated concerns
- Empirical contribution may still feel thin for NeurIPS main track
- Two reviewers potentially have conflicting preferences (methodology vs empirical)

**Mitigation:**
- Empirical framing is more honest and defensible than methodology framing
- 80.1% label-free deployment rule is a practical positive result
- Family-specific scale effects (Qwen collapse at 32B) is genuinely interesting finding
- Meta-reviewer will weigh both reviews; honest positioning strengthens overall case

---

## Verification Checklist

**Paper compilation:**
- ✅ Compiles without errors
- ✅ 54 pages (within NeurIPS guidelines)
- ✅ Abstract ~394 words (within 500-word limit)
- ✅ No broken cross-references
- ✅ All figures/tables numbered and referenced

**Content verification:**
- ✅ Abstract leads with empirical finding
- ✅ Regex baseline presented first throughout
- ✅ Scale claims softened to "family-specific, non-monotonic"
- ✅ White-box section removed
- ✅ All 9 minor issues addressed

**Response letter:**
- ✅ Addresses all 7 major concerns with specific section references
- ✅ Addresses all 9 minor issues
- ✅ Explains how changes address reviewer's path to weak accept
- ✅ Professional, appreciative tone

**Ready to submit!**

---

**Date completed:** April 26, 2026  
**Estimated effort:** ~8 hours (6h writing + 2h response letter)  
**Outcome:** Third revision complete, ready for NeurIPS resubmission
