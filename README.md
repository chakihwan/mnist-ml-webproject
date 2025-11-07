# MNIST 손글씨 숫자 인식 웹 프로젝트

이 프로젝트는 MNIST 손글씨 숫자 데이터셋으로 학습된 CNN(Convolutional Neural Network) 모델을 사용하여, 사용자가 웹 브라우저에서 직접 그린 숫자를 인식하는 웹 애플리케이션입니다.

## 주요 기능

* **모델 학습 (`train.py`)**
    * TensorFlow(Keras)를 사용하여 MNIST 데이터셋으로 CNN 모델을 학습합니다.
    * 학습 중 가장 높은 검증 정확도(val_accuracy)를 달성한 모델의 가중치를 체크포인트(`checkpoints/best.weights.h5`)로 저장합니다.
    * 조기 종료(EarlyStopping)를 적용하여 과적합을 방지하고 최적의 모델을 찾습니다.
    * 학습 완료 후, 학습 및 검증 과정의 손실(Loss)과 정확도(Accuracy)를 시각화한 그래프(`history.png`)를 생성합니다.
    * 최종적으로 가장 성능이 좋았던 모델 가중치를 불러와 서빙용 모델(`model.weights.h5`)로 저장합니다.

* **웹 애플리케이션 (`app.py`)**
    * Flask를 기반으로 하는 경량 웹 서버를 구현합니다.
    * 서버 시작 시 학습된 Keras 모델(`model.weights.h5`)을 미리 로드합니다.
    * 루트 경로(`/`): 사용자가 숫자를 그릴 수 있는 메인 페이지(`index.html`)를 렌더링합니다.
    * 예측 엔드포인트(`/predict`):
        * 사용자가 캔버스에서 그린 이미지 파일을 POST 요청으로 받습니다.
        * `utils.py`의 `preprocess_image` 함수를 사용해 이미지를 모델 입력에 맞게 (28x28 그레이스케일, 색상 반전, 정규화 등) 전처리합니다.
        * 전처리된 이미지로 모델 예측을 수행합니다.
        * `utils.py`의 `postprocess` 함수를 사용해 모델의 출력(확률 벡터)을 후처리하여, 예측된 숫자(digit), 확률(prob), 전체 클래스별 확률 리스트(probs)를 JSON 형식으로 반환합니다.

* **유틸리티 (`utils.py`)**
    * `preprocess_image`: 업로드된 이미지 파일(또는 캔버스 blob)을 받아, PIL을 이용해 그레이스케일 변환, 색상 반전, 28x28 크기로 패딩 및 리사이즈, NumPy 배열 변환 및 정규화를 수행하여 모델 입력 형식(1, 28, 28, 1)에 맞춥니다.
    * `postprocess`: 모델의 예측 결과를 받아 확률 분포로 변환하고, 가장 높은 확률의 숫자와 그 확률값, 그리고 전체 확률 리스트를 추출합니다.

* **프론트엔드 (`index.html`)**
    * HTML5 `<canvas>`를 사용하여 사용자가 마우스나 터치로 직접 숫자를 그릴 수 있는 인터페이스를 제공합니다.
    * '펜 굵기' 조절 및 '지우기' 기능을 지원합니다.
    * '예측하기' 버튼 클릭 시:
        * JavaScript(fetch API)를 사용하여 캔버스에 그려진 내용을 PNG 이미지 Blob으로 변환하고, `FormData`에 담아 `/predict` API로 비동기 요청을 전송합니다.
    * 서버로부터 받은 JSON 응답을 기반으로 결과를 동적으로 시각화합니다:
        * 예측된 숫자와 해당 확률을 텍스트로 표시합니다 (예: "예측: 7 (확률 99.50%)").
        * Top-3 예측 결과를 칩(chip) 형태로 보여줍니다.
        * Chart.js 라이브러리를 사용하여 0부터 9까지 각 숫자에 대한 예측 확률을 막대그래프로 시각화하며, 가장 높은 확률의 막대를 하이라이트합니다.

## 프로젝트 구조

```text
.
├── app.py             # Flask 웹 애플리케이션 (서버 실행)
├── train.py           # 모델 학습 스크립트
├── utils.py           # 이미지 전/후처리 유틸리티 함수
├── model.weights.h5   # (train.py 실행 후 생성) 서빙용 모델 가중치
├── checkpoints/       # (train.py 실행 중 생성) 학습 중 체크포인트
│   └── best.weights.h5
├── history.png        # (train.py 실행 후 생성) 학습 과정 그래프
├── templates/
│   └── index.html     # 메인 웹 페이지 (캔버스, 차트 UI)
└── static/
    └── style.css      # (선택) CSS 스타일 시트

## 실행 방법
모델 학습 (최초 1회):
  pip install tensorflow numpy matplotlib
  python train.py
(이 과정을 통해 model.weights.h5 파일이 생성됩니다.)
