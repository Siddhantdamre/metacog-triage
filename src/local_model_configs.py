"""Local open-weight model registry for the MetaCog-Triage benchmark.

All models are ungated and runnable on a single T4/P100 (Kaggle free tier)
or CPU. Add new entries here; do not change existing entries, so published
numbers stay reproducible.
"""

LOCAL_MODEL_CONFIGS = {
    "qwen": {
        "label": "Qwen/Qwen2.5-1.5B-Instruct",
        "hf_model_id": "Qwen/Qwen2.5-1.5B-Instruct",
        "max_new_tokens": 96,
        "notes": "Small instruct model with strong structured-output behavior for its size.",
    },
    "smollm": {
        "label": "HuggingFaceTB/SmolLM2-1.7B-Instruct",
        "hf_model_id": "HuggingFaceTB/SmolLM2-1.7B-Instruct",
        "max_new_tokens": 96,
        "notes": "Open small instruct baseline that avoids gated-model friction while staying Kaggle-feasible.",
    },
    "tinyllama": {
        "label": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "hf_model_id": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "max_new_tokens": 96,
        "notes": "Llama-family small instruct baseline; serves as a fragility floor.",
    },
    "granite": {
        "label": "ibm-granite/granite-3.1-2b-instruct",
        "hf_model_id": "ibm-granite/granite-3.1-2b-instruct",
        "max_new_tokens": 96,
        "notes": "Small open instruct model providing a non-Qwen comparison point.",
    },
    # Alignment-artifact hypothesis test (HYPOTHESIS_alignment_artifact.md):
    # base (non-instruct) checkpoints of the same families. Prediction: more
    # bluffing, less over-escalation collapse. May need higher max_new_tokens
    # and tolerant parsing; report instruction-collapse separately.
    "qwen_base": {
        "label": "Qwen/Qwen2.5-1.5B",
        "hf_model_id": "Qwen/Qwen2.5-1.5B",
        "max_new_tokens": 192,
        "notes": "BASE model paired with 'qwen' instruct — the alignment-artifact A/B test.",
    },
    "smollm_base": {
        "label": "HuggingFaceTB/SmolLM2-1.7B",
        "hf_model_id": "HuggingFaceTB/SmolLM2-1.7B",
        "max_new_tokens": 192,
        "notes": "BASE model paired with 'smollm' instruct.",
    },
    # Suggested additions for the v2 run (verify VRAM fit before enabling):
    "qwen3b": {
        "label": "Qwen/Qwen2.5-3B-Instruct",
        "hf_model_id": "Qwen/Qwen2.5-3B-Instruct",
        "max_new_tokens": 96,
        "notes": "Scale probe within the same family as qwen (1.5B -> 3B).",
    },
    "llama1b": {
        "label": "meta-llama/Llama-3.2-1B-Instruct",
        "hf_model_id": "meta-llama/Llama-3.2-1B-Instruct",
        "max_new_tokens": 96,
        "notes": "May require HF license acceptance; skip if gated access is unavailable.",
    },
    "phi": {
        "label": "microsoft/Phi-3.5-mini-instruct",
        "hf_model_id": "microsoft/Phi-3.5-mini-instruct",
        "max_new_tokens": 96,
        "notes": "3.8B; strongest small open baseline that still fits a T4 in fp16/bf16.",
    },
}


def get_model_config(model_name):
    normalized = model_name.strip().lower()
    if normalized not in LOCAL_MODEL_CONFIGS:
        raise ValueError(
            f"Unsupported local model '{model_name}'. Expected one of: {', '.join(sorted(LOCAL_MODEL_CONFIGS))}."
        )
    return dict(LOCAL_MODEL_CONFIGS[normalized])
