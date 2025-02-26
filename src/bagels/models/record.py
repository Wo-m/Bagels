from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from .database.db import Base


class Record(Base):
    __tablename__ = "record"

    createdAt = Column(DateTime, nullable=False, default=datetime.now)
    updatedAt = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)
    accountId = Column(Integer, ForeignKey("account.id"), nullable=False)
    categoryId = Column(Integer, ForeignKey("category.id"), nullable=True)

    tags = Column(String, nullable=True)  # unimplemented
    isInProgress = Column(Boolean, nullable=False, default=False)  # unimplemented

    # if record adds money to account
    isIncome = Column(Boolean, nullable=False, default=False)
    # if record is transfer to this account
    isTransfer = Column(
        Boolean,
        CheckConstraint("(isTransfer = FALSE) OR (isIncome = FALSE)"),
        nullable=False,
        default=False,
    )
    transferToAccountId = Column(Integer, ForeignKey("account.id"), nullable=True)

    account = relationship(
        "Account", foreign_keys=[accountId], back_populates="records"
    )
    category = relationship("Category", back_populates="records")
    transferToAccount = relationship(
        "Account",
        foreign_keys=[transferToAccountId],
        back_populates="transferFromRecords",
    )
    splits = relationship(
        "Split", back_populates="record", cascade="all, delete-orphan"
    )
