# ふれあいネット 抽選申込アプリ

川崎市ふれあいネット（https://www.fureai-net.city.kawasaki.jp/sp/）の抽選申込を自動化するアプリです。

## 機能

- 25人のアカウントから複数選択して一括申込
- 最大8件の申込設定（施設・日時）
- 設定の保存・読み込み
- 動作確認モード（申込せずに確認だけ）

## ファイル構成

```
fureai/
├── fureai_app.py      # GUIアプリ本体
├── fureai_auto.py     # 自動入力ロジック
├── fureai_config.json # 設定ファイル（自動生成）
├── build.py           # ビルドスクリプト
├── requirements.txt   # 依存パッケージ
└── dist/              # ビルド出力先
    ├── FureaiNet.exe  # Windows用（Windowsでビルド時）
    └── FureaiNet.app  # macOS用（macOSでビルド時）
```

---

## 使い方

### アプリの操作

1. **アカウント選択**
   - 使いたいアカウントにチェックを入れる
   - 「全選択」「全解除」ボタンで一括操作可能

2. **共通設定**
   - 利用目的、人数、催し物名を設定

3. **申込設定**
   - 各行のチェックボックスをONにして有効化
   - 施設、月、日、開始時間、終了時間を選択
   - 最大8件まで設定可能

4. **実行**
   - 「動作確認（申込しない）」→ 確認画面まで進むが申込はしない
   - 「申込実行」→ 実際に申込を行う

5. **設定を保存**
   - 次回起動時に設定が復元される

### 初回起動時の注意（Windows）

セキュリティ警告が出た場合：
1. 「詳細情報」をクリック
2. 「実行」をクリック

---

## ビルド方法

### 前提条件

- Python 3.8以上
- pip（Pythonパッケージマネージャー）

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

または個別にインストール：

```bash
pip install pyinstaller requests beautifulsoup4 openpyxl PyQt5
```

### 2. ビルド実行

```bash
python build.py
```

### 3. 出力先

- **Windows**: `dist/FureaiNet.exe`
- **macOS**: `dist/FureaiNet.app`

---

## Windows用ビルド手順（詳細）

Windows環境で以下を実行：

```powershell
# 1. このフォルダに移動
cd fureai

# 2. 依存パッケージをインストール
pip install pyinstaller requests beautifulsoup4 openpyxl PyQt5

# 3. ビルド実行
python build.py

# 4. 完成
# dist/FureaiNet.exe が生成される
```

### 配布時の注意

- `FureaiNet.exe` だけを渡せばOK（Pythonは不要）
- 初回起動時にWindows Defenderの警告が出る場合あり

---

## macOS用ビルド手順（詳細）

```bash
# 1. このフォルダに移動
cd fureai

# 2. 依存パッケージをインストール
pip3 install pyinstaller requests beautifulsoup4 openpyxl PyQt5

# 3. ビルド実行
python3 build.py

# 4. 完成
# dist/FureaiNet.app が生成される
```

### 配布時の注意

- `FureaiNet.app` フォルダごと渡す
- 初回起動時に「開発元を確認できない」警告が出る場合：
  - 右クリック → 「開く」を選択

---

## 対応施設

| 施設名 | 地域 | 時間枠 |
|--------|------|--------|
| 等々力第１サッカー場 | 中原区 | 6:00, 8:00, 10:00, 12:00, 14:00, 16:00, 18:30 |
| 等々力第２サッカー場 | 中原区 | 6:00, 8:00, 10:00, 12:00, 14:00, 16:00, 18:30 |
| 上平間サッカー場 | 中原区 | 6:00, 8:00, 10:00, 12:00, 14:00, 16:00, 18:00 |
| 丸子橋第１ | 中原区 | 8:00, 12:00, 16:00 |
| 丸子橋第３ | 中原区 | 8:00, 12:00, 16:00 |
| 古市場サッカー場 | 幸区 | 6:00, 8:00, 10:00, 12:00, 14:00, 16:00, 18:00 |

---

## トラブルシューティング

### Windows: 「No module named 'PyQt5'」エラー

複数のPythonがインストールされている場合、pipでインストールしたパッケージが別のPythonに入っている可能性があります。

**確認方法：**
```cmd
where python
pip show PyQt5
```

Location（PyQt5のインストール先）とpythonのパスが異なる場合、`py`コマンドでバージョンを指定：

```cmd
py -3.13 -m pip install pyinstaller requests beautifulsoup4 openpyxl PyQt5
py -3.13 fureai_app.py
py -3.13 build.py
```

※ `-3.13`の部分はPyQt5がインストールされているPythonのバージョンに合わせてください。

---

### ログインに失敗する

- ユーザーID、パスワードが正しいか確認
- ふれあいネットのサイトがメンテナンス中でないか確認

### 「抽選対象外」エラー

- 選択した日付が抽選期間内か確認
- 抽選申込は通常、利用日の1ヶ月前から受付

### アプリが起動しない（Windows）

- Microsoft Visual C++ 再頒布可能パッケージをインストール
- https://aka.ms/vs/17/release/vc_redist.x64.exe

---

## MacでWindows用.exeをビルドする方法

MacしかないけどWindows用の.exeを作りたい場合の手順です。

### 1. VMware Fusion Proをダウンロード（無料）

1. https://www.vmware.com/products/desktop-hypervisor/workstation-and-fusion にアクセス
2. 「Download Fusion」をクリック
3. Broadcomアカウント作成が必要（無料）
4. ダウンロードした`.dmg`を開いてインストール

### 2. Windows 11のISOをダウンロード

**Intel Mac の場合:**
1. https://www.microsoft.com/ja-jp/software-download/windows11 にアクセス
2. 「Windows 11 ディスク イメージ (ISO) をダウンロードする」を選択
3. 「Windows 11 (multi-edition ISO)」を選択
4. 言語「日本語」を選択
5. 「64-bit ダウンロード」をクリック（約6GB）

**Apple Silicon Mac（M1/M2/M3）の場合:**
- https://www.microsoft.com/ja-jp/software-download/windows11arm64 からARM版をダウンロード

### 3. VMware FusionでWindows VMを作成

1. VMware Fusionを起動
2. 「ファイル」→「新規」
3. 「ディスクまたはイメージからインストール」を選択
4. ダウンロードしたWindows 11のISOを選択
5. 設定：
   - メモリ: 4GB以上推奨
   - ストレージ: 60GB以上推奨
6. 「完了」でインストール開始

### 4. Windows 11の初期設定

インストールが始まったら画面に従って設定：

1. 地域「日本」
2. キーボード「Microsoft IME」
3. **ネットワーク接続をスキップする裏技**（Microsoftアカウント回避）：
   - `Shift + F10`でコマンドプロンプトを開く
   - `oobe\bypassnro` と入力してEnter
   - 再起動後「インターネットに接続していません」が選べる
4. ローカルアカウントを作成

### 5. Pythonをインストール（Windows内で）

1. https://www.python.org/downloads/ にアクセス
2. 「Download Python 3.x.x」をクリック
3. インストーラーを実行
4. **重要**: 「Add Python to PATH」にチェックを入れる
5. 「Install Now」

### 6. fureaiフォルダをWindowsにコピー

**方法A: 共有フォルダ（簡単）**
1. VMware Fusion メニュー →「仮想マシン」→「共有」→「共有設定」
2. 「Mac から Windows への共有を有効にする」をON
3. fureaiフォルダを追加
4. Windows側で`\\vmware-host\Shared Folders`にアクセス

**方法B: ドラッグ&ドロップ**
1. VMware Fusionメニュー →「仮想マシン」→「VMware Toolsのインストール」
2. 再起動後、MacからWindowsにファイルをドラッグ&ドロップ可能

### 7. ビルド実行（Windows内で）

コマンドプロンプトまたはPowerShellを開いて：

```powershell
# fureaiフォルダに移動
cd C:\Users\ユーザー名\Desktop\fureai

# 依存パッケージをインストール
pip install pyinstaller requests beautifulsoup4 openpyxl PyQt5

# ビルド実行
python build.py
```

完了後、`dist\FureaiNet.exe` が生成される。

### 8. .exeをMacに持ってくる

1. `dist\FureaiNet.exe` を共有フォルダにコピー
2. または直接Macにドラッグ&ドロップ

### 所要時間の目安

| 作業 | 時間 |
|------|------|
| VMware Fusionダウンロード | 5分 |
| Windows ISOダウンロード | 10-30分（回線次第） |
| Windowsインストール | 20-30分 |
| Python + ビルド | 10分 |
| **合計** | **約1時間** |

---

## 開発者向け

### 直接実行（ビルドせずに）

```bash
python fureai_app.py
```

### アカウント情報の更新

`fureai_app.py` の `ACCOUNTS` リストを編集

### 施設の追加

`fureai_app.py` の `FACILITIES` 辞書を編集
