from motor.repo_locator import RepoLocator
from motor.activities_loader import ActivitiesLoader
from motor.evidence_resolver import EvidenceResolver
from motor.correction_engine import CorrectionEngine


def build_member(locator: RepoLocator, unit: str, repo_path):
    info = locator.get_unit_info(unit)
    return {
        "id": unit,
        "unit": unit,
        "name": info.get("name", ""),
        "last_name1": info.get("last_name1", ""),
        "last_name2": info.get("last_name2", ""),
        "repo": repo_path.name,
    }


locator = RepoLocator()
activities = ActivitiesLoader()
resolver = EvidenceResolver()
engine = CorrectionEngine(known_units=locator.get_units())

for unit in locator.get_units():
    repo_path = locator.get_repo_path(unit)
    student_name = locator.get_unit_full_name(unit)

    print("\n============================")
    print("Alumne:", student_name or unit)
    print("Repo:", repo_path)

    if not repo_path.exists():
        print("❌ Repositori no trobat. Se salta aquesta unitat.")
        continue

    member = build_member(locator, unit, repo_path)

    for activity in activities.get_activities():
        evidence = resolver.resolve(repo_path, activity, unit)
        evidence["repo_path"] = repo_path
        evidence["repo_name"] = repo_path.name
        evidence["member"] = member
        evidence["unit"] = unit
        engine.correct(unit, activity, evidence)
