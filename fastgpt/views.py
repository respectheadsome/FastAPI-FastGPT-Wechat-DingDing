from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

# 创建FastAPI路由
router = APIRouter()

# 创建数据库连接
DATABASE_URL = "sqlite:///./conversations.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 定义SQLAlchemy模型
Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    month = Column(Integer, index=True)
    day = Column(Integer, index=True)
    message = Column(String)

# 创建数据库表格
Base.metadata.create_all(bind=engine)

# 依赖项：创建数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/send_message")
async def send_message(message: str, db: Session = Depends(get_db)):
    # 获取当前日期
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    
    # 创建并插入新的记录
    new_conversation = Conversation(year=year, month=month, day=day, message=message)
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)
    
    return {"status": "Message saved", "id": new_conversation.id}
def parse_date(date_str: str):
    """
    解析日期字符串，并根据日期格式返回相应的查询过滤器。
    """
    try:
        if len(date_str) == 10:  # YYYY-MM-DD
            year, month, day = map(int, date_str.split('-'))
            return {"year": year, "month": month, "day": day}
        elif len(date_str) == 7:  # YYYY-MM
            year, month = map(int, date_str.split('-'))
            return {"year": year, "month": month}
        elif len(date_str) == 5:  # MM-DD
            month, day = map(int, date_str.split('-'))
            return {"month": month, "day": day}
        elif len(date_str) == 4:  # YYYY
            year = int(date_str)
            return {"year": year}
        elif len(date_str) == 2:  # MM 或 DD
            if int(date_str) > 12:
                return {"day": int(date_str)}
            else:
                return {"month": int(date_str)}
        else:
            raise ValueError("Invalid date format")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Expected formats: YYYY-MM-DD, YYYY-MM, MM-DD, YYYY, MM, DD")

@router.get("/conversations/")
async def get_conversations(date: str, db: Session = Depends(get_db)):
    filters = parse_date(date)
    query = db.query(Conversation)
    
    for attr, value in filters.items():
        query = query.filter(getattr(Conversation, attr) == value)
    
    conversations = query.all()
    
    if not conversations:
        raise HTTPException(status_code=404, detail="No conversations found for the specified date")
    
    return conversations

@router.delete("/conversations/")
async def delete_conversations(date: str, db: Session = Depends(get_db)):
    filters = parse_date(date)
    query = db.query(Conversation)
    
    for attr, value in filters.items():
        query = query.filter(getattr(Conversation, attr) == value)
    
    conversations = query.all()
    
    if not conversations:
        raise HTTPException(status_code=404, detail="No conversations found for the specified date")
    
    for convo in conversations:
        db.delete(convo)
    db.commit()
    
    return {"status": "Deleted", "date": date}
