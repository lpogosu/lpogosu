"""Собрать блок со списком репозиториев для README профиля.

README между маркерами принадлежит генератору, всё остальное — человеку.
Источник правды о содержании — сам GitHub: состав берётся из списка репозиториев
аккаунта, раздел выводится из topics, описание — из поля description.

Так профиль не может разойтись с действительностью: закрытый репозиторий исчезает
из таблицы сам, новый появляется сам, и ссылки не ведут в 404.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

API = "https://api.github.com"
OWNER = "lpogosu"
START = "<!-- repos:start -->"
END = "<!-- repos:end -->"


class RenderError(RuntimeError):
    pass


@dataclass(frozen=True)
class Repo:
    name: str
    description: str
    topics: tuple[str, ...]
    url: str

    @property
    def row(self) -> str:
        return f"| [{self.name}]({self.url}) | {self.description} |"


@dataclass(frozen=True)
class Layout:
    sections: tuple[tuple[str, frozenset[str]], ...]
    fallback: str
    exclude: frozenset[str]
    overrides: dict[str, str]
    assign: dict[str, str]

    @classmethod
    def load(cls, path: Path) -> Layout:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        sections = tuple(
            (s["title"], frozenset(s.get("topics", []))) for s in raw.get("sections", [])
        )
        if not sections:
            raise RenderError(f"{path} не описывает ни одного раздела")
        return cls(
            sections=sections,
            fallback=raw.get("fallback", "Прочее"),
            exclude=frozenset(raw.get("exclude", [])),
            overrides={k: " ".join(v.split()) for k, v in (raw.get("overrides") or {}).items()},
            assign=dict(raw.get("assign") or {}),
        )

    def section_for(self, repo: Repo) -> str:
        """Раздел из `assign`, иначе первый совпавший по topics, иначе fallback.

        Порядок разделов в конфиге работает как приоритет, но широкие метки
        (`kubernetes`, `observability`) есть у многих проектов, поэтому спорные
        случаи разрешаются явным назначением, а не подбором порядка строк.
        """
        if repo.name in self.assign:
            return self.assign[repo.name]
        for title, topics in self.sections:
            if topics & set(repo.topics):
                return title
        return self.fallback


def fetch_repos(token: str) -> list[Repo]:
    """Публичные, не форки, не архивные — то, что можно показать и открыть."""
    request = urllib.request.Request(
        f"{API}/users/{OWNER}/repos?per_page=100&type=owner&sort=full_name",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        payload: list[dict[str, Any]] = json.load(urllib.request.urlopen(request, timeout=30))
    except urllib.error.HTTPError as exc:  # pragma: no cover - сетевой путь
        raise RenderError(f"GitHub ответил {exc.code}: {exc.read().decode()[:200]}") from exc

    repos = []
    for item in payload:
        if item["private"] or item["fork"] or item.get("archived"):
            continue
        repos.append(
            Repo(
                name=item["name"],
                description=(item.get("description") or "").strip(),
                topics=tuple(item.get("topics") or []),
                url=item["html_url"],
            )
        )
    return repos


def render(repos: list[Repo], layout: Layout) -> str:
    visible = [r for r in repos if r.name not in layout.exclude]
    described = [
        Repo(r.name, layout.overrides.get(r.name, r.description), r.topics, r.url)
        for r in visible
    ]

    missing = [r.name for r in described if not r.description]
    if missing:
        raise RenderError(
            "без описания, и подставить нечего: "
            + ", ".join(sorted(missing))
            + ". Заполните description репозитория или добавьте overrides в profile.yml."
        )

    grouped: dict[str, list[Repo]] = {}
    for repo in described:
        grouped.setdefault(layout.section_for(repo), []).append(repo)

    order = [title for title, _ in layout.sections] + [layout.fallback]
    lines: list[str] = []
    for title in order:
        rows = sorted(grouped.get(title, []), key=lambda r: r.name)
        if not rows:
            continue
        lines += [f"### {title}", "", "| Репозиторий | О чём |", "|---|---|"]
        lines += [r.row for r in rows]
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def splice(readme: str, block: str) -> str:
    if START not in readme or END not in readme:
        raise RenderError(f"в README нет маркеров {START} и {END}")
    head, _, rest = readme.partition(START)
    _, _, tail = rest.partition(END)
    return f"{head}{START}\n\n{block}\n{END}{tail}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readme", type=Path, default=Path("README.md"))
    parser.add_argument("--config", type=Path, default=Path("profile.yml"))
    parser.add_argument(
        "--check",
        action="store_true",
        help="ничего не писать; выйти с кодом 1, если README устарел",
    )
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("нужен GITHUB_TOKEN в окружении", file=sys.stderr)
        return 2

    try:
        layout = Layout.load(args.config)
        block = render(fetch_repos(token), layout)
        current = args.readme.read_text(encoding="utf-8")
        updated = splice(current, block)
    except RenderError as exc:
        print(f"ошибка: {exc}", file=sys.stderr)
        return 2

    if updated == current:
        print("README актуален")
        return 0
    if args.check:
        print("README устарел: список репозиториев разошёлся с аккаунтом", file=sys.stderr)
        return 1

    with args.readme.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(updated)
    print(f"README обновлён: {len(block.splitlines())} строк в блоке")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
