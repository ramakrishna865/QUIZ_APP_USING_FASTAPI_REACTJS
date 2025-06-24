# # from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
# # from sqlalchemy.orm import relationship
# # from database import Base

# # class Category(Base):
# #     __tablename__ = "categories"
# #     id = Column(Integer, primary_key=True, index=True)
# #     name = Column(String, unique=True, index=True)

# #     questions = relationship("Question", back_populates="category")

# # class Question(Base):
# #     __tablename__ = "questions"
# #     id = Column(Integer, primary_key=True, index=True)
# #     question = Column(String, nullable=False)
# #     answer = Column(String, nullable=False)
# #     type = Column(String(10), nullable=False)  
# #     limit = Column(Integer, nullable=False)  
# #     category_id = Column(Integer, ForeignKey("categories.id"))

# #     __table_args__ = (
# #         CheckConstraint("type IN ('string', 'numeric', 'boolean')", name="check_question_type"),
# #     )

# #     category = relationship("Category", back_populates="questions")


# from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
# from sqlalchemy.orm import relationship
# from database import Base

# class Category(Base):
#     __tablename__ = "categories"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)

#     questions = relationship("Question", back_populates="category")

# class Question(Base):
#     __tablename__ = "questions"
#     id = Column(Integer, primary_key=True, index=True)
#     question = Column(String, nullable=False)
#     answer = Column(String, nullable=False)
#     type = Column(String(10), nullable=False)  
#     limit = Column(Integer, nullable=False)
#     type_mandatory = Column(String(10), nullable=False)  # New column
#     limit_mandatory = Column(String(10), nullable=False)  # New column
#     category_id = Column(Integer, ForeignKey("categories.id"))

#     __table_args__ = (
#         CheckConstraint("type IN ('string', 'numeric', 'boolean')", name="check_question_type"),
#         CheckConstraint("type_mandatory IN ('mandatory', 'optional')", name="check_type_mandatory"),
#         CheckConstraint("limit_mandatory IN ('mandatory', 'optional')", name="check_limit_mandatory"),
#     )

#     category = relationship("Category", back_populates="questions")
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    questions = relationship("Question", back_populates="category")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    type = Column(String(10), nullable=False)  

    min_limit = Column(Integer, nullable=False)
    max_limit = Column(Integer, nullable=False)
    min_limit_mandatory = Column(String(10), nullable=False)
    max_limit_mandatory = Column(String(10), nullable=False)

    type_mandatory = Column(String(10), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))

    __table_args__ = (
        CheckConstraint("type IN ('string', 'numeric', 'boolean')", name="check_question_type"),
        CheckConstraint("type_mandatory IN ('mandatory', 'optional')", name="check_type_mandatory"),
        CheckConstraint("min_limit_mandatory IN ('mandatory', 'optional')", name="check_min_limit_mandatory"),
        CheckConstraint("max_limit_mandatory IN ('mandatory', 'optional')", name="check_max_limit_mandatory"),
    )

    category = relationship("Category", back_populates="questions")
