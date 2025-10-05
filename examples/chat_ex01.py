import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

chat = ChatOpenAI(model="gpt-3.5-turbo")

from langchain.schema import AIMessage, HumanMessage, SystemMessage

messages = [
    SystemMessage(content="Você é um assistente útil que responde perguntas."),
    HumanMessage(content="Olá Bot, como você está hoje?"),
    AIMessage(content="Estou bem, obrigado. Como posso ajudar?"),
    HumanMessage(content="Gostaria de entender o que é machine learning."),
]

res = chat.invoke(messages)
res

print(res.content)

messages.append(res)

print(messages)

prompt = HumanMessage(content="Qual é a diferença entre supervisionado e não supervisionado?")
messages.append(prompt)

res = chat.invoke(messages)
print(res.content)


# add latest response to messages
messages.append(res)

# create a new user prompt
prompt = HumanMessage(content="O que tem de tão especial no Mistral 7B?")
# append to messages
messages.append(prompt)

# send to GPT
res = chat.invoke(messages)

print(res.content)


# add latest response to messages
messages.append(res)

# create a new user prompt
prompt = HumanMessage(content="Você pode me falar sobre o LLMChain no LangChain?")
# append to messages
messages.append(prompt)

# send to GPT
res = chat.invoke(messages)

print(res.content)

# Context injection

llmchain_information = [
    "A LLMChain is the most common type of chain. It consists of a PromptTemplate, a model (either an LLM or a ChatModel), and an optional output parser. This chain takes multiple input variables, uses the PromptTemplate to format them into a prompt. It then passes that to the model. Finally, it uses the OutputParser (if provided) to parse the output of the LLM into a final format.",
    "Chains is an incredibly generic concept which returns to a sequence of modular components (or other chains) combined in a particular way to accomplish a common use case.",
    "LangChain is a framework for developing applications powered by language models. We believe that the most powerful and differentiated applications will not only call out to a language model via an api, but will also: (1) Be data-aware: connect a language model to other sources of data, (2) Be agentic: Allow a language model to interact with its environment. As such, the LangChain framework is designed with the objective in mind to enable those types of applications.",
]

source_knowledge = "\n".join(llmchain_information)

query = "Você pode me falar sobre o LLMChain no LangChain?"

augmented_prompt = f"""Use o contexto abaixo para responder à pergunta.

Contexto:
{source_knowledge}

Pergunta: {query}"""

prompt = HumanMessage(content=augmented_prompt)

messages.append(prompt)

res = chat.invoke(messages)
print(res.content)
