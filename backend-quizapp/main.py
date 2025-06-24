
# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List, Optional
# from fastapi.middleware.cors import CORSMiddleware

# from database import SessionLocal, engine, Base
# import models, schemas
# from mailer import send_email

# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.get("/categories/", response_model=List[schemas.Category])
# def get_categories(db: Session = Depends(get_db)):
#     return db.query(models.Category).all()

# @app.get("/questions/", response_model=List[schemas.QuestionOut])
# def get_questions(category_id: Optional[int] = None, name: Optional[str] = None, db: Session = Depends(get_db)):
#     if category_id:
#         questions = db.query(models.Question).filter(models.Question.category_id == category_id).all()
#     elif name:
#         category = db.query(models.Category).filter(models.Category.name == name).first()
#         if not category:
#             raise HTTPException(status_code=404, detail="Category not found")
#         questions = db.query(models.Question).filter(models.Question.category_id == category.id).all()
#     else:
#         raise HTTPException(status_code=400, detail="Provide category_id or name")
#     return questions

# # @app.post("/questions/", response_model=schemas.QuestionOut)
# # def add_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    
# #     answer_limit = len(question.answer.strip()) + 2
# #     db_question = models.Question(**question.dict(), limit=answer_limit)
# #     db.add(db_question)
# #     db.commit()
# #     db.refresh(db_question)
# #     return db_question

# @app.post("/questions/", response_model=schemas.QuestionOut)
# def add_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
#     db_question = models.Question(**question.dict())
#     db.add(db_question)
#     db.commit()
#     db.refresh(db_question)
#     return db_question


# @app.post("/submit/")
# def submit_answers(submission: schemas.Submission, db: Session = Depends(get_db)):
#     total = len(submission.answers)
#     correct = 0

#     for ans in submission.answers:
#         question = db.query(models.Question).filter(models.Question.id == ans.question_id).first()
#         if not question:
#             continue

#         expected_type = question.type.lower()
#         user_answer = ans.answer.strip()

#         try:
#             if expected_type == "numeric":
#                 float(user_answer)
#             elif expected_type == "boolean":
#                 if user_answer.lower() not in ["true", "false"]:
#                     raise ValueError()
#             elif expected_type == "string":
#                 pass
#             else:
#                 raise HTTPException(status_code=400, detail=f"Invalid type: {expected_type}")
#         except ValueError:
#             raise HTTPException(status_code=422, detail=f"Invalid answer type for question ID {question.id}. Expected {expected_type}")

#         if len(user_answer) > question.limit:
#             raise HTTPException(status_code=422, detail=f"Answer too long for question ID {question.id}. Max allowed is {question.limit} characters")

#         if question.answer.strip().lower() == user_answer.lower():
#             correct += 1

#     send_email(submission.email, submission.name, correct, total)
#     return {"score": correct, "total": total, "email_sent_to": submission.email}




from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, engine, Base
import models, schemas
from mailer import send_email

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/categories/", response_model=List[schemas.Category])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()

@app.get("/questions/", response_model=List[schemas.QuestionOut])
def get_questions(category_id: Optional[int] = None, name: Optional[str] = None, db: Session = Depends(get_db)):
    if category_id:
        questions = db.query(models.Question).filter(models.Question.category_id == category_id).all()
    elif name:
        category = db.query(models.Category).filter(models.Category.name == name).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        questions = db.query(models.Question).filter(models.Question.category_id == category.id).all()
    else:
        raise HTTPException(status_code=400, detail="Provide category_id or name")
    return questions

@app.post("/questions/", response_model=schemas.QuestionOut)
def add_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    db_question = models.Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@app.post("/submit/")
def submit_answers(submission: schemas.Submission, db: Session = Depends(get_db)):
    total = len(submission.answers)
    correct = 0

    for ans in submission.answers:
        question = db.query(models.Question).filter(models.Question.id == ans.question_id).first()
        if not question:
            continue

        expected_type = question.type.lower()
        user_answer = ans.answer.strip()

        # Type validation
        try:
            if expected_type == "numeric":
                float(user_answer)
            elif expected_type == "boolean":
                if user_answer.lower() not in ["true", "false"]:
                    raise ValueError()
            elif expected_type == "string":
                pass
            else:
                raise HTTPException(status_code=400, detail=f"Invalid type: {expected_type}")
        except ValueError:
            raise HTTPException(status_code=422, detail=f"Invalid answer type for question ID {question.id}. Expected {expected_type}")

        # Limit validation (only if marked mandatory)
        length = len(user_answer)

        if question.min_limit_mandatory == "mandatory" and length < question.min_limit:
            raise HTTPException(status_code=422, detail=f"Answer too short for question ID {question.id}. Minimum is {question.min_limit}")
        if question.max_limit_mandatory == "mandatory" and length > question.max_limit:
            raise HTTPException(status_code=422, detail=f"Answer too long for question ID {question.id}. Maximum is {question.max_limit}")

        # Check correctness (case-insensitive)
        if question.answer.strip().lower() == user_answer.lower():
            correct += 1

    send_email(submission.email, submission.name, correct, total)
    return {"score": correct, "total": total, "email_sent_to": submission.email}
