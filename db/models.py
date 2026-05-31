from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls):  # pylint: disable=no-self-argument
        return cls.__name__.lower() + "s"


class Question(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column()
    theme_id: Mapped[int] = mapped_column(
        ForeignKey("themes.id", name="fk_th_id", ondelete="CASCADE")
    )
    theme: Mapped["Theme"] = relationship(back_populates="questions")
    answers: Mapped[list["Answer"]] = relationship(back_populates="question")


class Theme(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    questions: Mapped[list["Question"]] = relationship(back_populates="theme")


class Answer(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(255))
    is_true: Mapped[bool] = mapped_column(default=False)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", name="fk_q_id", ondelete="CASCADE")
    )
    question: Mapped["Question"] = relationship(back_populates="answers")
