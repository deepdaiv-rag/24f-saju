from fastapi import FastAPI, HTTPException
from typing import List
from saju_rag import init, extract_saju, chat_with_saju
from saju_rag.core.entity.request_entity import SajuRequest, SajuRequestType
from saju_rag.core.entity.saju_info import SajuInfo, SajuExtractionResult
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

app = FastAPI(
    title="RAG API",
    description="Retrieval-Augmented Generation API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    load_dotenv()
    await init()  # 서버 시작 시 초기화 호출

@app.get("/")
async def root():
    return {"message": "RAG API가 실행 중입니다"}

@app.post("/extract_saju")
async def process_rag(conversation_history: List[dict]):
    try:
        # SajuRequest 생성
        input = SajuRequest(
            conversation_history=conversation_history,
            type=SajuRequestType.EXTRACT
        )

        # Saju 추출 실행
        result = await extract_saju(input)

        return {
            "successful": result.successful,
            "follow_up_prompt": result.follow_up_prompt,
            "extraction_result": result.extraction_result.dict() if result.successful else None,
            "saju_info": result.saju_info.dict() if result.saju_info else None,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/answer_with_saju")
async def process_rag(conversation_history: List[dict], saju_info: dict, extraction_result: dict):
    try:
        # SajuRequest 생성
        input = SajuRequest(
            conversation_history=conversation_history,
            saju_info=SajuInfo(**saju_info),
            extraction_result=SajuExtractionResult(**extraction_result),
            type=SajuRequestType.ANSWER
        )

        result = await chat_with_saju(input)

        return {"answer": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_app:app", host="0.0.0.0", port=8000, reload=True)
