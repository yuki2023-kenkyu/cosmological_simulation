"""GUIのデザイン設定．"""
import ctypes
import platform
import PySimpleGUI as sg


class Widget:
    """
    ウィジェット設定用のクラス
    """

    @staticmethod
    def make_dpi_aware():
        """
        DPIに関連する問題を修正するための関数
        """
        if int(platform.release()) >= 8:
            ctypes.windll.shcore.SetProcessDpiAwareness(True)

    @staticmethod
    def create_main_window():
        """
        メインウィンドウのレイアウトを定義する関数
        """
        file_selection_layout = [
            [sg.Text("設定ファイルを選択: ")],
            [sg.Text("モデルを選択: ")]
        ]

        model_selection_layout = [
            [
                sg.InputText("File Path", size=(30, 1),
                             key="-FILE-", enable_events=True),
                sg.FileBrowse(target="-FILE-",
                              file_types=(("設定ファイル", "*.ini"), ))
            ],
            [sg.Combo(values=[""], size=(30, 1), key="-MODEL-",
                      readonly=True, enable_events=True)]
        ]

        parameter_text_layout = [
            [sg.Text("sigma_0:")],
            [sg.Text("q_0:")]
        ]

        parameter_slider_layout = [
            [sg.Slider(range=(0.0, 1.5), default_value=0.0, resolution=0.01,
                       orientation="h", key="-SIGMA-", enable_events=True)],
            [sg.Slider(range=(-2.0, 2.0), default_value=0.0, resolution=0.01,
                       orientation="h", key="-Q-", enable_events=True)]
        ]

        parameter_view_layout = [
            [sg.InputText(default_text="0.00", size=(7, 1), key="-SIGMA-TEXT-",
                          enable_events=True)],
            [sg.InputText(default_text="0.00", size=(7, 1), key="-Q-TEXT-", enable_events=True)]
        ]

        figure_canvas_control = [sg.Canvas(key='-CONTROLS-')]
        figure_canvas = [sg.Canvas(key='-CANVAS-', size=(500, 500))]

        run_buttons_layout = [
            [sg.Submit('実行'), sg.Cancel('中止'), sg.Button('グラフ表示')]
        ]

        frame_read_file = sg.Frame('データの読み込み',
                                   [
                                       [sg.Column(file_selection_layout,
                                                  justification='l'),
                                        sg.Column(model_selection_layout)]
                                   ]
                                   )

        frame_parameter = sg.Frame('パラメーターの設定',
                                   [
                                       [sg.Column(parameter_text_layout,
                                                  justification='l'),
                                        sg.Column(
                                            parameter_slider_layout,
                                            justification='c'),
                                        sg.Column(parameter_view_layout,
                                                  justification='c')]
                                   ]
                                   )

        frame_graph = sg.Frame('グラフの表示設定',
                               [
                                   [sg.Text('仰　角'),
                                    sg.InputText(
                                       0, size=(5, 1), key='-ELEV-'),
                                    sg.Text('度')
                                    ],
                                   [sg.Text('方位角'),
                                    sg.InputText(
                                       0, size=(5, 1), key='-AZIM-'),
                                    sg.Text('度')
                                    ]
                               ]
                               )
        
        frame_theme_choice = sg.Frame('GUIデザインの変更',
                                     [
                                         [sg.Listbox(values=sg.theme_list(),
                                                     size=(10, 3),
                                                     key='-THEME-LIST-',
                                                     enable_events=True)
                                         ],
                                         [sg.Button('プレビュー'), sg.Button('確定')],
                                         
                                     ])

        layout = [
            [frame_read_file],
            [frame_parameter, frame_graph],
            [frame_theme_choice],
            [sg.Column(run_buttons_layout, justification='c')],
            [figure_canvas_control],
            [figure_canvas]
        ]

        return sg.Window("Friedmann Equations",
                         layout,
                         finalize=True,
                         alpha_channel=0.8,
                         size=(1000, 1000)
                         )
