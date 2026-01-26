import asyncio
import traceback

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.handlers.rag_handler import RagHandler
from application.indexes.rag_index import RagIndex

from application.controllers import OPENSEARCH_CONTROLLER_PREFIX
from application.enums.services.indexes import OpensearchIndexes
from application.models.deps import DBModel


class OpensearchController:
    router = APIRouter(prefix=f"/{OPENSEARCH_CONTROLLER_PREFIX}", tags=[OPENSEARCH_CONTROLLER_PREFIX])

    INDEX_MAPPER = {OpensearchIndexes.RAG_INDEX: RagIndex}
    INDEX_FILL_MAPPER = {
        OpensearchIndexes.RAG_INDEX: RagHandler.fill_rag_index,
    }

    @staticmethod
    @router.post(path=f"/create-index")
    async def create_index(index: OpensearchIndexes):
        try:
            index = OpensearchController.INDEX_MAPPER.get(index)
            asyncio.create_task(index.create_index())
            return {"result": True}
        except Exception:
            traceback.print_exc()
            return {"result": False}

    @staticmethod
    @router.delete(path=f"/delete-index")
    async def delete_index(index: OpensearchIndexes):
        try:
            index = OpensearchController.INDEX_MAPPER.get(index)
            asyncio.create_task(index.delete_index())
            return {"result": True}
        except Exception:
            traceback.print_exc()
            return {"result": False}

    @staticmethod
    @router.delete(path=f"/delete-records")
    async def delete_all_documents(index: OpensearchIndexes):
        try:
            _index = OpensearchController.INDEX_MAPPER.get(index)
            client = await _index.get_client()
            client.delete_by_query(index=index.value, body={"query": {"match_all": {}}})
            return {"result": True}
        except Exception:
            traceback.print_exc()
            return {"result": False}

    @staticmethod
    @router.post(path=f"/fill-index")
    async def fill_index(index: OpensearchIndexes, session: AsyncSession = Depends(DBModel.get_session)):
        try:
            await OpensearchController.INDEX_FILL_MAPPER[index](session)
            return {"result": True}
        except Exception:
            traceback.print_exc()
            return {"result": False}
