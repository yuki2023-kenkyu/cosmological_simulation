# cosmological_simulation
このアプリは一様等方宇宙モデルの３次元シミュレーションを行うことができるアプリです．

# 始め方
- git clone を行います．
```
git clone https://github.com/yuki2023-kenkyu/cosmological_simulation/
```
- 仮想環境を作成してライブラリをインストールします．
```
cd cosmological_simulation
python -m venv myvenv
myvenv\scripts\activate
pip install -r requirements.txt
```
- Universe.pyを起動します．
```
python Universe.py
```

# 使用方法
1. 設定ファイルの読み込み
    - アプリケーションの起動後，まず設定ファイルを読み込みます．
    - 「Browse」ボタンをクリックし，「Universe.py」と同じ階層に含まれている「config.ini」を選択してください．
<img width="503" alt="image" src="https://github.com/yuki2023-kenkyu/cosmological_simulation/assets/124911019/8c7f497c-3021-4a32-85c0-eaa53918be0c">

2. モデルの選択
    - 設定ファイルが正常に読み込まれていれば，その下の「モデルを選択」のコンボボックスから宇宙モデルを選択することができます．
<img width="503" alt="image" src="https://github.com/yuki2023-kenkyu/cosmological_simulation/assets/124911019/d326d55c-86e4-4f54-81ec-21e98d331423">

3. パラメーターの設定
    - モデルを選択すると，自動的にパラメータが設定されます．
    - スライダーを動かしたり，あるいはテキストボックスに半角数字を打ち込むことによってもパラメーターを設定できます．
    - sigma_0の値の範囲は0.0~1.5，q_0の値の範囲は-2.0~2.0となっていることに注意してください．
<img width="503" alt="image" src="https://github.com/yuki2023-kenkyu/cosmological_simulation/assets/124911019/ecb2ae8a-3cc1-414b-9f79-81bc92c6b869">

4. グラフの表示設定
    - こちらは最初に表示される画像の視点を設定できます．
    - デフォルトで仰角と方位角共に0度となっていますが，マウスで動かすことができるので設定の必要はありません．
<img width="503" alt="image" src="https://github.com/yuki2023-kenkyu/cosmological_simulation/assets/124911019/a4a443b7-3907-413f-be5e-784d82f5d9ac">

5. 計算の実行
    - 下にある実行ボタンをクリックすると計算が開始します．
    - 計算終了後，「計算が実行されました。」というポップアップが表示されるので，OKボタンをクリックしてください．
<img width="503" alt="image" src="https://github.com/yuki2023-kenkyu/cosmological_simulation/assets/124911019/6d41fab8-b2ed-4601-9a5b-805621246a93">

6. グラフの表示
    - 計算実行後，グラフ表示ボタンをクリックすることで，ボタン下に宇宙モデルの３次元グラフの画像が表示されます．
    - グラフ上でマウスをドラッグするなどするとグラフをぐりぐり動かすことができます．
<img width="503" alt="image" src="https://github.com/yuki2023-kenkyu/cosmological_simulation/assets/124911019/e92e83d9-bce5-42ec-bbf0-20643f2c4235">

7. 画像の保存
    - 画像を保存する際はグラフの左上にあるツールバーの右端にある保存アイコンをクリックしてください．
    - 保存先を選択し，名前を入力すれば完了です．
<img width="634" alt="image" src="https://github.com/yuki2023-kenkyu/cosmological_simulation/assets/124911019/9898378a-0f1a-40de-a39d-bba96b880fbf">

8. アプリの終了
    - アプリを終了する際は，右上の✕をクリックするか，実行ボタンの隣にある中止ボタンをクリックしてください．
