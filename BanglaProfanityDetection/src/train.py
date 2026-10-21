import os
import time
import torch
import numpy as np
from transformers import (
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback,
)
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from .dataset import BanglaDataset
from .model import get_tokenizer, load_model


def compute_metrics_for_trainer(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1": f1_score(labels, preds, average="weighted"),
        "precision": precision_score(labels, preds, average="weighted"),
        "recall": recall_score(labels, preds, average="weighted"),
    }


def train_model(
    model_name,
    train_texts,
    test_texts,
    train_labels,
    test_labels,
    config,
    output_dir="results",
    run_id=1,
):
    tokenizer = get_tokenizer(model_name)
    model = load_model(model_name, config.get("num_labels", 2))

    train_dataset = BanglaDataset(
        train_texts, train_labels, tokenizer, config["max_length"]
    )
    eval_dataset = BanglaDataset(
        test_texts, test_labels, tokenizer, config["max_length"]
    )

    run_output_dir = os.path.join(output_dir, f"run_{run_id}")

    training_args = TrainingArguments(
        output_dir=run_output_dir,
        num_train_epochs=config["epochs"],
        per_device_train_batch_size=config["batch_size"],
        per_device_eval_batch_size=config["batch_size"],
        learning_rate=config["learning_rate"],
        warmup_ratio=config.get("warmup_ratio", 0.1),
        weight_decay=config.get("weight_decay", 0.01),
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        logging_steps=50,
        fp16=torch.cuda.is_available(),
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        compute_metrics=compute_metrics_for_trainer,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
    )

    start_time = time.time()
    trainer.train()
    train_time = time.time() - start_time

    metrics = trainer.evaluate()
    metrics["train_time_seconds"] = train_time

    best_model_dir = os.path.join(run_output_dir, "best_model")
    trainer.save_model(best_model_dir)
    tokenizer.save_pretrained(best_model_dir)

    return metrics, best_model_dir


def train_with_multiple_runs(
    model_name,
    train_texts,
    test_texts,
    train_labels,
    test_labels,
    config,
    output_dir="results",
    num_runs=3,
):
    all_metrics = []
    for run_id in range(1, num_runs + 1):
        print(f"\n{'='*50}")
        print(f"Run {run_id}/{num_runs}")
        print(f"{'='*50}")
        metrics, model_dir = train_model(
            model_name,
            train_texts,
            test_texts,
            train_labels,
            test_labels,
            config,
            output_dir=os.path.join(output_dir, model_name.split("/")[-1]),
            run_id=run_id,
        )
        all_metrics.append(metrics)
        print(f"Run {run_id} - Accuracy: {metrics['eval_accuracy']:.4f}, "
              f"F1: {metrics['eval_f1']:.4f}")

    return all_metrics


def train_learning_curve(
    model_name,
    train_texts,
    test_texts,
    train_labels,
    test_labels,
    config,
    fractions=(0.25, 0.5, 1.0),
    output_dir="results",
):
    results = []
    n = len(train_texts)
    for frac in fractions:
        k = int(n * frac)
        print(f"\nTraining on {frac*100:.0f}% of data ({k} samples)...")
        metrics, _ = train_model(
            model_name,
            train_texts[:k],
            test_texts,
            train_labels[:k],
            test_labels,
            config,
            output_dir=os.path.join(
                output_dir, model_name.split("/")[-1], f"frac_{frac}"
            ),
        )
        metrics["fraction"] = frac
        metrics["num_samples"] = k
        results.append(metrics)
    return results
