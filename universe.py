"""メインの実行部分．"""
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
            
        elif event == "プレビュー":
            handlers.theme_view(values)

        elif event == "実行":
            handlers.handle_execute_event(values)

        elif event == "グラフ表示":
            handlers.handle_plot_event(values)

    window.close()


"""プログラムの実行"""
if __name__ == "__main__":
    main()
