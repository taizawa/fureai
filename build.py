#!/usr/bin/env python3
"""
ビルドスクリプト
PyInstallerを使用して.exe/.appを作成
"""

import subprocess
import sys
import platform

def install_pyinstaller():
    """PyInstallerをインストール"""
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller', '-q'])

def build():
    """ビルド実行"""
    system = platform.system()

    # 共通オプション
    if system == 'Darwin':  # macOS
        options = [
            'pyinstaller',
            '--onedir',            # ディレクトリにまとめる（macOS .app用）
            '--windowed',          # コンソールウィンドウを表示しない
            '--name=FureaiNet',    # 出力ファイル名
            '--add-data=fureai_auto.py:.',
            '--osx-bundle-identifier=com.fureai.app',
        ]
    elif system == 'Windows':
        options = [
            'pyinstaller',
            '--onefile',           # Windows用は1ファイル
            '--windowed',
            '--name=FureaiNet',
            '--add-data=fureai_auto.py;.',
        ]
    else:
        options = [
            'pyinstaller',
            '--onefile',
            '--name=FureaiNet',
            '--add-data=fureai_auto.py:.',
        ]

    options.append('fureai_app.py')

    print(f"ビルド開始 ({system})")
    print(f"コマンド: {' '.join(options)}")

    subprocess.run(options)

    print()
    print("=" * 50)
    print("ビルド完了!")
    print("=" * 50)
    if system == 'Darwin':
        print("出力: dist/FureaiNet.app")
    elif system == 'Windows':
        print("出力: dist/FureaiNet.exe")
    else:
        print("出力: dist/FureaiNet")

if __name__ == '__main__':
    install_pyinstaller()
    build()
