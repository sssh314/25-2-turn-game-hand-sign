import glob
import numpy as np

X, y = [], []
labels = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ','ㅏ','ㅑ','ㅓ','ㅕ','ㅗ','ㅛ','ㅜ','ㅠ','ㅡ','ㅣ']

for label in labels:
    files = glob.glob(f'dataset/{label}/*.csv')
    for f in files:
        data = np.loadtxt(f, delimiter=',')
        X.append(data)
        y.append(label)

X = np.array(X)
y = np.array(y)

np.save('X_data.npy', X)
np.save('y_data.npy', y)
