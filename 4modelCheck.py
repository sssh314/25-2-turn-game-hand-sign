import cv2
import numpy as np
import mediapipe as mp
import joblib
from PIL import ImageFont, ImageDraw, Image

# 한글 폰트 설정 (Windows 기준)
fontpath = "C:/Windows/Fonts/malgun.ttf"
font = ImageFont.truetype(fontpath, 80)

# 모델 불러오기
model = joblib.load('hand_korean_model.pkl')

# Mediapipe 설정
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# 카메라 시작
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    # 예측 결과 초기화
    pred_text = ""

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            data = []
            for lm in hand_landmarks.landmark:
                data.extend([lm.x, lm.y, lm.z])

            # 데이터 크기 점검 (21*3 = 63 이어야 함)
            if len(data) == 63:
                pred = model.predict([data])
                pred_text = pred[0]
            else:
                pred_text = "데이터 오류"

    # PIL로 한글 텍스트 표시
    img_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(img_pil)
    draw.text((30, 100), pred_text, font=font, fill=(0, 255, 0, 0))
    frame = np.array(img_pil)

    cv2.imshow('Korean Sign Recognition', frame)
    if cv2.waitKey(1) == 27:  # ESC 종료
        break

cap.release()
cv2.destroyAllWindows()
