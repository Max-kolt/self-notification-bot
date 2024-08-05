from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", Text, nullable=False)
    email = Column("email", Text, nullable=False)
    telegram_id = Column("telegram_id", Integer, nullable=False)

    notes = relationship("Note", back_populates='user', lazy='selectin')


class Note(Base):
    __tablename__ = "notes"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", ForeignKey(User.id), nullable=False)
    text = Column("text", Text, nullable=False)
    reminder_time = Column("reminder_time", TIMESTAMP, nullable=False)

    user = relationship(User, back_populates='notes', lazy='selectin')
