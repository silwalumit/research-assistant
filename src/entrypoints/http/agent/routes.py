from logging import getLogger

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage

from src.entrypoints.dependencies import AnnotatedResearchAssistant
from src.entrypoints.http.agent.models import AskRequestModel, AskResponse

logger = getLogger(__name__)
router = APIRouter(prefix="", tags=["Agent"])


@router.post("/ask")
async def ask_question_resource(
    model: AskRequestModel,
    agent: AnnotatedResearchAssistant,
):
    """
    Ask a question about the ingested documents.

    This endpoint performs retrieval-augmented generation.
    """

    logger.info(
        f"Retrieved question: {model.question[:100]}, session_id={model.session_id}"
    )
    try:
        config = {"configurable": {"thread_id": model.session_id}}
        response = await agent.graph.ainvoke(
            input={"messages": [HumanMessage(model.question)]}, config=config
        )
        logger.debug(f"Got Response from llm: {response}")
        content = response["messages"][-1].text()

        return JSONResponse(
            status_code=200,
            content=AskResponse(answer=content).model_dump(),
        )
    except Exception as err:
        logger.error(
            f"Error processing question, question={model.question[:100]}, err={str(err)}"
        )
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(err)}",
        )
