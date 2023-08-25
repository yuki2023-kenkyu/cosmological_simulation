"""フリードマン方程式の数値計算用モジュール．"""
import numpy as np
from scipy.integrate import solve_ivp


def friedmann_equation(time, variables, sigma_0, q_0):
    """
    フリードマン方程式の定義
    Args:
        time: 時間座標X
        variables: 変数Yの初期条件を格納した配列 [Y_0, dY_dX_0]
        sigma_0: 密度パラメーター
        q_0: 減速パラメーター

    Returns:
        np.array: フリードマン方程式の結果を表す配列 [dY_dX, ddY_dXdX]
    """
    normalized_scale_factor_a = variables[0]
    dY_dX = variables[1]
    ddY_dXdX = -sigma_0/normalized_scale_factor_a**2 + (sigma_0 - q_0)*normalized_scale_factor_a
    return np.array([dY_dX, ddY_dXdX])


def rotate_coordinates(theta, coordinate_matrix):
    """
    座標をz軸周りに回転変換する関数
    Args:
        theta: 回転角度（ラジアン）
        coordinate_matrix: 変換する座標を表す行列（3xNのNumPy配列）

    Returns:
        np.array: 回転変換後の座標行列（3xNのNumPy配列）
    """
    # 回転行列の定義（Z軸周り）
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0.0],
                                [np.sin(theta),  np.cos(theta), 0.0],
                                [0.0, 0.0, 1.0]])
    return rotation_matrix @ coordinate_matrix


class FriedmannEquationIntegrator:
    """
    数値積分を実行し，グラフ化のためのx,y,z座標を計算するためのクラス
    """

    def __init__(self,
                 ode_function,
                 coordinate_function,
                 sigma_0,
                 q_0,
                 K,
                 Lambda):
        """
        コンストラクタ：インスタンス化されたときに最初に呼ばれる特別なメソッド，データの初期化を行う
        Args:
            ode_function: 常微分方程式を定義した関数
            coordinate_function: 座標変換を定義した関数
            sigma_0: 密度パラメーター
            q_0: 減速パラメーター
            K：宇宙の空間曲率
            Lambda:宇宙項
        """
        self.ode_function = ode_function
        self.coordinate_function = coordinate_function
        self.sigma_0 = sigma_0
        self.q_0 = q_0
        self.K = K
        self.Lambda = Lambda
        self.initial_variables = np.array([1.0, 1.0])
        self.time_plus = np.array([0.0, 6.0])
        self.time_minus = np.array([0.0, -1.0])
        self.num_points = 50
        self.phi = np.linspace(0, 2*np.pi, self.num_points).reshape(1, self.num_points)

    def integrate(self, time_direction):
        """
        時間方向にフリードマン方程式を積分するメソッド
        Args:
            time_direction: 時間方向を表すタプル (t0, t1)

        Returns:
            sol: 積分結果を含むオブジェクト
        """
        sol = solve_ivp(self.ode_function,
                        time_direction,
                        self.initial_variables,
                        method='RK45',
                        t_eval=None,
                        rtol=1e-8,
                        atol=1e-10,
                        args=(self.sigma_0, self.q_0),
                        dense_output=True)
        return sol

    def concatenate_sol_array(self):
        """
        積分して得られたndarray型の配列を結合し，回転変換前のx,y,z座標を求めるメソッド

        Returns:
            time_array: 過去の計算結果と未来の計算結果を結合した時間座標Xの配列
            coordinate: 過去の計算結果と未来の計算結果を結合し，条件に沿って定義した回転変換前の３次元座標の配列
        """
        sol_plus = self.integrate(self.time_plus)
        sol_minus = self.integrate(self.time_minus)
        time_array = np.concatenate([sol_minus.t[::-1], sol_plus.t])
        scale_array = np.concatenate([sol_minus.y[0][::-1], sol_plus.y[0]])
        coordinate = np.array(
            [scale_array, np.zeros(len(time_array)), time_array]
        ).reshape(3, len(time_array))
        return time_array, coordinate

    def calculate_rotated_coordinates(self):
        """
        回転行列によって変換したx,y,z座標を求めるメソッド
        Returns:
            x_new: 回転変換後のx座標の配列
            y_new: 回転変換後のy座標の配列
            z_new: 回転変換後のz座標の配列
        """
        time_array, coordinate = self.concatenate_sol_array()
        new_coordinate = np.array(
            [
                np.array([
                    self.coordinate_function(self.phi[0, i], coordinate[:, j])
                    for i in range(self.phi.shape[1])
                ]).T
                for j in range(len(time_array))
            ]
        )
        x_new = new_coordinate[:, 0, :]
        y_new = new_coordinate[:, 1, :]
        z_new = new_coordinate[:, 2, :]
        return x_new, y_new, z_new
