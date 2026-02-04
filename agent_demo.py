import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ==========================================
# CONFIGURATION SECTION
# ==========================================

class Config:
    """Store all configuration in one place."""
    MODEL_NAME = "gemini-2.5-flash"
    TEMPERATURE = 0.7
    SYSTEM_MESSAGE = "You are a helpful Python tutor who explains concepts clearly."


# ==========================================
# SIMPLE MEMORY CLASS (built by us!)
# ==========================================

class SimpleMemory:
    """A simple conversation memory we built ourselves."""
    
    def __init__(self):
        # Store messages as a list of tuples (role, content)
        self.messages = []
    
    def add_message(self, role, content):
        """Add a message to memory."""
        self.messages.append((role, content))
    
    def get_history(self):
        """Get all messages in chat format."""
        history = []
        for role, content in self.messages:
            if role == "user":
                history.append(("user", content))
            else:
                history.append(("assistant", content))
        return history
    
    def clear(self):
        """Clear all memory."""
        self.messages = []
    
    def show(self):
        """Display what's in memory."""
        print("\n📦 Memory contents:")
        if not self.messages:
            print("  (empty)")
        for i, (role, content) in enumerate(self.messages, 1):
            print(f"  {i}. {role}: {content[:80]}...")
        print()


# ==========================================
# LLM SETUP FUNCTIONS
# ==========================================

def load_api_key():
    """Load and validate the API key from .env file."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("❌ GOOGLE_API_KEY not found in .env file")
    
    return api_key

def create_llm():
    """Create and return the language model."""
    api_key = load_api_key()
    
    llm = ChatGoogleGenerativeAI(
        model=Config.MODEL_NAME,
        temperature=Config.TEMPERATURE,
        google_api_key=api_key
    )
    
    print(f"✓ LLM initialized: {Config.MODEL_NAME}")
    return llm


# ==========================================
# PROMPT FUNCTIONS
# ==========================================

def create_prompt():
    """Create the prompt template with history support."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", Config.SYSTEM_MESSAGE),
        ("placeholder", "{chat_history}"),
        ("user", "{input}")
    ])
    print("✓ Prompt template created")
    return prompt


# ==========================================
# CHAT FUNCTIONS
# ==========================================

def send_message(user_input, prompt, llm, memory):
    """
    Send a message to the AI and get a response.
    
    Args:
        user_input: What the user wants to say
        prompt: The prompt template
        llm: The language model
        memory: Our simple memory object
    
    Returns:
        AI's response as a string
    """
    # Step 1: Get chat history from our memory
    history = memory.get_history()
    
    # Step 2: Create the processing chain
    chain = prompt | llm | StrOutputParser()
    
    # Step 3: Send message with history
    response = chain.invoke({
        "input": user_input,
        "chat_history": history
    })
    
    # Step 4: Save to memory
    memory.add_message("user", user_input)
    memory.add_message("assistant", response)
    
    return response


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():
    """Main function to run the chat application."""
    print("\n" + "="*50)
    print("🤖 PYTHON TUTOR CHATBOT")
    print("="*50 + "\n")
    
    # Initialize everything
    llm = create_llm()
    memory = SimpleMemory()  # Our custom memory!
    prompt = create_prompt()
    
    print("\n✅ Ready to chat!\n")
    print("-"*50 + "\n")
    
    # Example conversation
    messages = [
        "Hi, my name is Shah",
        "What's my name?",
        "Can you help me with Python loops?"
    ]
    
    for user_input in messages:
        print(f"You: {user_input}")
        response = send_message(user_input, prompt, llm, memory)
        print(f"AI: {response}\n")
        print("-"*50)
        
        # Show what's stored in memory after each message
        memory.show()


# Run the program
if __name__ == "__main__":
    main()