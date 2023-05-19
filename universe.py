"""
このコードは、GUIを使用してフリードマン方程式を計算し、結果をグラフとして表示するプログラムです。以下は、このコードの概要です。

1. 必要なライブラリをインポートします。
2. `FriedmannEquationIntegrator`クラスを使用してフリードマン方程式を計算するためのGUIを作成します。
3. イベントハンドラとして、各ボタンや入力フィールドの動作を定義します。
4. イベントハンドラ内で、各イベントに対応する処理を行います。
5. `main()`関数を呼び出して、プログラムを実行します。

このコードでは、PySimpleGUIを使用してGUIを作成し、`FriedmannEquationIntegrator`クラスを使用してフリードマン方程式の計算を行っています。
計算結果は3Dグラフとして表示されます。

注意点：
このコードの実行には、`calculate.py`、`guidesign.py`、`output.py`、`eventhandlers.py`という他のファイルが必要です。
これらのファイルが正しくインポートされていることを確認してください。
また、設定ファイルも必要であり、適切なフォーマットで提供されている必要があります。
"""

import configparser
import PySimpleGUI as sg
from guidesign import Widget
from eventhandlers import EventHandlers


def main():
    """
    メイン関数
    """
    Widget.make_dpi_aware()
    window = Widget.create_main_window()
    config_ini = configparser.ConfigParser()

    handlers = EventHandlers(window, config_ini)

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, '中止'):
            sg.popup_ok('中止しました。')
            break

        if event == "-FILE-":
            handlers.handle_file_event(values)

        elif event == "-MODEL-":
            handlers.handle_model_event(values)

        elif event == "-SIGMA-":
            handlers.handle_sigma_event(values)

        elif event == "-Q-":
            handlers.handle_q_event(values)

        elif event == "-SIGMA-TEXT-":
            handlers.handle_sigma_text_event(values)

        elif event == "-Q-TEXT-":
            handlers.handle_q_text_event(values)

        elif event == "実行":
            handlers.handle_execute_event(values)

        elif event == "グラフ表示":
            handlers.handle_plot_event(values)

    window.close()


if __name__ == "__main__":
    main()
