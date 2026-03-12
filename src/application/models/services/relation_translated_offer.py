from sqlalchemy import Integer, ForeignKey, UUID, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.models.base import Base


class RelationTranslatedOfferModel(Base):
    __tablename__ = "relation_translated_offer"

    relation_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    offer_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("offers.offer_id"), nullable=False, index=True)
    offer_type_translation_id: Mapped[int] = mapped_column(Integer, ForeignKey("offer_type_translations.offer_type_translation_id"), nullable=False, index=True)

    offer: Mapped["OfferModel"] = relationship(
        "OfferModel",
        back_populates="relation_translated_offers",
        lazy="selectin"
    )
    offer_type_translation: Mapped["OfferTypeTranslationsModel"] = relationship(
        "OfferTypeTranslationsModel",
        back_populates="relation_translated_offers",
        lazy="selectin"
    )

    __table_args__ = (
        UniqueConstraint("offer_id", "offer_type_translation_id", name="uq_offer_translation"),
    )
