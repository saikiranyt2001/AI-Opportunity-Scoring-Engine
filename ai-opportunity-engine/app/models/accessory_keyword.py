from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AccessoryKeyword(Base):
    __tablename__ = "accessory_keywords"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    keyword: Mapped[str] = mapped_column(String(255), index=True)
    rank: Mapped[int] = mapped_column(Integer)
    source_model: Mapped[str] = mapped_column(String(100), default="claude")
