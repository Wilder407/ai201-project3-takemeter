# Planning spec sheet for TakeMeter Fine-tuning model
## TakeMeter community description

### Community

<!-- Define community, label and why these distinctions matter to people in the community. What community did you choose and why? Why is this community a good fit for a classification task — what makes the discourse varied enough to be interesting? -->

TakeMeter evaluates running community discourse covering analysis on training plans, race strategy, nutrition, gear reviews, plus more. This community is familiar to me especially since I am currently training for the Leadville Trail Marathon. Participating in discussions connects me to the community and provides a sense of belonging. 

The online running community is a good fit for a fine-tuning model for a few reasons: The conversations cover different labels, the depth of the dataset is deep and the discourse is varied enough. Some conversations are reactions such as runner achievements or PR's, others are gear review hot takes, with others as training plan analysis based on data. 

---

## Annotated Dataset

### Labels Definitions:
<!-- What are your 2–4 labels? Define each in a complete sentence. Include 2 example posts per label. One-sentence definition and 2 concrete examples for each label. -->
 
`analysis` — the post makes a structured argument supported by evidence. Evidence may include scientific studies, statistics, historical comparison, tactical observation, or personal tracked data (e.g. training logs, race splits, biometric data over time). The claim is specific and the evidence is referenced explicitly, even if anecdotal.
`hot_take` — a bold, confident opinion stated without supporting evidence. The claim might be true, but the post asserts rather than argues. A single offhand data reference does not qualify as evidence — the argument must be built around it.
`reaction` — an immediate emotional response to a specific event. Little to no argument — the post is expressing a feeling in the moment. If insight or opinion appears, it is incidental to the emotional frame.
`inquiry` — the post is primarily asking for input, recommendations, or guidance. No strong argument is made and no strong emotion is the dominant register.
`other` — spam, incoherent posts, or content with no classifiable primary purpose. Should be rare.

### Tie-breaker rules:
1. **Label by dominant purpose, not incidental content.** A post that leads with emotion and ends with an opinion is `reaction`. A post that leads with an opinion and uses an event as context is `hot_take`.
2. **Personal tracked data counts as evidence for `analysis`**, but only when the argument is built around it — not when data is mentioned in passing to support an assertion.

### Examples:
**`analysis`**
- "I tracked my cadence over 6 months and increased it from 165 to 180 spm. My injury rate dropped to zero — higher cadence reduces injury risk."
- "Comparing Pfitzinger vs. Hansons over two training cycles: my long run pace dropped 18 sec/mile on Pfitzinger but my fatigue index was significantly higher in weeks 14–16."

**`hot_take`**
- "Zone 2 training is completely overhyped. Most recreational runners would be better off just running more."
- "Carbon plates are ruining the sport — everyone is chasing times that don't reflect real fitness."

**`reaction`**
- "Just crossed the finish line of my first marathon. I am crying. I cannot believe I did that."
- "DNF'd today at mile 23. I trained for six months and my knee just gave out. Completely devastated."

**`inquiry`**
- "Just signed up for my first ultra — has anyone run Leadville before? No idea where to start with training."
- "IT band completely gave out at mile 18. Has anyone dealt with this? How long did recovery take?"

**`other`**
- Spam posts, promotional links, or posts with no coherent content.

### Anticipated Hard Edge-cases
<!-- What type of post will be genuinely ambiguous between two labels? How will you handle it when you encounter it during annotation? -->
analysis vs hot_take boundary
### `analysis` vs. `hot_take`

| Post | Label | Reasoning |
|---|---|---|
| "Pfitzinger 18/70 is objectively the best marathon plan for sub-3 runners. I've seen it work for dozens of people in my running club." | `hot_take` | "I've seen it work" is a vague social observation, not tracked data. No argument built around evidence. |
| "I tracked my cadence over 6 months and increased it from 165 to 180 spm. My injury rate dropped to zero. Higher cadence prevents injury — full stop." | `analysis` | Tracked data over time with specific numbers. Argument is built around the evidence even if conclusion is overstated. |
| "Zone 2 is overhyped. I ran my PR on mostly tempo work and I have the Strava data to prove it." | `hot_take` | One PR mentioned in passing. Data is a footnote to an assertion, not the structure of the argument. |

### `hot_take` vs. `reaction`

| Post | Label | Reasoning |
|---|---|---|
| "Just got passed by a guy in Hokas at mile 24 of Chicago. Carbon plates are a crutch and I want nothing to do with them." | `hot_take` | The race event is context; the dominant claim is the opinion about carbon plates. |
| "DNF'd my goal race today. Honestly think 20-week plans are too long — you peak too early." | `hot_take` | The training argument is the dominant claim; the DNF is context, not the frame. |

### `reaction` vs. `inquiry`

| Post | Label | Reasoning |
|---|---|---|
| "Just signed up for my first ultra and I have no idea what I'm doing — anyone run Leadville before?" | `inquiry` | Excitement is present but the dominant purpose is seeking guidance. |
| "IT band completely gave out at mile 18. Has anyone dealt with this? How long did recovery take?" | `inquiry` | Emotion present but clearly seeking input. |

### Genuinely Hard Cases

| Post | Label | Reasoning |
|---|---|---|
|  The rule originally comes from famed exercise physiologist Stephen Seiler. When he studied elite athletes, he found that 80% of their sessions were done at low intensity. 20% of their sessions were high intensity. High intensity is anything above the first ventilatory threshold, or the top of Zone 1 in a 3-zone model. Note that the athletes he studied were typically doing more than 10 sessions per week, which maps out to 2-3 high-intensity sessions per week. This is consistent with what other research has found to be optimal.

Many people here and elsewhere incorrectly believe that the ratio applies to either time or distance in zone. Instead, it refers to the ratio of hard sessions to easy ones. Any session that includes efforts in zones 2 or 3 (again, in a 3-zone model), is classified as a “hard” session.

It is also important to note that this “rule” began as an observation. Seiler observed elite athletes behaving a certain way and wrote it down. The “rule” was not intended to be a prescription. If you run 3 days/wk including 1 hard session, you’re at 67/33. That might work for you. Many people run 5-6 days/wk with 2 hard sessions. That might be 40% hard, but it works well for many people (myself included). There are many differences between us and elite athletes. Don’t mindlessly do what they do without understanding why.

So what does this mean for us? At its simplest level, it means mostly run slow, occasionally run hard. Don’t get bogged down in the exact distribution. DEFINITELY don’t spend any time (not one single second) trying to get your time-in-zone to work out to exactly 80/20. That misses the point entirely.

It is entirely possible to be in a speed block (focusing on 200m and 400m repeats, for example) and only spend 5% of your time or distance above zone 1. This would be normal and productive.

TLDR: The going-away most important factor in endurance training is time spent training. Want to get faster? Run more. Want to run more without getting hurt or burnt out? Run slow most of the time. That’s it; that’s the whole thing." | `analysis` | While a question is posed, there is a long conversation about the merits/demerits of the technology in question |
| "It has been 13 years of running and six marathons; I figured it would be wrong to call myself a beginner any more. So, having just graduated from the moniker, I thought I'd write down a few notes from my personal experience, in case someone new might find it amusing or slightly useful. Here goes:

You are almost certainly running too fast

You get the most gains training on slow runs, especially if you are trying to build endurance. In fact, by running too fast, you are sacrificing gains. Running slower will also keeps injuries down. And "slow" is likely slower than you think. Yes, you will need speedwork and tempo runs, but you are likely overestimating their contribution to becoming fast.

Your injuries are likely less serious and less permanent than you think

I lived through a good number of them. What felt like a stress-fracture was just tendonitis. What I thought was hip-bursitis was just strained groin and hip muscles. In the end, it wasn’t the x-rays that solved them - it was rest and ice and Advil. Usual caveats apply.

Think less shoe=better

Don’t fall for that whole over-pronation nonsense. Let your feet work like they want to, and ramp up slowly. If a shoe promises to do anything more than prevent scrapes, provide just a little cushioning and maybe, look good, steer clear. Barefooting, I hear, is awesome. I have tried it but have never given it a full-fledged shot.

Think 2 Years

That’s how long it will take your body to get 80-90% of gains. It takes a while to build additional vasculature, metabolic capacity, aerobic capacity, muscle and tendon strength etc. Yes, it only takes a few weeks to get “5k ready”, but it takes longer to get the big gains. Lots of caveats - you have to train etc.

You will run races too fast and crash

There isn’t another way to learn what you are capable of and how to adjust for weather, hydration etc. So, go right ahead, crash and burn. This stuff cannot be taught.

You will run too slow and fail to make up time

Corrollary to previous section.

If you commit to running a marathon, you will

Running a marathon is more about commitment and planning than it is about innate ability, willpower, insanity or pain tolerance. You underestimate your body’s ability to adapt. It is one of the most rewarding things I have done for myself.

Enjoy the running

It's the single biggest factor of whether you will be a runner for life. Keep it fun.

" | `reaction` | Experience is cited but it is more advice than data-driven. |
| "I noticed that a difference between my Vivo Barefoots and Altra Escalante 2.0's. The Vivo's have a grippy insole which allows better traction between the foot and shoe, especially during turns. This feels more natural given how our feet grip the ground when barefoot. The Altra's are smooth and the foot slides within the upper a ton during runs; I wonder if a grippy insole could help this issue." | `reaction` | Wonder is present but the dominant purpose is sharing an insight. |

---

## Data Collection Plan

<!-- Where will you collect examples? How many per label? What will you do if a label is underrepresented after 200 examples? -->
**Source:** r/running via Reddit API (PRAW)

**Target:** 200+ posts, aiming for ~40 per label across `analysis`, `hot_take`, `reaction`, and `inquiry`. `other` will be collected opportunistically and is expected to be rare.

**Sampling strategy:** Pull from `hot`, `top`, and `new` feeds to balance engagement levels and recency.

**If a label is underrepresented after 200 examples:** Review label definitions and tiebreaker rules to check whether the boundary cases have been adequately handled. Adjust sampling strategy (e.g. target specific post flairs or keywords) before expanding the dataset.

---

## Evaluation Metrics

### Fine-tuning Pipeline
<!-- describe the model you started from, the training approach, and at least one key hyperparameter decision you made (e.g., learning rate, number of epochs, batch size). -->
**Base model:** `distilbert-base-uncased` — a lightweight, fast transformer that retains ~97% of BERT's performance at half the size, making it practical for fine-tuning on a small dataset.

**Training approach:** Add a classification head on top of DistilBERT's pooled output. Freeze the base model for the first epoch to stabilize the classifier head, then unfreeze and fine-tune end-to-end.

**Key hyperparameter decisions:**

- **Learning rate:** `2e-5` — standard for fine-tuning transformers; high enough to adapt the model, low enough to avoid catastrophic forgetting of pre-trained weights
- **Epochs:** 3–5 — with only ~200 examples, more epochs risk overfitting; monitor validation loss to early-stop
- **Batch size:** 16 — balances memory constraints with stable gradient estimates on a small dataset

### Evaluation Metrics:
**Primary metric: Macro F1** — averages F1 equally across all five labels (`analysis`, `hot_take`, `reaction`, `inquiry`, `other`). Chosen because class imbalance is likely (r/running skews toward `reaction` and `inquiry`), and accuracy alone would reward a model that ignores rare classes like `analysis`.

**Reported metrics:**
- Overall accuracy
- Per-class F1, precision, and recall (full classification report)
- Confusion matrix showing which label pairs get confused most
- At least 3 misclassified examples with written analysis of why the model failed

### Definition of Success
<!-- What performance would make this classifier genuinely useful? What would you accept as "good enough" for deployment in a real community tool? -->
This classifies is considered genuinely useful at a MacroF1 of 0.70 or above across all five labels on the held-out test set. 

At 0.70, the model reliably distinguished the core label pairs(`analysis` vs. `hot_take`, `reaction` vs. `inquiry`) well enough to asist a human moderator or researcher - not to replace human judgement, but to triage and surface patterns at scale. 

Below 0.70, the model's errors would undermine trust in its output and require too much human correction to be worth deploying. Above 0.80 on a ~200 example datset would warrant scrutiny for overfitting before claiming success. 

---

## AI Tool Plan

### Label Stress-testing
<!-- Give the AI your label definitions and edge case description, and ask it to generate 5–10 posts that sit at the boundary between two labels. If it produces posts you can't classify cleanly, your definitions need tightening — do that now, before you annotate 200 examples. -->

Label definitions were stress-tested against 10 boundary posts generated by Claude before annotation began. All 10 resolved cleanly after adding the two tiebreaker rules above. See the Anticipated Hard Edge Cases section for the full results.

### Annotation Assistance

**Pre-labeling tool:** Claude (`claude-sonnet-4-6`)

**Process:**
1. Scrape 200+ posts from r/running via PRAW
2. Feed each post to Claude with the full label definitions and tiebreaker rules
3. Claude assigns a preliminary label per post
4. Lisa reviews every label and overrides where needed
5. Final human-reviewed label is the ground truth

**Tracking table format:**

| post_id | title | body | score | ai_label | label | ai_assisted |
|---|---|---|---|---|---|---|
| Reddit post ID | Post title | Post body text | Reddit upvotes | Claude preliminary label | Final human-reviewed label | `True` for all rows in this batch |

**Disclosure note:** Every example was seen and verified by a human before being treated as ground truth. Disagreements between `ai_label` and `label` will be noted and reviewed as part of the failure analysis.


### Failure Analysis
<!-- Plan to give your list of wrong predictions to an AI tool and ask it to identify patterns before you write up your evaluation. Note what you'll look for and how you'll verify the patterns yourself. -->
**Input to AI tool:** Misclassified posts paired with their correct human-reviewed label and the model's predicted label.

**Process:**
1. Run classifier on held-out test set
2. Extract all misclassified examples into a separate CSV
3. Feed to Claude with the prompt: *"Here are posts my classifier got wrong. Each has the correct label and the predicted label. Identify patterns in where it fails — are errors concentrated between specific label pairs, post lengths, or linguistic features?"*
4. Claude returns hypothesized error patterns
5. Manually verify each pattern by reading through the examples — do not accept Claude's characterization without checking

**What to look for:**
- Which label pairs get confused most (e.g. `hot_take` → `reaction`)
- Whether errors cluster on short posts, long posts, or posts with mixed signals
- Whether boundary cases from stress-testing show up disproportionately in errors

**How to verify:**
- Spot-check at least 5 examples per pattern Claude identifies
- If a pattern does not hold up on manual review, note it as a false pattern in the writeup — that itself is a finding

---

## Evaluation Report

*To be completed after classifier training and evaluation.*

**Metrics to report:**
- Overall accuracy (both models)
- Per-class F1, precision, and recall
- Confusion matrix
- At least 3 specific misclassified examples with analysis of why the model failed
- Reflection on what the model learned vs. what was intended
