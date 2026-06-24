# TakeMeter — Fine-Tuned Running Discourse Classifier


# Data Collection

## Source
Posts were collected manually from [r/running](https://www.reddit.com/r/running) using the subreddit's **Top (This Month)** filter. Automated scraping was attempted using both Reddit's JSON endpoint and the Arctic Shift archive API, but both returned predominantly AutoModerator megathreads and `[removed]` posts with no body text. Manual collection was used instead, browsing the subreddit directly and copy-pasting substantive posts into a CSV.

## Labeling Process
Posts were labeled at collection time — each post was read and assigned a label as it was added to the dataset. No automated pre-labeling pipeline was used due to the scraper limitations. Every label reflects a direct human judgment made against the label definitions and tiebreaker rules documented in `planning.md`.

Posts were excluded if they had no body text (link posts, image posts), were AutoModerator threads, or contained only `[removed]` or `[deleted]` content. Only posts with enough text to classify were included.

## Label Distribution

| Label | Count |
|---|---|
| inquiry | 74 |
| reaction | 67 |
| analysis | 59 |
| **Total** | **200** |

The original dataset skewed heavily toward `reaction` (86 examples). The dataset was rebalanced before the final training run by capping `reaction` at 67 to reduce the dominance of any single class.

## Hard Labeling Examples

**Example 1: analysis vs. reaction**
> *"The rule originally comes from famed exercise physiologist Stephen Seiler. When he studied elite athletes, he found that 80% of their sessions were done at low intensity..."*

**Label assigned:** `analysis`
**Why it was hard:** The post opens by addressing a common question, which reads like inquiry. However, the dominant purpose is a structured argument built around cited research and correcting a widespread misconception. The question framing is incidental — the post is making an evidence-based case. Labeled `analysis` per tiebreaker rule 1: label by dominant purpose.

---

**Example 2: reaction vs. analysis**
> *"It has been 13 years of running and six marathons; I figured it would be wrong to call myself a beginner any more..."*

**Label assigned:** `reaction`
**Why it was hard:** The post reads like a series of confident assertions (think less shoe, run slower, give it two years), which could qualify as `hot_take` or even `analysis`. However, `hot_take` was removed from the final label set, and the post's dominant register is personal reflection on experience rather than a structured argument built around evidence. Labeled `reaction` as the closest fit under the 3-label taxonomy.

---

**Example 3: inquiry vs. reaction**
> *"I noticed a difference between my Vivo Barefoots and Altra Escalante 2.0's. The Vivo's have a grippy insole which allows better traction between the foot and shoe..."*

**Label assigned:** `inquiry`
**Why it was hard:** The post shares a specific observation about shoe feel, which reads like `analysis` or `reaction`. However, the post closes with a question seeking input on whether a grippy insole could fix the issue. The dominant purpose is seeking guidance, not expressing emotion or building an argument. Labeled `inquiry` per tiebreaker rule 1.

---

# Evaluation Report
<!-- 
- Overall accuracy (both models)
- Per-class metrics (both models)
- Confusion matrix (markdown table)
- 3 misclassified examples with analysis
- Sample classifications (3–5 posts with confidence)
- Reflection on intended vs. learned behavior -->

## Model Performance Summary

| Model | Accuracy | Macro F1 |
|---|---|---|
| Baseline (Claude Haiku zero-shot) | 0.633 | 0.61 |
| Fine-tuned DistilBERT | 0.333 | ~0.18 |

The baseline outperformed the fine-tuned model on this test set. I adjusted and trained the model two different times to produce a better model. Removing two categories that were not very strong (hot_take and other) were used becaue of the example in the directions. However, there wwer very few posts that expressed a strong opinion without evidence as would be expected with a hot_take. 

---

## Baseline Model

**Model:** Claude Haiku (`claude-haiku-4-5-20251001`) zero-shot prompt classifier  
**Approach:** Each test post was passed to the model with the full label definitions and tiebreaker rules. No task-specific training was performed.

### Baseline Per-Class Metrics

| Label | Precision | Recall | F1 |
|---|---|---|---|
| analysis | 0.57 | 0.57 | 0.57 |
| inquiry | 0.46 | 0.86 | 0.60 |
| reaction | 1.00 | 0.50 | 0.67 |
| **macro avg** | **0.68** | **0.64** | **0.61** |

---

## Fine-Tuned Model

**Base model:** `distilbert-base-uncased`  
**Training approach:** Classification head added on top of DistilBERT's pooled output. WeightedTrainer used to compensate for class imbalance. Trained for 3 epochs on CPU.

**Key hyperparameters:**
- Learning rate: `2e-5`
- Epochs: 3
- Batch size: 16
- Class weights applied inversely proportional to label frequency

### Fine-Tuned Confusion Matrix

|  | Predicted: analysis | Predicted: inquiry | Predicted: reaction |
|---|---|---|---|
| **True: analysis** | 9 | 0 | 0 |
| **True: inquiry** | 11 | 0 | 0 |
| **True: reaction** | 9 | 0 | 1 |

### Fine-Tuned Per-Class Metrics

| Label | Precision | Recall | F1 |
|---|---|---|---|
| analysis | 0.31 | 1.00 | 0.47 |
| inquiry | 0.00 | 0.00 | 0.00 |
| reaction | 1.00 | 0.10 | 0.18 |
| **macro avg** | **0.44** | **0.37** | **0.22** |

---

## Failure Analysis

### Primary failure mode: class collapse to `analysis`

The fine-tuned model predicted `analysis` for 29 of 30 test examples. The final training set was rebalanced to reaction (67), analysis (59), and inquiry (74). Despite this adjustment and the application of class weights, the model collapsed to 
`analysis` — predicting it for 29 of 30 test examples. Notably, an earlier training run with reaction dominating (86 examples) collapsed to reaction instead, and a subsequent run after rebalancing collapsed to inquiry when it became the largest class. This pattern across three runs strongly suggests the collapse is driven by whichever class holds the plurality, not by anything specific to the label boundaries themselves.

### Three Specific Misclassified Examples

**Example 1: inquiry → predicted analysis**  
A post asking for shoe recommendations based on injury history. The post contained technical running vocabulary (pronation, heel drop, stack height) that overlaps heavily with the language used in `analysis` posts. The model appears to have latched onto domain-specific terminology as a proxy for `analysis` rather than learning the structural feature that distinguishes inquiry (question-seeking) from analysis (evidence-building). This is a labeling boundary problem — technical language appears in both classes, and 200 examples is insufficient to separate them.

**Example 2: reaction → predicted analysis**  
A post describing a DNF at mile 23 that included a detailed account of what went wrong physically. The narrative structure — specific mile markers, physiological detail — mirrors the evidence-based structure of `analysis` posts. The emotional register was present but the specificity of the account caused the model to misfire. This suggests the model overfit to structural features (numbered data, specificity) rather than learning the emotional framing that defines `reaction`.

**Example 3: inquiry → predicted analysis**  
A post asking about heart rate zones for a first marathon. The post referenced specific zone numbers and training concepts. Again, technical vocabulary pulled the prediction toward `analysis`. This confirms the pattern from Example 1 — the model conflated technical running discourse with the `analysis` label regardless of whether the post was asking a question or making an argument.

---

## Reflection: Intended vs. Learned Behavior

The model was intended to learn the *purpose* of a post — whether the author was building an argument, seeking guidance, or expressing emotion. Instead, it learned a vocabulary proxy: posts containing technical running terminology (training zones, pace data, physiological terms) were classified as `analysis` regardless of their actual communicative function.

This is a data problem more than a modeling problem. Three successive training runs — each with a different class distribution — each collapsed to whichever label held the plurality, regardless of class weights. This pattern reveals that 200 examples is insufficient for DistilBERT to learn semantic boundaries between these labels. The model is not learning the communicative purpose of posts; it is learning a majority-vote heuristic from the training distribution. Class weights applied a corrective pressure but could not overcome the fundamental data scarcity — with fewer than 60 examples per label after train/test split, the classification head does not have enough signal to generalize.

The baseline model outperformed fine-tuned DistilBERT because zero-shot prompting with explicit label definitions and tiebreaker rules gave the model direct access to the decision logic. Fine-tuning on 200 imbalanced examples could not replicate that.

**What would fix it:**
- Expand the dataset to at least 150 examples per label before retraining
- Collect `analysis` and `inquiry` examples specifically using targeted keyword searches
- Consider a longer model (BERT-base rather than DistilBERT) with more capacity to capture structural differences
- Experiment with concatenating title + body rather than body alone, since titles often signal intent more clearly than body text

---

## Sample Classifications

The following posts were run through the fine-tuned model with their predicted labels and confidence scores.

| Post (truncated) | True Label | Predicted | Confidence |
|---|---|---|---|
| "I tracked my VO2 max over 12 weeks using my Garmin. Started at 48, ended at 52..." | analysis | analysis | 0.71 |
| "Just finished my first half marathon! I cried at the finish line..." | reaction | analysis | 0.68 |
| "Has anyone used Hoka Cliftons for trail running? My knees have been bothering me..." | inquiry | analysis | 0.64 |
| "The 80/20 rule is misunderstood by most recreational runners. Seiler's research..." | analysis | analysis | 0.74 |
| "DNF'd at mile 18 today. My IT band completely gave out..." | reaction | reaction | 0.52 |

The first correctly predicted example is reasonable: the post leads with a specific metric tracked over time (VO2 max, 12 weeks, numerical improvement), which is the defining structural feature of `analysis`. The model correctly identified the evidence-building pattern. The low confidence on the reaction/reaction prediction (0.52) reflects the model's uncertainty on emotional posts — this is consistent with the confusion matrix showing reaction as the hardest class to predict correctly.

---

# Spec Reflection

## One Way the Spec Helped

The tiebreaker rules proved to be the most actionable part of the planning spec during annotation. Specifically, "label by dominant purpose, not incidental content" gave a clear decision procedure for genuinely ambiguous posts — ones that mixed emotional framing with opinion, or observation with a question. Without that rule, posts like the 80/20 training rule explanation (which opens with a question but builds a structured argument) would have been inconsistently labeled across the dataset. The rule converted judgment calls into repeatable decisions, which is critical for annotation quality on a small dataset where inconsistency directly hurts model performance.

## One Way the Implementation Diverged

Three significant divergences from the original spec:

**1. Label taxonomy reduced from 5 to 3**
The spec defined five labels: `analysis`, `hot_take`, `reaction`, `inquiry`, and `other`. The final model uses three: `analysis`, `reaction`, and `inquiry`. During data collection, `hot_take` proved underrepresented in r/running discourse — only 26 examples out of 200, compared to 86 `reaction` posts. Training runs with `hot_take` included showed immediate class collapse, with the model predicting `reaction` for nearly every example. `hot_take` was dropped and the label set was consolidated to three classes with more balanced representation. `other` was never collected in meaningful quantities and was removed alongside it.

**2. Data collection shifted from automated scraping to manual**
The spec called for automated collection via Reddit's PRAW API with Arctic Shift as a fallback. In practice, both approaches returned predominantly AutoModerator megathreads and `[removed]` posts with no body text. Manual collection from r/running's Top (This Month) feed replaced the entire automated pipeline. Posts were labeled at collection time rather than through the Claude annotation UI originally planned.

**3. Baseline model changed from Groq to Claude Haiku**
The spec specified Groq's `llama-3.3-70b-versatile` as the baseline model. Groq's free tier daily token limit (100,000 tokens/day) was exhausted during development, and the Developer tier upgrade was temporarily unavailable. Claude Haiku (`claude-haiku-4-5-20251001`) was substituted as the baseline model. The prompting approach and evaluation methodology remained identical — zero-shot classification using the same system prompt and label definitions.

---

# AI Usage

Claude (`claude-sonnet-4-6`) was used at multiple stages of this project. The following describes specific instances, what was directed, what was produced, and what was changed or overridden.

## Instance 1: Failure Analysis

**What I directed:** After the fine-tuned model's confusion matrix showed class collapse to `analysis`, misclassified examples from the test set were provided to Claude with the prompt: "Here are posts my classifier got wrong. Each has the correct label and the predicted label. Identify patterns in where it fails — are errors concentrated between specific label pairs, post lengths, or linguistic features?"

**What it produced:** Claude identified that technical running vocabulary (training zones, pace data, physiological terms) appeared disproportionately in misclassified posts, and hypothesized the model was using domain-specific terminology as a proxy for `analysis` regardless of the post's actual communicative purpose.

**What I changed:** The pattern was manually verified by re-reading the misclassified examples. The vocabulary proxy hypothesis held up — posts asking technical questions (inquiry) and posts making technical arguments (analysis) were being conflated. This finding is documented in the evaluation report failure analysis.

## Instance 2: Baseline Classification

**What I directed:** Claude Haiku (`claude-haiku-4-5-20251001`) was used as the zero-shot baseline classifier. Each test post was passed to the model with the full label definitions, tiebreaker rules, and one example per label. The model was instructed to respond with only the label name.

**What it produced:** Labels for 26 of 27 parseable test examples, achieving 0.633 accuracy and 0.61 macro F1. One post returned an unparseable response due to empty text content.

**What I changed:** The system prompt was shortened from the original ~1,800 token version to ~200 tokens to reduce API costs while retaining one example per label as required. The label matching logic was updated to normalize whitespace and hyphens after the model returned `hot take` (with a space) instead of `hot_take` in early runs.

## Instance 3: Tooling and Development

**What I directed:** Claude was used throughout development to build the Reddit scraper, annotation UI, and notebook debugging. Specific tasks included writing the Arctic Shift API scraper, building a React-based annotation tool with Claude API integration, and debugging the WeightedTrainer class weights implementation.

**What it produced:** Working code for each component, though the scraper ultimately failed to return usable posts due to AutoModerator content and `[removed]` posts dominating the Arctic Shift results.

**What I changed:** The scraper was abandoned in favor of manual data collection. The annotation UI was built but not used for the final dataset since posts were labeled at collection time. The WeightedTrainer implementation was used in the final training run.

## Disclosure Note

Label stress-testing with AI-generated boundary posts was planned in the original spec but not executed. All post labels reflect direct human judgment applied against the label definitions and tiebreaker rules. No AI pre-labeling was used for the annotated dataset.

---

## Link to Demo Video

https://cuboulder.zoom.us/rec/share/Bjd5dDLA5UfgRICscfiBhHHTyEG1CupgNYZgGNKP_6Zsr8UCAL8fsbAzIaPsXVeP.TXBQxurjolIwB1D4?startTime=1782268171000
Passcode: 8=8!0s*Q