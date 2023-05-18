import PySimpleGUI as sg
import ctypes
import platform

"""
PysimpleGUIを用いてWindowのレイアウトを定義するクラス
"""
class Widget:
    
    """GUIがぼやける現象を防ぐ関数"""
    def make_dpi_aware():
        if int(platform.release()) >= 8:
            ctypes.windll.shcore.SetProcessDpiAwareness(True)
    
    """メインウィンドウのレイアウトを定義する関数"""
    def create_main_window():
        # 設定ファイルの選択ボタン
        file_selection_layout = [
            [sg.Text("設定ファイルを選択: ")],
            [sg.Text("モデルを選択: ")]
        ]

        # モデルのコンボボックス
        model_selection_layout = [
            [sg.InputText("File Path", size=(30, 1), key="-FILE-", enable_events=True), sg.FileBrowse(target="-FILE-", file_types=(("設定ファイル", "*.ini"), ))],
            [sg.Combo(values=[""], size=(30, 1), key="-MODEL-", readonly=True, enable_events=True)]
        ]

        # パラメーターのテキストボックス
        parameter_text_layout = [
            [sg.Text("sigma_0:")],
            [sg.Text(text = "", visible=(False))],
            [sg.Text("q_0:")]
        ]

        # パラメーターのスライダー
        parameter_slider_layout = [
            [sg.Slider(range=(0.0, 1.5), default_value=0.0, resolution=0.01, orientation="h", key="-SIGMA-", enable_events=True)],
            [sg.Slider(range=(-2.0, 2.0), default_value=0.0, resolution=0.01, orientation="h", key="-Q-", enable_events=True)],
        ]

        # パラメーターの表示用テキストボックス
        parameter_view_layout = [
            [sg.InputText(size=(7, 1), key="-SIGMA-TEXT-", enable_events=True)],
            [sg.Text(text = "", visible=(False))],
            [sg.InputText(size=(7, 1), key="-Q-TEXT-", enable_events=True)]
        ]

        # gui上のツールバーを描画するcanvasを定義
        figure_canvas_control = [sg.Canvas(key='-CONTROLS-')]

        # gui上のfigureを描画するcanvasを定義
        figure_canvas = [sg.Canvas(key='-CANVAS-',
                                   # ! サイズを確保しておく。
                                   size=(500, 500))]

        # 実行・中止ボタン
        run_buttons_layout = [
            [sg.Submit('実行'), sg.Cancel('中止'), sg.Button('グラフ表示')]
        ]

        # 各フレームの作成
        frame_read_file = sg.Frame('データの読み込み',
                                   [
                                       [sg.Column(file_selection_layout, justification='l'),
                                        sg.Column(model_selection_layout)]
                                   ]
                                  )

        frame_parameter = sg.Frame('パラメーターの設定',
                           [
                                [sg.Column(parameter_text_layout, justification='l'),
                                sg.Column(parameter_slider_layout, justification='c'),
                                sg.Column(parameter_view_layout, justification='c')]
                           ]
                          )

        frame_graph = sg.Frame('グラフの表示設定',
                               [
                                   [sg.Text('仰　角'), sg.InputText(0, size=(5, 1), key='-ELEV-'), sg.Text('度')],
                                   [sg.Text('方位角'), sg.InputText(0, size=(5, 1), key='-AZIM-'), sg.Text('度')],
                               ]
                              )

        # レイアウトの結合
        layout = [
            [frame_read_file],
            [frame_parameter],
            [frame_graph],
            [sg.Column(run_buttons_layout, justification='c')],
            [figure_canvas_control],
            [figure_canvas]
        ]

        return sg.Window("Friedmann Equations", layout, finalize=True, alpha_channel=0.8, size=(1000, 1000))
    
