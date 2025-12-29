import asyncio

from fastapi import APIRouter

from application.indexes.rag_index import RagIndex

from application.controllers import OPENSEARCH_CONTROLLER_PREFIX
from application.enums.services.indexes import OpensearchIndexes


class OpensearchController:
    router = APIRouter(prefix=f"/{OPENSEARCH_CONTROLLER_PREFIX}", tags=[OPENSEARCH_CONTROLLER_PREFIX])

    INDEX_MAPPER = {OpensearchIndexes.RAG_INDEX: RagIndex}

    @staticmethod
    @router.post(path=f"/create-index")
    async def create_index(index: OpensearchIndexes):
        try:
            index = OpensearchController.INDEX_MAPPER.get(index)
            asyncio.create_task(index.create_index())
            return {"result": True}
        except Exception as ex:
            return {"result": False}

    @staticmethod
    @router.delete(path=f"/delete-index")
    async def delete_index(index: OpensearchIndexes):
        try:
            index = OpensearchController.INDEX_MAPPER.get(index)
            asyncio.create_task(index.delete_index())
            return {"result": True}
        except Exception as ex:
            return {"result": False}

    @staticmethod
    @router.delete(path=f"/delete-records")
    async def delete_all_documents(index: OpensearchIndexes):
        try:
            _index = OpensearchController.INDEX_MAPPER.get(index)
            client = await _index.get_client()
            client.delete_by_query(index=index.value, body={"query": {"match_all": {}}})
            return {"result": True}
        except Exception as ex:
            print(ex)
            return {"result": False}