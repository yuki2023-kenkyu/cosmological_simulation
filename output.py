"""グラフ出力用のモジュール."""
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk,
)
import matplotlib.pyplot as plt
import matplotlib.ticker as ptick
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


class Toolbar(NavigationToolbar2Tk):
    """
    グラフツールバーを呼び出すクラス
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    """
    グラフとツールバーを更新しGUI上に描画する関数
    """
    # グラフとツールバーを更新するために一旦クリアする
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    # 一旦ツールバーを消去する
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    # グラフとツールバーをGUIウィンドウ上のキャンバスに描画する
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='left', fill='both', expand=2)


def draw_plot(x, y, z):
    """
    figureを作成する関数
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection=Axes3D.name)

    # 背景色の変更
    ax.w_xaxis.set_pane_color((0., 0., 0., 0.))
    ax.w_yaxis.set_pane_color((0., 0., 0., 0.))
    ax.w_zaxis.set_pane_color((0., 0., 0., 0.))
    ax.set_box_aspect((1, 1, 1))

    # 軸ラベルの設定
    ax.set_xlabel(r'$a_x$')
    ax.set_ylabel(r'$a_y$')
    ax.set_zlabel(r'$cosmic \ time$')
    
    # 目盛りの値の表示を指数表記に変更
    max_number_of_digits = len(str(int(np.max(x))))
    ax.xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    ax.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style="sci", axis="x", scilimits=(max_number_of_digits, 
                                                          max_number_of_digits))
    ax.ticklabel_format(style="sci", axis="y", scilimits=(max_number_of_digits,
                                                          max_number_of_digits))

    # グラフをプロット
    surf = ax.plot_surface(x,
                           y,
                           z,
                           cmap='Blues',
                           alpha=0.4,
                           rcount=101,
                           ccount=101,
                           antialiased=False,
                           shade=True)

    # カラーバーを表示
    fig.colorbar(surf, shrink=0.75)
    return fig
