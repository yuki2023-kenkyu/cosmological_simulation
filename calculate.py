import numpy as np
from scipy.integrate import solve_ivp

"""フリードマン方程式の定義（※変更しないでください）"""
def Friedmann_Equation(time, variables, sigma_0, q_0):
    Y = variables[0]
    dY_dX = variables[1]
    dA_dX = -sigma_0/Y**2 + (sigma_0 - q_0)*Y
    return [dY_dX, dA_dX]


"""座標をZ軸周りに回転変換する関数"""
def rotate_coordinates(theta, coordinate_matrix):
    # 回転行列の定義（Z軸周り）
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                                [np.sin(theta),  np.cos(theta), 0],
                                [0.0, 0.0, 1.0]])
    return rotation_matrix @ coordinate_matrix


"""
数値積分を実行し，グラフ化のためのX,Y,Z座標を計算するためのクラス
"""
class FriedmannEquationIntegrator:
    
    # 積分区間・刻みの設定
    t_min = 0.0
    t_max = 6.0
    t_true_min = -1.0
    
    # 初期条件
    x_plus = [t_min, t_max]
    x_minus = [t_min, t_true_min]
    y0 = 1.0
    y_dash_0 = 1.0
    initial_variables = np.array([y0, y_dash_0])
    
    # 円周上の点数に関する設定
    num_points = 50
    phi = np.linspace(0, 2*np.pi, num_points).reshape(1, num_points)
    
    def __init__(self, ode_function, coordinate_function, sigma_0, q_0, K, Lambda):
        self.ode_function = ode_function
        self.coordinate_function = coordinate_function
        self.sigma_0 = sigma_0
        self.q_0 = q_0
        self.K = K
        self.Lambda = Lambda
    
    """時間の正の方向にフリードマン方程式を積分する関数"""
    def integrate_plus(self):
        sol_plus  = solve_ivp(self.ode_function,
                              self.x_plus,
                              self.initial_variables,
                              method = 'Radau',
                              t_eval = None,
                              rtol=1e-8,
                              atol=1e-10,
                              args = (self.sigma_0, self.q_0),
                              dense_output=True)
        return sol_plus
    
    """時間の負の方向にフリードマン方程式を積分する関数"""
    def integrate_minus(self):
        sol_minus = solve_ivp(self.ode_function,
                              self.x_minus,
                              self.initial_variables,
                              method = 'Radau',
                              t_eval = None,
                              rtol=1e-8,
                              atol=1e-10,
                              args = (self.sigma_0, self.q_0),
                              dense_output=True)
        return sol_minus
    
    """積分して得られたndarray型の配列を結合し，回転変換前のx,y,z座標を求める関数"""
    def concatenate_sol_array(self):
        # クラス内の関数を呼び出して実行
        sol_plus = self.integrate_plus()
        sol_minus = self.integrate_minus()
        # 適応刻み幅制御によって求められた時間の配列を１つに結合
        sol_t = np.concatenate([sol_minus.t[::-1], sol_plus.t])
        # 数値積分の結果配列を１つに結合
        sol_y = np.concatenate([sol_minus.y[0][::-1], sol_plus.y[0]])
        # 変換前の座標を定義
        coordinate = np.array([sol_y, np.zeros(len(sol_t)), sol_t]).reshape(3, len(sol_t))
        return sol_t, sol_y, coordinate
    
    """回転行列によって変換したX,Y,Z座標を求める関数"""
    def calculate_rotated_coordinates(self):
        # クラス内の関数を呼び出して実行
        sol_t, sol_y, coordinate = self.concatenate_sol_array()
        # 回転変換後の座標
        new_coordinate = np.array([np.array([self.coordinate_function(self.phi[0, i], coordinate[:, j])
                                             for i in range(self.phi.shape[1])]).T
                                   for j in range(len(sol_t))])
        # 回転後の座標を格納した配列をx,y,z軸ごとに分割
        x_new = new_coordinate[:, 0, :]
        y_new = new_coordinate[:, 1, :]
        z_new = new_coordinate[:, 2, :]
        return x_new, y_new, z_new
