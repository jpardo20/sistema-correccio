
import json

from pathlib import Path
from motor.tools.grading import ask_score_and_comment

def check_act_013_json_docs(repo_path, repo_name, corrections, save_corrections):

    print("🔎 ACT013 JSON docs")

    valid_json = []

    for path in repo_path.rglob("*.json"):
        try:
            with open(path) as f:
                json.load(f)
            valid_json.append(str(path))
        except Exception:
            pass

    if len(valid_json) >= 2:
        score = 10
    elif len(valid_json) == 1:
        score = 6
    else:
        score = 0

    corrections[repo_name]["ACT_013_JSON_DOCS"] = {
        "score": score,
        "max_score": 10,
        "files": valid_json
    }

    save_corrections()

    print(f"✔ ACT013 -> {score}/10")
