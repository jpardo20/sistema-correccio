from pathlib import Path
from motor.tools.grading import ask_score_and_comment

KEYWORDS = [
    "checkpoint",
    "review",
    "resum",
    "conclusions"
]

def check_act_015_checkpoint(repo_path, repo_name, corrections, save_corrections):

    print("🔎 ACT015 checkpoint")

    docs = []

    for path in repo_path.rglob("*"):
        name = path.name.lower()

        if any(k in name for k in KEYWORDS):
            if name.endswith(".md") or name.endswith(".pdf") or name.endswith(".docx"):
                docs.append(str(path))

    score, comment = ask_score_and_comment()

    corrections[repo_name]["ACT_015_CHECKPOINT"] = {
        "score": score,
        "comment": comment,
        "max_score": 10,
        "files": docs
    }

    save_corrections()

    print(f"✔ ACT015 -> {score}/10")
