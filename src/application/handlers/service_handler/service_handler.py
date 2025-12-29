import traceback
import uuid

from fastapi import HTTPException, status
from geopy import Location
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from requests import post

from application.enums.services.rag_source import RagSource
from application.indexes.rag_index import RagIndex
from application.models import ServiceModel, OrganizationModel, OfferModel
from application.schemas.service_schemas.request_schema import AddServiceRequestSchema, FilterServiceRequestSchema, \
    AddOffersRequestSchema
from application.schemas.service_schemas.response_schema import ManipulateServiceResponseSchema, RagResponseSchema, \
    RagResponseItemSchema
from application.utils.get_location import get_location


class ServiceHandler:
    @classmethod
    async def add_service(cls, service_schema: AddServiceRequestSchema, user_id: str, session: AsyncSession):
        location: Location = await get_location(
            country=service_schema.country,
            city=service_schema.city,
            street=service_schema.street,
            house_number=service_schema.house_number,
            postal_code=service_schema.postal_code,
        )

        if not location:
            return ManipulateServiceResponseSchema(status=False, msg="Address was not found").model_dump()

        if service_schema.organization_id:
            org_query = select(OrganizationModel).filter(OrganizationModel.organization_id == service_schema.organization_id)
            org_query_res = await session.execute(org_query)
            org_model = org_query_res.scalar_one_or_none()

            if not org_model:
                return ManipulateServiceResponseSchema(status=False, msg="Organization doesn't exist").model_dump()

        try:
            service_model = ServiceModel(
                **service_schema.model_dump(),
                service_id=str(uuid.uuid4()),
                owner=user_id,
                longitude=location.longitude,
                latitude=location.latitude,
                original_full_address=location.address
            )
            session.add(service_model)
            await ServiceHandler.store_to_rag_idx(service_model)
            return ManipulateServiceResponseSchema(status=True, msg="Service added").model_dump()
        except Exception:
            traceback.print_exc()
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "DB exception")

    @classmethod
    async def add_offers(cls, offer_schema: AddOffersRequestSchema, session: AsyncSession):
        service_id = offer_schema.service_id

        service_query = select(ServiceModel).filter(ServiceModel.service_id == service_id)
        service_query_res = await session.execute(service_query)
        service_model = service_query_res.scalar_one_or_none()

        if not service_model:
            return ManipulateServiceResponseSchema(status=False, msg="Service doesn't exist").model_dump()

        try:
            offers = []
            for offer_schema in offer_schema.offers:
                offer_model = OfferModel(**offer_schema.model_dump(), service_id=str(service_id))
                session.add(offer_model)
                offers.append(offer_model)

            await cls.update_rag_idx(service_model, offers)
            return ManipulateServiceResponseSchema(status=True, msg="Offer added").model_dump()
        except Exception:
            traceback.print_exc()
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "DB exception")

    @classmethod
    async def update_rag_idx(cls, service: ServiceModel, offers: [OfferModel]):
        rag_document = await RagIndex.retrieve_by_id(service.service_id)

        if not rag_document:
            content = await cls.store_to_rag_idx(service)
        else:
            content = rag_document["_source"]["content"]

        offers = "\n".join([
            f"- Offer {idx+1}/{len(offers)} Car type: {offer.car_type} Description: {offer.description}\n, Price: {offer.base_price} {offer.currency}\n"
            for idx, offer in enumerate(offers)
        ])

        content = f"""{content}\n Offers:\n{offers}"""

        await RagIndex.create_document(
            document_id=service.service_id,
            document_body={
                "content": content,
                "embedding": cls.embedding(content),
                "source": RagSource.POSTGRESQL.value,
            },
        )

    @classmethod
    async def store_to_rag_idx(cls, service: ServiceModel):
        content = f"""Service Name: {service.name}\n\nDescription: {service.description}\n\nAddress: {service.original_full_address}\n"""

        await RagIndex.create_document(
            document_id=service.service_id,
            document_body={
                "content": content,
                "embedding": cls.embedding(content),
                "source": RagSource.POSTGRESQL.value
            }
        )

        return content

    @classmethod
    async def rag_query(cls, question: str):
        result = RagResponseSchema(data=[])

        query_vector = cls.embedding(question)
        res = await RagIndex.retrieve_by_query(query={"knn": {"embedding": {"vector": query_vector, "k": 5}}}, size=5)

        for doc in res:
            score = doc["_score"]
            if score < 0.75:
                continue

            result.data.append(RagResponseItemSchema(
                service_id=doc["_id"],
                content=doc["_source"]["content"],
                score=score
            ))

        if not result.data:
            result.data.append(RagResponseItemSchema(
                service_id=None,
                content="No relevant service found.",
                score=0.0
            ))

        return result.model_dump()

    @classmethod
    def embedding(cls, text: str):
        response = post(
            url="http://localhost:11434/api/embeddings",
            json={
                "model": "nomic-embed-text",
                "prompt": text
            }
        )
        return response.json()["embedding"]
