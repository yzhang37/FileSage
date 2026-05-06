from __future__ import annotations

from dataclasses import dataclass
from itertools import count
from pathlib import Path


DEFAULT_EXTENSION_CATEGORIES: dict[str, str] = {
    ".7z": "Archives",
    ".aac": "Audio",
    ".ai": "Design",
    ".avi": "Video",
    ".csv": "Spreadsheets",
    ".doc": "Documents",
    ".docx": "Documents",
    ".epub": "Documents",
    ".flac": "Audio",
    ".gif": "Images",
    ".gz": "Archives",
    ".heic": "Images",
    ".jpeg": "Images",
    ".jpg": "Images",
    ".js": "Code",
    ".json": "Code",
    ".key": "Presentations",
    ".md": "Documents",
    ".mov": "Video",
    ".mp3": "Audio",
    ".mp4": "Video",
    ".numbers": "Spreadsheets",
    ".odt": "Documents",
    ".pages": "Documents",
    ".pdf": "Documents",
    ".png": "Images",
    ".ppt": "Presentations",
    ".pptx": "Presentations",
    ".psd": "Design",
    ".py": "Code",
    ".rar": "Archives",
    ".rtf": "Documents",
    ".svg": "Images",
    ".tar": "Archives",
    ".ts": "Code",
    ".txt": "Documents",
    ".wav": "Audio",
    ".webm": "Video",
    ".xls": "Spreadsheets",
    ".xlsx": "Spreadsheets",
    ".yaml": "Code",
    ".yml": "Code",
    ".zip": "Archives",
}


@dataclass(frozen=True)
class PlanItem:
    source: Path
    destination: Path
    category: str
    reason: str

    def as_dict(self) -> dict[str, str]:
        return {
            "source": str(self.source),
            "destination": str(self.destination),
            "category": self.category,
            "reason": self.reason,
        }


def classify_path(
    path: Path,
    extension_categories: dict[str, str] | None = None,
) -> tuple[str, str]:
    categories = extension_categories or DEFAULT_EXTENSION_CATEGORIES
    suffix = path.suffix.lower()
    if suffix in categories:
        category = categories[suffix]
        return category, f"extension {suffix} maps to {category}"
    return "Other", "no extension rule matched"


def build_plan(
    root: Path,
    *,
    recursive: bool = False,
    include_hidden: bool = False,
    extension_categories: dict[str, str] | None = None,
) -> list[PlanItem]:
    root = root.expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Folder does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Not a folder: {root}")

    occupied_destinations: set[Path] = set()
    items: list[PlanItem] = []

    for source in iter_candidate_files(root, recursive=recursive, include_hidden=include_hidden):
        category, reason = classify_path(source, extension_categories)
        destination = unique_destination(root / category / source.name, occupied_destinations)

        if source == destination:
            continue

        occupied_destinations.add(destination)
        items.append(
            PlanItem(
                source=source,
                destination=destination,
                category=category,
                reason=reason,
            )
        )

    return items


def iter_candidate_files(root: Path, *, recursive: bool, include_hidden: bool) -> list[Path]:
    pattern = "**/*" if recursive else "*"
    paths: list[Path] = []

    for path in root.glob(pattern):
        if not path.is_file():
            continue
        if not include_hidden and is_hidden_relative_path(path.relative_to(root)):
            continue
        paths.append(path)

    return sorted(paths)


def is_hidden_relative_path(path: Path) -> bool:
    return any(part.startswith(".") for part in path.parts)


def unique_destination(destination: Path, occupied_destinations: set[Path]) -> Path:
    if destination not in occupied_destinations and not destination.exists():
        return destination

    for index in count(1):
        candidate = destination.with_name(f"{destination.stem} ({index}){destination.suffix}")
        if candidate not in occupied_destinations and not candidate.exists():
            return candidate

    raise RuntimeError("Unable to find a unique destination")

