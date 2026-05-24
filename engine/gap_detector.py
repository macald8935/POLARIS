"""Semantic policy gap detection for POLARIS.

The detector compares each framework clause with policy sentences using local
sentence-transformer embeddings. Scoring remains deterministic: every required
clause is classified as covered or missing from similarity scores, then controls
receive a 0-3 score from their clause coverage ratio.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Protocol


DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"
DEFAULT_THRESHOLD = 0.45


class EmbeddingModel(Protocol):
    def encode(self, sentences: list[str], convert_to_tensor: bool = False):
        """Return embeddings for the provided sentences."""


@dataclass(frozen=True)
class ClauseMatch:
    clause: str
    best_sentence: str
    similarity: float
    status: str


class HashingEmbeddingModel:
    """Small deterministic fallback used when the transformer model is absent.

    Production analysis should use sentence-transformers. This fallback keeps
    POLARIS usable in offline CI or fresh clones before the model is downloaded.
    """

    dimensions = 384

    def encode(self, sentences: list[str], convert_to_tensor: bool = False):
        return [self._embed(sentence) for sentence in sentences]

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        tokens = re.findall(r"[a-z0-9]+", text.lower())
        for token in tokens:
            vector[hash(token) % self.dimensions] += 1.0
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]


def load_framework(framework_path: str | Path) -> dict:
    """Load a framework JSON file and normalize legacy/new schemas."""

    path = Path(framework_path)
    with path.open("r", encoding="utf-8") as file:
        raw = json.load(file)

    if "controls" in raw and isinstance(raw["controls"], list):
        return raw

    controls = []
    for control_id, control in raw.items():
        controls.append(
            {
                "id": control_id,
                "function": control.get("function", "Unknown"),
                "name": control.get("name") or control.get("title", control_id),
                "description": control.get("description")
                or control.get("objective", ""),
                "required_clauses": control.get("required_clauses", []),
                "risk_if_missing": control.get("risk_if_missing", ""),
            }
        )

    return {
        "framework": path.stem,
        "version": "legacy",
        "controls": controls,
    }


@lru_cache(maxsize=2)
def get_embedding_model(model_name: str = DEFAULT_MODEL_NAME):
    """Load the local sentence-transformer model, falling back gracefully."""

    try:
        from sentence_transformers import SentenceTransformer

        return SentenceTransformer(model_name)
    except Exception:
        return HashingEmbeddingModel()


def split_policy_sentences(policy_text: str) -> list[str]:
    """Split policy text into sentence-like units suitable for embeddings."""

    normalized = re.sub(r"\s+", " ", policy_text).strip()
    if not normalized:
        return []

    pieces = re.split(r"(?<=[.!?;])\s+|\n+|(?:\s+-\s+)", normalized)
    sentences = [piece.strip(" \t\r\n-:*") for piece in pieces if piece.strip()]
    if len(sentences) == 1 and len(sentences[0]) > 500:
        return [chunk.strip() for chunk in re.split(r"\s{2,}", sentences[0]) if chunk.strip()]
    return sentences


def cosine_similarity(left: Iterable[float], right: Iterable[float]) -> float:
    left_values = list(left)
    right_values = list(right)
    dot = sum(a * b for a, b in zip(left_values, right_values))
    left_norm = math.sqrt(sum(a * a for a in left_values))
    right_norm = math.sqrt(sum(b * b for b in right_values))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def _as_vectors(embeddings) -> list[list[float]]:
    if hasattr(embeddings, "detach"):
        embeddings = embeddings.detach().cpu().tolist()
    elif hasattr(embeddings, "tolist"):
        embeddings = embeddings.tolist()
    return [list(row) for row in embeddings]


def _score_from_coverage(coverage_ratio: float) -> int:
    if coverage_ratio == 0:
        return 0
    if coverage_ratio < 0.5:
        return 1
    if coverage_ratio < 1:
        return 2
    return 3


def _status_from_similarity(similarity: float, threshold: float) -> str:
    if similarity >= threshold:
        return "covered"
    if similarity >= threshold * 0.75:
        return "partial"
    return "missing"


def detect_gaps(
    policy_text: str,
    framework_path: str | Path,
    threshold: float = DEFAULT_THRESHOLD,
    model: EmbeddingModel | None = None,
) -> list[dict]:
    """Detect policy gaps against a framework using semantic similarity."""

    framework = load_framework(framework_path)
    controls = framework["controls"]
    sentences = split_policy_sentences(policy_text.lower())
    model = model or get_embedding_model()

    if not sentences:
        return [
            {
                "control": control["id"],
                "title": control.get("name", control["id"]),
                "function": control.get("function", "Unknown"),
                "description": control.get("description", ""),
                "missing": control.get("required_clauses", []),
                "covered": [],
                "partial": [],
                "matches": [],
                "score": 0,
                "risk": control.get("risk_if_missing", ""),
            }
            for control in controls
        ]

    sentence_vectors = _as_vectors(model.encode(sentences, convert_to_tensor=False))
    findings = []

    for control in controls:
        clauses = control.get("required_clauses", [])
        clause_vectors = _as_vectors(model.encode(clauses, convert_to_tensor=False)) if clauses else []
        matches: list[ClauseMatch] = []

        for clause, clause_vector in zip(clauses, clause_vectors):
            scored_sentences = [
                (sentences[index], cosine_similarity(clause_vector, sentence_vector))
                for index, sentence_vector in enumerate(sentence_vectors)
            ]
            best_sentence, similarity = max(scored_sentences, key=lambda item: item[1])
            matches.append(
                ClauseMatch(
                    clause=clause,
                    best_sentence=best_sentence,
                    similarity=round(similarity, 4),
                    status=_status_from_similarity(similarity, threshold),
                )
            )

        covered = [match.clause for match in matches if match.status == "covered"]
        partial = [match.clause for match in matches if match.status == "partial"]
        missing = [match.clause for match in matches if match.status == "missing"]
        coverage_ratio = len(covered) / len(clauses) if clauses else 1.0

        findings.append(
            {
                "control": control["id"],
                "title": control.get("name", control["id"]),
                "function": control.get("function", "Unknown"),
                "description": control.get("description", ""),
                "missing": missing,
                "covered": covered,
                "partial": partial,
                "matches": [match.__dict__ for match in matches],
                "score": _score_from_coverage(coverage_ratio),
                "risk": control.get("risk_if_missing", ""),
            }
        )

    return findings
