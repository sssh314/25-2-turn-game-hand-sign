import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# 1. 데이터 불러오기
X = np.load('X_data.npy')
y = np.load('y_data.npy')

# 2. 학습/테스트 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. 모델 생성 및 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4. 정확도 확인
acc = model.score(X_test, y_test)
print("모델 학습 완료! 정확도:", acc)

# 5. 모델 저장
joblib.dump(model, 'hand_korean_model.pkl')
print("모델이 hand_korean_model.pkl 로 저장되었습니다.")

