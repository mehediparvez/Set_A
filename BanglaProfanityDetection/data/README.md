# Dataset

## Bangla Toxic Comment Dataset

### Option 1: Kaggle Dataset
Download a Bangla hate speech / toxic comment dataset from Kaggle:
- Search for "Bangla Hate Speech" or "Bangla Toxic Comment" on Kaggle
- Popular options:
  - [Bengali Hate Speech Dataset](https://www.kaggle.com/datasets/naurosahmed/bengali-hate-speech-dataset)
  - [Bangla Abusive Comment Dataset](https://www.kaggle.com/datasets)

### Option 2: GitHub Dataset
Several research groups have published Bangla toxic comment datasets:
- https://github.com/rezacsedu/Bengali-Hate-Speech-Dataset

### Expected Format

Place your dataset files here as CSV with at minimum two columns:

| Column | Description |
|--------|-------------|
| `text` | The Bangla comment text |
| `label` | 0 = non-toxic, 1 = toxic |

Example:
```csv
text,label
"এটি একটি সুন্দর মন্তব্য",0
"তুই একটা বোকা",1
```

### File Structure
After downloading, place files as:
```
data/
├── README.md          (this file)
├── train.csv          (the full labelled dataset)
└── raw/               (optional: original downloaded files)
```

Only `train.csv` is needed. Every notebook and `main.py` step splits it with
the same stratified `test_size` / `random_seed` from `configs/config.yaml`,
so all models are evaluated on exactly the same held-out test samples.
If your download already has separate train/test files, concatenate them
into `train.csv`.
