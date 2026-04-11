# Paper Restructuring Plan — Round 11 Revision

## Overview

Addresses reviewer W1 (mock dominates paper) by:
1. **Trimming appendix** from 265 lines (A.1-A.9) to ~120 lines (A.1-A.3)
2. **Expanding real-LLM sections** with 3 new experiment subsections
3. **Reframing narrative** to center real-LLM findings, treat mock as validation only

---

## Part 1: Appendix Consolidation (265 → ~120 lines)

### Current Structure (9 subsections, 265 lines)

```
A.1  Example Transcripts (mock)              52 lines  [3 examples]
A.2  Threshold Sweep (mock)                  39 lines  [2 tables + explanation]
A.3  Baseline Comparison (mock)              21 lines  [1 table]
A.4  Diverse Claim Types (mock)              18 lines  [1 table]
A.5  Core Detection Accuracy (mock)          23 lines  [1 table]
A.6  Feature Distributions (mock)            22 lines  [1 table + CV text]
A.7  Adaptive vs Fixed (mock)                18 lines  [1 table]
A.8  Question Type Diagnosticity (mock)      19 lines  [1 table]
A.9  Confidence Trajectory (mock)            21 lines  [1 table + failure analysis]
-----
Total: 265 lines
```

### Target Structure (3 subsections, ~120 lines)

```
A.1  Example Interrogation Transcripts                    ~50 lines
     - Keep: 2 examples (1 correct truthful, 1 misclassified lying)
     - Cut: Transcript 2 (correctly detected lie — redundant)
     - Trim: Reduce commentary, focus on behavioral patterns

A.2  Mock Validation Summary                              ~50 lines
     - Merge: Core accuracy (A.5), feature distributions (A.6), 
              baseline comparison (A.3), adaptive vs fixed (A.7)
     - Keep: 2-3 key tables (feature separability, accuracy summary)
     - Cut: Verbose explanations already in main body
     - Cut: A.4 (diverse claims), A.8 (question types), A.9 (confidence trajectory)

A.3  Claim Construction and Experimental Design            ~20 lines
     - NEW section addressing reviewer minor concern
     - How claims generated (factual vs personal)
     - Ground truth assignment
     - Balanced sampling strategy
     - Examples of claim pairs for prompt-equalized control
-----
Target: ~120 lines
```

### Specific Deletions

**Delete entirely:**
- A.4: Diverse claim types (already mentioned in main body §4.9)
- A.7: Adaptive vs fixed table (redundant with main body Table 1)
- A.8: Question type diagnosticity (not critical)
- A.9: Confidence trajectory table (failure analysis already in main body)

**Merge/consolidate:**
- A.2: Keep 1 threshold sweep table (the min_questions=2 one), drop the other
- A.3: Baseline comparison → merge into A.2 as 1-2 rows in summary table
- A.5: Core accuracy → already in main body Table 1, just reference it
- A.6: Feature distributions → keep table, trim CV text (1 sentence sufficient)

---

## Part 2: Experiments Section Expansion

### Current Structure (§4.1-4.9)

```
4.1  Experimental Setup                      (26 lines)
4.2  Mock Pipeline Validation                (18 lines + 1 table)
4.3  Real LLM Pilot (Claude Haiku n=9)       (30 lines + 1 table)
4.4  Ollama Llama 3.2 3B (n=98)              (52 lines + 2 tables)
4.5  Recalibration on Real LLM Data          (26 lines + 1 table)
4.6  Cross-Model: Mistral 7B (n=100)         (28 lines + 1 table)
4.7  Zero-Shot LLM Judge Baseline            (24 lines + 1 table)
4.8  Adaptive Stopping Threshold Sweep       (27 lines + 1 table)
4.9  Claim Category Breakdown (mock)         (2 lines, brief)
```

### Target Structure (add 3 new subsections)

**NEW SECTIONS TO ADD:**

**§4.X — Prompt-Equalized Control (EXP-1) [CRITICAL]**
```
Position: After §4.6 (Mistral) or as §4.4b (after Llama, before recalibration)
Purpose: Address W2 (prompt confound)
Content (~30 lines + 1 table):
  - Design: Neutral prompt for both conditions
  - Truth condition uses true factual claims
  - Deceptive condition uses modified-false versions
  - Model never told to lie — signal arises from knowledge conflict
  - Results table: Overall, Truthful, Deceptive accuracy
  - Feature separability comparison (original vs equalized)
  - Interpretation:
    * If accuracy ≈ original → genuine behavioral signal (strong)
    * If accuracy drops → partial instruction artifact (nuanced)
    * If accuracy ≈ chance → prompt-driven (honest negative)
```

**§4.Y — Claude Haiku Evaluation at Scale (EXP-2)**
```
Position: Replace/extend §4.3 (current n=9 pilot)
Purpose: Address W3 (need capable model, adequate n)
Content (~35 lines + 2 tables):
  - Expand from n=9 pilot to n=100
  - Mock-trained results
  - Recalibration results (LOO)
  - Zero-shot baseline
  - Feature separability analysis
  - Comparison to Llama/Mistral (model capability effects)
  - Addresses "models too small" concern with frontier-adjacent model
```

**§4.Z — Enhanced Zero-Shot Baselines (EXP-3)**
```
Position: Expand §4.7 (replace simple zero-shot section)
Purpose: Address W7 (zero-shot baseline underdeveloped)
Content (~40 lines + 2 tables):
  - Three variants tested:
    1. Original (simple direct judgment)
    2. Chain-of-thought (guided feature analysis)
    3. Few-shot (2 labeled examples)
  - Results on both Llama n=98 and Mistral n=100
  - Comparison table: all 3 variants vs recalibrated pipeline
  - Analysis: which optimization closes gap most?
  - Best zero-shot vs pipeline: quantify remaining advantage
  - Validates structured pipeline contribution
```

### Section Ordering Options

**Option A (by model):**
```
4.1  Setup
4.2  Mock validation
4.3  Claude Haiku n=100 (EXP-2) [EXPANDED from pilot]
4.4  Llama 3.2 3B (n=98)
4.5  Mistral 7B (n=100)
4.6  Prompt-Equalized Control (EXP-1) [NEW — tested on Mistral]
4.7  Recalibration (all models)
4.8  Enhanced Zero-Shot Baselines (EXP-3) [NEW — replaces simple §4.7]
4.9  Adaptive Stopping Threshold Sweep
```

**Option B (by method):**
```
4.1  Setup
4.2  Mock validation
4.3  Ollama Evaluation (Llama 3B, Mistral 7B)
4.4  Prompt-Equalized Control (EXP-1) [NEW]
4.5  Real LLM Evaluation (Claude Haiku n=100, EXP-2) [EXPANDED]
4.6  Recalibration
4.7  Enhanced Zero-Shot Baselines (EXP-3) [NEW]
4.8  Adaptive Stopping Threshold Sweep
```

**Recommended: Option A** — keeps model-specific sections together, easier to follow.

---

## Part 3: Narrative Reframing (Discussion/Conclusion)

### Discussion.tex Changes

**Add §5.X: Recalibration Does Not Undermine Interrogation (W4)**
```
Position: After main findings, before limitations
Content (~15 lines):
  - Interrogation generates raw multi-turn behavioral signal (5 features × N turns)
  - Without probing, no features exist to classify
  - Recalibration adjusts decision boundary, not measurement instrument
  - Single-question baseline (59%) shows interrogation depth matters
  - Analogy: medical test requires calibration for population, but still measures real biomarkers
```

**Add §5.Y: Adaptive Stopping Value (W6)**
```
Position: Within efficiency discussion
Content (~10 lines):
  - Reframe as: "65-72% reduction in interrogation cost (2.20-2.56 vs 8.0 questions)"
  - Cost reduction with identical accuracy on real data
  - Mock setting: stopping vacuous (always 2Q)
  - Real LLM setting: genuine modulation (2.2-2.6Q depending on τ)
  - Value proposition: efficiency gain at no accuracy cost
```

**Add §5.Z: Feature Extractor Leakage Discussion (Q4)**
```
Position: In limitations or methods discussion
Content (~8 lines):
  - Concern: LOO may overestimate if extractor biases are correlated across trials
  - Evidence against: 5-fold CV (92.8% ± 2.5%) consistent with LOO (93.9%)
  - If leakage substantial, 5-fold should drop (test set has no overlap)
  - Stable performance across CV schemes suggests correlated extraction biases minor
  - Future: test with different extractor architectures
```

### Abstract Updates

**Current abstract issues:**
- Leads with mock results (93% accuracy, 75% fewer questions)
- Real-LLM results appear later, less prominent
- Doesn't mention prompt-equalized control

**Target abstract structure:**
```
1. Problem statement (detecting deceptive behavior in LLMs)
2. ADAGE framework (adaptive interrogation for behavioral mode classification)
3. Real-LLM results FIRST:
   - Llama 3.2 3B: 61.2% mock-trained → 93.9% recalibrated (n=98)
   - Mistral 7B: 79.0% mock-trained → 100% recalibrated (n=100)
   - Claude Haiku: [results from EXP-2, n=100]
4. Prompt-equalized control: [accuracy with neutral prompts for both conditions]
5. Zero-shot comparison: recalibrated outperforms best zero-shot by [X] pp
6. Mock validation: 93% accuracy using 75% fewer questions (pipeline correctness)
7. Framing caveat: behavioral mode classification under roleplay, see §5.2 for limitations
```

---

## Part 4: Implementation Checklist

### Phase 1: After EXP-1/2/3 Complete

- [ ] Run recalibration on EXP-1 (prompt-equalized Mistral data)
- [ ] Run recalibration on EXP-2 (Claude Haiku n=100 data)
- [ ] Run EXP-3 on Llama n=98 and Mistral n=100 saved transcripts
- [ ] Compute comparison metrics (original vs equalized, all zero-shot variants)
- [ ] Generate all new tables

### Phase 2: Appendix Trimming

- [ ] Edit appendix.tex:
  - [ ] A.1: Delete Transcript 2, trim commentary to ~50 lines
  - [ ] A.2: Merge A.2, A.3, A.5, A.6, A.7 into one section (~50 lines)
  - [ ] A.3: Write new claim construction section (~20 lines)
  - [ ] Delete old A.4, A.8, A.9

### Phase 3: Experiments Expansion

- [ ] Edit experiments.tex:
  - [ ] Expand §4.3 (Claude Haiku) with n=100 results
  - [ ] Add §4.6 (Prompt-equalized control) after Mistral
  - [ ] Replace §4.7 with enhanced zero-shot section
  - [ ] Update §4.5 (recalibration) to include all 3 models

### Phase 4: Discussion/Abstract Updates

- [ ] Edit discussion.tex:
  - [ ] Add recalibration defense paragraph (W4)
  - [ ] Add adaptive stopping value framing (W6)
  - [ ] Add feature leakage discussion (Q4)
- [ ] Edit abstract.tex:
  - [ ] Reorder: real-LLM results first, mock last
  - [ ] Add prompt-equalized result
  - [ ] Update zero-shot comparison with enhanced variants
  - [ ] Add Claude Haiku n=100 result

### Phase 5: Minor Fixes

- [ ] methodology.tex: Add claim construction paragraph
- [ ] Reduce redundancy across sections (deduplicate result restatements)
- [ ] Update introduction to reference new experiments
- [ ] Verify all cross-references (section numbers will shift)

---

## Expected Outcomes

**Page count:** Current paper is ~20-24 pages. Changes:
- Appendix trimming: -3 pages
- New experiment sections: +3 pages
- Net change: ≈ same length, but rebalanced toward real-LLM content

**Narrative shift:**
- Mock becomes "validation of pipeline correctness" (minor role)
- Real-LLM becomes "empirical findings" (major role)
- Prompt-equalized control becomes "critical robustness check" (centerpiece for W2)
- Enhanced baselines become "comparison to optimized alternatives" (addresses W7)

**Reviewer concerns addressed:**
- W1: Mock no longer dominates (appendix trimmed, real-LLM expanded)
- W2: Prompt-equalized control directly tests instruction artifact
- W3: Claude Haiku n=100 provides capable model at scale
- W4: Recalibration defense added to discussion
- W6: Adaptive stopping reframed as efficiency gain
- W7: Enhanced zero-shot baselines test optimized alternatives
- Q4: Feature leakage addressed with 5-fold CV comparison

---

## Timeline Estimate

**Implementation time:**
- Experiments running: EXP-1 ~8h, EXP-2 ~4h (in progress)
- EXP-3 + analysis: ~2-3 hours
- Appendix editing: 2-3 hours
- Experiments section editing: 3-4 hours
- Discussion/abstract updates: 1-2 hours
- **Total: ~1 day after experiments complete**

**Critical path:**
1. Wait for EXP-1 (Mistral prompt-equalized, ~8h remaining)
2. Wait for EXP-2 (Claude Haiku n=100, ~4h remaining)
3. Run EXP-3 (enhanced zero-shot, ~2h)
4. Run all recalibrations + analyses (~1h)
5. Edit paper (~6-8h)
6. Review, compile, verify cross-refs (~2h)

**Estimated completion:** ~24 hours from now (assuming experiments succeed)
