import streamlit as st
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Replace with your Yelp API key or any other relevant API
YELP_API_KEY = 'QqpMmw2tuGPpmPbikkghpkgZFvxfdetl3NPhp6THcPA8NcuRRDBmD8sY-QAqxdjD-Fe4KAOwvhkVp7xFmG2jbFiND-amRCkloLeHOn9ncLlHQdNHBKx10xd2AiPPZnYx' 
YELP_API_URL = 'https://api.yelp.com/v3/businesses/search'  # Corrected to use the Yelp API endpoint

# Custom CSS for background image
def set_background_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to fetch restaurant data from Yelp API
def fetch_restaurant_data(term, location, price_range, sort_by='rating', limit=5):
    headers = {
        'Authorization': f'Bearer {YELP_API_KEY}',
    }
    params = {
        'term': term,
        'location': location,
        'price': price_range,
        'sort_by': sort_by,
        'limit': limit
    }
    response = requests.get(YELP_API_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data: {response.status_code}")
        return {}

# Load and preprocess data
@st.cache_data
def load_data():
    # Dummy data example - replace with your actual dataset loading logic
    file_path = 'https://raw.githubusercontent.com/Lovelylove03/Restaurant/main/df_mich.csv'  
    data = pd.read_csv(file_path)
    return data

def main():
    # Set background image
    set_background_image('https://cdn.pixabay.com/photo/2018/06/14/13/35/restaurant-3489374_1280.jpg')  # Corrected image URL
    
    st.title("Gourmet Restaurant Recommendation System")

    # Load data
    data = load_data()

    # Sidebar Inputs
    st.sidebar.header('Your Search')

    # Country Selection
    country = st.sidebar.selectbox("Choose Country", sorted(data['Country'].unique()))

    # Town Selection (Filtered by selected country)
    filtered_towns = data[data['Country'] == country]['Town'].unique()
    town = st.sidebar.selectbox("Choose Town", sorted(filtered_towns))

    # Cuisine and Price Range Inputs
    cuisine_preference = st.sidebar.selectbox("Choose Cuisine Type", data['Cuisine'].unique())
    min_price = st.sidebar.number_input("Minimum Price", min_value=0, value=10)
    max_price = st.sidebar.number_input("Maximum Price", min_value=0, value=100)

    # Award Selection (Unique Awards)
    unique_awards = data['Award'].dropna().unique()
    selected_award = st.sidebar.selectbox("Choose Award", sorted(unique_awards))

    # Fetch Recommendations on Button Click
    if st.sidebar.button("Get Recommendations"):
        st.write(f"Showing restaurants in {town}, {country} with cuisine type '{cuisine_preference}', award '{selected_award}', within price range {min_price} - {max_price}.")

        # Fetching restaurant data
        data = fetch_restaurant_data(term=cuisine_preference, location=town, price_range='1,2,3,4', limit=5)
        if 'businesses' in data:
            businesses = data['businesses']
            
            # Filter results by selected award
            filtered_businesses = [business for business in businesses if selected_award in business.get('categories', [])]

            if filtered_businesses:
                for business in filtered_businesses:
                    st.subheader(business['name'])
                    st.write(f"Rating: {business['rating']}")
                    st.write(f"Address: {', '.join(business['location']['display_address'])}")
                    st.write(f"Phone: {business.get('display_phone', 'N/A')}")
                    if business.get('photos'):
                        st.image(business['photos'][0])
                    st.write(f"Price: {business.get('price', 'N/A')}")
                    st.write(f"URL: {business.get('url', 'N/A')}")
                    st.write("\n")
            else:
                st.write("No results found with the selected award.")
        else:
            st.write("No results found.")
    
if __name__ == '__main__':
    main()
