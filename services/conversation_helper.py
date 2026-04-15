"""
Conversation Helper Service
Manages multi-turn conversations with context awareness and helper messages
"""

from typing import List, Tuple, Optional, Dict, Any, Union
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage


class ConversationContext:
    """Manages conversation context for multi-turn interactions."""

    def __init__(self, user_id: str, max_history: int = 10):
        self.user_id = user_id
        self.max_history = max_history
        self.conversation_summary = ""
        self.current_topic = None

    def extract_key_topics(self, history: List[Tuple[str, str]]) -> List[str]:
        """Extract key topics from conversation history."""
        topics = []
        keywords = ["python", "loop", "function", "class", "variable", "list", 
                   "dictionary", "string", "method", "module", "import"]
        
        for role, content in history:
            content_lower = content.lower()
            for keyword in keywords:
                if keyword in content_lower and keyword not in topics:
                    topics.append(keyword)
        
        return topics[:5]  # Return top 5 topics

    def format_conversation_summary(self, history: List[Tuple[str, str]]) -> str:
        """Create a summary of the conversation so far."""
        if not history:
            return "No previous conversation history."
        
        topics = self.extract_key_topics(history)
        exchange_count = len([h for h in history if h[0] == "user"])
        
        summary = f"Conversation summary: {exchange_count} user questions"
        if topics:
            summary += f", discussing topics: {', '.join(topics)}"
        summary += "."
        
        return summary

    def get_last_n_turns(self, history: List[Tuple[str, str]], n: int = 5) -> List[Tuple[str, str]]:
        """Get the last n conversation turns."""
        # Each turn is typically user + assistant, so multiply by 2
        return history[-(n*2):] if len(history) > n*2 else history


class MessageFormatter:
    """Formats messages for better multi-turn conversation handling."""

    @staticmethod
    def format_chat_history(history: List[Tuple[str, str]]) -> str:
        """Format chat history into a readable string for the prompt."""
        if not history:
            return "No previous conversation history."
        
        formatted = "Previous conversation:\n"
        for i, (role, content) in enumerate(history, 1):
            role_label = "User" if role == "user" else "Assistant"
            formatted += f"{i}. {role_label}: {content}\n"
        
        return formatted

    @staticmethod
    def format_context_message(history: List[Tuple[str, str]], 
                               user_question: str) -> str:
        """Format a helper message that provides context."""
        if not history:
            return f"This is the start of the conversation. User asks: {user_question}"
        
        last_user_msg = next((content for role, content in reversed(history) 
                             if role == "user"), None)
        
        context_msg = f"Previous question: '{last_user_msg}'\n" if last_user_msg else ""
        context_msg += f"Current question: '{user_question}'\n"
        context_msg += "Provide a helpful, clear answer."
        
        return context_msg

    @staticmethod
    def create_langchain_messages(history: List[Tuple[str, str]], 
                                  user_input: str) -> List[BaseMessage]:
        """Convert history to LangChain message objects."""
        messages: List[BaseMessage] = []
        
        for role, content in history:
            if role == "user":
                messages.append(HumanMessage(content=content))
            else:
                messages.append(AIMessage(content=content))
        
        # Add current user input
        messages.append(HumanMessage(content=user_input))
        
        return messages


class ConversationEnricher:
    """Enriches conversations with helpful metadata and formatting."""

    @staticmethod
    def add_turn_counter(history: List[Tuple[str, str]]) -> str:
        """Add turn counter information."""
        user_turns = len([h for h in history if h[0] == "user"])
        return f"This is turn {user_turns} of the conversation."

    @staticmethod
    def add_context_awareness(history: List[Tuple[str, str]], 
                             current_input: str) -> str:
        """Generate context-awareness messages."""
        if not history:
            return "Starting new conversation session."
        
        last_assistant_msg = next((content for role, content in reversed(history) 
                                  if role == "assistant"), None)
        
        if last_assistant_msg:
            return f"Building on previous response about the topic. Current question: {current_input}"
        
        return f"Continuing the conversation. Current question: {current_input}"

    @staticmethod
    def generate_helper_prompt(history: List[Tuple[str, str]], 
                              current_input: str,
                              conversation_context: ConversationContext) -> str:
        """Generate a comprehensive helper prompt."""
        helper_parts = []
        
        # Add conversation state
        if history:
            helper_parts.append(f"Turn #{len([h for h in history if h[0] == 'user']) + 1}")
            
            # Add summary
            summary = conversation_context.format_conversation_summary(history)
            helper_parts.append(summary)
            
            # Add recent context
            helper_parts.append("Recent exchange:")
            last_n_turns = conversation_context.get_last_n_turns(history, n=2)
            helper_parts.append(MessageFormatter.format_chat_history(last_n_turns))
        else:
            helper_parts.append("Starting new conversation")
        
        helper_parts.append(f"Current user input: {current_input}")
        
        return "\n".join(helper_parts)


def create_multi_turn_prompt_template(system_message: str) -> str:
    """
    Create an enhanced system message for multi-turn conversations.
    """
    enhanced_system = f"""{system_message}

IMPORTANT CONVERSATION GUIDELINES:
- You are having a multi-turn conversation with the user
- Remember context from previous messages
- Build on previous explanations if relevant
- If the user asks a follow-up question, connect it to the previous discussion
- Provide concise but thorough answers
- Use examples when helpful
- Clarify any ambiguous questions
"""
    return enhanced_system
