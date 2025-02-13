import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

pg = st.navigation([
  #st.Page("app_pages/Home.py", title="Home", icon=":material/home:"), 
  #st.Page("app_pages/Why_Get_A_Credit_Card.py", title="Why Get a Credit Card", icon=":material/credit_card:"), 
  #st.Page("app_pages/Credit_Card_Terminology.py", title="Credit Card Terminology", icon=":material/credit_card:"), 
  #st.Page("app_pages/Types_of_Credit_Cards.py", title="Types of Credit Cards", icon=":material/credit_card:"), 
  #st.Page("app_pages/Authorized_User.py", title="Authorized User", icon=":material/credit_card:"), 
  #st.Page("app_pages/Using_A_Credit_Card.py", title="Using a Credit Card", icon=":material/credit_card:"), 
  #st.Page("app_pages/Analyzing_A_Credit_Card.py", title="Analyzing a Credit Card", icon=":material/credit_card:"), 
  st.Page("app_pages/Pokemon_Insight.py", title="Pokemon Insight"),
])

if __name__ == "__main__":
    pg.run()