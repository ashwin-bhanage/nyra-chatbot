"""
Chat Router - API endpoints for chatbot interactions
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse, ChatHistoryResponse
from app.services.chat_service import chat_service
import uuid

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Main chat endpoint - send message, get AI response

    - **message**: User's message
    - **session_id**: Session ID (create one if new conversation)
    - **user_id**: User ID (optional)
    - **phone_number**: Phone number (optional, for user tracking)

    Returns AI-generated response with intent detection
    """

    try:
        # Process the message through chat service
        response_data = await chat_service.process_message(
            user_message=request.message,
            session_id=request.session_id,
            db=db,
            user_id=request.user_id,
            phone_number=request.phone_number
        )

        return ChatResponse(
            response=response_data['response'],
            intent=response_data['intent'],
            session_id=response_data['session_id'],
            data={
                "user_id": response_data.get('user_id'),
                "menu_items": response_data.get('menu_items')
            }
        )

    except Exception as e:
        print(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat: {str(e)}"
        )


@router.get("/chat/history/{session_id}", response_model=list[ChatHistoryResponse])
async def get_chat_history(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Get chat history for a session

    - **session_id**: Session ID to retrieve history for

    Returns list of all messages in the conversation
    """

    history = chat_service.get_session_history(db, session_id)

    if not history:
        return []

    return [
        ChatHistoryResponse(
            id=log.id,
            user_message=log.user_message,
            bot_response=log.bot_response,
            intent=log.intent,
            timestamp=log.timestamp.isoformat()
        )
        for log in history
    ]


@router.post("/chat/session/new")
async def create_new_session():
    """
    Create a new chat session ID

    Returns a unique session ID for starting a new conversation
    """

    session_id = str(uuid.uuid4())

    return {
        "session_id": session_id,
        "message": "New chat session created"
    }


@router.get("/chat/test")
async def test_gemini():
    """
    Test Gemini API connection

    Simple endpoint to verify Gemini is working
    """

    from app.services.gemini_service import gemini_service

    try:
        response = await gemini_service.generate_response(
            user_message="Hello! Can you introduce yourself?",
            menu_items=None,
            chat_history=None
        )

        if response['success']:
            return {
                "status": "success",
                "message": "Gemini API is working!",
                "test_response": response['response']
            }
        else:
            return {
                "status": "error",
                "message": "Gemini API error",
                "error": response['error']
            }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini test failed: {str(e)}"
        )
