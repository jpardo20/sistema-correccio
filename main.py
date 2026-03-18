from motor.repo_locator import RepoLocator
from motor.activities_loader import ActivitiesLoader

locator = RepoLocator()
activities = ActivitiesLoader()

print("Unitats detectades:")
print(locator.get_units())

for unit in locator.get_units():

    repo_path = locator.get_repo_path(unit)

    print(f"\nUnitat: {unit}")
    print(f"Repo: {repo_path}")

    for activity in activities.get_activities():

        evidence_path = activities.resolve_activity_path(
            activity,
            repo_path,
            unit
        )

        print(
            f"  {activity['id']} -> {evidence_path} -> {evidence_path.exists()}"
        )