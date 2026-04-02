# 1. Base Image - 경량화된 slim 버전 사용 (불필요한 시스템 패키지 제외)
FROM python:3.10-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 환경 변수 설정 (Python 동작 최적화)
# PYTHONDONTWRITEBYTECODE: 파이썬이 .pyc 파일을 쓰지 않도록 설정
# PYTHONUNBUFFERED: 파이썬 출력이 버퍼링 없이 즉시 출력되도록 설정 (로그 확인 용이)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


# 5. 종속성 파일 복사 및 패키지 설치
# 소스코드 전체를 먼저 복사하지 않는 이유: Docker Layer 캐시를 최대한 활용하기 위함.
# requirements.txt에 변화가 없을 때, pip install 과정이 캐시되어 재빌드 속도가 매우 빨라집니다.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. 소스 코드 복사
COPY ./src ./src

# 7. 서비스 포트 노출
EXPOSE 8000

# 8. 컨테이너 시작 시 실행될 명령어
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
