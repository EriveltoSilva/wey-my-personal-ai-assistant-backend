from dotenv import load_dotenv
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage
from langchain_openai.chat_models import ChatOpenAI

load_dotenv()

model = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0)
print(model.invoke([HumanMessage(content="Tell me 5 famous phrases from Well Known Software Developers.")]))


# 1. "Any fool can write code that a computer can understand. Good programmers write code that humans can understand." - Martin Fowler
# 2. "Talk is cheap. Show me the code." - Linus Torvalds
# 3. "The best way to predict the future is to invent it." - Alan Kay
# 4. "Programming isn't about what you know; it's about what you can figure out." - Chris Pine
# 5. "The most important single aspect of software development is to be clear about what you are trying to build." - Bjarne Stroustrup

# content='
# 1. "Any fool can write code that a computer can understand. Good programmers write code that humans can understand." - Martin Fowler\n\n
# 2. "Talk is cheap. Show me the code." - Linus Torvalds\n\n
# 3. "The best way to predict the future is to invent it." - Alan Kay\n\n
# 4. "Programming isn\'t about what you know; it\'s about what you can figure out." - Chris Pine\n\n
# 5. "The most important single aspect of software development is to be clear about what you are trying to build." - Bjarne Stroustrup'
# additional_kwargs={} response_metadata={'finish_reason': 'stop', 'model_name': 'gpt-3.5-turbo-0125', 'service_tier': 'default'} id='run--13b50ff7-abfa-4a6c-90bb-aad00ae75703-0'
