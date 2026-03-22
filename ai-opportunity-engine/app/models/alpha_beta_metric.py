from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AlphaBetaMetric(Base):
    __tablename__ = "alpha_beta_metrics"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    alpha_score: Mapped[float] = mapped_column(Float)
    beta_score: Mapped[float] = mapped_column(Float)
    oqs: Mapped[float] = mapped_column(Float)
    alpha_half_life_days: Mapped[float] = mapped_column(Float)
