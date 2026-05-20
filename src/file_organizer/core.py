"""Backward-compatible core imports for the original prototype package name."""

from filesage.core import (
    DEFAULT_EXTENSION_CATEGORIES,
    PlanItem,
    build_plan,
    classify_path,
    is_hidden_relative_path,
    iter_candidate_files,
    unique_destination,
)

__all__ = [
    "DEFAULT_EXTENSION_CATEGORIES",
    "PlanItem",
    "build_plan",
    "classify_path",
    "is_hidden_relative_path",
    "iter_candidate_files",
    "unique_destination",
]
