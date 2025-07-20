from pydantic import Field

from src.entrypoints.http.base import ApiRequestModelBase, ApiResponseBase


class AskRequestModel(ApiRequestModelBase):
    question: str
    session_id: str | None = Field(
        default="session",
        description="Session ID for maintaining conversation context",
    )


class Source(ApiResponseBase):
    """Model for document sources."""

    document_id: str = Field(..., description="Unique identifier for the document")
    filename: str = Field(..., description="Name of the source file")
    content_snippet: str = Field(..., description="Relevant snippet from the document")
    relevance_score: float = Field(..., description="Relevance score for this source")


class AskResponse(ApiResponseBase):
    answer: str = Field(..., description="The generated answer to the question")
    # sources: list[Source] = Field(
    #     ..., description="List of sources used to generate the answer"
    # )
