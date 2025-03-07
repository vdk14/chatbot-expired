import streamlit as st
import wikipedia
import random
import datetime
import json
import os
from datetime import datetime
import uuid

# File to store conversation history
HISTORY_FILE = "conversation_history.json"

def load_conversation_history():
    """Load conversation history from file"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as file:
                return json.load(file)
        except:
            return {"conversations": []}
    return {"conversations": []}

def save_conversation_history(history):
    """Save conversation history to file"""
    with open(HISTORY_FILE, 'w') as file:
        json.dump(history, file, indent=4)

def is_greeting(text):
    """Check if the input text is a greeting"""
    greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 
                 'good evening', 'good day', 'namaste', 'howdy', 'what\'s up', 
                 'how are you', 'how\'s it going', 'hola', 'sup']
    
    text_lower = text.lower()
    return any(greeting in text_lower for greeting in greetings)

def get_greeting_response(text):
    """Generate an appropriate response to a greeting"""
    text_lower = text.lower()
    
    # Time-based greetings
    current_hour = datetime.now().hour
    time_of_day = "morning" if 5 <= current_hour < 12 else "afternoon" if 12 <= current_hour < 17 else "evening"
    
    # Check for specific greetings
    if 'how are you' in text_lower or 'how\'s it going' in text_lower:
        responses = [
            "I'm doing well, thanks for asking! How can I help you today?",
            "I'm fine, thank you! What would you like to know about?",
            "All systems operational! What can I search for you today?"
        ]
    elif 'good morning' in text_lower:
        responses = [
            f"Good morning! It's a great {time_of_day} for learning something new.",
            "Good morning! How can I assist you today?",
            "Morning! What would you like to know about?"
        ]
    elif 'good afternoon' in text_lower:
        responses = [
            f"Good afternoon! How can I help you this {time_of_day}?",
            "Good afternoon! What would you like to explore today?",
            "Afternoon! What are you curious about?"
        ]
    elif 'good evening' in text_lower:
        responses = [
            f"Good evening! Still curious about something this {time_of_day}?",
            "Good evening! What would you like to learn tonight?",
            "Evening! What can I help you discover?"
        ]
    else:
        responses = [
            "Hello there! What would you like to know about today?",
            "Hi! I'm ready to search for information. What topic interests you?",
            "Hey! What can I help you discover?",
            "Greetings! What would you like to learn about?"
        ]
    
    return random.choice(responses)

def main():
    st.set_page_config(page_title="Chatbot", page_icon="📚", layout="wide")
    
    # Initialize history data
    if "history_data" not in st.session_state:
        st.session_state.history_data = load_conversation_history()
    
    # Initialize current conversation ID
    if "current_conversation_id" not in st.session_state:
        # Create a new conversation ID when app starts
        st.session_state.current_conversation_id = str(uuid.uuid4())
        # Add new conversation to history
        new_conversation = {
            "id": st.session_state.current_conversation_id,
            "title": f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "messages": []
        }
        st.session_state.history_data["conversations"].append(new_conversation)
        save_conversation_history(st.session_state.history_data)
    
    # Initialize chat history in session state if it doesn't exist
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        # Try to load previous messages from current conversation
        for conv in st.session_state.history_data["conversations"]:
            if conv["id"] == st.session_state.current_conversation_id:
                st.session_state.chat_history = conv["messages"]
                break
    
    # Create two columns: sidebar and main content
    col1, col2 = st.columns([1, 3])
    
    # Sidebar for conversation history
    with col1:
        st.sidebar.title("Conversation History")
        
        # New conversation button
        if st.sidebar.button("New Conversation"):
            # Create a new conversation ID
            st.session_state.current_conversation_id = str(uuid.uuid4())
            # Add new conversation to history
            new_conversation = {
                "id": st.session_state.current_conversation_id,
                "title": f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "messages": []
            }
            st.session_state.history_data["conversations"].append(new_conversation)
            save_conversation_history(st.session_state.history_data)
            # Clear current chat history
            st.session_state.chat_history = []
            st.rerun()
        
        # Show conversation history
        st.sidebar.markdown("---")
        if st.session_state.history_data["conversations"]:
            for i, conv in enumerate(reversed(st.session_state.history_data["conversations"])):
                # Determine the title to display
                display_title = conv["title"]
                if len(conv["messages"]) > 0:
                    # Use first user message as title if available
                    for msg in conv["messages"]:
                        if msg["role"] == "user":
                            display_title = msg["content"][:30] + "..." if len(msg["content"]) > 30 else msg["content"]
                            break
                
                # Create clickable conversation history
                if st.sidebar.button(f"{display_title}", key=f"hist_{conv['id']}"):
                    st.session_state.current_conversation_id = conv["id"]
                    st.session_state.chat_history = conv["messages"]
                    st.rerun()
                
                # Show date in smaller text
                st.sidebar.caption(conv["date"])
                
                if i < len(st.session_state.history_data["conversations"]) - 1:
                    st.sidebar.markdown("---")
        else:
            st.sidebar.write("No conversation history yet.")
        
        # Clear all history button
        if st.sidebar.button("Clear All History"):
            st.session_state.history_data = {"conversations": []}
            save_conversation_history(st.session_state.history_data)
            # Create a new conversation
            st.session_state.current_conversation_id = str(uuid.uuid4())
            new_conversation = {
                "id": st.session_state.current_conversation_id,
                "title": f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "messages": []
            }
            st.session_state.history_data["conversations"].append(new_conversation)
            save_conversation_history(st.session_state.history_data)
            st.session_state.chat_history = []
            st.rerun()
    
    # Main chat area
    with col2:
        # Page title and description
        st.title("Chatbot")
        st.markdown("Ask me anything, and I'll search Wikipedia for information!")
        
        # Display the chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # User input
        user_query = st.chat_input("Type your question here...")
        
        if user_query:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            
            # Update the conversation in history
            for conv in st.session_state.history_data["conversations"]:
                if conv["id"] == st.session_state.current_conversation_id:
                    conv["messages"] = st.session_state.chat_history
                    save_conversation_history(st.session_state.history_data)
                    break
            
            # Display user message
            with st.chat_message("user"):
                st.write(user_query)
            
            # Display bot thinking indicator
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                
                # Check if it's a greeting or conversation
                if is_greeting(user_query):
                    response = get_greeting_response(user_query)
                    message_placeholder.write(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Check for goodbye messages
                elif any(word in user_query.lower() for word in ['bye', 'goodbye', 'see you', 'exit', 'quit']):
                    farewell_responses = [
                        "Goodbye! Feel free to return whenever you have questions.",
                        "See you later! I'll be here when you need information.",
                        "Take care! Come back anytime you're curious about something."
                    ]
                    response = random.choice(farewell_responses)
                    message_placeholder.write(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Check for thank you messages
                elif any(word in user_query.lower() for word in ['thank', 'thanks', 'appreciate']):
                    thank_responses = [
                        "You're welcome! Is there anything else you'd like to know?",
                        "Glad I could help! What else are you curious about?",
                        "My pleasure! Feel free to ask if you have more questions."
                    ]
                    response = random.choice(thank_responses)
                    message_placeholder.write(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Regular Wikipedia query
                else:
                    message_placeholder.write("Searching...")
                    
                    try:
                        # Get Wikipedia summary
                        result = wikipedia.summary(user_query, sentences=3)
                        
                        # Find related articles
                        related = wikipedia.search(user_query, results=3)
                        related_links = [f"- [{title}](https://en.wikipedia.org/wiki/{title.replace(' ', '_')})" for title in related if title != user_query]
                        
                        # Format the response
                        if related_links:
                            full_response = f"{result}\n\n**Related topics:**\n" + "\n".join(related_links)
                        else:
                            full_response = result
                        
                        # Update the message placeholder with the full response
                        message_placeholder.write(full_response)
                        
                        # Add bot response to chat history
                        st.session_state.chat_history.append({"role": "assistant", "content": full_response})
                        
                    except wikipedia.exceptions.DisambiguationError as e:
                        options = e.options[:5]
                        response = "Your query is ambiguous. Did you mean one of these?\n" + "\n".join([f"- {option}" for option in options])
                        message_placeholder.write(response)
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                        
                    except wikipedia.exceptions.PageError:
                        response = "Sorry, I couldn't find any information on that topic."
                        message_placeholder.write(response)
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                        
                    except Exception as e:
                        response = f"An error occurred: {str(e)}"
                        message_placeholder.write(response)
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Update the conversation in history after bot response
                for conv in st.session_state.history_data["conversations"]:
                    if conv["id"] == st.session_state.current_conversation_id:
                        conv["messages"] = st.session_state.chat_history
                        save_conversation_history(st.session_state.history_data)
                        break

if __name__ == "__main__":
    main()