import json
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.models.schemas.pydantic_schemas import ChatRequest, ChatResponse
from app.services.ai.agents import ai_assistant
from app.services.ai.memory import get_chat_history_for_langchain, save_chat_turn
from app.api.v1.dependencies import get_current_user_id

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(
    payload: ChatRequest,
    current_user_id: str = Depends(get_current_user_id)
):
    try:
        history = await get_chat_history_for_langchain(user_id=current_user_id)
        ai_response = ai_assistant.ask(user_input=payload.message, history=history)
        
        clean_response = ""
        if isinstance(ai_response, list) and len(ai_response) > 0:
            if isinstance(ai_response[0], dict) and "text" in ai_response[0]:
                clean_response = ai_response[0]["text"]
            elif hasattr(ai_response[0], 'text'):
                clean_response = ai_response[0].text
            else:
                clean_response = str(ai_response[0])
        elif isinstance(ai_response, dict) and "text" in ai_response:
            clean_response = ai_response["text"]
        else:
            clean_response = str(ai_response)
            
        await save_chat_turn(
            user_id=current_user_id,
            user_message=payload.message,
            ai_response=clean_response
        )
        
        return ChatResponse(response=clean_response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Processing Issue: {str(e)}")

@router.post("/chat/stream")
async def chat_stream_with_assistant(
    payload: ChatRequest,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Real-time Server-Sent Events (SSE) streaming endpoint for instantaneous token delivery.
    """
    async def event_generator():
        accumulated_text = ""
        try:
            history = await get_chat_history_for_langchain(user_id=current_user_id)
            
            async for token in ai_assistant.astream_ask(user_input=payload.message, history=history):
                if token:
                    accumulated_text += token
                    payload_json = json.dumps({"token": token})
                    yield f"data: {payload_json}\n\n"
                    
            # Save final response to MongoDB
            if accumulated_text:
                await save_chat_turn(
                    user_id=current_user_id,
                    user_message=payload.message,
                    ai_response=accumulated_text
                )
                
            yield f"data: {json.dumps({'done': True, 'full_response': accumulated_text})}\n\n"
        except Exception as e:
            error_json = json.dumps({"error": str(e), "done": True})
            yield f"data: {error_json}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )