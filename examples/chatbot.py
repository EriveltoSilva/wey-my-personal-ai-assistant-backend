from dotenv import load_dotenv
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage
from langchain_openai.chat_models import ChatOpenAI

load_dotenv()

model = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0)
print(model.invoke([HumanMessage(content="Tell me 5 famous phrases from Well Known Software Developers.")]))
