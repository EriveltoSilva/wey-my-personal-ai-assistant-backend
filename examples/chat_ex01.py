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


# {
#     "action": "next",
#     "messages": [
#         {
#             "id": "54616c99-1eee-4ee2-b0d5-0e573251c7c2",
#             "author": {
#                 "role": "user"
#             },
#             "create_time": 1754516383.997,
#             "content": {
#                 "content_type": "text",
#                 "parts": [
#                     "quero saber tudo o que a saber sobre RAG"
#                 ]
#             },
#             "metadata": {
#                 "selected_github_repos": [],
#                 "selected_all_github_repos": false,
#                 "serialization_metadata": {
#                     "custom_symbol_offsets": []
#                 }
#             }
#         }
#     ],
#     "conversation_id": "6893cb63-e4f0-8013-a656-07f857768f6b",
#     "parent_message_id": "b0644cec-4073-46c9-a83c-17c7e4915c44",
#     "model": "auto",
#     "timezone_offset_min": -60,
#     "timezone": "Africa/Luanda",
#     "history_and_training_disabled": true,
#     "conversation_mode": {
#         "kind": "primary_assistant"
#     },
#     "enable_message_followups": true,
#     "system_hints": [],
#     "supports_buffering": true,
#     "supported_encodings": [
#         "v1"
#     ],
#     "client_contextual_info": {
#         "is_dark_mode": true,
#         "time_since_loaded": 68,
#         "page_height": 801,
#         "page_width": 825,
#         "pixel_ratio": 2,
#         "screen_height": 801,
#         "screen_width": 825
#     },
#     "paragen_cot_summary_display_override": "allow",
#     "force_parallel_switch": "auto"
# }
