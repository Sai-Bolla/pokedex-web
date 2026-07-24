# 📖 Pokédex Application

A Streamlit-based Pokédex application that displays detailed Pokémon information from the live PokéAPI using a dynamic search feature with **theme colors that match each Pokémon**.

## ✨ Features

- **🔍 Aligned Search Bar** - Clean, professional search interface with aligned search button
- **🎨 Dynamic Theme Colors** - Background colors automatically change based on the Pokémon's official color
  - Primary color from Pokédex species data
  - Fallback to type-based colors (fire=red, water=blue, etc.)
  - Smart text contrast for readability
- **Overview Tab**: Display Pokémon profile image, basic stats, type(s), and shiny variant toggle
- **Stats Tab**: Visualize base stats with interactive bar chart and detailed table
- **Abilities & Moves Tab**: Show abilities and type effectiveness information
- **Detailed Info Tab**: View complete formatted data and raw JSON
- **Live Data**: Fetches real-time data directly from PokéAPI
- **Error Handling**: User-friendly messages for invalid Pokémon searches
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

## Installation

1. **Clone or download the application files**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### Run the Application

```bash
streamlit run pokedex_app.py
```

The application will open in your default browser at `http://localhost:8501`

## Searching for Pokémon

1. Enter a Pokémon **name** (e.g., "pikachu", "charizard", "bulbasaur")
2. OR enter a **Pokédex ID** (e.g., "25" for Pikachu, "6" for Charizard)
3. Click the **🔍 Search** button or press Enter
4. The app will fetch and display the Pokémon's data with themed colors

**Default**: The app loads **Piplup** (#393) by default when first opened.

## 🎨 Dynamic Color Theming

The Pokédex app automatically changes the background color based on the Pokémon you're viewing:

### How It Works

1. **Fetches the Pokémon's official color** from the PokéAPI species endpoint
2. **Applies a gradient background** in that color
3. **Adjusts text/button colors** automatically for readability
4. **Uses type-based fallback colors** if species color data is unavailable

### Color Sources

- 🎯 **Primary**: Official Pokémon species color from PokéAPI
- 🔄 **Fallback**: Type-based colors (e.g., Fire Pokémon = Red, Water = Blue)

### Supported Colors

The app recognizes 10 primary colors:
- 🔴 **Red** - Fire, Electric, Psychic types
- 🔵 **Blue** - Water, Flying, Psychic types  
- 🟢 **Green** - Grass, Bug types
- 🟡 **Yellow** - Electric, Ground types
- 🟣 **Purple** - Poison, Dragon, Ghost types
- 🟠 **Brown** - Ground, Rock types
- ⚪ **White** - Normal, Steel, Ice types
- ⚫ **Black** - Dark, Ghost types
- 🌸 **Pink** - Fairy, Psychic types
- 🔘 **Gray** - Normal, Steel types

### Example Color Changes

- **Search "Pikachu"** → Page turns ⚡ **Yellow**
- **Search "Charizard"** → Page turns 🔥 **Red/Orange**
- **Search "Blastoise"** → Page turns 💧 **Blue**
- **Search "Venusaur"** → Page turns 🌿 **Green**
- **Search "Dragonite"** → Page turns 🐉 **Purple**

### UI Elements with Color Theming

- ✅ **Background**: Pokémon color gradient
- 🔘 **Search Button**: Matches Pokémon theme color
- 📋 **Content Cards**: White backgrounds for readability
- 📊 **Metrics**: Semi-transparent white with shadows
- 🖼️ **Sidebar**: Light background for navigation clarity

## Customization

### Adjust Color Intensity

Modify the color intensity in `apply_pokemon_colors()`:

```python
# Current: Slightly transparent gradient
background: linear-gradient(135deg, {bg_color} 0%, {bg_color}dd 100%);

# More transparent
background: linear-gradient(135deg, {bg_color}99 0%, {bg_color}66 100%);

# More solid
background: linear-gradient(135deg, {bg_color}ff 0%, {bg_color}ff 100%);
```

### Custom Color Mapping

Add or modify custom color mappings in the `color_map` dictionary:

```python
color_map = {
    "black": "#2C2C2C",      # Darker black
    "blue": "#0066CC",       # Darker blue
    "red": "#FF0000",        # Brighter red
    # Add custom colors here
}
```

### Adjust Button Colors

The search button automatically matches the Pokémon's theme color. To make it always the same:

```python
button {{
    border-radius: 5px;
    background-color: #6890F0 !important;  # Fixed color (water blue)
    color: #FFFFFF !important;
}}
```

### Disable Dynamic Colors

To use a static background color instead of dynamic theming:

```python
# Replace the apply_pokemon_colors() function with:
def apply_pokemon_colors(pokemon_data):
    st.markdown("""
        <style>
            .stApp {
                background-color: #F5F5F5;
            }
        </style>
    """, unsafe_allow_html=True)
```

### Change Default Pokémon

To change the default Pokémon loaded on startup, modify this line in `pokedex_app.py`:

```python
# Load default Pokemon (Piplup)
pokemon_data = fetch_pokemon("piplup")  # Change "piplup" to another Pokémon name or ID
```

Example:
```python
pokemon_data = fetch_pokemon("pikachu")  # Will load Pikachu by default
pokemon_data = fetch_pokemon("1")        # Will load Bulbasaur by default (Pokédex #1)
```

### Add Multiple Search Suggestions

Add suggested searches in the sidebar:

```python
st.sidebar.title("Quick Search")
suggestions = ["pikachu", "charizard", "blastoise", "dragonite"]
for suggestion in suggestions:
    if st.sidebar.button(f"🔹 {suggestion.title()}"):
        pokemon_data = fetch_pokemon(suggestion)
```

### Add Search History

Track previously searched Pokémon:

```python
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

if pokemon_data:
    if pokemon_data['name'] not in st.session_state.search_history:
        st.session_state.search_history.append(pokemon_data['name'])
    
    st.sidebar.write("**Recent Searches:**")
    for recent in st.session_state.search_history[-5:]:
        st.sidebar.write(f"• {recent.title()}")
```

### Display Full Moves List

Expand the Abilities & Moves section to show all moves:

```python
elif view_mode == "Abilities & Moves":
    st.subheader("All Moves")
    
    if "moves" in pokemon_data:
        # Show first 20 moves
        for move in pokemon_data["moves"][:20]:
            move_name = move['move']['name'].replace("-", " ").title()
            methods = [v['move_learn_method']['name'] for v in move['version_group_details']]
            st.write(f"• **{move_name}** - Learned by: {', '.join(set(methods))}")
    else:
        st.info("No moves data available")
```

### Add Evolution Chain

Fetch and display evolution information:

```python
@st.cache_data
def fetch_evolution_chain(pokemon_species_id):
    """Fetch evolution chain data"""
    try:
        url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_species_id}"
        response = requests.get(url)
        species_data = response.json()
        
        # Get evolution chain
        evolution_url = species_data['evolution_chain']['url']
        evo_response = requests.get(evolution_url)
        return evo_response.json()
    except:
        return None

# Then add to your app:
if pokemon_data:
    evolution_data = fetch_evolution_chain(pokemon_data['id'])
    if evolution_data:
        st.subheader("Evolution Chain")
        # Process and display evolution data
```

### Add Type Effectiveness Chart

Show which types are effective against the Pokémon:

```python
type_effectiveness = {
    "water": {
        "strong_against": ["fire", "ground", "rock"],
        "weak_to": ["grass", "electric"]
    },
    # ... add all types
}

pokemon_type = pokemon_data['types'][0]['type']['name']
if pokemon_type in type_effectiveness:
    effectiveness = type_effectiveness[pokemon_type]
    st.write(f"**Strong against:** {', '.join(effectiveness['strong_against'])}")
    st.write(f"**Weak to:** {', '.join(effectiveness['weak_to'])}")
```

## How It Works

The application uses the **PokéAPI** to fetch live Pokémon data:

1. **User enters a Pokémon name or ID** in the search bar
2. **API request** is sent to `https://pokeapi.co/api/v2/pokemon/{name_or_id}`
3. **Data is cached** using `@st.cache_data` to avoid repeated API calls
4. **UI updates** to display the Pokémon's complete information

### API Endpoint

```
https://pokeapi.co/api/v2/pokemon/{name_or_id}
```

**Examples:**
- `https://pokeapi.co/api/v2/pokemon/pikachu`
- `https://pokeapi.co/api/v2/pokemon/25`
- `https://pokeapi.co/api/v2/pokemon/charizard`

## API Resources

- **PokéAPI**: https://pokeapi.co/
- **API Documentation**: https://pokeapi.co/docs/v2
- **GitHub**: https://github.com/PokeAPI/pokeapi

## Supported Search Formats

You can search by:

| Format | Example | Works? |
|--------|---------|--------|
| Pokémon Name | `pikachu` | ✅ Yes |
| Pokédex ID | `25` | ✅ Yes |
| Mixed Case | `PiKaChU` | ✅ Yes (converted to lowercase) |
| Spaces in Name | `mr mime` | ✅ Yes |
| Hyphens | `mr-mime` | ✅ Yes (both formats work) |

## Caching

The app uses Streamlit's `@st.cache_data` decorator to cache API responses. This means:
- ✅ Repeated searches for the same Pokémon are instant
- ✅ Reduces API calls to PokéAPI
- ✅ Better performance

To clear the cache in Streamlit:
```bash
streamlit cache clear
```

## Project Structure

```
pokedex_app/
├── pokedex_app.py      # Main Streamlit application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Technologies Used

- **Streamlit**: Interactive web app framework
- **Pandas**: Data manipulation and analysis
- **Pillow**: Image processing
- **Requests**: HTTP library for API calls

## Future Enhancements

- [ ] Multi-Pokémon comparison side-by-side
- [ ] Evolution chain visualization with images
- [ ] Complete move list with filtering by type/learn method
- [ ] Interactive type effectiveness matrix
- [ ] Advanced Pokédex filters (by type, generation, region)
- [ ] Team builder (save favorite Pokémon)
- [ ] Weakness calculator for competitive play
- [ ] Variant/Form selector (Alola forms, Galar forms, etc.)
- [ ] Move damage calculator
- [ ] Dark mode support
- [ ] Pokémon breeding information
- [ ] Location finder (where to catch)

## License

This project uses data from **PokéAPI**, which is licensed under **CC0 1.0 Universal** (public domain).

## Troubleshooting

### Pokémon Not Found
**Issue:** "Pokémon 'xyz' not found!"

**Solutions:**
- Check spelling (e.g., "mr-mime" instead of "mr mime")
- Use the Pokédex ID number instead (e.g., "25" for Pikachu)
- Note: Some alternate forms/variants may not have separate entries

### Images Not Loading
**Issue:** Blank or broken images

**Solutions:**
- Check your internet connection
- Verify PokéAPI is accessible (visit https://pokeapi.co)
- PokéAPI sprites might be temporarily unavailable
- Some Pokémon may have limited sprite data

### API Connection Errors
**Issue:** "Error fetching Pokémon" or timeout errors

**Solutions:**
- Check internet connection
- Verify PokéAPI is online: https://pokeapi.co/health
- Restart the Streamlit app: `Ctrl+C` then run again
- PokéAPI might be experiencing temporary downtime

### Streamlit Errors
**Issue:** Module import errors or cache issues

**Solutions:**
```bash
# Install/update dependencies
pip install -r requirements.txt

# Clear Streamlit cache
streamlit cache clear

# Run app with dev mode
streamlit run pokedex_app.py --logger.level=debug
```

### Slow Performance
**Issue:** App is slow or laggy

**Solutions:**
- First search is slower (API call)
- Subsequent searches are instant (cached)
- Check internet connection speed
- Reduce browser tabs/apps running in background

## Common Pokémon to Try

Get started with these popular Pokémon:

- **Pikachu** (#25) - The iconic Pokémon
- **Charizard** (#6) - Fire/Flying powerhouse
- **Blastoise** (#9) - Water-type champion
- **Dragonite** (#149) - Pseudo-legendary
- **Alakazam** (#65) - Psychic master
- **Mewtwo** (#150) - Legendary psychic powerhouse
- **Gyarados** (#130) - Water/Flying beast
- **Lapras** (#131) - Ice/Water tank
- **Machamp** (#68) - Fighting-type crusher
- **Arcanine** (#59) - Fire-type loyal companion

## Tips & Tricks

- 💡 Use Pokédex IDs for faster searches on specific Pokémon
- 🔍 The search is case-insensitive (PIKACHU = pikachu)
- ⚡ Results are cached - searching again is instant
- 📱 App works on desktop, tablet, and mobile
- 🎨 Toggle shiny variants in the Overview tab
- 📊 Stats tab includes visual bar charts

---

Happy Pokémon exploring! 🎮✨
