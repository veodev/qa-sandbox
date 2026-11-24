from datetime import date
from uuid import UUID, uuid4

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Work(Base):
    __tablename__ = "works"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    car_id: Mapped[UUID] = mapped_column(ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)

    description: Mapped[str] = mapped_column(String(500), nullable=False)
    mileage: Mapped[int] = mapped_column(nullable=False)
    cost: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    performed_date: Mapped[date] = mapped_column(Date, nullable=False)

    car: Mapped["Car"] = relationship(back_populates="works")
