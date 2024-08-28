import streamlit as st
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Replace with your Yelp API key or any other relevant API
YELP_API_KEY = 'YOUR_YELP_API_KEY'
YELP_API_URL = 'https://api.yelp.com/v3/businesses/search'  # Correct Yelp API endpoint

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
    
    # Price Range Selection
    price_options = {
        '€€€€': 1079, '€€': 743, '€€€': 449, '¥¥¥': 260, '$$': 210,
        '$$$$': 180, '¥¥¥¥': 163, '$': 129, '££££': 128, '¥¥': 114,
        '££': 107, '$$$': 94, '¥': 92, '€': 89, '₩': 65,
        '£££': 54, '฿฿': 52, '₫': 49, '฿': 37, '₩₩₩₩': 24,
        '฿฿฿฿': 21, '฿฿฿': 14, '₫₫': 11, '₩₩': 9, '₩₩₩': 8,
        '₫₫₫₫': 5, '£': 3, '₺₺₺₺': 1
    }
    selected_price = st.sidebar.selectbox("Choose Price Range", list(price_options.keys()))

    # Award Selection (Unique Awards)
    unique_awards = data['Award'].dropna().unique()
    selected_award = st.sidebar.selectbox("Choose Award", sorted(unique_awards))

    # Fetch Recommendations on Button Click
    if st.sidebar.button("Get Recommendations"):
        st.write(f"Showing restaurants in {town}, {country} with cuisine type '{cuisine_preference}', award '{selected_award}', and price range '{selected_price}'.")

        # Convert selected price to Yelp price parameter format
        price_mapping = {
            '$': '1', '$$': '2', '$$$': '3', '$$$$': '4'
        }
        yelp_price = price_mapping.get(selected_price[0], '1,2,3,4')

        # Fetching restaurant data
        data = fetch_restaurant_data(term=cuisine_preference, location=f"{town}, {country}", price_range=yelp_price, limit=5)
        if 'businesses' in data:
            businesses = data['businesses']
            
            # Filter results by selected award
            filtered_businesses = [business for business in businesses if selected_award in [cat['title'] for cat in business.get('categories', [])]]

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
