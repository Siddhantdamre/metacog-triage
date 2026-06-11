"""Frontier API adapter layer for MetaCog-Triage v3 (scaffold).

One interface over Anthropic / OpenAI / Google + the existing local runner,
so frontier and local models produce the same results schema.

Design (see FRONTIER_ARCHITECTURE.md): temperature 0 + 3 samples,
logprob capture where available, response cache keyed by
(model, contract_version, task_id, sample_idx), cost guard, no imputation.

Requires (only for the providers you use):
    pip install anthropic openai google-genai
API keys via environment: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY.

Status: scaffold — reviewed, not yet executed against live APIs. Verify each
adapter against current provider SDK docs before the frontier run; SDK
surfaces change. Nothing here runs without explicit keys and a --confirm-cost flag.
"""

import hashlib
import json
import os
import time
from pathlib import Path

CACHE_DIR = Path(__file__).resolve().parent.parent / "results" / "api_cache"

API_MODEL_CONFIGS = {
    # Fill model IDs at run time from each provider's current model list —
    # do not trust hardcoded names to remain valid.
    "claude": {"provider": "anthropic", "model_id": "SET_AT_RUN_TIME", "max_tokens": 512},
    "gpt": {"provider": "openai", "model_id": "SET_AT_RUN_TIME", "max_tokens": 512, "logprobs": True},
    "gemini": {"provider": "google", "model_id": "SET_AT_RUN_TIME", "max_tokens": 512},
}


def _cache_key(model, contract_version, task_id, sample_idx):
    return hashlib.sha256(f"{model}|{contract_version}|{task_id}|{sample_idx}".encode()).hexdigest()[:24]


class ResponseCache:
    """File-per-response cache; doubles as the auditable raw record."""

    def __init__(self, cache_dir=CACHE_DIR):
        self.dir = Path(cache_dir)
        self.dir.mkdir(parents=True, exist_ok=True)

    def get(self, key):
        p = self.dir / f"{key}.json"
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None

    def put(self, key, payload):
        (self.dir / f"{key}.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


class BaseAdapter:
    provider = "base"

    def generate(self, system_prompt, user_prompt, config):
        """Return dict: {text, logprobs|None, usage:{in,out}, error|None}."""
        raise NotImplementedError

    def call_with_retry(self, system_prompt, user_prompt, config, retries=3):
        last_err = None
        for attempt in range(retries):
            try:
                return self.generate(system_prompt, user_prompt, config)
            except Exception as exc:  # provider SDKs raise heterogeneous errors
                last_err = str(exc)
                time.sleep(2 ** attempt)
        return {"text": None, "logprobs": None, "usage": None, "error": f"failed after {retries} retries: {last_err}"}


class AnthropicAdapter(BaseAdapter):
    provider = "anthropic"

    def __init__(self):
        import anthropic  # noqa: deferred import keeps unused providers optional
        self.client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

    def generate(self, system_prompt, user_prompt, config):
        resp = self.client.messages.create(
            model=config["model_id"],
            max_tokens=config["max_tokens"],
            temperature=0,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return {
            "text": "".join(b.text for b in resp.content if getattr(b, "type", "") == "text"),
            "logprobs": None,
            "usage": {"in": resp.usage.input_tokens, "out": resp.usage.output_tokens},
            "error": None,
        }


class OpenAIAdapter(BaseAdapter):
    provider = "openai"

    def __init__(self):
        import openai
        self.client = openai.OpenAI()  # reads OPENAI_API_KEY

    def generate(self, system_prompt, user_prompt, config):
        kwargs = dict(
            model=config["model_id"],
            max_tokens=config["max_tokens"],
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        if config.get("logprobs"):
            kwargs.update(logprobs=True, top_logprobs=5)
        resp = self.client.chat.completions.create(**kwargs)
        choice = resp.choices[0]
        lp = None
        if getattr(choice, "logprobs", None):
            lp = [
                {"token": t.token, "logprob": t.logprob}
                for t in choice.logprobs.content
            ]
        return {
            "text": choice.message.content,
            "logprobs": lp,
            "usage": {"in": resp.usage.prompt_tokens, "out": resp.usage.completion_tokens},
            "error": None,
        }


class GoogleAdapter(BaseAdapter):
    provider = "google"

    def __init__(self):
        from google import genai
        self.client = genai.Client()  # reads GOOGLE_API_KEY

    def generate(self, system_prompt, user_prompt, config):
        resp = self.client.models.generate_content(
            model=config["model_id"],
            contents=user_prompt,
            config={
                "system_instruction": system_prompt,
                "temperature": 0,
                "max_output_tokens": config["max_tokens"],
            },
        )
        return {"text": resp.text, "logprobs": None, "usage": None, "error": None}


ADAPTERS = {"anthropic": AnthropicAdapter, "openai": OpenAIAdapter, "google": GoogleAdapter}


def run_frontier(model_name, tasks, system_prompt, build_user_prompt,
                 contract_version, n_samples=3, cost_cap_usd=None, confirm_cost=False):
    """Evaluate one frontier model over tasks. Returns records in the v2 schema
    plus: contract_version, sample_idx, logprobs, usage, api_error."""
    config = API_MODEL_CONFIGS[model_name]
    if config["model_id"] == "SET_AT_RUN_TIME":
        raise SystemExit(f"Set a current model_id for '{model_name}' in API_MODEL_CONFIGS first.")
    if not confirm_cost:
        est_tokens = len(tasks) * n_samples * 700
        raise SystemExit(
            f"Estimated ~{est_tokens:,} tokens for {model_name} "
            f"({len(tasks)} tasks x {n_samples} samples). Rerun with confirm_cost=True."
        )
    adapter = ADAPTERS[config["provider"]]()
    cache = ResponseCache()
    records = []
    for task in tasks:
        for sample_idx in range(n_samples):
            key = _cache_key(model_name, contract_version, task["task_id"], sample_idx)
            cached = cache.get(key)
            if cached is None:
                cached = adapter.call_with_retry(system_prompt, build_user_prompt(task), config)
                cached.update(task_id=task["task_id"], model=model_name,
                              contract_version=contract_version, sample_idx=sample_idx,
                              timestamp=time.time())
                cache.put(key, cached)
            records.append(cached)
    return records
