from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class DigestDispatch(Base):
    __tablename__ = "digest_dispatches"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subscriber_email: Mapped[str] = mapped_column(String(255), index=True)
    subject: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(30), default="queued")
    provider_message_id: Mapped[str] = mapped_column(String(255), default="")
