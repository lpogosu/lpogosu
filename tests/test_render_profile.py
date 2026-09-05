"""Проверки генератора профиля.

Здесь важнее обычного: ошибка тут выкладывает на витрину ссылку в 404 или,
наоборот, прячет существующий проект — и заметно это только со стороны.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from render_profile import END, START, Layout, RenderError, Repo, render, splice

CONFIG = """
sections:
  - title: Платформа
    topics: [kubernetes, terraform]
  - title: LLM
    topics: [llm, operator]
fallback: Прочее
assign:
  явный: LLM
exclude: [lpogosu]
overrides:
  sharp: Формулировка для витрины
"""


@pytest.fixture
def layout(tmp_path: Path) -> Layout:
    path = tmp_path / "profile.yml"
    path.write_text(CONFIG, encoding="utf-8")
    return Layout.load(path)


def repo(name: str, *topics: str, description: str = "описание") -> Repo:
    return Repo(name=name, description=description, topics=topics,
                url=f"https://github.com/lpogosu/{name}")


def test_repo_lands_in_the_section_matching_its_topics(layout: Layout) -> None:
    assert layout.section_for(repo("a", "kubernetes")) == "Платформа"
    assert layout.section_for(repo("b", "llm")) == "LLM"


def test_section_order_decides_ambiguous_repositories(layout: Layout) -> None:
    """Метки пересекаются у многих проектов; порядок разделов — это приоритет."""
    both = repo("operator", "kubernetes", "llm")
    assert layout.section_for(both) == "Платформа"


def test_explicit_assignment_wins_over_topic_matching(layout: Layout) -> None:
    """Широкие метки есть у многих проектов; спор решает человек, а не порядок строк."""
    assert layout.section_for(repo("явный", "kubernetes", "terraform")) == "LLM"


def test_unknown_topics_fall_back_instead_of_disappearing(layout: Layout) -> None:
    """Забытая метка не должна прятать репозиторий с витрины."""
    assert layout.section_for(repo("mystery", "brainfuck")) == "Прочее"
    out = render([repo("mystery")], layout)
    assert "### Прочее" in out
    assert "mystery" in out


def test_excluded_repository_never_appears(layout: Layout) -> None:
    # Проверяется ссылка на строку таблицы, а не подстрока: имя владельца есть
    # в каждом URL, и наивная проверка прошла бы всегда.
    out = render([repo("lpogosu", "kubernetes"), repo("a", "llm")], layout)
    assert "[lpogosu]" not in out
    assert "[a]" in out


def test_override_replaces_the_repository_description(layout: Layout) -> None:
    out = render([repo("sharp", "llm", description="сухое описание из карточки")], layout)
    assert "Формулировка для витрины" in out
    assert "сухое описание" not in out


def test_a_repository_without_any_description_is_an_error(layout: Layout) -> None:
    """Пустая ячейка в таблице выглядит как недосмотр, а он им и является."""
    with pytest.raises(RenderError, match="без описания"):
        render([repo("silent", "llm", description="")], layout)


def test_rows_are_sorted_so_the_diff_stays_readable(layout: Layout) -> None:
    out = render([repo("zeta", "llm"), repo("alpha", "llm")], layout)
    assert out.index("alpha") < out.index("zeta")


def test_empty_sections_are_not_printed(layout: Layout) -> None:
    out = render([repo("only", "llm")], layout)
    assert "### Платформа" not in out


def test_splice_replaces_only_the_marked_block() -> None:
    readme = f"шапка\n\n{START}\nстарое\n{END}\n\nподвал\n"
    out = splice(readme, "новое\n")
    assert "шапка" in out and "подвал" in out
    assert "старое" not in out and "новое" in out


def test_splice_refuses_a_readme_without_markers() -> None:
    with pytest.raises(RenderError, match="маркеров"):
        splice("никаких маркеров\n", "блок\n")


def test_splice_is_stable_when_run_twice() -> None:
    """Workflow коммитит только при изменениях — значит повтор обязан совпасть."""
    readme = f"шапка\n{START}\nстарое\n{END}\nподвал\n"
    once = splice(readme, "блок\n")
    assert splice(once, "блок\n") == once


def test_layout_without_sections_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "empty.yml"
    path.write_text("fallback: Прочее\n", encoding="utf-8")
    with pytest.raises(RenderError, match="ни одного раздела"):
        Layout.load(path)
