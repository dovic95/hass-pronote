import importlib.util
import pathlib
from datetime import date
from types import SimpleNamespace

spec = importlib.util.spec_from_file_location(
    "grades_merge",
    pathlib.Path(__file__).parents[1] / "custom_components/pronote/grades_merge.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
merge_grades = mod.merge_grades


def g(id_, d):
    return SimpleNamespace(id=id_, date=date(2026, *d))


def test_union_sorted_desc():
    t1 = [g("a", (9, 10)), g("b", (10, 5))]
    t2 = [g("c", (11, 2))]
    assert [x.id for x in merge_grades(t2, t1)] == ["c", "b", "a"]


def test_dedup_by_id():
    a = g("a", (9, 10))
    assert len(merge_grades([a], [a, g("b", (9, 11))])) == 2


def test_none_and_empty_ignored():
    assert merge_grades(None, [], [g("a", (9, 1))])[0].id == "a"


def test_no_cap():
    many = [g(str(i), (9, 1 + i % 28)) for i in range(100)]
    assert len(merge_grades(many)) == 100


def test_grades_without_id_kept():
    assert len(merge_grades([g(None, (9, 1)), g(None, (9, 1))])) == 2
