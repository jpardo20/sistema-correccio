from datetime import datetime
from pathlib import Path

from motor.results_manager import GROUP_MEMBER_ID
from motor.tools.grading import ask_score_and_comment


def check_readme_mer_grup(activity, evidence, corrections, save_corrections):
    print("\n[README GRUP]")

    repo_path = Path(evidence["repo_path"])
    repo_name = evidence["repo_name"]
    activity_id = activity["id"]

    repo_bucket = corrections.setdefault(repo_name, {})
    group_bucket = repo_bucket.setdefault(GROUP_MEMBER_ID, {})
    if activity_id in group_bucket:
        print("✔ README grup ja corregit")
        return

    readme_file = repo_path / "README.md"
    if not readme_file.exists():
        print("❌ README.md no trobat")
        group_bucket[activity_id] = {
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
    group_bucket[activity_id] = {
        "score": score,
        "max_score": 10,
        "comment": comment,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    save_corrections()
