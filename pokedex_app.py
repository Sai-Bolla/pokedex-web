import streamlit as st
import json
import pandas as pd
from PIL import Image
from io import BytesIO
import requests

# Page configuration
st.set_page_config(page_title="Pokédex", layout="wide", initial_sidebar_state="expanded")

# Title
st.title("📖 Pokédex")

# Fetch Pokemon data from PokéAPI
@st.cache_data
def fetch_pokemon(pokemon_name):
    """Fetch Pokémon data from PokéAPI"""
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching Pokémon: {e}")
        return None

# Fetch Pokemon species data for color
@st.cache_data
def fetch_pokemon_species(pokemon_id):
    """Fetch Pokémon species data for color information"""
    try:
        url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# Type to color mapping (fallback)
TYPE_COLORS = {
    "normal": "#A8A878",
    "fire": "#F08030",
    "water": "#6890F0",
    "grass": "#78C850",
    "electric": "#F8D030",
    "ice": "#98D8D8",
    "fighting": "#C03028",
    "poison": "#A040A0",
    "ground": "#E0C068",
    "flying": "#A890F0",
    "psychic": "#F85888",
    "bug": "#A8B820",
    "rock": "#B8A038",
    "ghost": "#705898",
    "dragon": "#7038F8",
    "dark": "#705848",
    "steel": "#B8B8D0",
    "fairy": "#EE99AC"
}

# Apply background color based on Pokemon
def apply_pokemon_colors(pokemon_data):
    """Apply background color based on Pokemon's color"""
    species_data = fetch_pokemon_species(pokemon_data['id'])
    
    # Try to get color from species data
    bg_color = None
    if species_data and 'color' in species_data:
        color_name = species_data['color']['name']
        # Map color names to hex codes
        color_map = {
            "black": "#2C2C2C",
            "blue": "#6890F0",
            "brown": "#A8714F",
            "gray": "#A0A0A0",
            "green": "#78C850",
            "pink": "#EE99AC",
            "purple": "#A040A0",
            "red": "#F08030",
            "white": "#F5F5F5",
            "yellow": "#F8D030"
        }
        bg_color = color_map.get(color_name)
    
    # Fallback to type color
    if not bg_color and pokemon_data.get('types'):
        type_name = pokemon_data['types'][0]['type']['name']
        bg_color = TYPE_COLORS.get(type_name, "#FFFFFF")
    
    if not bg_color:
        bg_color = "#FFFFFF"
    
    # Determine text color based on background brightness
    rgb = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))
    brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
    text_color = "#FFFFFF" if brightness < 128 else "#333333"
    
    # Apply CSS styling
    st.markdown(f"""
        <style>
            .stApp {{
                background: linear-gradient(135deg, {bg_color} 0%, {bg_color}dd 100%);
                background-attachment: fixed;
            }}
            
            .stMetric {{
                background-color: rgba(255, 255, 255, 0.95);
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            
            .stInfo, .stSuccess, .stWarning {{
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 10px;
            }}
            
            section[data-testid="stSidebar"] {{
                background-color: rgba(255, 255, 255, 0.95);
            }}
            
            .stTextInput > div > div > input {{
                background-color: rgba(255, 255, 255, 0.95);
                color: #333333;
                border-radius: 5px;
            }}
            
            button {{
                border-radius: 5px;
                background-color: {bg_color} !important;
                color: {text_color} !important;
            }}
        </style>
    """, unsafe_allow_html=True)

# Main search section
st.subheader("Search for a Pokémon")
col1, col2 = st.columns([4, 1])

with col1:
    pokemon_input = st.text_input(
        "Enter Pokémon name or ID:",
        value="piplup",
        placeholder="e.g., pikachu, charizard, 25"
    )

with col2:
    search_button = st.button("🔍 Search", use_container_width=True, key="search_btn")

# Fetch and display Pokemon data
pokemon_data = None

if search_button or pokemon_input:
    if pokemon_input.strip():
        with st.spinner(f"Loading {pokemon_input}..."):
            pokemon_data = fetch_pokemon(pokemon_input)
        
        if pokemon_data is None:
            st.error(f"❌ Pokémon '{pokemon_input}' not found! Please try another name or ID.")
            st.info("💡 Tip: Try searching for common names like 'pikachu', 'bulbasaur', 'charmander', etc.")
            st.stop()
    else:
        st.warning("Please enter a Pokémon name or ID")
        st.stop()
else:
    # Load default Pokemon (Piplup)
    pokemon_data = fetch_pokemon("piplup")

# Sidebar for navigation
if pokemon_data:
    st.sidebar.title("Options")
    view_mode = st.sidebar.radio("Select View:", ["Overview", "Stats", "Abilities & Moves", "Detailed Info"])
else:
    view_mode = "Overview"

# Main content area
if not pokemon_data:
    st.warning("Please search for a Pokémon to get started!")
    st.stop()

# Apply Pokemon-themed colors to the page
apply_pokemon_colors(pokemon_data)

# Display current Pokemon indicator
st.divider()
st.success(f"✅ Displaying data for: **{pokemon_data['name'].upper()}** (#{pokemon_data['id']})")
st.divider()

if view_mode == "Overview":
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Profile Image")
        try:
            img_url = pokemon_data["sprites"]["front_default"]
            st.image(img_url, use_container_width=True)
            
            # Shiny variant toggle
            if st.checkbox("Show Shiny Variant"):
                shiny_url = pokemon_data["sprites"]["front_shiny"]
                st.image(shiny_url, use_container_width=True, caption="Shiny Form")
        except Exception as e:
            st.warning(f"Could not load image: {e}")
    
    with col2:
        # Pokemon Name and ID
        st.subheader(f"{pokemon_data['name'].upper()} #{pokemon_data['id']}")
        
        # Basic Info
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.metric("Height", f"{pokemon_data['height']} dm")
            st.metric("Base Experience", pokemon_data['base_experience'])
        
        with col_info2:
            st.metric("Weight", f"{pokemon_data['weight']} hg")
        
        # Type(s)
        st.subheader("Type(s)")
        types = [t["type"]["name"].upper() for t in pokemon_data["types"]]
        type_cols = st.columns(len(types))
        for i, ptype in enumerate(types):
            with type_cols[i]:
                st.info(ptype)

elif view_mode == "Stats":
    st.subheader("Base Stats")
    
    # Create stats dataframe
    stats_data = []
    for stat in pokemon_data["stats"]:
        stats_data.append({
            "Stat": stat["stat"]["name"].replace("-", " ").title(),
            "Base Value": stat["base_stat"]
        })
    
    stats_df = pd.DataFrame(stats_data)
    
    # Display as bar chart
    st.bar_chart(stats_df.set_index("Stat"))
    
    # Display as table
    st.dataframe(stats_df, use_container_width=True, hide_index=True)

elif view_mode == "Abilities & Moves":
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Abilities")
        for ability in pokemon_data["abilities"]:
            ability_name = ability["ability"]["name"].replace("-", " ").title()
            is_hidden = " (Hidden)" if ability["is_hidden"] else ""
            st.write(f"• {ability_name}{is_hidden}")
    
    with col2:
        st.subheader("Type Effectiveness")
        st.info("💧 Water Type is super effective against: Fire, Ground, Rock")
        st.warning("⚠️ Water Type is weak to: Grass, Electric")

elif view_mode == "Detailed Info":
    st.subheader("Complete Pokémon Data")
    
    # Display raw JSON in expandable section
    with st.expander("View Raw JSON Data"):
        st.json(pokemon_data)
    
    # Display formatted details
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Physical Characteristics")
        st.write(f"**Height:** {pokemon_data['height']} decimeters ({pokemon_data['height']*10} cm)")
        st.write(f"**Weight:** {pokemon_data['weight']} hectograms ({pokemon_data['weight']/10} kg)")
        st.write(f"**Base Experience:** {pokemon_data['base_experience']}")
    
    with col2:
        st.subheader("Classification")
        st.write(f"**ID Number:** {pokemon_data['id']}")
        st.write(f"**Name:** {pokemon_data['name']}")
        st.write(f"**Types:** {', '.join([t['type']['name'].title() for t in pokemon_data['types']])}")

# Footer
st.divider()
st.caption("📚 Data from PokéAPI | Made with Streamlit")
