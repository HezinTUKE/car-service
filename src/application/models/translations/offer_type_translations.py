from sqlalchemy import Integer, Enum, Text, UniqueConstraint, String
from sqlalchemy.orm import mapped_column, relationship, Mapped

from application.enums.services.language import LanguageCode
from application.models.base import Base


class OfferTypeTranslationsModel(Base):
    __tablename__ = "offer_type_translations"

    offer_type_translation_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String, index=True)
    language_code: Mapped[LanguageCode] = mapped_column(Enum(LanguageCode, native_enum=False, length=10), index=True)
    name: Mapped[str] = mapped_column(String, index=True, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    relation_translated_offers: Mapped[list["RelationTranslatedOfferModel"]] = relationship(
        "RelationTranslatedOfferModel",
        back_populates="offer_type_translation",
        lazy="selectin"
    )
    __table_args__ =(
        UniqueConstraint("code", "language_code", name="offer_type_translation_codes"),
    )
