#!/usr/bin/env python3
"""
LimoneIDE Mobile Backend Server
FastAPI 기반 음성 자동화 백엔드
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
import json
import logging
from datetime import datetime
import sys
import os

# LimoneIDE Core 모듈 import
sys.path.append('../LimoneIDE_Core')
from src.core.ai_engine import AIEngine
from src.voice.intent_analyzer import IntentAnalyzer
from src.automation.workflow_engine import WorkflowEngine
from src.rag.personal_ai import PersonalAI

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="LimoneIDE Mobile API",
    description="음성 자동화 플랫폼 백엔드 API",
    version="1.0.0"
)

# CORS 설정 (모바일 PWA에서 접근 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터 모델
class VoiceCommand(BaseModel):
    command: str
    timestamp: str
    user_agent: Optional[str] = None
    user_id: Optional[str] = None

class CommandResponse(BaseModel):
    title: str
    content: str
    type: str
    url: Optional[str] = None
    steps: Optional[List[str]] = None
    speak: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

# 전역 변수
ai_engine = None
intent_analyzer = None
workflow_engine = None
personal_ai = None

@app.on_event("startup")
async def startup_event():
    """서버 시작 시 초기화"""
    global ai_engine, intent_analyzer, workflow_engine, personal_ai
    
    try:
        logger.info("LimoneIDE Mobile 백엔드 서버 시작 중...")
        
        # AI 엔진 초기화
        ai_engine = AIEngine()
        logger.info("✅ AI 엔진 초기화 완료")
        
        # 의도 분석기 초기화
        intent_analyzer = IntentAnalyzer()
        logger.info("✅ 의도 분석기 초기화 완료")
        
        # 워크플로우 엔진 초기화
        workflow_engine = WorkflowEngine()
        logger.info("✅ 워크플로우 엔진 초기화 완료")
        
        # 개인화 AI 초기화
        personal_ai = PersonalAI()
        logger.info("✅ 개인화 AI 초기화 완료")
        
        logger.info("🚀 LimoneIDE Mobile 백엔드 서버 시작 완료!")
        
    except Exception as e:
        logger.error(f"서버 초기화 실패: {e}")
        raise

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "LimoneIDE Mobile API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "ai_engine": ai_engine is not None,
            "intent_analyzer": intent_analyzer is not None,
            "workflow_engine": workflow_engine is not None,
            "personal_ai": personal_ai is not None
        }
    }

@app.post("/voice-command", response_model=CommandResponse)
async def process_voice_command(command: VoiceCommand):
    """음성 명령 처리"""
    try:
        logger.info(f"음성 명령 수신: {command.command}")
        
        # 1. 의도 분석
        intent = await intent_analyzer.analyze_intent(command.command)
        logger.info(f"의도 분석 결과: {intent}")
        
        # 2. 개인화 AI로 컨텍스트 추가
        context = await personal_ai.get_context(command.command)
        logger.info(f"컨텍스트: {context}")
        
        # 3. AI 엔진으로 응답 생성
        ai_response = await ai_engine.generate_response(
            command.command,
            intent=intent,
            context=context
        )
        
        # 4. 워크플로우 실행 (필요시)
        workflow_result = None
        if intent.get('action') in ['create_website', 'send_email', 'schedule_task']:
            workflow_result = await workflow_engine.execute_workflow(
                intent['action'],
                command.command,
                ai_response
            )
        
        # 5. 응답 구성
        response = await build_response(command.command, intent, ai_response, workflow_result)
        
        # 6. 개인화 AI에 대화 기록 저장
        await personal_ai.save_conversation(command.command, response)
        
        logger.info(f"명령 처리 완료: {response.title}")
        return response
        
    except Exception as e:
        logger.error(f"음성 명령 처리 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def build_response(command: str, intent: dict, ai_response: str, workflow_result: Optional[dict]) -> CommandResponse:
    """응답 구성"""
    
    # 기본 응답
    response = CommandResponse(
        title="명령 처리 완료",
        content=ai_response,
        type=intent.get('category', 'general'),
        speak=ai_response[:100] + "..." if len(ai_response) > 100 else ai_response
    )
    
    # 웹사이트 생성
    if intent.get('action') == 'create_website':
        response.title = "웹사이트 생성 완료"
        response.type = "website"
        if workflow_result and workflow_result.get('url'):
            response.url = workflow_result['url']
            response.content = f"요청하신 웹사이트가 성공적으로 생성되었습니다.\n\nURL: {workflow_result['url']}"
    
    # 이메일 작성
    elif intent.get('action') == 'send_email':
        response.title = "이메일 작성 완료"
        response.type = "email"
        response.content = "이메일이 작성되었습니다. 확인해보세요."
    
    # 일정 관리
    elif intent.get('action') == 'schedule_task':
        response.title = "일정 관리 완료"
        response.type = "schedule"
        response.content = "일정이 성공적으로 관리되었습니다."
    
    # 문서 요약
    elif intent.get('action') == 'summarize_document':
        response.title = "문서 요약 완료"
        response.type = "document"
        response.content = ai_response
    
    # 일반 대화
    else:
        response.title = "AI 응답"
        response.content = ai_response
    
    return response

@app.get("/recent-tasks")
async def get_recent_tasks(user_id: Optional[str] = None):
    """최근 작업 목록 조회"""
    try:
        if personal_ai:
            tasks = await personal_ai.get_recent_tasks(user_id)
            return {"tasks": tasks}
        else:
            return {"tasks": []}
    except Exception as e:
        logger.error(f"최근 작업 조회 오류: {e}")
        return {"tasks": []}

@app.post("/feedback")
async def submit_feedback(feedback: dict):
    """사용자 피드백 제출"""
    try:
        logger.info(f"피드백 수신: {feedback}")
        # 피드백 처리 로직 (향후 구현)
        return {"message": "피드백이 성공적으로 제출되었습니다."}
    except Exception as e:
        logger.error(f"피드백 처리 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user-insights")
async def get_user_insights(user_id: Optional[str] = None):
    """사용자 인사이트 조회"""
    try:
        if personal_ai:
            insights = await personal_ai.get_user_insights(user_id)
            return insights
        else:
            return {"message": "개인화 AI가 초기화되지 않았습니다."}
    except Exception as e:
        logger.error(f"사용자 인사이트 조회 오류: {e}")
        return {"error": str(e)}

# 개발용 데모 엔드포인트
@app.post("/demo/voice-command")
async def demo_voice_command(command: VoiceCommand):
    """데모용 음성 명령 처리 (실제 AI 없이)"""
    await asyncio.sleep(1)  # 처리 시간 시뮬레이션
    
    if "웹사이트" in command.command:
        return CommandResponse(
            title="웹사이트 생성 완료",
            content="요청하신 웹사이트가 성공적으로 생성되었습니다.",
            type="website",
            url="https://sites.google.com/view/demo-site",
            speak="웹사이트가 성공적으로 생성되었습니다."
        )
    elif "이메일" in command.command:
        return CommandResponse(
            title="이메일 작성 완료",
            content="이메일이 작성되었습니다. 확인해보세요.",
            type="email",
            speak="이메일이 작성되었습니다."
        )
    elif "일정" in command.command:
        return CommandResponse(
            title="일정 관리 완료",
            content="일정이 성공적으로 관리되었습니다.",
            type="schedule",
            speak="일정이 관리되었습니다."
        )
    else:
        return CommandResponse(
            title="명령 처리 완료",
            content=f"'{command.command}' 명령이 성공적으로 처리되었습니다.",
            type="general",
            speak="명령이 처리되었습니다."
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 