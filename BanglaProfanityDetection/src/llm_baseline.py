import os
import re
import time
import json

from .model import LABEL_MAP


def _parse_groq_response(response_text, num_comments):
    labels = []
    for line in response_text.strip().split("\n"):
        line = line.strip()
        match = re.match(r"^\d+[\.\):\-]\s*(toxic|non-toxic|non toxic)", line, re.IGNORECASE)
        if match:
            label_str = match.group(1).lower().replace(" ", "-")
            labels.append(1 if label_str == "toxic" else 0)
    if len(labels) != num_comments:
        return None
    return labels


def classify_batch_groq(texts, client, model="llama-3.3-70b-versatile"):
    prompt_lines = [f"{i+1}. {t}" for i, t in enumerate(texts)]
    prompt = (
        "Classify each Bangla comment as 'toxic' or 'non-toxic'. "
        "Reply with ONLY a numbered list like:\n"
        "1. toxic\n2. non-toxic\n...\n\n"
        "Comments:\n" + "\n".join(prompt_lines)
    )

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=1024,
    )
    return _parse_groq_response(response.choices[0].message.content, len(texts))


def classify_batch_gemini(texts, model):
    prompt_lines = [f"{i+1}. {t}" for i, t in enumerate(texts)]
    prompt = (
        "Classify each Bangla comment as 'toxic' or 'non-toxic'. "
        "Reply with ONLY a numbered list like:\n"
        "1. toxic\n2. non-toxic\n...\n\n"
        "Comments:\n" + "\n".join(prompt_lines)
    )

    response = model.generate_content(prompt)
    return _parse_groq_response(response.text, len(texts))


def run_llm_baseline(
    texts,
    labels,
    client,
    model_name="llama-3.3-70b-versatile",
    batch_size=25,
    delay=2,
    max_retries=3,
    provider="groq",
):
    all_preds = [None] * len(texts)
    failed_indices = []

    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i : i + batch_size]
        batch_idx = list(range(i, min(i + batch_size, len(texts))))

        success = False
        for attempt in range(max_retries):
            try:
                if provider == "groq":
                    batch_labels = classify_batch_groq(batch_texts, client, model_name)
                else:
                    batch_labels = classify_batch_gemini(batch_texts, client)

                if batch_labels is not None:
                    for idx, label in zip(batch_idx, batch_labels):
                        all_preds[idx] = label
                    success = True
                    break
            except Exception as e:
                print(f"Batch {i//batch_size + 1} attempt {attempt+1} failed: {e}")
                time.sleep(delay * (attempt + 1))

        if not success:
            failed_indices.extend(batch_idx)
            print(f"Batch {i//batch_size + 1} failed after {max_retries} retries")

        if i + batch_size < len(texts):
            time.sleep(delay)

    valid_idx = [i for i in range(len(texts)) if all_preds[i] is not None]
    valid_preds = [all_preds[i] for i in valid_idx]
    valid_labels = [labels[i] for i in valid_idx]

    return {
        "predictions": all_preds,
        "valid_predictions": valid_preds,
        "valid_labels": valid_labels,
        "failed_indices": failed_indices,
        "total": len(texts),
        "successful": len(valid_preds),
    }


def run_better_profanity_baseline(texts, labels):
    from better_profanity import profanity

    profanity.load_censor_words()
    preds = []
    for text in texts:
        preds.append(1 if profanity.contains_profanity(text) else 0)

    return preds
