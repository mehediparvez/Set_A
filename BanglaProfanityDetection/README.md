# Bangla Profanity & Toxic Comment Detection

A machine learning project for detecting profanity and toxic comments in Bangla text using transformer-based models (BanglaBERT, XLM-RoBERTa), LLM baselines, and a library baseline.

## Project Overview

This project compares multiple approaches for Bangla toxic comment classification:

| Approach | Model | Type |
|----------|-------|------|
| Library Baseline | `better_profanity` | Rule-based word list |
| Fine-tuned Transformer | BanglaBERT (`sagorsarker/bangla-bert-base`) | Fine-tuned classifier |
| Fine-tuned Transformer | XLM-RoBERTa (`xlm-roberta-base`) | Fine-tuned classifier |
| LLM Zero-shot | Gemini Flash-Lite / Groq | Prompt-based |

## Project Structure

```
BanglaProfanityDetection/
├── README.md
├── requirements.txt
├── main.py                      # CLI entry point for full pipeline
├── Makefile                     # Automation shortcuts
├── configs/
│   └── config.yaml              # Hyperparameters and paths
├── data/
│   └── README.md                # Dataset download instructions
├── src/
│   ├── __init__.py
│   ├── dataset.py               # Dataset loading and preprocessing
│   ├── model.py                 # Model definitions
│   ├── train.py                 # Training loop with multi-run support
│   ├── evaluate.py              # Evaluation metrics and error analysis
│   ├── predict.py               # Inference utilities
│   ├── llm_baseline.py          # Groq/Gemini LLM zero-shot baseline
│   ├── visualize.py             # Publication-ready chart generation
│   ├── results.py               # Shared results format (save/load for all models)
│   └── utils.py                 # Helper functions
├── tests/
│   ├── test_dataset.py
│   ├── test_model.py
│   ├── test_evaluate.py
│   ├── test_utils.py
│   ├── test_results.py
│   └── test_llm_baseline.py
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_baseline_better_profanity.ipynb
│   ├── 03_finetune_banglabert.ipynb
│   ├── 04_finetune_xlmr.ipynb
│   ├── 05_llm_baseline.ipynb
│   └── 06_evaluation_and_visualization.ipynb
├── app/
│   └── demo.py                  # Gradio demo application
├── results/                     # Saved metrics and CSVs
└── plots/                       # Generated charts and figures
```

## Setup

### 1. Install Dependencies
```bash
cd BanglaProfanityDetection
pip install -r requirements.txt
```

### 2. Download Dataset
See `data/README.md` for dataset download instructions.

### 3. Configure
Edit `configs/config.yaml` to set paths and hyperparameters.
API keys are read from the environment: `GROQ_API_KEY` (preferred) or `GEMINI_API_KEY`.

All approaches are evaluated on the same stratified test split of `data/train.csv`
(`test_size` / `random_seed` in the config), so their scores are directly comparable.

## Running the Project

### Step 1: Data Exploration
```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```

### Step 2: Library Baseline
```bash
jupyter notebook notebooks/02_baseline_better_profanity.ipynb
```

### Step 3: Fine-tune Models (run on Kaggle/Colab with GPU)
```bash
jupyter notebook notebooks/03_finetune_banglabert.ipynb
jupyter notebook notebooks/04_finetune_xlmr.ipynb
```

### Step 4: LLM Baseline
```bash
jupyter notebook notebooks/05_llm_baseline.ipynb
```

### Step 5: Evaluation & Visualization
```bash
jupyter notebook notebooks/06_evaluation_and_visualization.ipynb
```
Notebook 06 loads whatever notebooks 02-05 saved under `results/` and plots it;
models that have not been run yet are left out.

### Step 6: Demo App
```bash
cd app
python demo.py
```

### Alternative: Run Full Pipeline via CLI
```bash
python main.py --step all        # Train + Evaluate + Baselines + Visualize
python main.py --step train      # Fine-tune BanglaBERT and XLM-R (3 runs + learning curve)
python main.py --step evaluate   # Evaluate saved fine-tuned models
python main.py --step baseline   # better_profanity library baseline
python main.py --step llm        # LLM zero-shot baseline (skipped without an API key)
python main.py --step visualize  # Generate plots from everything in results/
python main.py --step demo       # Launch Gradio demo
```

### Results Layout
Notebooks and the CLI write the same files, one directory per model
(`better_profanity`, `banglabert`, `xlmr`, `llm`):

| File | Contents | Written for |
|------|----------|-------------|
| `results/<model>/evaluation.json` | metrics, inference speed, confusion matrix, FP/FN counts | all models |
| `results/<model>/summary.json` | mean / std over the training runs | fine-tuned models |
| `results/<model>/learning_curve.json` | metrics at 25% / 50% / 100% of training data | fine-tuned models |

### Run Tests
```bash
make test
# or
cd .. && python -m pytest BanglaProfanityDetection/tests/ -v
```

## Visualizations Generated

- Model comparison bar chart (accuracy, F1, precision, recall)
- Accuracy vs. inference speed scatter plot
- Learning curves (25%, 50%, 100% training data)
- Confusion matrices for each model
- Error type distribution bar chart

## Free Tier Compute Strategy

| Need | Platform | Limits |
|------|----------|--------|
| GPU for fine-tuning | Kaggle (primary), Colab (backup) | ~30 h/week, 12-hour sessions |
| LLM inference | Groq free tier | ~1,000 req/day, 200K tokens/day |
| LLM inference (alt) | Gemini Flash-Lite | ~500 req/day on free tier |

## License

MIT
