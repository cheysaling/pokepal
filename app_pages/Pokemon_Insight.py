import streamlit as st
from api_key import my_api_key
from ChatClient import ChatClient
from css import css

# Content modifier for Pokémon-specific responses
content_mod = "I am a helpful assistant, only answering questions about Pokémon. I should not answer any other questions that don't explicitly request information about Pokémon. Here is the question:"

def chatbot():
    # Check if chat client is already in session state
    if "client" in st.session_state:
        chat_client = st.session_state.client
    else:
        try:
            chat_client = ChatClient(my_api_key())
        except Exception as e:
            st.write("Chat Features are currently unavailable")
            return
        st.session_state.client = chat_client

    client = chat_client.get_client()
    ai_model = chat_client.get_model()
    
    # Set image paths for user and assistant (PokéPal)
    ai_image = './static/images/pokeball.jpg'  
    user_image = './static/images/user_image.png'  

    # Initialize chat history if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        avatar = ai_image if message["role"] == "assistant" else user_image
        
        # Display each message with the appropriate avatar (user or assistant)
        with st.chat_message(message["role"], avatar=avatar):
            if message["role"] == "user":
                st.markdown(f"**User:** {message['content']}")
            else:
                st.markdown(f"**PokéPal:** {message['content']}")

    # Accept user input via chat input box
    if prompt := st.chat_input("How do you want to catch em all today?"):
        # Add user's message to session history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user's message with their avatar and label it as 'User'
        with st.chat_message("user", avatar=user_image):
            st.markdown(f"**User:** {prompt}")

        try:
            # Display assistant's response with PokéPal's avatar and label it as 'PokéPal'
            with st.chat_message("assistant", avatar=ai_image):
                stream = client.chat.completions.create(
                    model=ai_model,
                    messages=[
                        {"role": m["role"], "content": (content_mod + m["content"])}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                response = ""
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        response += chunk.choices[0].delta.content
                
                # Display PokéPal's response after accumulating it
                st.markdown(f"**PokéPal:** {response}")

            # Add assistant's response to session history
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        except Exception as e:
            st.toast("Whoops, there seems to be an error with the chatbot\n\n" + str(e))

# Set page configuration for Streamlit app
st.set_page_config(page_title="Pokémon Insight")

# Title of the app (Do not remove '#')
st.markdown("# Pokémon Insight")

# Description blurb for the AI assistant (PokéPal)
st.markdown("*Hello! I’m PokéPal, your go-to chatbot for all things Pokémon. I'm here to answer your questions about the Pokémon universe, but please remember that I'm an artificial intelligence and can't replace human interactions. I don’t protect your identity, data, or privacy, and I have no memory from one session to the next. While I strive to provide accurate information, not everything I say is guaranteed to be 100% correct. I’ll do my best to give you the best answers possible and suggest websites for further exploration. Let’s dive into the world of Pokémon together!*")

# Uncomment this section to set a logo in the top left of the page.
# Add image to static/images/ folder and replace paths below.
# st.logo(image="./static/images/pokeball.jpg", size="large", icon_image="./static/images/pokeball.jpg")

# Apply custom CSS if needed (stored in 'css' variable)
#st.markdown(css, unsafe_allow_html=True) ##look at this possible undo for bkg image

# Run chatbot function to start interaction
chatbot()