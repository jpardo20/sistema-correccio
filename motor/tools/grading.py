def default_comment_from_score(score):

    if score >= 10:
        return "Molt bona feina!"
    elif score >= 8:
        return "Bona feina!"
    elif score >= 6:
        return "Correcte."
    elif score >= 4:
        return "Cal millorar."
    else:
        return "No compleix els requisits."


def ask_score_and_comment(default_score=None):

    while True:
        try:
            prompt = "\nNota (0-10): "
            if default_score is not None:
                prompt = f"\nNota (0-10) [{default_score}]: "

            raw = input(prompt).strip()
            if raw == "" and default_score is not None:
                score = float(default_score)
            else:
                score = float(raw)

            if 0 <= score <= 10:
                break
        except ValueError:
            pass

        print("**************")
        print("Introdueix un número entre 0 i 10")

    default_comment = default_comment_from_score(score)

    comment = input(f"\nComentari general (ENTER = {default_comment}): ")

    if comment.strip() == "":
        comment = default_comment

    return score, comment
