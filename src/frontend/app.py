import streamlit as st
import requests
import os

# Set page title and header
st.title("Classification de sentiment")
st.header("Classification de sentiment")
# Text area for user input
user_input = st.text_area("Entrez votre texte ici :")

if st.button("Classifier"):
    if user_input:
        # Send request to API
        url = os.getenv("url_api")
        print(url)
        response = requests.post(url, json={"reviews": [user_input]})
        
        if response.status_code == 200:
            result = response.json()
            print(result)
            sentiment = result['sentiments'][0]
            st.success(f"Sentiment du message : {sentiment}")
        else:
            st.error("Erreur lors de la classification du texte.")
    else:
        st.warning("Veuillez entrer du texte avant de classifier.")
# Environment variable for API URL
#export url_api=http://localhost:8000/predict