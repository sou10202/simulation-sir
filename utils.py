import numpy as np

def distance_age(x1, y1, x2, y2):
  return (np.sqrt((x1 - x2)**2 + (y1 - y2)**2))

def power_low(ganma, min_value):
  r = np.random.uniform(0, 1)
  return min_value * (1 - r)**(-1 / (ganma-1))

def generate_dense_position(flag):
    if flag < 0.25:
      mean_dense = [12.5, 12.5]   # 密なエリアの中心
    elif flag < 0.5:
      mean_dense = [37.5, 12.5]
    elif flag < 0.75:
      mean_dense = [12.5, 37.5]
    else:
      mean_dense = [37.5, 37.5]
    std_dev_dense = 3       # 密なエリアの標準偏差
    while True:
        position = np.random.normal(loc=mean_dense, scale=std_dev_dense, size=(2,))
        if all(0 <= position) and all(position < 50):
            return position

# 疎なエリアの位置生成関数
def generate_sparse_position(flag):
    if flag < 0.25:
      mean_sparse = [12.5, 12.5]   # 密なエリアの中心
    elif flag < 0.5:
      mean_sparse = [37.5, 12.5]
    elif flag < 0.75:
      mean_sparse = [12.5, 37.5]
    else:
      mean_sparse = [37.5, 37.5]
    std_dev_sparse = 12     # 疎なエリアの標準偏差
    while True:
      position = np.random.normal(loc=mean_sparse, scale=std_dev_sparse, size=(2,))
      if all(0 <= position) and all(position < 50):
            return position