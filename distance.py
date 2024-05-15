import matplotlib.pyplot as plt
import csv
# 空のリストを作成
data_list = []

# テキストファイルを読み込む
with open('distance2.0.txt', 'r', encoding='utf-8') as file:
    # 各行をループ処理してリストに追加
    for line in file:
        # 行の改行文字を取り除き、浮動小数点数に変換してリストに追加
        data_list.append(float(line.strip()))

# 結果を表示
print(data_list)


# ヒストグラムとPDF
plt.hist(data_list, bins=30, density=True, alpha=0.6, color='g', label='Histogram')
plt.title('gamma:')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.legend()

plt.show()