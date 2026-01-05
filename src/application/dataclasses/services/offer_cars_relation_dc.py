from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, Undefined, DataClassJsonMixin

from application.models import OfferModel, OfferCarCompatibilityModel, ServiceModel


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OfferCarRelationDC(DataClassJsonMixin):
    offer: OfferModel
    car_compatibility_models: list[OfferCarCompatibilityModel] = field(default_factory=list)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OfferCarRelationsListDC(DataClassJsonMixin):
    service_model: ServiceModel
    offer_car_relations: list[OfferCarRelationDC] = field(default_factory=list)

    def get_offers(self):
        return [relation.offer for relation in self.offer_car_relations]

    def get_car_compatibility_models(self):
        compatibility_models = []
        for relation in self.offer_car_relations:
            compatibility_models.extend(relation.car_compatibility_models)
        return compatibility_models
