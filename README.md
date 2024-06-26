# cosmological_simulation
## Author:Yuki Hashimoto, Fukushima University
このパッケージは、GUIを使用してフリードマン方程式を計算し、結果をグラフとして表示するシミュレーションプログラムです。

URL:https://github.com/yuki2023-kenkyu/cosmological_simulation/

メイン実行部分のプログラムは`universe.py`です。

以下は、`universe.py`の概要です。

1. 必要なライブラリをインポートします。
2. `Widget`クラスを使用してGUIのウィンドウを作成します。
3. `EventHandler`クラスを使用して各イベントに対応する処理を定義します。
4. `main()`関数を呼び出して、プログラムを実行します。
5. アプリケーションが起動し、シミュレーションを開始します。

このコードでは、PySimpleGUIを使用してGUIを作成し、`FriedmannEquationIntegrator`クラスを使用してフリードマン方程式の計算を行っています。
計算結果は3Dグラフとして表示されます。

注意点：
このコードの実行には、`calculate.py`、`guidesign.py`、`output.py`、`eventhandlers.py`という他のファイルが必要です。
これらのファイルが正しくインポートされていることを確認してください。
また、設定ファイルも必要であり、適切なフォーマットで提供されている必要があります。

# インストール方法
- gitをインストールします．
    - 次のURLを参考にgitをインストールしてください．
    - URL：[Git downloading Package](https://git-scm.com/download/win)
- Pythonをインストールします．
    - 以下のURLから「Python3.7」を選択し，「python-3.7.9-amd64.exe」をダウンロードしてください．
    - URL：[非公式Pythonダウンロードリンク](https://pythonlinks.python.jp/ja/index.html)
    - 以下のURLを参考にPythonのインストールを進めてください．
    - URL：[Windows版Pythonのインストール](https://www.python.jp/install/windows/install.html)
- git clone を行います．
```
git clone https://github.com/yuki2023-kenkyu/cosmological_simulation/
```
- コマンドプロンプトを開き，仮想環境を作成してライブラリをインストールします．
```
cd cosmological_simulation
python -m venv myvenv
myvenv\scripts\activate
pip install -r requirements.txt
```
- universe.pyを起動します．
```
python universe.py
```

# アプリの操作方法
1. 設定ファイルの読み込み
    - アプリケーションの起動後，まず設定ファイルを読み込みます．
    - 「Browse」ボタンをクリックし，「universe.py」と同じ階層に含まれている「config.ini」を選択してください．
![image](https://github.com/yuki2023-kenkyu/cosmological_simulation/assets/124911019/1b72cdf6-16e3-4c57-a283-3044a758ef25)

2. モデルの選択
    - 設定ファイルが正常に読み込まれていれば，その下の「モデルを選択」のコンボボックスから宇宙モデルを選択することができます．
![image](https://github.com/yuki2023-kenkyu/cosmological_simulation/assets/124911019/332a11e8-66cf-4329-91e3-90c153031e99)

3. パラメーターの設定
    - モデルを選択すると，自動的にパラメータが設定されます．
    - スライダーを動かしたり，あるいはテキストボックスに半角数字を打ち込むことによってもパラメーターを設定できます．
    - sigma_0の値の範囲は0.0 ~ 1.5，q_0の値の範囲は-2.0 ~ 2.0となっていることに注意してください．
![image](https://github.com/yuki2023-kenkyu/cosmological_simulation/assets/124911019/14dc20d1-6325-461b-9f49-c98de5e416c3)

4. 計算の実行
    - 下にある実行ボタンをクリックすると計算が開始します．
    - 計算終了後，「計算が実行されました。」というポップアップが表示されるので，OKボタンをクリックしてください．
![image](https://github.com/yuki2023-kenkyu/cosmological_simulation/assets/124911019/53af72a4-5880-479b-b46f-45323e1d9e66)

5. グラフの表示
    - 計算実行後，グラフ表示ボタンをクリックすることで，ボタン下に宇宙モデルの３次元グラフの画像が表示されます．
    - グラフ上でマウスをドラッグするなどするとグラフをぐりぐり動かすことができます．
![image](https://github.com/yuki2023-kenkyu/cosmological_simulation/assets/124911019/1e829851-7a68-4fd4-b994-f68a78381710)

6. 画像の保存
    - 画像を保存する際はグラフの左上にあるツールバーの右端にある保存アイコンをクリックしてください．
    - 保存先を選択し，名前を入力すれば完了です．
![image](https://github.com/yuki2023-kenkyu/cosmological_simulation/assets/124911019/0f2de47b-fbc5-432c-be47-05aa3c1e3fac)

7. アプリの終了
    - アプリを終了する際は，右上の✕をクリックするか，実行ボタンの隣にある中止ボタンをクリックしてください．
