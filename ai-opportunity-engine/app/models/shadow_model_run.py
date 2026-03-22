from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ShadowModelRun(Base):
    __tablename__ = "shadow_model_runs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    models_responded: Mapped[int] = mapped_column(Integer)
    failures: Mapped[int] = mapped_column(Integer)
    average_score: Mapped[float] = mapped_column(Float)
    score_spread: Mapped[float] = mapped_column(Float)
    raw_payload: Mapped[str] = mapped_column(String)
