import random
from io import BytesIO
from PIL import Image

def predict_age(image_bytes: bytes) -> dict:
    """
    가벼운 나이 예측 모델을 가정한 Mock(임시) 함수입니다.
    실제로 모델을 도입하실 때는 이 부분을 ONNX나 TFLite, OpenCV DNN 등을
    이용하여 이미지를 추론하는 코드로 변경하시면 됩니다.
    """
    try:
        # 이미지 데이터 검증
        img = Image.open(BytesIO(image_bytes))
        img.verify() 
        
        # 임시 예측 로직: 15 ~ 65 사이의 무작위 나이 반환
        estimated_age = random.randint(15, 65)
        
        return {"age": estimated_age}
    except Exception as e:
        raise ValueError(f"이미지 처리 실패: {str(e)}")
