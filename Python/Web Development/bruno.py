from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAi

load_dotenv()

llm = ChatOpenAi(model="gpt-5")
responce = llm.invoke("Who are you?")
print(responce)