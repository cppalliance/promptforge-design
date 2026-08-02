# Results

Cases: 29226 | Catalog: 9922 tools

## BAAI/bge-small-en-v1.5
- random distractors: top-1 0.929, recall@3 0.978
    - restatement: top-1 0.984, recall@3 0.997 (n=9742)
    - synonym: top-1 0.945, recall@3 0.986 (n=9742)
    - goal: top-1 0.857, recall@3 0.951 (n=9742)
- hard distractors: top-1 0.553, recall@3 0.753
    - restatement: top-1 0.764, recall@3 0.912 (n=9742)
    - synonym: top-1 0.544, recall@3 0.760 (n=9742)
    - goal: top-1 0.349, recall@3 0.586 (n=9742)
- abstention (hard regime), max coverage at false-bind budget:
    - fb<=0.01: coverage 0.07 at accuracy 0.903 (thr 0.863)
    - fb<=0.05: coverage 0.18 at accuracy 0.862 (thr 0.825)
    - fb<=0.10: coverage 0.27 at accuracy 0.822 (thr 0.805)

## sentence-transformers/all-MiniLM-L6-v2
- random distractors: top-1 0.925, recall@3 0.977
    - restatement: top-1 0.978, recall@3 0.995 (n=9742)
    - synonym: top-1 0.939, recall@3 0.986 (n=9742)
    - goal: top-1 0.857, recall@3 0.952 (n=9742)
- hard distractors: top-1 0.557, recall@3 0.754
    - restatement: top-1 0.739, recall@3 0.888 (n=9742)
    - synonym: top-1 0.554, recall@3 0.770 (n=9742)
    - goal: top-1 0.376, recall@3 0.605 (n=9742)
- abstention (hard regime), max coverage at false-bind budget:
    - fb<=0.01: coverage 0.06 at accuracy 0.912 (thr 0.790)
    - fb<=0.05: coverage 0.16 at accuracy 0.855 (thr 0.719)
    - fb<=0.10: coverage 0.25 at accuracy 0.820 (thr 0.678)
