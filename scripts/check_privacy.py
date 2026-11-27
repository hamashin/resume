"""公開前の簡易チェック：data/ に個人情報らしき文字列が入っていないかを調べる。

見つかった場合は終了コード1でビルドを止める。
（現職の社名などの「伏せたい固有名詞」は、このファイルに書くと公開されてしまうため、
 ここでは扱わない。必要ならリポジトリの Secrets に NG_WORDS をカンマ区切りで登録すると、
 その語も検査する）
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PATTERNS = {
    "メールアドレス": r"[\w.+-]+@[\w-]+\.[\w.-]+",
    "電話番号": r"0\d{1,4}-?\d{1,4}-?\d{3,4}\b|\b0[789]0\d{8}\b",
    "郵便番号": r"〒\s*\d{3}|\b\d{3}-\d{4}\b",
    "生年月日": r"生年月日|\d{4}年\d{1,2}月\d{1,2}日生",
}

ng_words = [w.strip() for w in os.environ.get("NG_WORDS", "").split(",") if w.strip()]

found = []
for path in (ROOT / "data").rglob("*"):
    if not path.is_file():
        continue
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for label, pat in PATTERNS.items():
            if re.search(pat, line):
                found.append(f"{path.relative_to(ROOT)}:{n}: {label}らしき記述")
        for w in ng_words:
            if w in line:
                found.append(f"{path.relative_to(ROOT)}:{n}: 非公開にしている語が含まれています")

if found:
    print("\n".join(found))
    sys.exit(1)
print("privacy check: ok")
