# ai201-project3-takemeter

## Data Collection

- Where data collected?

- Labeling Process

- Label Distribution (count per abel)

- 3 examples 
<!-- examples that were particularly hard to label and what was decided -->

## AI Usage disclosure 
Annotation
Every example was seen and verified by a human before being treated as ground truth
Disagreements between ai_label and label are themselves useful data — they'll likely cluster around your boundary cases and inform your failure analysis section



🎯 Baseline accuracy: 0.533  (evaluated on 30/30 parseable responses)

Per-class metrics (baseline):
              precision    recall  f1-score   support

    analysis       1.00      0.57      0.73         7
    hot_take       0.00      0.00      0.00         4
    reaction       0.50      0.42      0.45        12
     inquiry       0.50      1.00      0.67         7

    accuracy                           0.53        30
   macro avg       0.50      0.50      0.46        30
weighted avg       0.55      0.53      0.51        30

Baseline struggled with the hot_take which makes sense since I don't think that there were many heated opinions in the running forum. Many could easiy be categorized as reaction. I categorized them as hot_take since they were brief and had an opinion. 


Inlcuded weight in the training parameters to navigate lower hot_take numbers in the training set. 