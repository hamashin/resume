# resume

インフラエンジニアの職務経歴書を、GitHub Pages で公開するためのリポジトリです。

公開ページ: https://hamashin.github.io/resume/

## 仕組み

```
data/resume.yml ──(scripts/build.py)──▶ _site/index.html ──(GitHub Actions)──▶ GitHub Pages
```

- 経歴の中身は `data/resume.yml` だけで管理します。
- `main` ブランチに push すると、GitHub Actions（`.github/workflows/pages.yml`）が
  個人情報チェック → ビルド → 公開 を自動で行います。
- 見た目は `templates/index.html.j2`（HTML）と `static/style.css`（CSS）です。

## 更新のしかた

1. `data/resume.yml` を編集する（案件は `companies[].projects[]` に新しい順で追加）
2. commit して `main` に push する
3. 1〜2分後にページに反映される（Actions タブで進み具合を確認できる）

### 手元で確認する場合

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python scripts/check_privacy.py
python scripts/build.py
python -m http.server -d _site 8000   # http://localhost:8000 を開く
```

## 公開しないもの

- 氏名・住所・電話番号・メールアドレス・生年月日・学校名などの個人情報
- 現職の社名と、現職での顧客名

`scripts/check_privacy.py` が、メールアドレス・電話番号・郵便番号らしき文字列を検出するとビルドを止めます。
伏せたい固有名詞（社名など）も検査したい場合は、リポジトリの Settings → Secrets and variables → Actions に
`NG_WORDS`（カンマ区切り）を登録してください（ワークフローは設定済みです）。
語そのものはリポジトリに書かずに済みます。

## 印刷・PDF

ブラウザの印刷から A4 で PDF にできます（印刷用のレイアウトを `static/style.css` に用意しています）。
