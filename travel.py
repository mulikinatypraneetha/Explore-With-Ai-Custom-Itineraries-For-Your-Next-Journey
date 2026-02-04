import streamlit as st 
from google import genai

import os

#api key is not hold public to protect from misuse
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def generate_itinerary(destination, days, nights):
    #Create model configuration
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 50,
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain"
    }

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
            Create a detailed travel itinerary for {destination}
            for {days} days and {nights} nights.
            Include daily activities, nearby attractions,
        food recommendations, and travel tips.
        """
    )

    return response.text


#Streamlit app
st.title("Travel Itinerary Generator")

#Get user inputs
destination = st.text_input("Enter your desired destination:")
days = st.number_input("Enter the number of days:", min_value = 1)
nights = st.number_input("Enter the number of nights:", min_value = 0)

#Ensure that user inputs are provided
if st.button("Generate Itinerary:"):
    if destination.strip() and days > 0 and nights >= 0:
        try:
            itinerary = generate_itinerary(destination, days, nights)
            st.text_area("Generated Itinerary:", value = itinerary, height = 300)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please make sure all inputs are provided and valid.")


