import asyncio
import logging
from typing import AsyncIterable
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import HumanMessage, SystemMessage
from langchain_pinecone import PineconeVectorStore
from pydantic import BaseModel

load_dotenv()

logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    content: str


async def send_message(content: str) -> AsyncIterable[str]:
    # 検索
    index_name = "langchain-book"
    embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
    vectorstore_from_docs = PineconeVectorStore(index_name=index_name, embedding=embeddings)
    docs = vectorstore_from_docs.similarity_search(content)

    # 検索結果の結合
    sys_prompts = "You are a good assistant."
    search_result = "\n".join(doc.page_content for doc in docs)
    prompts = [("system", sys_prompts), ("human", f"以下の内容を「{content}」を基に次の内容をまとめてください。###{search_result}###")]
    logger.info(f"prompts: {prompts}")
    print(prompts)

    callback = AsyncIteratorCallbackHandler()
    model = ChatOpenAI(
        model="gpt-3.5-turbo-16k-0613",
        streaming=True,
        verbose=True,
        callbacks=[callback],
    )

    task = asyncio.create_task(
        model.agenerate(messages=[[HumanMessage(content=f"以下の内容を「{content}」を基に次の内容をまとめてください。###{search_result}###")],
                                  [SystemMessage(content="あなたは、頼れるアシスタントです。")]
                                  ])
        # model.agenerate(messages=[prompts])
    )

    try:
        async for token in callback.aiter():
            # print(token)
            yield token
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        callback.done.set()

    await task


@app.post("/stream_chat/")
async def stream_chat(message: Message):
    generator = send_message(message.content)
    return StreamingResponse(generator, media_type="text/event-stream")