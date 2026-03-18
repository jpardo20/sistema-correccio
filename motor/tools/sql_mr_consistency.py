from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Set
import unicodedata

from motor.tools.mr_parser import extract_tables_from_mr, find_model_relacional, validate_diagrams_xml


@dataclass
class MrSqlConsistency:
    mr_file: str | None
    mr_status: str | None
    mr_tables: list[str]
    sql_tables: list[str]
    matching_tables: list[str]
    missing_in_mr: list[str]
    extra_in_mr: list[str]
    score: int

    def to_dict(self):
        return asdict(self)


# 🔥 NORMALITZACIÓ ROBUSTA (clau)
def normalize(name: str) -> str:
    name = name.lower().rstrip("s")
    name = unicodedata.normalize("NFD", name)
    name = "".join(c for c in name if unicodedata.category(c) != "Mn")
    return name


def compare_mr_sql(repo_path: Path, sql_tables: Iterable[str]) -> MrSqlConsistency:
    sql_set: Set[str] = {table.upper() for table in sql_tables}

    mr_file = find_model_relacional(repo_path)
    if mr_file is None:
        return MrSqlConsistency(
            mr_file=None,
            mr_status=None,
            mr_tables=[],
            sql_tables=sorted(sql_set),
            matching_tables=[],
            missing_in_mr=sorted(sql_set),
            extra_in_mr=[],
            score=0,
        )

    mr_status = validate_diagrams_xml(mr_file) if mr_file.suffix.lower() == ".xml" else "TEXT"

    # 🔥 IMPORTANT: passar sql_tables per activar fallback intel·ligent
    raw_mr_tables = extract_tables_from_mr(mr_file, sql_tables)
    mr_tables = {table.upper() for table in raw_mr_tables}

    # 🔥 MATCHING INTEL·LIGENT
    sql_norm = {normalize(t): t for t in sql_set}
    mr_norm = {normalize(t): t for t in mr_tables}

    matching = []
    for key in sql_norm:
        if key in mr_norm:
            matching.append(sql_norm[key])

    matching = sorted(matching)

    missing = sorted([
        sql_norm[k] for k in sql_norm if k not in mr_norm
    ])

    extra = sorted([
        mr_norm[k] for k in mr_norm if k not in sql_norm
    ])

    # 🔍 DEBUG (molt útil)
    print("\nDEBUG MR TABLES:")
    for t in sorted(mr_tables):
        print(" -", t)

    print("\nDEBUG MATCHING NORMALIZED:")
    for k in sql_norm:
        print(f"SQL: {sql_norm[k]} → {k} | MR:", mr_norm.get(k, "❌"))

    # 🎯 SCORE
    if not sql_set:
        score = 0
    else:
        score = round((len(matching) / len(sql_set)) * 10)

    return MrSqlConsistency(
        mr_file=str(mr_file),
        mr_status=mr_status,
        mr_tables=sorted(mr_tables),
        sql_tables=sorted(sql_set),
        matching_tables=matching,
        missing_in_mr=missing,
        extra_in_mr=extra,
        score=score,
    )