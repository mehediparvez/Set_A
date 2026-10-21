"""
Command-line entry point for the Bangla Profanity Detection pipeline.

Usage:
    python main.py --step all          # Run full pipeline
    python main.py --step train        # Train models only
    python main.py --step evaluate     # Evaluate trained models
    python main.py --step visualize    # Generate plots from saved results
    python main.py --step demo         # Launch Gradio demo
"""

import argparse
import os
import sys
import json

from src.utils import load_config, save_metrics, ensure_dirs
from src.dataset import load_dataset
from src.train import train_model, train_with_multiple_runs, train_learning_curve
from src.evaluate import evaluate_model, aggregate_runs, get_confusion_matrix, analyze_errors
from src.model import load_trained_model, LABEL_MAP
from src.visualize import generate_all_plots


def step_train(config):
    data_cfg = config["data"]
    train_texts, test_texts, train_labels, test_labels = load_dataset(
        data_cfg["train_path"],
        text_column=data_cfg["text_column"],
        label_column=data_cfg["label_column"],
        test_size=data_cfg["test_size"],
        random_seed=data_cfg["random_seed"],
    )
    print(f"Loaded {len(train_texts)} train, {len(test_texts)} test samples")

    results_dir = config["paths"]["results"]
    num_runs = config["training"]["num_runs"]

    for key in ["banglabert", "xlmr"]:
        model_cfg = config["models"][key]
        model_name = model_cfg["name"]
        print(f"\n{'='*60}")
        print(f"Training {model_name} ({num_runs} runs)")
        print(f"{'='*60}")

        all_metrics = train_with_multiple_runs(
            model_name,
            train_texts, test_texts,
            train_labels, test_labels,
            model_cfg,
            output_dir=results_dir,
            num_runs=num_runs,
        )
        summary = aggregate_runs(all_metrics)
        save_metrics(summary, os.path.join(results_dir, key, "summary.json"))
        save_metrics(all_metrics, os.path.join(results_dir, key, "all_runs.json"))
        print(f"\n{key} summary: F1={summary['eval_f1']['mean']:.4f} "
              f"(+/- {summary['eval_f1']['std']:.4f})")

        print(f"\nTraining learning curve for {model_name}...")
        lc_results = train_learning_curve(
            model_name,
            train_texts, test_texts,
            train_labels, test_labels,
            model_cfg,
            output_dir=results_dir,
        )
        save_metrics(lc_results, os.path.join(results_dir, key, "learning_curve.json"))


def step_evaluate(config):
    data_cfg = config["data"]
    train_texts, test_texts, train_labels, test_labels = load_dataset(
        data_cfg["train_path"],
        text_column=data_cfg["text_column"],
        label_column=data_cfg["label_column"],
        test_size=data_cfg["test_size"],
        random_seed=data_cfg["random_seed"],
    )

    results_dir = config["paths"]["results"]
    all_results = {}

    for key in ["banglabert", "xlmr"]:
        model_cfg = config["models"][key]
        best_model_dir = os.path.join(results_dir, model_cfg["name"].split("/")[-1], "run_1", "best_model")

        if not os.path.exists(best_model_dir):
            print(f"Skipping {key}: no trained model at {best_model_dir}")
            continue

        print(f"\nEvaluating {key}...")
        model, tokenizer = load_trained_model(best_model_dir)
        import torch
        if torch.cuda.is_available():
            model = model.cuda()

        metrics, preds = evaluate_model(model, tokenizer, test_texts, test_labels)
        cm = get_confusion_matrix(test_labels, preds)
        errors = analyze_errors(test_texts, test_labels, preds)

        all_results[key] = {
            "metrics": metrics,
            "confusion_matrix": cm.tolist(),
            "errors": {
                "false_positive": int((errors["error_type"] == "false_positive").sum()) if len(errors) > 0 else 0,
                "false_negative": int((errors["error_type"] == "false_negative").sum()) if len(errors) > 0 else 0,
            },
        }
        save_metrics(all_results[key], os.path.join(results_dir, key, "evaluation.json"))
        print(f"{key}: Accuracy={metrics['accuracy']:.4f}, F1={metrics['f1']:.4f}")

    return all_results


def step_visualize(config):
    results_dir = config["paths"]["results"]
    plots_dir = config["paths"]["plots"]
    ensure_dirs(plots_dir)

    comparison_results = {}
    curves = {}
    cm_dict = {}
    error_counts = {}

    for key in ["banglabert", "xlmr"]:
        summary_path = os.path.join(results_dir, key, "summary.json")
        if os.path.exists(summary_path):
            with open(summary_path) as f:
                summary = json.load(f)
            display_name = "BanglaBERT" if key == "banglabert" else "XLM-RoBERTa"
            comparison_results[display_name] = {
                "accuracy": summary.get("eval_accuracy", {}).get("mean", 0),
                "accuracy_std": summary.get("eval_accuracy", {}).get("std", 0),
                "f1": summary.get("eval_f1", {}).get("mean", 0),
                "f1_std": summary.get("eval_f1", {}).get("std", 0),
                "precision": summary.get("eval_precision", {}).get("mean", 0),
                "precision_std": summary.get("eval_precision", {}).get("std", 0),
                "recall": summary.get("eval_recall", {}).get("mean", 0),
                "recall_std": summary.get("eval_recall", {}).get("std", 0),
                "samples_per_second": summary.get("samples_per_second", {}).get("mean", 0),
            }

        lc_path = os.path.join(results_dir, key, "learning_curve.json")
        if os.path.exists(lc_path):
            with open(lc_path) as f:
                display_name = "BanglaBERT" if key == "banglabert" else "XLM-RoBERTa"
                curves[display_name] = json.load(f)

        eval_path = os.path.join(results_dir, key, "evaluation.json")
        if os.path.exists(eval_path):
            with open(eval_path) as f:
                eval_data = json.load(f)
            display_name = "BanglaBERT" if key == "banglabert" else "XLM-RoBERTa"
            import numpy as np
            cm_dict[display_name] = np.array(eval_data["confusion_matrix"])
            error_counts[display_name] = eval_data["errors"]

    if comparison_results:
        generate_all_plots(comparison_results, curves, cm_dict, error_counts, plots_dir)
    else:
        print("No results found. Run training and evaluation first.")


def step_demo():
    from app.demo import demo
    demo.launch(server_name="0.0.0.0", server_port=7860)


def main():
    parser = argparse.ArgumentParser(description="Bangla Profanity Detection Pipeline")
    parser.add_argument(
        "--step",
        choices=["train", "evaluate", "visualize", "demo", "all"],
        required=True,
        help="Pipeline step to run",
    )
    parser.add_argument("--config", default="configs/config.yaml", help="Config file path")
    args = parser.parse_args()

    config = load_config(args.config)
    ensure_dirs(config["paths"]["results"], config["paths"]["plots"])

    if args.step in ("train", "all"):
        step_train(config)

    if args.step in ("evaluate", "all"):
        step_evaluate(config)

    if args.step in ("visualize", "all"):
        step_visualize(config)

    if args.step == "demo":
        step_demo()


if __name__ == "__main__":
    main()
