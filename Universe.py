# GUI用
import PySimpleGUI as sg
# 設定ファイル読み込み用
import configparser
import numpy as np

from calculate import FriedmannEquationIntegrator, Friedmann_Equation, rotate_coordinates
from GUI_design import Widget
from output import draw_figure_w_toolbar, draw_plot

# メインプログラム
def main():
    Widget.make_dpi_aware()
    # メインウィンドウの作成
    window = Widget.create_main_window()
    
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "中止":
            sg.popup_ok('中止しました。')
            break
        
        elif event == "-FILE-":
            file_path = values["-FILE-"]
            # 設定ファイルを読み込む準備
            config_ini = configparser.ConfigParser()
            config_ini.read(file_path, encoding='utf-8')
            model_name = config_ini.sections()
            window.find_element("-MODEL-").Update(values = model_name)
        
        elif event == "-MODEL-":
            model = str(values["-MODEL-"])
            default_sigma = float(config_ini.get(model, "sigma_0"))
            default_q = float(config_ini.get(model, "q_0"))
            window.find_element("-SIGMA-").Update(default_sigma)
            window.find_element("-Q-").Update(default_q)
            window.find_element("-SIGMA-TEXT-").Update(default_sigma)
            window.find_element("-Q-TEXT-").Update(default_q)
        
        elif event == "-SIGMA-":
            window.find_element("-SIGMA-TEXT-").Update(values["-SIGMA-"])
            
        elif event == "-Q-":
            window.find_element("-Q-TEXT-").Update(values["-Q-"])
            
        elif event == "-SIGMA-TEXT-":
            window.find_element("-SIGMA-").Update(values["-SIGMA-TEXT-"])
        elif event == "-Q-TEXT-":
            window.find_element("-Q-").Update(values["-Q-TEXT-"])
            
        elif event == "実行":
            sigma_0 = float(values["-SIGMA-TEXT-"])
            q_0 = float(values["-Q-TEXT-"])        
            K = np.sign(3*sigma_0-q_0-1.0)
            Lambda = 3*(sigma_0-q_0)
            
            elev = float(values["-ELEV-"])
            azim = float(values["-AZIM-"])
            
            instance = FriedmannEquationIntegrator(Friedmann_Equation,
                                                   rotate_coordinates,
                                                   sigma_0,
                                                   q_0,
                                                   K,
                                                   Lambda)
            x_new, y_new, z_new = instance.calculate_rotated_coordinates()
            sg.popup_ok('計算が実行されました。')  # Shows OK button
            
        elif event=="グラフ表示":
            fig_3d = draw_plot(elev, azim, x_new, y_new, z_new)
            draw_figure_w_toolbar(window['-CANVAS-'].TKCanvas, fig_3d, window['-CONTROLS-'].TKCanvas)

main()
