from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
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

# 정적 파일(HTML, CSS, JS) 서빙을 위한 디렉토리 마운트
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    # 루트 주소 접속 시 index.html 렌더링
    return FileResponse(os.path.join(static_dir, "index.html"))

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
