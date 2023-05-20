"""イベント処理用モジュール"""
import numpy as np
import PySimpleGUI as sg
from calculate import (
    FriedmannEquationIntegrator,
    friedmann_equation,
    rotate_coordinates,
)
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
            friedmann_equation, rotate_coordinates, sigma_0, q_0, K, Lambda)
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

    def theme_view(self, values):
        """
        GUIデザインテーマのプレビュー表示
        """
        sg.theme(values['-THEME-LIST-'][0])
        sg.popup_get_text('This is {}'.format(values['-THEME-LIST-'][0]))
        
    def theme_choice(self, values):
        sg.theme.Update(values['-THEME-LIST-'][0])