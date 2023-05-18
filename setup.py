import sys
from cx_Freeze import setup, Executable
 
base = None
 
if sys.platform == 'win32': base = 'Win32GUI'

# exeにするソースファイルを指定
exe = Executable(script = "universe.py", base= base)
 
setup(name = 'Universe', #ファイルの名前
    version = '0.2',     #バージョン表記]
    author = 'Yuki Hashimoto', #作者の名前
    description = '一様等方宇宙モデルのシミュレーション', #アプリケーションの説明
    executables = [exe])  #実行ファイルの形式