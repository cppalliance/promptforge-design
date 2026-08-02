# Results

Cases: 4440 | Catalog: 9922 tools

## BAAI/bge-small-en-v1.5
- random distractors: top-1 0.931, recall@3 0.982
    - restatement: top-1 0.982, recall@3 0.998 (n=1480)
    - synonym: top-1 0.938, recall@3 0.986 (n=1480)
    - goal: top-1 0.873, recall@3 0.963 (n=1480)
- hard distractors: top-1 0.531, recall@3 0.742
    - restatement: top-1 0.747, recall@3 0.904 (n=1480)
    - synonym: top-1 0.507, recall@3 0.742 (n=1480)
    - goal: top-1 0.339, recall@3 0.580 (n=1480)
- abstention (hard regime), max coverage at false-bind budget:
    - fb<=0.01: coverage 0.07 at accuracy 0.902 (thr 0.857)
    - fb<=0.05: coverage 0.17 at accuracy 0.830 (thr 0.823)
    - fb<=0.10: coverage 0.25 at accuracy 0.805 (thr 0.804)

## sentence-transformers/all-MiniLM-L6-v2
- random distractors: top-1 0.919, recall@3 0.975
    - restatement: top-1 0.972, recall@3 0.995 (n=1480)
    - synonym: top-1 0.926, recall@3 0.983 (n=1480)
    - goal: top-1 0.860, recall@3 0.948 (n=1480)
- hard distractors: top-1 0.543, recall@3 0.746
    - restatement: top-1 0.722, recall@3 0.878 (n=1480)
    - synonym: top-1 0.545, recall@3 0.756 (n=1480)
    - goal: top-1 0.362, recall@3 0.603 (n=1480)
- abstention (hard regime), max coverage at false-bind budget:
    - fb<=0.01: coverage 0.06 at accuracy 0.902 (thr 0.781)
    - fb<=0.05: coverage 0.17 at accuracy 0.853 (thr 0.711)
    - fb<=0.10: coverage 0.25 at accuracy 0.806 (thr 0.671)
