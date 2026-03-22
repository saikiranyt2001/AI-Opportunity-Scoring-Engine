from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PatentRiskFlag(Base):
    __tablename__ = "patent_risk_flags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    risk_level: Mapped[str] = mapped_column(String(30), index=True)
    rationale: Mapped[str] = mapped_column(String)
    action: Mapped[str] = mapped_column(String(50), default="informational_only")
