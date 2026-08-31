from app.database.mongodb import db_mongo
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage

_IN_MEMORY_CHAT_HISTORY = {}

async def save_chat_turn(user_id: str, user_message: str, ai_response: str):
    """User aur AI dono ki conversation ko save karne ke liye (MongoDB with memory fallback)"""
    conversation_turn = {
        "user_id": user_id,
        "user_message": user_message,
        "ai_response": ai_response,
        "timestamp": datetime.utcnow()
    }
    
    # Save in memory cache
    if user_id not in _IN_MEMORY_CHAT_HISTORY:
        _IN_MEMORY_CHAT_HISTORY[user_id] = []
    _IN_MEMORY_CHAT_HISTORY[user_id].append(conversation_turn)
    
    try:
        if db_mongo.db is not None:
            chat_collection = db_mongo.db["chat_histories"]
            await chat_collection.insert_one(conversation_turn)
    except Exception as e:
        print(f"[Memory Notice] Chat turn saved in memory cache ({str(e)})")

async def get_chat_history_for_langchain(user_id: str, limit: int = 10):
    """MongoDB ya memory cache se purani chat nikal kar LangChain format me convert karna"""
    records = []
    try:
        if db_mongo.db is not None:
            chat_collection = db_mongo.db["chat_histories"]
            cursor = chat_collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
            records = await cursor.to_list(length=limit)
            records.reverse()
    except Exception:
        pass
        
    if not records and user_id in _IN_MEMORY_CHAT_HISTORY:
        records = _IN_MEMORY_CHAT_HISTORY[user_id][-limit:]
        
    langchain_history = []
    for record in records:
        langchain_history.append(HumanMessage(content=record["user_message"]))
        langchain_history.append(AIMessage(content=record["ai_response"]))
        
    return langchain_history