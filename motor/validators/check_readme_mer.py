from datetime import datetime
from pathlib import Path

from motor.tools.grading import ask_score_and_comment


def check_readme_mer(activity, evidence, corrections, save_corrections):
    print("\n[README]")

    repo_path = Path(evidence["repo_path"])
    repo_name = evidence["repo_name"]
    member = evidence.get("member", {})
    member_id = member.get("id") or evidence.get("unit")
    activity_id = activity["id"]

    repo_bucket = corrections.setdefault(repo_name, {})
    member_bucket = repo_bucket.setdefault(member_id, {})
    if activity_id in member_bucket:
        print("✔ README ja corregit")
        return

    readme_file = repo_path / "README.md"
    if not readme_file.exists():
        print("❌ README.md no trobat")
        member_bucket[activity_id] = {
            "score": 0,
            "max_score": 10,
            "comment": "README absent",
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
        save_corrections()
        return

    print("Fitxer:", readme_file)
    print("\n----- INICI README.md -----\n")
    try:
        print(readme_file.read_text(encoding="utf-8", errors="ignore"))
    finally:
        print("\n----- FI README.md -----\n")

    score, comment = ask_score_and_comment()
    member_bucket[activity_id] = {
        "score": score,
        "max_score": 10,
        "comment": comment,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    save_corrections()
