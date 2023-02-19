# Tsinghua University
# @Minsi Lu
# 9/26/2022 16:13
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from yellowbrick.cluster.elbow import kelbow_visualizer
from sklearn.cluster import KMeans
from sklearn import metrics


# 1. Load data
def load_data(file_path):
    data = []
    f = open(file_path)
    # 读取第一行
    line = f.readline()
    line = line.split()
    line.insert(0, "gene")
    data.append(line)
    # 读取其他行
    line = f.readline()
    while line:
        line = line.split()
        data.append(line)
        line = f.readline()
    f.close()
    data = pd.DataFrame(data[1:], columns=data[0])
    df = data['gene']
    data =data.T
    data = data.drop(['gene'])
    data.columns = df
    # 缺失数据插值
    data = data.fillna(data.mean())
    return data


# 2. Data preprocessing
def data_preprocessing(data):
    # 提取数据矩阵
    matrix = data.to_numpy().astype(float)
    # 数据标准化
    scaler = StandardScaler()
    matrix_scaler = scaler.fit_transform(matrix)
    # 降维
    tsne = TSNE(n_components=2)
    matrix_tsne = tsne.fit_transform(matrix_scaler)
    # # 作图显示matrix_tsne各点
    # plt.scatter(matrix_tsne[:, 0], matrix_tsne[:, 1])
    # plt.show()
    return matrix_tsne


# 4. Evaluation
# 加载lable数据
def load_label(file_path):
    label = []
    f = open(file_path)
    # 读取第一行
    line = f.readline()
    # 读取其他行
    line = f.readline()
    while line:
        temp = []
        line = line.split()
        temp.append(line[0])
        line = " ".join(line[1:])
        temp.append(line)
        label.append(temp)
        line = f.readline()
    f.close()
    # 第一行和第一列以后转换为DataFrame
    label = pd.DataFrame(label, columns=['cell', 'cell_type'])
    # 将cell列转换为索引
    label = label.set_index('cell')
    return label


if __name__ == "__main__":
    while True:
        # 1. Load data
        dataset=input('please input a dataset name: ')
        data = load_data(f'singleCellData/{dataset}')
        # print(data)

        # 2. Data preprocessing
        matrix_tsne = data_preprocessing(data)

        # 3. Clustering
        oz = kelbow_visualizer(KMeans(random_state=1), matrix_tsne, k=(2, 21))   # 默认metric = 'distortion'
        k = oz.elbow_value_
        model = KMeans(n_clusters=k)
        model.fit(matrix_tsne)
        # 给结果打标签
        cluster_label = model.labels_
        result = pd.DataFrame(cluster_label, index=data.index, columns=['cell_type'])
        # 把结果写入文件
        result.to_csv(f'output/{dataset}_result.csv')
        # 作图显示聚类彩色散点结果
        plt.scatter(matrix_tsne[:, 0], matrix_tsne[:, 1], c=cluster_label, cmap='rainbow')
        # 保存图片
        plt.savefig(f'output/{dataset}_result.png')

        # 4. Evaluation
        label = load_label(f'labels/{dataset}_label')
        # 4.1 NMI
        # print(type(cluster_label[0]))
        # print(type(label['cell_type'][0]))
        # 计算NMI
        nmi = metrics.normalized_mutual_info_score(cluster_label, label['cell_type'])
        # 计算ARI
        ari = metrics.adjusted_rand_score(cluster_label, label['cell_type'])
        # 将NMI和ARI写入文件末尾
        with open(f'output/{dataset}_result.csv', 'a') as f:
            f.write(f'\nNMI: {nmi}\nARI: {ari}')




