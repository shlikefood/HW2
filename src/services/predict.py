import random
from io import BytesIO
from PIL import Image

def predict_attributes(image_bytes: bytes) -> dict:
    """
    가벼운 나이 및 성별 예측 모델을 가정한 Mock(임시) 함수입니다.
    실제 모델 도입 시 이 부분을 수정하시면 됩니다.
    """
    try:
        # 이미지 데이터 검증
        img = Image.open(BytesIO(image_bytes))
        img.verify() 
        
        # 임시 예측 로직
        estimated_age = random.randint(15, 65)
        estimated_gender = random.choice(["Male", "Female"])
        
        return {
            "age": estimated_age,
            "gender": estimated_gender
        }
    except Exception as e:
        raise ValueError(f"이미지 처리 실패: {str(e)}")
