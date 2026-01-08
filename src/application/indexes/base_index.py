from opensearchpy import OpenSearch, helpers

from application import config


class BaseIndex:
    opensearch_config = config.opensearch

    index = ""
    __mapping__ = {}

    @classmethod
    async def get_client(cls) -> OpenSearch:
        host = cls.opensearch_config.host
        port = cls.opensearch_config.port
        password = cls.opensearch_config.password
        username = cls.opensearch_config.username

        kwargs = {
            "hosts": [{"host": host, "port": port}],
            "http_compress": True,
            "use_ssl": cls.opensearch_config.use_ssl,
            "verify_certs": False,
            "ssl_assert_hostname": False,
            "ssl_show_warn": False,
            "http_auth": (username, password),
        }

        return OpenSearch(**kwargs)

    @classmethod
    async def retrieve_by_id(cls, index_id: str):
        client = await cls.get_client()
        return client.get(index=cls.index, id=index_id)

    @classmethod
    async def retrieve_by_query(cls, query: dict):
        client = await cls.get_client()
        response = client.search(index=cls.index, body=query)
        return response.get("hits", {}).get("hits", [])

    @classmethod
    async def create_index(cls):
        client = await cls.get_client()
        client.indices.create(index=cls.index, body=cls.__mapping__)

    @classmethod
    async def delete_index(cls):
        client = await cls.get_client()
        client.indices.delete(index=cls.index, ignore_unavailable=False)

    @classmethod
    async def bulk_create(cls, actions):
        client = await cls.get_client()
        helpers.bulk(client=client, actions=actions, index=cls.index)

    @classmethod
    async def create_or_update_document(cls, document_id: str, document_body: dict):
        client = await cls.get_client()
        client.index(index=cls.index, id=document_id, body=document_body)
