from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config.settings import Config, load_api_key
from services.conversation_helper import (
    ConversationContext,
    MessageFormatter,
    ConversationEnricher,
    create_multi_turn_prompt_template
)


def create_llm():
    api_key = load_api_key()
    llm = ChatGoogleGenerativeAI(
        model=Config.MODEL_NAME,
        temperature=Config.TEMPERATURE,
        google_api_key=api_key,
        max_output_tokens=150,
    )
    return llm


def create_prompt():
    """Create an enhanced prompt template for multi-turn conversations."""
    enhanced_system_message = create_multi_turn_prompt_template(Config.SYSTEM_MESSAGE)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", enhanced_system_message),
        ("placeholder", "{chat_history}"),
        ("user", "{input}"),
    ])
    return prompt


def send_message(user_input: str, prompt, llm, memory, user_id: str):
    """
    Send a message using multi-turn conversation support with helper messages.
    
    Args:
        user_input: The user's current message
        prompt: The LangChain prompt template
        llm: The language model instance
        memory: The conversation memory service
        user_id: The user's unique identifier
    
    Returns:
        The LLM's response
    """
    chain = prompt | llm | StrOutputParser()
    
    # Get conversation history
    history = memory.get_history(user_id)
    
    # Create conversation context for helper messages
    conversation_context = ConversationContext(user_id)
    
    # Format history with helper messages
    if history:
        # Get enhanced context information
        turn_info = ConversationEnricher.add_turn_counter(history)
        context_info = ConversationEnricher.add_context_awareness(history, user_input)
        
        # Format the chat history
        formatted_history = MessageFormatter.format_chat_history(history)
        
        # Create helper prompt with all context
        helper_prompt = ConversationEnricher.generate_helper_prompt(
            history, user_input, conversation_context
        )
        
        # Combine all helper information
        enhanced_chat_history = f"{turn_info}\n{context_info}\n\n{formatted_history}"
    else:
        enhanced_chat_history = "Starting new conversation"
    
    # Send message with enhanced context
    response = chain.invoke({
        "input": user_input,
        "chat_history": enhanced_chat_history
    })
    
    # Store messages in memory
    memory.add_message(user_id, "user", user_input)
    memory.add_message(user_id, "assistant", response)
    
    return response


def send_message_with_helper_context(user_input: str, prompt, llm, memory, user_id: str):
    """
    Alternative message sending with explicit helper message management.
    Provides more control over helper message generation.
    """
    chain = prompt | llm | StrOutputParser()
    history = memory.get_history(user_id)
    
    conversation_context = ConversationContext(user_id)
    
    # Build the conversation context message
    if history:
        helper_message = MessageFormatter.format_context_message(history, user_input)
        enhanced_input = f"{user_input}\n\n[Context Helper: {helper_message}]"
    else:
        enhanced_input = user_input
    
    response = chain.invoke({
        "input": enhanced_input,
        "chat_history": MessageFormatter.format_chat_history(history)
    })
    
    memory.add_message(user_id, "user", user_input)
    memory.add_message(user_id, "assistant", response)
    
    return response
