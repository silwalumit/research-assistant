from logging import getLogger
from typing import Self

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_huggingface import HuggingFaceEmbeddings
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from src.config.settings import Settings

logger = getLogger(__name__)


class ResearchAgent:
    def __init__(self: Self, settings: Settings):
        logger.info("Initialize embedder")

        embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        self.vector_store = Chroma(
            collection_name=settings.vector_store.collection_name,
            persist_directory=str(settings.vector_store.location),
            embedding_function=embedder,
        )

        print(self.vector_store._collection.count())
        logger.info("Initialize llm")
        # self.llm = ChatOllama(
        #     model=settings.llm.ollama.model_name,
        #     num_gpu=1,
        #     temperature=0.1,
        #     base_url=str(settings.llm.ollama.base_uri),
        # )

        self.llm = init_chat_model(
            settings.llm.ollama.model_name,
            model_provider="ollama",
        )
        logger.info("Building graph")
        self.graph = self._build_graph()

    def _build_graph(self: Self):
        @tool(response_format="content_and_artifact")
        async def retrieve(query: str) -> tuple[str, list[Document]]:
            """Retrieve information related to a query."""

            retriever = self.vector_store.as_retriever(
                search_type="similarity", search_kwargs={"k": 4}
            )
            retrieved_docs = await retriever.ainvoke(query)
            logger.info(
                f"Retrieved docs: {[doc.metadata['source'] for doc in retrieved_docs]}"
            )

            content = "\n\n".join(
                (f"Source: {doc.metadata}\nContent: {doc.page_content}")
                for doc in retrieved_docs
            )
            return content, retrieved_docs

        async def agent(state: MessagesState) -> dict[str, list[BaseMessage]]:
            """
            Invokes the agent model to generate a response based on the current state. Given
            the question, it will decide to retrieve using the retriever tool, or simply end.
            """

            llm_with_tools = self.llm.bind_tools([retrieve])
            response = await llm_with_tools.ainvoke(state["messages"])

            logger.info(f"Response from retriever tool: {response.text()[:10]}")
            return {"messages": [response]}

        async def generate(state: MessagesState) -> dict[str, list[BaseMessage]]:
            recent_retrieved_docs = []

            for message in reversed(state["messages"]):
                if message.type == "tool":
                    recent_retrieved_docs.append(message)
                else:
                    print(message)
                    break

            last_retrieved_docs = recent_retrieved_docs[::-1]
            logger.info(f"Last doc retrieved: {last_retrieved_docs[:50]}")

            docs_content = "\n\n".join(doc.content for doc in last_retrieved_docs)

            system_message = (
                "You are an assistant for question-answering tasks. "
                "Use the following pieces of retrieved context to answer "
                "the question. If you don't know the answer, say that you "
                "don't know. Always be factual and keep the answer concise"
                "\n\n"
                f"{docs_content}"
            )
            message_history = [
                message
                for message in state["messages"]
                if message.type in ("human", "system")
                or (message.type == "ai" and not message.tool_calls)
            ]

            prompt = [SystemMessage(system_message)] + message_history

            answer = await self.llm.ainvoke(prompt)

            return {"messages": [answer]}

        tools = ToolNode([retrieve])

        memory = MemorySaver()

        workflow = StateGraph(MessagesState)
        workflow.add_node("agent", agent)
        workflow.add_node(tools)
        workflow.add_node("generate", generate)

        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent",
            tools_condition,
            {END: END, "tools": "tools"},
        )
        workflow.add_edge("tools", "generate")
        workflow.add_edge("generate", END)

        return workflow.compile(memory)
