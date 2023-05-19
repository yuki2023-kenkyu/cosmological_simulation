"""
このコードは、GUIを使用してフリードマン方程式を計算し、結果をグラフとして表示するプログラムです。以下は、このコードの概要です。

1. 必要なライブラリをインポートします。
2. `FriedmannEquationIntegrator`クラスを使用してフリードマン方程式を計算するためのGUIを作成します。
3. イベントハンドラとして、各ボタンや入力フィールドの動作を定義します。
4. イベントハンドラ内で、各イベントに対応する処理を行います。
5. `main()`関数を呼び出して、プログラムを実行します。

このコードでは、PySimpleGUIを使用してGUIを作成し、`FriedmannEquationIntegrator`クラスを使用してフリードマン方程式の計算を行っています。計算結果は3Dグラフとして表示されます。

注意点：
このコードの実行には、`calculate.py`、`GUI_design.py`、`output.py`という他のファイルが必要です。これらのファイルが正しくインポートされていることを確認してください。また、設定ファイルも必要であり、適切なフォーマットで提供されている必要があります。
"""

import PySimpleGUI as sg
import configparser
import numpy as np

from calculate import FriedmannEquationIntegrator, Friedmann_Equation, rotate_coordinates
from GUI_design import Widget
from output import draw_figure_w_toolbar, draw_plot

class EventHandlers:
    def __init__(self, window, config_ini):
        self.window = window
        self.config_ini = config_ini
        self.x_new = None
        self.y_new = None
        self.z_new = None

    def handle_file_event(self, values):
        # 設定ファイルを読み込む準備
        file_path = values["-FILE-"]
        self.config_ini.read(file_path, encoding='utf-8')
        model_name = self.config_ini.sections()
        self.window["-MODEL-"].Update(values=model_name)

    def handle_model_event(self, values):
        # 選択されたモデルに応じて初期値を設定
        model = str(values["-MODEL-"])
        default_sigma = float(self.config_ini.get(model, "sigma_0"))
        default_q = float(self.config_ini.get(model, "q_0"))
        self.window["-SIGMA-"].Update(default_sigma)
        self.window["-Q-"].Update(default_q)
        self.window["-SIGMA-TEXT-"].Update(default_sigma)
        self.window["-Q-TEXT-"].Update(default_q)

    def handle_sigma_event(self, values):
        # スライダーの値をテキストに反映
        self.window["-SIGMA-TEXT-"].Update(values["-SIGMA-"])

    def handle_q_event(self, values):
        # スライダーの値をテキストに反映
        self.window["-Q-TEXT-"].Update(values["-Q-"])

    def handle_sigma_text_event(self, values):
        # テキストの値をスライダーに反映
        self.window["-SIGMA-"].Update(values["-SIGMA-TEXT-"])

    def handle_q_text_event(self, values):
        # テキストの値をスライダーに反映
        self.window["-Q-"].Update(values["-Q-TEXT-"])

    def handle_execute_event(self, values):
        # 計算実行ボタンが押されたときの処理
        sigma_0 = float(values["-SIGMA-TEXT-"])
        q_0 = float(values["-Q-TEXT-"])
        K = np.sign(3 * sigma_0 - q_0 - 1.0)
        Lambda = 3 * (sigma_0 - q_0)

        elev = float(values["-ELEV-"])
        azim = float(values["-AZIM-"])

        # フリードマン方程式を数値積分して座標を計算
        instance = FriedmannEquationIntegrator(Friedmann_Equation, rotate_coordinates, sigma_0, q_0, K, Lambda)
        self.x_new, self.y_new, self.z_new = instance.calculate_rotated_coordinates()
        sg.popup_ok('計算が実行されました。')

    def handle_plot_event(self, elev, azim):
        # グラフ表示ボタンが押されたときの処理
        if self.x_new is not None and self.y_new is not None and self.z_new is not None:
            fig_3d = draw_plot(elev, azim, self.x_new, self.y_new, self.z_new)
            draw_figure_w_toolbar(self.window['-CANVAS-'].TKCanvas, fig_3d, self.window['-CONTROLS-'].TKCanvas)
        else:
            sg.popup_error('実行ボタンを先にクリックしてください。')


def main():
    Widget.make_dpi_aware()
    window = Widget.create_main_window()

    # 設定ファイルの読み込み
    config_ini = configparser.ConfigParser()

    # イベントハンドラーオブジェクトの作成
    handlers = EventHandlers(window, config_ini)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "中止":
            sg.popup_ok('中止しました。')
            break

        # 各イベントごとの処理をイベントハンドラークラス内のメソッドに移動
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
            handlers.handle_plot_event(float(values["-ELEV-"]), float(values["-AZIM-"]))

    window.close()


if __name__ == "__main__":
    main()
