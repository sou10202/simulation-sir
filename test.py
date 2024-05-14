import numpy as np
import matplotlib.pyplot as plt

def power_law_distribution(alpha, min_value, max_value, size=1):
    """
    パワー・ロー分布に従う乱数を生成する関数
    
    Parameters:
    - alpha: パワー・ロー分布の指数
    - min_value: 最小値（スケール）
    - max_value: 最大値
    - size: 生成する乱数の数
    
    Returns:
    - パワー・ロー分布に従う乱数の配列
    """
    r = np.random.uniform(0, 1, size)
    return (min_value * (1 - r) ** (-1 / (alpha - 1))-1)*200

# パラメータの設定
alpha = 20
min_value = 1
max_value = 100
size = 10000

# パワー・ロー分布に従う乱数を生成
values = power_law_distribution(alpha, min_value, max_value, size)

print(values)

# ヒストグラムをプロットして確認
plt.hist(values, bins=50, density=True)
plt.xlabel('Value')
plt.ylabel('Probability Density')
plt.title('Power Law Distribution')
plt.show()
