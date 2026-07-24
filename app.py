#will host the streamlit website here

#make sure to make a requirements.txt

import requests
from pprint import pprint
import time

import pandas as pd

def get_data(name):
  base_url = 'https://pokeapi.co/api/v2/pokemon/'
  name = name.lower()
  full_url=f'{base_url}{name}'

  return True
