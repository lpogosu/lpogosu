"""Проверить, что каждая ссылка в README открывается.

Профиль — витрина: ссылка в 404 здесь заметнее, чем где бы то ни было, и
появляется она незаметно — достаточно закрыть репозиторий или переименовать его.
Проверка ходит по ссылкам сама, чтобы об этом не приходилось помнить.
"""

from __future__ import annotations

import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

LINK = re.compile(r"\]\((https?://[^)\s]+)\)")
IMAGE = re.compile(r'srcset="(https?://[^"]+)"|src="(https?://[^"]+)"')


def links(text: str) -> list[str]:
    found = {m.group(1) for m in LINK.finditer(text)}
    for match in IMAGE.finditer(text):
        found.add(match.group(1) or match.group(2))
    return sorted(found)


def check(url: str, token: str | None) -> str | None:
    """Вернуть описание проблемы или None, если ссылка в порядке."""
    request = urllib.request.Request(url, method="GET")
    request.add_header("User-Agent", "profile-link-check")
    # Токен нужен только для api.github.com; на обычные страницы он не влияет,
    # а на raw-ссылки приватных файлов дал бы ложное «открывается».
    if token and url.startswith("https://api.github.com/"):
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            if response.status >= 400:
                return f"{response.status}"
    except urllib.error.HTTPError as exc:
        return f"HTTP {exc.code}"
    except Exception as exc:  # любая сетевая беда здесь одинаково важна
        return type(exc).__name__
    return None


def main() -> int:
    readme = Path(sys.argv[1] if len(sys.argv) > 1 else "README.md")
    token = os.environ.get("GITHUB_TOKEN")
    urls = links(readme.read_text(encoding="utf-8"))
    if not urls:
        print("ссылок не найдено — README пуст или изменился формат", file=sys.stderr)
        return 2

    broken: list[tuple[str, str]] = []
    for url in urls:
        problem = check(url, token)
        print(f"  {'ок  ' if problem is None else 'БИТАЯ'}  {url}"
              + (f"  ({problem})" if problem else ""))
        if problem:
            broken.append((url, problem))

    if broken:
        print(f"\nне открываются: {len(broken)} из {len(urls)}", file=sys.stderr)
        return 1
    print(f"\nвсе {len(urls)} ссылок открываются")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
