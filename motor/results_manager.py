import ast
import json
from pathlib import Path
from typing import Any, Dict

GROUP_MEMBER_ID = "__group__"

OLD_TO_NEW_ACTIVITY_IDS = {
    "EV_MER_GRUP": "MER_GRUP",
    "EV_MER_INDIVIDUAL": "MER_INDIVIDUAL",
    "EV_SQL_SCHEMA": "SQL",
    "SQL_SCHEMA": "SQL",
    "README_MER": "README",
    "README_MER_GRUP": "README",
}


def canonical_activity_id(activity_id: str) -> str:
    return OLD_TO_NEW_ACTIVITY_IDS.get(activity_id, activity_id)


def is_score_entry(value: Any) -> bool:
    return isinstance(value, dict) and ("score" in value or "comment" in value or "max_score" in value)


def parse_member_key(key: Any) -> str:
    if isinstance(key, dict):
        return str(key.get("id") or key.get("cognom") or GROUP_MEMBER_ID)

    if not isinstance(key, str):
        return str(key)

    if key.startswith("{") and key.endswith("}"):
        try:
            parsed = ast.literal_eval(key)
            if isinstance(parsed, dict):
                return str(parsed.get("id") or parsed.get("cognom") or GROUP_MEMBER_ID)
        except Exception:
            pass

    return key


def normalize_results(raw: Dict[str, Any], known_units=None) -> Dict[str, Dict[str, Dict[str, Any]]]:
    known_units = set(known_units or [])
    normalized: Dict[str, Dict[str, Dict[str, Any]]] = {}

    if not isinstance(raw, dict):
        return normalized

    for top_key, top_value in raw.items():
        if top_key in known_units:
            # Entrades contaminades antigues (unitat al nivell superior).
            # Es descarten per forçar un únic format canònic: repo -> member -> activity.
            continue

        repo_bucket = normalized.setdefault(top_key, {})
        if not isinstance(top_value, dict):
            continue

        for inner_key, inner_value in top_value.items():
            if is_score_entry(inner_value):
                repo_bucket.setdefault(GROUP_MEMBER_ID, {})[
                    canonical_activity_id(inner_key)
                ] = inner_value
                continue

            member_id = parse_member_key(inner_key)
            if not isinstance(inner_value, dict):
                continue

            member_bucket = repo_bucket.setdefault(member_id, {})
            for act_id, payload in inner_value.items():
                if is_score_entry(payload):
                    member_bucket[canonical_activity_id(act_id)] = payload

    return normalized


def load_results(results_file: Path, known_units=None) -> Dict[str, Dict[str, Dict[str, Any]]]:
    if not results_file.exists():
        return {}

    with open(results_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return normalize_results(data, known_units=known_units)
