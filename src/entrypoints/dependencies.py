from typing import Annotated

from fastapi import Depends, Request

from src.app.agent import ResearchAgent


def get_research_assistant(request: Request):
    return request.app.state.agent


AnnotatedResearchAssistant = Annotated[ResearchAgent, Depends(get_research_assistant)]
