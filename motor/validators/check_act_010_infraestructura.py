from pathlib import Path
from motor.tools.grading import ask_score_and_comment

KEYWORDS = [
    "infraestructura",
    "xarxa",
    "network",
    "vm"
]


def check_act_010_infraestructura(repo_path, repo_name, corrections, save_corrections):

    print("🔎 ACT010 infraestructura")

    found = []

    for path in repo_path.rglob("*"):

        name = path.name.lower()

        if any(k in name for k in KEYWORDS):
            found.append(str(path))

    if len(found) >= 2:
        score = 10
    elif len(found) == 1:
        score = 6
    else:
        score = 0

    corrections[repo_name]["ACT_010_INFRA"] = {
        "score": score,
        "max_score": 10,
        "files": found
    }

    save_corrections()

    print(f"✔ ACT010 -> {score}/10")