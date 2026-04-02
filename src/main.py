from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import sys
import os

# src 폴더를 python path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.predict import predict_attributes

app = FastAPI(
    title="Age & Gender Prediction API", 
    version="1.1.0", 
    description="MLOps 기반 가벼운 얼굴 인식 및 나이/성별 예측 서버"
)

@app.get("/")
def read_root():
    return {"message": "나이 예측 API 서버가 정상적으로 실행되었습니다."}

@app.post("/predict/")
async def predict_attributes_endpoint(file: UploadFile = File(...)):
    # 업로드된 파일 확장자 검사
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="유효한 이미지 파일(.png, .jpg, .jpeg)이 아닙니다.")
    
    try:
        content = await file.read()
        # predict.py 서비스 호출
        result = predict_attributes(content)
        
        return JSONResponse(content={
            "filename": file.filename, 
            "predicted_age": result["age"],
            "predicted_gender": result["gender"]
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"추론 중 에러 발생: {str(e)}")

if __name__ == "__main__":
    # 로컬 테스트용 서버 실행
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
