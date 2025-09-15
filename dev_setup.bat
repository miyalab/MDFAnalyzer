@echo off

@rem 仮想環境
py -m venv .venv

@rem 必要モジュールのインストール
.venv\Scripts\python -m pip install pip --upgrade
.venv\Scripts\pip install openpyxl
.venv\Scripts\pip install asammdf
.venv\Scripts\pip install pyinstaller
.venv\Scripts\pip install inspect
