from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import IntegrityError
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Load the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine and session factory
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# Dependency function for getting a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define the ChatSession model
class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    session_id = Column(String, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    function = Column(String, nullable=True)
    params = Column(Text, nullable=True)  # Store params as a JSON string

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Function to store chat history in the database
def store_chat_session(session_id: str, prompt: str, function: str, params: dict, db: Session):
    params_json = json.dumps(params) if params else None

    # Check if session exists
    existing_session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()

    if existing_session:
        # ✅ Update existing row instead of inserting a duplicate
        existing_session.prompt = prompt
        existing_session.function = function
        existing_session.params = params_json
    else:
        # Create new session ONLY IF IT DOES NOT EXIST
        session_entry = ChatSession(session_id=session_id, prompt=prompt, function=function, params=params_json)
        db.add(session_entry)

    db.commit()


# Function to retrieve chat history
def retrieve_chat_history(session_id: str, db: Session):
    chat_entries = db.query(ChatSession).filter(ChatSession.session_id == session_id).all()
    return [{"prompt": entry.prompt, "function": entry.function, "params": json.loads(entry.params) if entry.params else None} for entry in chat_entries]

# Function to get or create a session in the database
def get_or_create_session(user_ip: str, db: Session):
    session_id = f"session_{user_ip}"

    # Check if the session already exists
    existing_session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
    
    if existing_session:
        return session_id  # Return existing session_id
    
    # No need to create an empty session entry here
    return session_id

