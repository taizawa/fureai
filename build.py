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

    # 共通オプション（python -m PyInstaller を使用）
    if system == 'Darwin':  # macOS
        options = [
            sys.executable, '-m', 'PyInstaller',
            '--onedir',            # ディレクトリにまとめる（macOS .app用）
            '--windowed',          # コンソールウィンドウを表示しない
            '--name=FureaiNet',    # 出力ファイル名
            '--add-data=fureai_auto.py:.',
            '--osx-bundle-identifier=com.fureai.app',
        ]
    elif system == 'Windows':
        options = [
            sys.executable, '-m', 'PyInstaller',
            '--onefile',           # Windows用は1ファイル
            '--windowed',
            '--name=FureaiNet',
            '--add-data=fureai_auto.py;.',
            '--hidden-import=PyQt5',
            '--hidden-import=PyQt5.QtCore',
            '--hidden-import=PyQt5.QtGui',
            '--hidden-import=PyQt5.QtWidgets',
            '--hidden-import=requests',
            '--hidden-import=bs4',
            '--collect-all=PyQt5',
        ]
    else:
        options = [
            sys.executable, '-m', 'PyInstaller',
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
