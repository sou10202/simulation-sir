import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
import numpy as np

# サンプルデータの作成
data = {
    'x': np.random.rand(10) * 10,
    'y': np.random.rand(10) * 10,
    'status': np.random.choice(['A', 'B', 'C'], 10)
}

# データフレームの作成
df = pd.DataFrame(data)

# 色マッピングの設定
color_map = {'A': 'red', 'B': 'green', 'C': 'blue'}

# プロットの初期設定
fig, ax = plt.subplots()
scat = ax.scatter(df['x'], df['y'], c=[color_map[status] for status in df['status']])

# 軸の範囲設定
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_title('Real-time Scatter Plot with Status Colors')

# 更新関数
def update(frame):
    # ランダムにデータを更新（サンプル用）
    df['x'] = np.random.rand(10) * 10
    df['y'] = np.random.rand(10) * 10
    df['status'] = np.random.choice(['A', 'B', 'C'], 10)
    
    # 更新されたデータに基づいて散布図を再描画
    scat.set_offsets(np.c_[df['x'], df['y']])
    scat.set_color([color_map[status] for status in df['status']])
    return scat,

# アニメーションの設定
ani = FuncAnimation(fig, update, frames=range(50), interval=500, blit=True)

# グラフの表示
plt.show()
