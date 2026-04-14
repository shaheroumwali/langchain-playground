from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config.settings import Config, load_api_key


def create_llm():
    api_key = load_api_key()
    llm = ChatAnthropic(
        model=Config.MODEL_NAME,
        temperature=Config.TEMPERATURE,
        api_key=api_key,
        max_tokens=Config.MAX_TOKENS,
    )
    return llm


def create_prompt():
    prompt = ChatPromptTemplate.from_messages([
        ("system", Config.SYSTEM_MESSAGE),
        ("placeholder", "{chat_history}"),
        ("user", "{input}"),
    ])
    return prompt


def send_message(user_input: str, prompt, llm, memory, user_id: str):
    """Send a message using the existing prompt, llm, and memory objects."""
    chain = prompt | llm | StrOutputParser()
    history = memory.get_history(user_id)
    response = chain.invoke({"input": user_input, "chat_history": history})
    memory.add_message(user_id, "user", user_input)
    memory.add_message(user_id, "assistant", response)
    return response
