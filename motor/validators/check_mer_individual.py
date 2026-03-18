from datetime import datetime
from pathlib import Path
import subprocess

from motor.tools.grading import ask_score_and_comment


def open_image(path):
    try:
        subprocess.run(["xdg-open", str(path)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        print("⚠ No s'ha pogut obrir la imatge")


def check_mer_individual(activity, evidence, corrections, save_corrections):
    print("\n[MER INDIVIDUAL]")

    repo_path = Path(evidence["repo_path"])
    repo_name = evidence["repo_name"]
    member = evidence.get("member", {})
    member_id = member.get("id") or evidence.get("unit")
    activity_id = activity["id"]

    repo_bucket = corrections.setdefault(repo_name, {})
    member_bucket = repo_bucket.setdefault(member_id, {})
    if activity_id in member_bucket:
        print("✔ MER individual ja corregit")
        return

    mer_dir = repo_path / f"{member_id}-mer"
    png_files = list(mer_dir.glob("*.png")) if mer_dir.exists() else []
    xml_files = list(mer_dir.glob("*.xml")) if mer_dir.exists() else []
    status = "OK_LOCATION" if (png_files or xml_files) else "NOT_FOUND"

    if status == "NOT_FOUND":
        png_files = list(repo_path.rglob(f"*{member_id}*mer*.png"))
        xml_files = list(repo_path.rglob(f"*{member_id}*mer*.xml"))
        if png_files or xml_files:
            status = "WRONG_LOCATION"

    print({
        "OK_LOCATION": "✔ MER individual al lloc correcte",
        "WRONG_LOCATION": "⚠ MER individual trobat fora de lloc",
        "NOT_FOUND": "❌ MER individual no trobat",
    }[status])

    if png_files:
        print("PNG trobats:")
        for p in png_files:
            print(" ", p)
        open_image(png_files[0])
    if xml_files:
        print("XML trobats:")
        for x in xml_files:
            print(" ", x)

    score, comment = ask_score_and_comment()
    member_bucket[activity_id] = {
        "score": score,
        "max_score": 10,
        "comment": comment,
        "structure_status": status,
        "files_png": [str(p) for p in png_files],
        "files_xml": [str(x) for x in xml_files],
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    save_corrections()
