
# from pydantic import BaseModel, Field
# from typing import List

# class Category(BaseModel):
#     id: int
#     name: str

#     class Config:
#         from_attributes = True

# class QuestionOut(BaseModel):
#     id: int
#     question: str
#     category_id: int
#     type: str
#     limit: int
#     type_mandatory: str  # new
#     limit_mandatory: str  # new

#     class Config:
#         from_attributes = True

# class QuestionCreate(BaseModel):
#     question: str
#     answer: str
#     type: str = Field(..., max_length=10, pattern="^(string|numeric|boolean)$")
#     limit: int
#     type_mandatory: str = Field(..., pattern="^(mandatory|optional)$")  # new
#     limit_mandatory: str = Field(..., pattern="^(mandatory|optional)$")  # new
#     category_id: int

# class Answer(BaseModel):
#     question_id: int
#     answer: str

# class Submission(BaseModel):
#     name: str
#     email: str
#     answers: List[Answer]
from pydantic import BaseModel, Field
from typing import List

class Category(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class QuestionOut(BaseModel):
    id: int
    question: str
    category_id: int
    type: str
    min_limit: int
    max_limit: int
    type_mandatory: str
    min_limit_mandatory: str
    max_limit_mandatory: str
    answer:str

    class Config:
        from_attributes = True

class QuestionCreate(BaseModel):
    question: str
    answer: str
    type: str = Field(..., max_length=10, pattern="^(string|numeric|boolean)$")
    min_limit: int
    max_limit: int
    type_mandatory: str = Field(..., pattern="^(mandatory|optional)$")
    min_limit_mandatory: str = Field(..., pattern="^(mandatory|optional)$")
    max_limit_mandatory: str = Field(..., pattern="^(mandatory|optional)$")
    category_id: int

class Answer(BaseModel):
    question_id: int
    answer: str

class Submission(BaseModel):
    name: str
    email: str
    answers: List[Answer]
