#!/usr/bin/env python3
"""
Evaluation script — measures model accuracy on a labeled dataset.
Usage: python scripts/evaluate.py
"""
import json
import sys
from pathlib import Path
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    confusion_matrix, classification_report
)
from sklearn.calibration import calibration_curve
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.ml.model import get_model

EVAL_PATH = Path(__file__).parent.parent / "data" / "evaluation" / "sample_labeled.json"


def main():
    if not EVAL_PATH.exists():
        print(f"Evaluation dataset not found: {EVAL_PATH}")
        print("Create data/evaluation/sample_labeled.json with [{text, label}, ...] entries")
        sys.exit(1)

    data = json.loads(EVAL_PATH.read_text())
    texts = [d["text"] for d in data]
    true_labels = [d["label"] for d in data]

    print(f"Loaded {len(texts)} labeled examples")

    model = get_model()
    model.load()

    results = model.predict_batch(texts)
    pred_labels = [r.label for r in results]
    pred_probs = [r.probabilities.get("POSITIVE", 0.0) for r in results]

    acc = accuracy_score(true_labels, pred_labels)
    prec, rec, f1, _ = precision_recall_fscore_support(true_labels, pred_labels, average="macro", zero_division=0)
    wf1 = precision_recall_fscore_support(true_labels, pred_labels, average="weighted", zero_division=0)[2]

    print("\n=== Model Evaluation ===")
    print(f"Accuracy       : {acc:.4f}")
    print(f"Macro Precision: {prec:.4f}")
    print(f"Macro Recall   : {rec:.4f}")
    print(f"Macro F1       : {f1:.4f}")
    print(f"Weighted F1    : {wf1:.4f}")
    print("\nClassification Report:")
    print(classification_report(true_labels, pred_labels, zero_division=0))
    print("Confusion Matrix:")
    print(confusion_matrix(true_labels, pred_labels))


if __name__ == "__main__":
    main()