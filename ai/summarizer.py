"""Daily/weekly summarization. Cluster-first, then LLM."""
from __future__ import annotations

from .budget import budget
from .lm_studio_client import chat

SYSTEM = (
    "You synthesize concise daily summaries of communications. "
    "Output: top topics, pending tasks, key people. Be terse."
)


def summarize_clusters(cluster_excerpts: list[str], *, max_tokens: int = 600) -> str:
    if not budget.can_spend(max_tokens):
        return ""
    user = "\n\n---\n\n".join(cluster_excerpts)
    out = chat(SYSTEM, user, max_tokens=max_tokens)
    budget.spend(max_tokens)
    return out
