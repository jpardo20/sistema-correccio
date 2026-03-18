import json
from pathlib import Path

from motor.evidence_viewer import EvidenceViewer
from motor.results_manager import GROUP_MEMBER_ID, load_results
from motor.validator_router import route_validator
from motor.tools.grading import ask_score_and_comment


class CorrectionEngine:

    def __init__(self, results_file="results/corrections.json", known_units=None):
        self.viewer = EvidenceViewer()
        self.results_file = Path(results_file)
        self.known_units = known_units or []
        self.results = load_results(self.results_file, known_units=self.known_units)
        self.save()

    def _get_member_id(self, activity, evidence):
        if activity.get("group_activity") is True:
            return GROUP_MEMBER_ID

        if activity["id"] in {"MER_GRUP", "MR_GRUP"}:
            return GROUP_MEMBER_ID

        member = evidence.get("member") or {}
        if isinstance(member, dict):
            return str(member.get("id") or member.get("unit") or member.get("cognom") or GROUP_MEMBER_ID)

        return str(member or GROUP_MEMBER_ID)

    def correct(self, unit, activity, evidence):
        print("\n======================")
        print("Activitat:", activity.get("name", activity["id"]))

        repo = evidence.get("repo_name")
        member_id = self._get_member_id(activity, evidence)

        self.results.setdefault(repo, {})
        self.results[repo].setdefault(member_id, {})

        if activity["id"] in self.results[repo][member_id]:
            print("✔ Activitat ja corregida")
            return

        handled = route_validator(
            activity=activity,
            evidence=evidence,
            corrections=self.results,
            save_corrections=self.save,
        )
        if handled:
            return

        if not evidence.get("exists"):
            print("❌ Evidència no trobada")
            score = 0
            comment = "No lliurat"
        else:
            if "path" in evidence:
                print("Fitxer:", evidence["path"])

            if "candidates" in evidence:
                print("\nFitxers possibles:")
                for i, c in enumerate(evidence["candidates"], start=1):
                    print(f"{i}) {c}")
                print("0) cap")

                cmd = "0"
                while True:
                    cmd = input("o<num>=obrir  s<num>=seleccionar  0=cap : ").strip()
                    if cmd == "0":
                        score = 0
                        comment = "No lliurat"
                        break
                    if cmd.startswith("o"):
                        try:
                            i = int(cmd[1:]) - 1
                            if 0 <= i < len(evidence["candidates"]):
                                self.viewer.show(evidence["candidates"][i], activity.get("type", "text"))
                        except Exception:
                            print("Comanda incorrecta")
                        continue
                    if cmd.startswith("s"):
                        try:
                            i = int(cmd[1:]) - 1
                            if 0 <= i < len(evidence["candidates"]):
                                evidence["path"] = evidence["candidates"][i]
                                break
                        except Exception:
                            print("Comanda incorrecta")

                if cmd != "0":
                    score, comment = ask_score_and_comment()
            else:
                score, comment = ask_score_and_comment()

        self.results[repo][member_id][activity["id"]] = {
            "score": score,
            "comment": comment,
        }
        self.save()

    def save(self):
        self.results_file.parent.mkdir(exist_ok=True)
        with open(self.results_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
