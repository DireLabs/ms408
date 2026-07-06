from ms408.studies.anchor_labels import _recurrence, recurrence_test


def test_recurrence_counts():
    # 'x' on 3 pages, 'y' on 1, 'z' on 2
    page_tokens = [["x", "y"], ["x", "z"], ["x", "z"]]
    types, recurring, mean = _recurrence(page_tokens)
    assert types == 3
    assert recurring == 2  # x and z appear on >=2 pages
    assert mean == (3 + 1 + 2) / 3


def test_recurrence_empty():
    assert _recurrence([]) == (0, 0, 0.0)


def test_naming_system_detected_when_labels_repeat():
    # a real nomenclature: 6 fixed part-names reused on every page, while running
    # text is globally unique (large pools -> near-zero collision recurrence)
    names = ["rootname", "leafname", "flowername", "stemname", "seedname", "barkname"]
    pages = {
        f"p{i}": {"label": list(names),
                  "running": [f"w{i}_{j}" for j in range(120)]}
        for i in range(15)
    }
    result = recurrence_test(pages, seed=1)
    assert result["label_types_recurring_2plus"] == 6
    assert result["labels_are_naming_system"] is True


def test_no_naming_system_when_labels_hapax():
    # labels all unique (hapax); running text has recurring high-freq words
    pages = {
        f"p{i}": {"label": [f"uniquelabel{i}"],
                  "running": ["daiin", "ol", "chedy"] + [f"r{i}_{j}" for j in range(5)]}
        for i in range(10)
    }
    result = recurrence_test(pages, seed=1)
    assert result["labels_are_naming_system"] is False
    assert result["label_types_recurring_2plus"] == 0
