"""data/resume.yml から公開用の静的サイト(_site/)を生成する。

使い方:
    pip install -r requirements.txt
    python scripts/build.py          # _site/ に出力
"""
from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"


def parse_ym(s: str | None) -> tuple[int, int] | None:
    if not s:
        return None
    y, m = str(s).split("-")
    return int(y), int(m)


def months_between(start: str, end: str | None) -> int:
    sy, sm = parse_ym(start)
    if end:
        ey, em = parse_ym(end)
    else:
        today = date.today()
        ey, em = today.year, today.month
    return (ey - sy) * 12 + (em - sm) + 1


def fmt_ym(s: str | None, sep: str = "年") -> str:
    """'2023-09' -> '2023年9月'。None は '現在'。"""
    if not s:
        return "現在"
    y, m = parse_ym(s)
    return f"{y}{sep}{m}月"


def fmt_dot(s: str | None) -> str:
    """'2023-09' -> '2023.09'。None は ''。"""
    if not s:
        return ""
    y, m = parse_ym(s)
    return f"{y}.{m:02d}"


def fmt_duration(months: int) -> str:
    y, m = divmod(months, 12)
    if y and m:
        return f"{y}年{m}ヶ月"
    if y:
        return f"{y}年"
    return f"{m}ヶ月"


def main() -> None:
    data = yaml.safe_load((ROOT / "data" / "resume.yml").read_text(encoding="utf-8"))

    for c in data["companies"]:
        c["duration"] = fmt_duration(months_between(c["start"], c.get("end")))
        for p in c["projects"]:
            p["duration"] = fmt_duration(months_between(p["start"], p.get("end")))

    all_projects = [p for c in data["companies"] for p in c["projects"]]
    first = min(parse_ym(c["start"]) for c in data["companies"])
    today = date.today()
    stats = {
        "years": today.year - first[0] - (1 if today.month < first[1] else 0),
        "projects": len(all_projects),
        "leads": sum(1 for p in all_projects if p["role"] in ("リーダー", "PL", "PM補佐")),
    }

    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["ym"] = fmt_ym
    env.filters["dot"] = fmt_dot

    html = env.get_template("index.html.j2").render(d=data, stats=stats)

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "index.html").write_text(html, encoding="utf-8")
    shutil.copytree(ROOT / "static", OUT, dirs_exist_ok=True)
    (OUT / ".nojekyll").write_text("")
    print(f"built {OUT / 'index.html'} ({stats['projects']} projects)")


if __name__ == "__main__":
    main()
