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
このコードの実行には、`calculate.py`、`GUI_design.py`、`output.py`という他のファイルが必要です。
これらのファイルが正しくインポートされていることを確認してください。
また、設定ファイルも必要であり、適切なフォーマットで提供されている必要があります。
"""

import configparser
import PySimpleGUI as sg
import numpy as np

from calculate import (
    FriedmannEquationIntegrator,
    friedmann_equation,
    rotate_coordinates,
)
from guidesign import Widget
from output import draw_figure_w_toolbar, draw_plot


class EventHandlers:
    """
    イベントハンドラーをまとめたクラス
    """
    def __init__(self, window, config_ini):
        self.window = window
        self.config_ini = config_ini
        self.x_new = None
        self.y_new = None
        self.z_new = None

    def handle_file_event(self, values):
        """
        設定ファイル読み込みイベント発生時の処理
        """
        file_path = values["-FILE-"]
        self.config_ini.read(file_path, encoding='utf-8')
        model_name = self.config_ini.sections()
        self.window["-MODEL-"].Update(values=model_name)

    def handle_model_event(self, values):
        """
        モデル選択イベント発生時の処理
        """
        model = str(values["-MODEL-"])
        default_sigma = float(self.config_ini.get(model, "sigma_0"))
        default_q = float(self.config_ini.get(model, "q_0"))
        self.window["-SIGMA-"].Update(default_sigma)
        self.window["-Q-"].Update(default_q)
        self.window["-SIGMA-TEXT-"].Update(default_sigma)
        self.window["-Q-TEXT-"].Update(default_q)

    def handle_sigma_event(self, values):
        """
        sigma_0のテキストボックスにスライダーの値を反映する処理
        """
        self.window["-SIGMA-TEXT-"].Update(values["-SIGMA-"])

    def handle_q_event(self, values):
        """
        q_0のテキストボックスにスライダーの値を反映する処理
        """
        self.window["-Q-TEXT-"].Update(values["-Q-"])

    def handle_sigma_text_event(self, values):
        """
        sigma_0のスライダーにテキストボックスの値を反映する処理
        """
        self.window["-SIGMA-"].Update(values["-SIGMA-TEXT-"])

    def handle_q_text_event(self, values):
        """
        q_0のスライダーにテキストボックスの値を反映する処理
        """
        self.window["-Q-"].Update(values["-Q-TEXT-"])

    def handle_execute_event(self, values):
        """
        実行ボタンがクリックされた後の計算処理
        """
        sigma_0 = float(values["-SIGMA-TEXT-"])
        q_0 = float(values["-Q-TEXT-"])
        K = np.sign(3 * sigma_0 - q_0 - 1.0)
        Lambda = 3 * (sigma_0 - q_0)

        instance = FriedmannEquationIntegrator(
            Friedmann_Equation, rotate_coordinates, sigma_0, q_0, K, Lambda)
        (self.x_new,
         self.y_new,
         self.z_new) = instance.calculate_rotated_coordinates()
        sg.popup_ok('計算が実行されました。')

    def handle_plot_event(self, values):
        """
        グラフ表示ボタンがクリックされたときの処理
        """
        if (self.x_new is not None and
                self.y_new is not None and
                self.z_new is not None):
            elev = float(values["-ELEV-"])
            azim = float(values["-AZIM-"])
            fig_3d = draw_plot(elev, azim, self.x_new, self.y_new, self.z_new)
            draw_figure_w_toolbar(
                self.window['-CANVAS-'].TKCanvas,
                fig_3d,
                self.window['-CONTROLS-'].TKCanvas)
        else:
            sg.popup_error('実行ボタンを先にクリックしてください。')


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

        if event == sg.WINDOW_CLOSED or event == "中止":
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
