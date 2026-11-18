"""Pure helpers to merge grades of several periods (no Home Assistant dependency)."""


def merge_grades(*grade_lists):
    """Union of grade lists, de-duplicated by `id`, sorted by date descending.

    Grades without an id are always kept (they cannot be de-duplicated safely).
    None / empty lists are ignored.
    """
    seen = set()
    merged = []
    for grades in grade_lists:
        for grade in grades or []:
            grade_id = getattr(grade, "id", None)
            if grade_id:
                if grade_id in seen:
                    continue
                seen.add(grade_id)
            merged.append(grade)
    return sorted(merged, key=lambda grade: grade.date, reverse=True)
