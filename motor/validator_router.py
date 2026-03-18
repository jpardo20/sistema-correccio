from motor.validators.check_mer_grup import check_mer_grup
from motor.validators.check_mer_individual import check_mer_individual
from motor.validators.check_mr_grup import check_mr_grup
from motor.validators.check_readme_mer import check_readme_mer
from motor.validators.check_readme_mer_grup import check_readme_mer_grup
from motor.validators.check_sql_schema import check_sql_schema


def route_validator(activity, evidence, corrections, save_corrections):
    activity_id = activity["id"]

    if activity_id == "MER_GRUP":
        check_mer_grup(activity, evidence, corrections, save_corrections)
        return True

    if activity_id == "MER_INDIVIDUAL":
        check_mer_individual(activity, evidence, corrections, save_corrections)
        return True

    if activity_id == "MR_GRUP":
        check_mr_grup(activity, evidence, corrections, save_corrections)
        return True

    if activity_id == "README":
        check_readme_mer(activity, evidence, corrections, save_corrections)
        return True

    if activity_id == "README_GRUP":
        check_readme_mer_grup(activity, evidence, corrections, save_corrections)
        return True

    if activity_id == "SQL":
        check_sql_schema(activity, evidence, corrections, save_corrections)
        return True

    return False
