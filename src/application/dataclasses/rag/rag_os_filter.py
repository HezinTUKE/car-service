from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, DataClassJsonMixin, Undefined


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RagEmbeddingFilter(DataClassJsonMixin):
    vector: list[float] = field(default_factory=list)
    k: int = 30


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RagKNNFilter(DataClassJsonMixin):
    embedding: RagEmbeddingFilter = field(default_factory=RagEmbeddingFilter)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RagGeoDistanceAttrsFilter(DataClassJsonMixin):
    distance: str = ""
    point: dict = field(default_factory=dict)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RagTermFilter(DataClassJsonMixin):
    country: str
    city: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RagNestedTermFilter(DataClassJsonMixin):
    term: dict[str, any] = field(default_factory=dict)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RagNestedFilter(DataClassJsonMixin):
    query: RagNestedTermFilter = field(default_factory=RagNestedTermFilter)
    path: str = "offers"


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RagBoolOsAttrsFilter(DataClassJsonMixin):
    geo_distance: RagGeoDistanceAttrsFilter = field(default_factory=RagGeoDistanceAttrsFilter)
    term: dict[str, str] = field(default_factory=dict)
    nested: RagNestedTermFilter = field(default_factory=RagNestedTermFilter)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RagMustOsFilter(DataClassJsonMixin):
    knn: RagKNNFilter = field(default_factory=RagKNNFilter)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RagBoolOsFilter(DataClassJsonMixin):
    filter: list[RagBoolOsAttrsFilter] = field(default_factory=list)
    must: list[RagMustOsFilter] = field(default_factory=list)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RagOsFilter(DataClassJsonMixin):
    bool: RagBoolOsFilter = field(default_factory=RagBoolOsFilter)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RagOsFilterRequestBody(DataClassJsonMixin):
    query: RagOsFilter = field(default_factory=RagOsFilter)
    sort: list[dict[str, any]] = field(default_factory=list)
