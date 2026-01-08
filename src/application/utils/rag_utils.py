import json
from collections import defaultdict

from requests import post
from application.dataclasses.rag.question_metadata_dc import QuestionMetadataDc
from application.dataclasses.rag.rag_os_filter import *
from application.dataclasses.services.offer_cars_relation_dc import OfferCarRelationsListDC
from application.dataclasses.services.user_point import UserPoint
from application.enums.services.metadata import FuncMetadata
from application.enums.services.rag_source import RagSource
from application.indexes.rag_index import RagIndex
from application.schemas.service_schemas.response_schema import RagResponseItemSchema, RagResponseSchema
from application.utils.globals import extract_question_data_prompt


class RagUtils:
    @classmethod
    async def rag_query(cls, question: str):
        result = RagResponseSchema(data=[])

        question_metadata = cls.question_understanding(question)
        question_metadata = QuestionMetadataDc.from_dict(question_metadata)

        generated_query = cls.generate_os_query(question, question_metadata)

        res = await RagIndex.retrieve_by_query(query=generated_query)

        for doc in res:
            score = doc["_score"]
            if score and score < 0.70:
                continue

            result.data.append(
                RagResponseItemSchema(service_id=doc["_id"], content=doc["_source"]["content"], score=score or 100)
            )

        if not result.data:
            result.data.append(RagResponseItemSchema(service_id=None, content="No relevant service found.", score=0.0))

        return result.model_dump()

    @classmethod
    def generate_os_query(
        cls, question: str, question_metadata: QuestionMetadataDc, user_point: UserPoint = None
    ) -> dict:
        query_vector = cls.embedding(question)

        query_body = RagOsFilterRequestBody()
        query_body.query.bool.must.append(
            RagMustOsFilter(
                knn=RagKNNFilter(
                    embedding=RagEmbeddingFilter(
                        vector=query_vector,
                        k=30,
                    )
                )
            )
        )

        if (question_metadata.max_distance or question_metadata.func == FuncMetadata.MAX_DISTANCE) and user_point:
            query_body.query.bool.filter.geo_distance = RagGeoDistanceAttrsFilter(
                distance=f"{question_metadata.max_distance}km",
                point={"lat": user_point.latitude, "lon": user_point.longitude},
            )

        if question_metadata.country:
            query_body.query.bool.filter.append(RagBoolOsAttrsFilter(term={"country": question_metadata.country.name}))

        if question_metadata.city:
            query_body.query.bool.filter.append(RagBoolOsAttrsFilter(term={"city": question_metadata.city}))

        if question_metadata.offer_type:
            query_body.query.bool.nested = RagNestedTermFilter(
                term={"offers.offer_type": question_metadata.offer_type.name}
            )

        if question_metadata.max_price:
            query_body.query.bool.nested = RagNestedTermFilter(
                term={"offers.base_price": {"lte": question_metadata.max_price}}
            )

        if question_metadata.func == FuncMetadata.CHEAPEST:
            query_body.sort.append(
                {
                    "offers.base_price": {
                        "order": "asc",
                        "mode": "min",
                        "nested": {
                            "path": "offers",
                            "filter": {"term": {"offers.offer_type": question_metadata.offer_type.name}},
                        },
                    }
                }
            )

        if question_metadata.func == FuncMetadata.MAX_DISTANCE and user_point:
            query_body.sort.append(
                {
                    "_geo_distance": {
                        "point": {"lat": user_point.latitude, "lon": user_point.longitude},
                        "order": "asc",
                        "unit": "km",
                        "mode": "min",
                        "distance_type": "arc",
                    }
                }
            )

        return cls.dict_cleaner(query_body.to_dict())

    @classmethod
    def embedding(cls, text: str):
        normalized_text = "".join(text.strip().strip())
        response = post(
            url="http://localhost:11434/api/embeddings", json={"model": "nomic-embed-text", "prompt": normalized_text}
        )
        return response.json()["embedding"]

    @classmethod
    def question_understanding(cls, question: str):
        request = post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3:8b",
                "prompt": f"{extract_question_data_prompt}\nQuestion: {question}",
                "stream": False,
            },
        )

        if request.status_code != 200:
            return None

        res = request.json()["response"]
        return json.loads(res)

    @classmethod
    async def update_or_create_rag_idx(cls, offer_service_relation: OfferCarRelationsListDC):
        service = offer_service_relation.service_model
        relations = offer_service_relation.offer_car_relations
        content = f"""Service Name: {service.name}\n\nDescription: {service.description}\n\nAddress: {service.original_full_address}\n"""

        if relations:
            content += f"Offers:\n"

        for idx, relation in enumerate(relations):
            offer_content = f"- Offer {idx+1}/{len(relations)}:\n Offer type: {relation.offer.offer_type.name}\n Description: {relation.offer.description}\n, Price: {relation.offer.base_price} {relation.offer.currency.name}\n"
            compatible_dict = defaultdict(list)

            for car_relation in relation.car_compatibility_models:
                compatible_dict[car_relation.car_type.name].append(car_relation.car_brand.name)

            compatible_content = "\n".join(
                f"""Car type: {key}, Car Brands: {",".join(brands)}""" for key, brands in compatible_dict.items()
            )
            offer_content += f"Compatible Cars:\n {compatible_content}\n\n"

            content += offer_content

        await RagIndex.create_or_update_document(
            document_id=service.service_id,
            document_body={
                "content": content,
                "embedding": RagUtils.embedding(content),
                "source": RagSource.POSTGRESQL.value,
                "name": service.name,
                "point": {"lat": service.latitude, "lon": service.longitude},
                "city": service.city,
                "country": service.country.name,
                "offers": [
                    {
                        "base_price": offer.base_price,
                        "sale": offer.sale,
                        "currency": offer.currency.name,
                        "offer_type": offer.offer_type.name,
                        "car_compatibilities": [
                            {
                                "car_type": car_relation.car_type.name,
                                "car_brand": car_relation.car_brand.name,
                            }
                            for car_relation in offer_service_relation.get_car_compatibility_models()
                            if car_relation.offer_id == offer.offer_id
                        ],
                    }
                    for offer in offer_service_relation.get_offers()
                    if offer
                ],
            },
        )

    @classmethod
    def dict_cleaner(cls, obj: dict | list) -> dict | list:
        empty_values = (None, {}, [], "")

        if isinstance(obj, dict):
            return {k: cls.dict_cleaner(v) for k, v in obj.items() if cls.dict_cleaner(v) not in empty_values}
        if isinstance(obj, list):
            return [cls.dict_cleaner(v) for v in obj if cls.dict_cleaner(v) not in empty_values]

        return obj
