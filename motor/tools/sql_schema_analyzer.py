import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

CREATE_TABLE_RE = re.compile(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"]?([a-zA-Z0-9_]+)[`"]?', re.IGNORECASE)
PRIMARY_KEY_RE = re.compile(r'PRIMARY\s+KEY', re.IGNORECASE)
FOREIGN_KEY_RE = re.compile(r'FOREIGN\s+KEY', re.IGNORECASE)


@dataclass
class SqlAnalysis:
    file: str
    tables: List[str]
    primary_keys_count: int
    foreign_keys_count: int
    estimated_score: int

    def to_dict(self):
        return asdict(self)


def analyze_sql_text(sql_text: str) -> SqlAnalysis:
    tables = CREATE_TABLE_RE.findall(sql_text)
    pk_count = len(PRIMARY_KEY_RE.findall(sql_text))
    fk_count = len(FOREIGN_KEY_RE.findall(sql_text))

    estimated_score = 0
    if tables:
        estimated_score += 2
    if len(tables) >= 5:
        estimated_score += 2
    if pk_count > 0:
        estimated_score += 3
    if fk_count > 0:
        estimated_score += 3

    return SqlAnalysis(
        file="",
        tables=tables,
        primary_keys_count=pk_count,
        foreign_keys_count=fk_count,
        estimated_score=min(10, estimated_score),
    )


def analyze_sql_file(sql_file: Path) -> SqlAnalysis:
    sql_text = sql_file.read_text(encoding="utf-8", errors="ignore")
    analysis = analyze_sql_text(sql_text)
    analysis.file = str(sql_file)
    return analysis


def find_sql_candidates(repo_path: Path, repo_name: str, expected_relative_path: str | None = None):
    docs_dir = repo_path / "docs"
    sql_dir = repo_path / "sql"

    candidates: List[Path] = []
    status = "NOT_FOUND"

    preferred_paths = []
    if expected_relative_path:
        preferred_paths.append(repo_path / expected_relative_path)
    preferred_paths.append(docs_dir / f"{repo_name}-schema.sql")
    preferred_paths.append(sql_dir / "schema.sql")

    for preferred in preferred_paths:
        if preferred.exists() and preferred not in candidates:
            candidates.append(preferred)

    if candidates:
        status = "OK_LOCATION"
    else:
        tolerant = []
        search_roots = [docs_dir, sql_dir, repo_path]
        for root in search_roots:
            if not root.exists():
                continue
            iterator = root.rglob("*.sql") if root == repo_path else root.glob("*.sql")
            for f in iterator:
                if f not in tolerant:
                    tolerant.append(f)
        if tolerant:
            status = "WRONG_LOCATION"
            candidates = tolerant

    return status, candidates
