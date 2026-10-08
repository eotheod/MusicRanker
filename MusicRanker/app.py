import base64
import os
import random
import urllib.parse
import uuid
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Music Vault & Arena 🎧", page_icon="🎵", layout="wide"
)


# -----------------------------------------------------------------------------
# USTAWIANIE OBRAZU W TLE
# -----------------------------------------------------------------------------
def set_background(image_file):
  if os.path.exists(image_file):
    with open(image_file, 'rb') as f:
      encoded_string = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), url("data:image/jpg;base64,{encoded_string}");
            background-attachment: fixed;
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Wczytujemy tło z folderu assets
set_background('assets/blackpink.jpg')


# -----------------------------------------------------------------------------
# 1. BAZA DANYCH OFICJALNEJ DYSKOGRAFII
# -----------------------------------------------------------------------------
@st.cache_data
def load_full_official_discography():
  data = [
      # === BLACKPINK ===
      {"Artist": "Blackpink", "Title": "Whistle", "Album": "Square One (2016)"},
      {"Artist": "Blackpink", "Title": "Boombayah", "Album": "Square One (2016)"},
      {
          "Artist": "Blackpink",
          "Title": "Playing with Fire",
          "Album": "Square Two (2016)",
      },
      {"Artist": "Blackpink", "Title": "Stay", "Album": "Square Two (2016)"},
      {
          "Artist": "Blackpink",
          "Title": "Whistle (Acoustic Ver.)",
          "Album": "Square Two (2016)",
      },
      {
          "Artist": "Blackpink",
          "Title": "As If It's Your Last",
          "Album": "Single (2017)",
      },
      {
          "Artist": "Blackpink",
          "Title": "DDU-DU DDU-DU",
          "Album": "Square Up (2018)",
      },
      {
          "Artist": "Blackpink",
          "Title": "Forever Young",
          "Album": "Square Up (2018)",
      },
      {"Artist": "Blackpink", "Title": "Really", "Album": "Square Up (2018)"},
      {
          "Artist": "Blackpink",
          "Title": "See U Later",
          "Album": "Square Up (2018)",
      },
      {
          "Artist": "Blackpink",
          "Title": "Kill This Love",
          "Album": "Kill This Love (2019)",
      },
      {
          "Artist": "Blackpink",
          "Title": "Don't Know What to Do",
          "Album": "Kill This Love (2019)",
      },
      {
          "Artist": "Blackpink",
          "Title": "Kick It",
          "Album": "Kill This Love (2019)",
      },
      {
          "Artist": "Blackpink",
          "Title": "Hope Not",
          "Album": "Kill This Love (2019)",
      },
      {
          "Artist": "Blackpink",
          "Title": "Kiss and Make Up (with Dua Lipa)",
          "Album": "Dua Lipa Complete (2018)",
      },
      {
          "Artist": "Blackpink",
          "Title": "How You Like That",
          "Album": "The Album (2020)",
      },
      {
          "Artist": "Blackpink",
          "Title": "Ice Cream (with Selena Gomez)",
          "Album": "The Album (2020)",
      },
      {
          "Artist": "Blackpink",
          "Title": "Pretty Savage",
          "Album": "The Album (2020)",
      },
      {
          "Artist": "Blackpink",
          "Title": "Bet You Wanna (feat. Cardi B)",
          "Album": "The Album (2020)",
      },
      {
          "Artist": "Blackpink",
          "Title": "Lovesick Girls",
          "Album": "The Album (2020)",
      },
      {
          "Artist": "Blackpink",
          "Title": "Crazy Over You",
          "Album": "The Album (2020)",
      },
      {
          "Artist": "Blackpink",
          "Title": "Love To Hate Me",
          "Album": "The Album (2020)",
      },
      {
          "Artist": "Blackpink",
          "Title": "You Never Know",
          "Album": "The Album (2020)",
      },
      {
          "Artist": "Blackpink",
          "Title": "Sour Candy (with Lady Gaga)",
          "Album": "Chromatica (2020)",
      },
      {"Artist": "Blackpink", "Title": "Pink Venom", "Album": "Born Pink (2022)"},
      {"Artist": "Blackpink", "Title": "Shut Down", "Album": "Born Pink (2022)"},
      {"Artist": "Blackpink", "Title": "Typa Girl", "Album": "Born Pink (2022)"},
      {
          "Artist": "Blackpink",
          "Title": "Yeah Yeah Yeah",
          "Album": "Born Pink (2022)",
      },
      {
          "Artist": "Blackpink",
          "Title": "Hard to Love",
          "Album": "Born Pink (2022)",
      },
      {
          "Artist": "Blackpink",
          "Title": "The Happiest Girl",
          "Album": "Born Pink (2022)",
      },
      {"Artist": "Blackpink", "Title": "Tally", "Album": "Born Pink (2022)"},
      {
          "Artist": "Blackpink",
          "Title": "Ready for Love",
          "Album": "Born Pink (2022)",
      },
      {
          "Artist": "Blackpink",
          "Title": "The Girls (BLACKPINK THE GAME OST)",
          "Album": "Single (2023)",
      },
      {"Artist": "Jennie (Blackpink)", "Title": "SOLO", "Album": "Solo (2018)"},
      {
          "Artist": "Jennie (Blackpink)",
          "Title": "You & Me",
          "Album": "Single (2023)",
      },
      {
          "Artist": "Jennie (Blackpink)",
          "Title": "One of the Girls (with The Weeknd & Lily-Rose Depp)",
          "Album": "The Idol OST (2023)",
      },
      {"Artist": "Rosé (Blackpink)", "Title": "On The Ground", "Album": "-R- (2021)"},
      {"Artist": "Rosé (Blackpink)", "Title": "Gone", "Album": "-R- (2021)"},
      {
          "Artist": "Rosé (Blackpink)",
          "Title": "APT. (feat. Bruno Mars)",
          "Album": "rosie (2024)",
      },
      {"Artist": "Lisa (Blackpink)", "Title": "LALISA", "Album": "LALISA (2021)"},
      {"Artist": "Lisa (Blackpink)", "Title": "MONEY", "Album": "LALISA (2021)"},
      {
          "Artist": "Lisa (Blackpink)",
          "Title": "SG (with DJ Snake, Ozuna, Megan Thee Stallion)",
          "Album": "Single (2021)",
      },
      {
          "Artist": "Lisa (Blackpink)",
          "Title": "Rockstar",
          "Album": "Single (2024)",
      },
      {
          "Artist": "Lisa (Blackpink)",
          "Title": "New Woman (feat. Rosalía)",
          "Album": "Single (2024)",
      },
      {
          "Artist": "Lisa (Blackpink)",
          "Title": "Moonlit Floor",
          "Album": "Single (2024)",
      },
      {"Artist": "Jisoo (Blackpink)", "Title": "FLOWER", "Album": "ME (2023)"},
      {
          "Artist": "Jisoo (Blackpink)",
          "Title": "All Eyes On Me",
          "Album": "ME (2023)",
      },
      # === BABYMONSTER ===
      {
          "Artist": "BABYMONSTER",
          "Title": "BATTER UP",
          "Album": "BABYMONS7ER (2024)",
      },
      {
          "Artist": "BABYMONSTER",
          "Title": "Stuck In The Middle",
          "Album": "BABYMONS7ER (2024)",
      },
      {
          "Artist": "BABYMONSTER",
          "Title": "SHEESH",
          "Album": "BABYMONS7ER (2024)",
      },
      {
          "Artist": "BABYMONSTER",
          "Title": "LIKE THAT",
          "Album": "BABYMONS7ER (2024)",
      },
      {"Artist": "BABYMONSTER", "Title": "DREAM", "Album": "BABYMONS7ER (2024)"},
      {
          "Artist": "BABYMONSTER",
          "Title": "Stuck In The Middle (Remix)",
          "Album": "BABYMONS7ER (2024)",
      },
      {"Artist": "BABYMONSTER", "Title": "FOREVER", "Album": "DRIP (2024)"},
      {"Artist": "BABYMONSTER", "Title": "CLIK CLAK", "Album": "DRIP (2024)"},
      {"Artist": "BABYMONSTER", "Title": "DRIP", "Album": "DRIP (2024)"},
      {
          "Artist": "BABYMONSTER",
          "Title": "Love In My Heart",
          "Album": "DRIP (2024)",
      },
      {
          "Artist": "BABYMONSTER",
          "Title": "Woke Up In Tokyo (Ruka & Asa)",
          "Album": "DRIP (2024)",
      },
      {"Artist": "BABYMONSTER", "Title": "BILLIONAIRE", "Album": "DRIP (2024)"},
      {"Artist": "BABYMONSTER", "Title": "Love, Maybe", "Album": "DRIP (2024)"},
      {
          "Artist": "BABYMONSTER",
          "Title": "Really Like You",
          "Album": "DRIP (2024)",
      },
      {
          "Artist": "BABYMONSTER",
          "Title": "BATTER UP (Remix)",
          "Album": "DRIP (2024)",
      },

      # === KATSEYE ===
      {
          "Artist": "KATSEYE",
          "Title": "Debut",
          "Album": "SIS (Soft Is Strong) (2024)",
      },
      {
          "Artist": "KATSEYE",
          "Title": "Touch",
          "Album": "SIS (Soft Is Strong) (2024)",
      },
      {
          "Artist": "KATSEYE",
          "Title": "My Way",
          "Album": "SIS (Soft Is Strong) (2024)",
      },
      {
          "Artist": "KATSEYE",
          "Title": "I'm Pretty",
          "Album": "SIS (Soft Is Strong) (2024)",
      },
      {
          "Artist": "KATSEYE",
          "Title": "Tonight I Might",
          "Album": "SIS (Soft Is Strong) (2024)",
      },
      {
          "Artist": "KATSEYE",
          "Title": "Touch (feat. YEONJUN of TXT)",
          "Album": "Single (2024)",
      },
      {
          "Artist": "KATSEYE",
          "Title": "Flame",
          "Album": "Jentry Chau vs The Underworld OST (2024)",
      },
      {
          "Artist": "KATSEYE",
          "Title": "Gnarly",
          "Album": "BEAUTIFUL CHAOS (2025)",
      },
      {
          "Artist": "KATSEYE",
          "Title": "Gabriela",
          "Album": "BEAUTIFUL CHAOS (2025)",
      },
      {
          "Artist": "KATSEYE",
          "Title": "Gameboy",
          "Album": "BEAUTIFUL CHAOS (2025)",
      },
      {
          "Artist": "KATSEYE",
          "Title": "Mean Girls",
          "Album": "BEAUTIFUL CHAOS (2025)",
      },
      {"Artist": "KATSEYE", "Title": "M.I.A", "Album": "BEAUTIFUL CHAOS (2025)"},
      {"Artist": "KATSEYE", "Title": "PINKY UP", "Album": "WILD (2026)"},
      {"Artist": "KATSEYE", "Title": "Animal", "Album": "WILD (2026)"},
      {"Artist": "KATSEYE", "Title": "Hootie Frutti", "Album": "WILD (2026)"},
      {"Artist": "KATSEYE", "Title": "Bel Air", "Album": "WILD (2026)"},
      {"Artist": "KATSEYE", "Title": "That Way", "Album": "WILD (2026)"},

      # === TINI ===
      {"Artist": "Tini", "Title": "All You Gotta Do", "Album": "Tini (2016)"},
      {"Artist": "Tini", "Title": "Great Escape", "Album": "Tini (2016)"},
      {"Artist": "Tini", "Title": "Still Standing", "Album": "Tini (2016)"},
      {"Artist": "Tini", "Title": "Got Me Started", "Album": "Tini (2016)"},
      {"Artist": "Tini", "Title": "My Stupid Heart", "Album": "Tini (2016)"},
      {"Artist": "Tini", "Title": "Don't Cry for Me", "Album": "Tini (2016)"},
      {"Artist": "Tini", "Title": "Finders Keepers", "Album": "Tini (2016)"},
      {"Artist": "Tini", "Title": "Handwritten", "Album": "Tini (2016)"},
      {"Artist": "Tini", "Title": "Sólo Dime Tú", "Album": "Tini (2016)"},
      {"Artist": "Tini", "Title": "Sigo Adelante", "Album": "Tini (2016)"},
      {"Artist": "Tini", "Title": "Si Tu Te Vas", "Album": "Tini (2016)"},
      {"Artist": "Tini", "Title": "Lo Que Tu Alma Escribe", "Album": "Tini (2016)"},
      {"Artist": "Tini", "Title": "Siempre Brillarás", "Album": "Tini (2016)"},
      {"Artist": "Tini", "Title": "Se Escapa Tu Amor", "Album": "Tini (2016)"},
      {
          "Artist": "Tini",
          "Title": "Yo Te Amo a Ti (with Jorge Blanco)",
          "Album": "Tini (2016)",
      },
      {"Artist": "Tini", "Title": "Confía en Mí", "Album": "Tini (2016)"},
      {
          "Artist": "Tini",
          "Title": "Te Quiero Más (feat. Nacho)",
          "Album": "Quiero Volver (2018)",
      },
      {
          "Artist": "Tini",
          "Title": "Princesa (feat. Karol G)",
          "Album": "Quiero Volver (2018)",
      },
      {
          "Artist": "Tini",
          "Title": "Consejo de Amor (feat. Morat)",
          "Album": "Quiero Volver (2018)",
      },
      {
          "Artist": "Tini",
          "Title": "Quiero Volver (feat. Sebastián Yatra)",
          "Album": "Quiero Volver (2018)",
      },
      {
          "Artist": "Tini",
          "Title": "Por Que Te Vas (feat. Cali y El Dandee)",
          "Album": "Quiero Volver (2018)",
      },
      {
          "Artist": "Tini",
          "Title": "Waves (feat. Transmission)",
          "Album": "Quiero Volver (2018)",
      },
      {
          "Artist": "Tini",
          "Title": "22 (feat. Greeicy)",
          "Album": "Tini Tini Tini (2020)",
      },
      {
          "Artist": "Tini",
          "Title": "Sueltate El Pelo",
          "Album": "Tini Tini Tini (2020)",
      },
      {
          "Artist": "Tini",
          "Title": "Fresa (feat. Lalo Ebratt)",
          "Album": "Tini Tini Tini (2020)",
      },
      {
          "Artist": "Tini",
          "Title": "Oye (feat. Sebastián Yatra)",
          "Album": "Tini Tini Tini (2020)",
      },
      {
          "Artist": "Tini",
          "Title": "Recuerdo (feat. Mau y Ricky)",
          "Album": "Tini Tini Tini (2020)",
      },
      {
          "Artist": "Tini",
          "Title": "Ella Dice (feat. KHEA)",
          "Album": "Tini Tini Tini (2020)",
      },
      {
          "Artist": "Tini",
          "Title": "Un Beso en Madrid (feat. Alejandro Sanz)",
          "Album": "Tini Tini Tini (2020)",
      },
      {
          "Artist": "Tini",
          "Title": "High (Remix with María Becerra & Lola Índigo)",
          "Album": "Tini Tini Tini (2020)",
      },
      {
          "Artist": "Tini",
          "Title": "Mi Mientes (feat. María Becerra)",
          "Album": "Cupido (2023)",
      },
      {
          "Artist": "Tini",
          "Title": "Maldita Foto (feat. Manuel Turizo)",
          "Album": "Cupido (2023)",
      },
      {"Artist": "Tini", "Title": "Bar (feat. L-Gante)", "Album": "Cupido (2023)"},
      {
          "Artist": "Tini",
          "Title": "Fantasi (feat. Beéle)",
          "Album": "Cupido (2023)",
      },
      {
          "Artist": "Tini",
          "Title": "La Loto (feat. Anitta & Becky G)",
          "Album": "Cupido (2023)",
      },
      {
          "Artist": "Tini",
          "Title": "El Último Beso (feat. Tiago PZK)",
          "Album": "Cupido (2023)",
      },
      {"Artist": "Tini", "Title": "Cupido", "Album": "Cupido (2023)"},
      {
          "Artist": "Tini",
          "Title": "La_Original.mp3 (feat. Emilia)",
          "Album": "Cupido / Single (2023)",
      },
      {"Artist": "Tini", "Title": "pa", "Album": "un mechon de pelo (2024)"},
      {"Artist": "Tini", "Title": "postares", "Album": "un mechon de pelo (2024)"},
      {
          "Artist": "Tini",
          "Title": "Buenos Aires",
          "Album": "un mechon de pelo (2024)",
      },
      {
          "Artist": "Tini",
          "Title": "Tinta Buena",
          "Album": "un mechon de pelo (2024)",
      },
      {"Artist": "Tini", "Title": "ni de ti", "Album": "un mechon de pelo (2024)"},
      {"Artist": "Tini", "Title": "ángel", "Album": "un mechon de pelo (2024)"},
      {
          "Artist": "Tini",
          "Title": "We Pray (with Coldplay, Little Simz, Burna Boy)",
          "Album": "Moon Music (2024)",
      },

      # === JUSTIN BIEBER ===
      {"Artist": "Justin Bieber", "Title": "One Time", "Album": "My World (2009)"},
      {
          "Artist": "Justin Bieber",
          "Title": "One Less Lonely Girl",
          "Album": "My World (2009)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Love Me",
          "Album": "My World (2009)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Favorite Girl",
          "Album": "My World (2009)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Down to Earth",
          "Album": "My World (2009)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Bigger",
          "Album": "My World (2009)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "First Dance (feat. Usher)",
          "Album": "My World (2009)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Baby (feat. Ludacris)",
          "Album": "My World 2.0 (2010)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Somebody to Love",
          "Album": "My World 2.0 (2010)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "U Smile",
          "Album": "My World 2.0 (2010)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Runaway Love",
          "Album": "My World 2.0 (2010)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Never Let You Go",
          "Album": "My World 2.0 (2010)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Overboard (feat. Jessica Jarrell)",
          "Album": "My World 2.0 (2010)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Eenie Meenie (with Sean Kingston)",
          "Album": "My World 2.0 (2010)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Up",
          "Album": "My World 2.0 (2010)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "That Should Be Me",
          "Album": "My World 2.0 (2010)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Never Say Never (feat. Jaden Smith)",
          "Album": "Never Say Never (2011)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Mistletoe",
          "Album": "Under the Mistletoe (2011)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Boyfriend",
          "Album": "Believe (2012)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "As Long As You Love Me (feat. Big Sean)",
          "Album": "Believe (2012)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Beauty and a Beat (feat. Nicki Minaj)",
          "Album": "Believe (2012)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "All Around the World (feat. Ludacris)",
          "Album": "Believe (2012)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Die in Your Arms",
          "Album": "Believe (2012)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Right Here (feat. Drake)",
          "Album": "Believe (2012)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "All That Matters",
          "Album": "Journals (2013)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Confident (feat. Chance the Rapper)",
          "Album": "Journals (2013)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Heartbreaker",
          "Album": "Journals (2013)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "What Do You Mean?",
          "Album": "Purpose (2015)",
      },
      {"Artist": "Justin Bieber", "Title": "Sorry", "Album": "Purpose (2015)"},
      {
          "Artist": "Justin Bieber",
          "Title": "Love Yourself",
          "Album": "Purpose (2015)",
      },
      {"Artist": "Justin Bieber", "Title": "Company", "Album": "Purpose (2015)"},
      {
          "Artist": "Justin Bieber",
          "Title": "I'll Show You",
          "Album": "Purpose (2015)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Where Are Ü Now (with Jack Ü)",
          "Album": "Purpose (2015)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Despacito (Remix with Luis Fonsi & Daddy Yankee)",
          "Album": "Single (2017)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "I'm the One (with DJ Khaled, Quavo, Chance the Rapper, Lil"
          " Wayne)",
          "Album": "Grateful (2017)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "I Don't Care (with Ed Sheeran)",
          "Album": "No.6 Collaborations Project (2019)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "10,000 Hours (with Dan + Shay)",
          "Album": "Good Things (2019)",
      },
      {"Artist": "Justin Bieber", "Title": "Yummy", "Album": "Changes (2020)"},
      {
          "Artist": "Justin Bieber",
          "Title": "Intentions (feat. Quavo)",
          "Album": "Changes (2020)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Forever (feat. Post Malone & Clever)",
          "Album": "Changes (2020)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Stuck with U (with Ariana Grande)",
          "Album": "Single (2020)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Holy (feat. Chance the Rapper)",
          "Album": "Justice (2021)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Lonely (with Benny Blanco)",
          "Album": "Justice (2021)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Anyone",
          "Album": "Justice (2021)",
      },
      {"Artist": "Justin Bieber", "Title": "Hold On", "Album": "Justice (2021)"},
      {
          "Artist": "Justin Bieber",
          "Title": "Peaches (feat. Daniel Caesar & Giveon)",
          "Album": "Justice (2021)",
      },
      {"Artist": "Justin Bieber", "Title": "Ghost", "Album": "Justice (2021)"},
      {
          "Artist": "Justin Bieber",
          "Title": "STAY (with The Kid LAROI)",
          "Album": "Single (2021)",
      },
      {
          "Artist": "Justin Bieber",
          "Title": "Honest (feat. Don Toliver)",
          "Album": "Single (2022)",
      },
  ]
  df = pd.DataFrame(data)
  df['Full_Name'] = df['Artist'] + ' - ' + df['Title']
  return df


if 'db' not in st.session_state:
  st.session_state.db = load_full_official_discography()

df = st.session_state.db


def get_spotify_url(artist, title):
  query = urllib.parse.quote(f'{artist} {title}')
  return f'https://open.spotify.com/search/{query}'


def get_youtube_url(artist, title):
  query = urllib.parse.quote(f'{artist} {title}')
  return f'https://www.youtube.com/results?search_query={query}'


# --- STAN APLIKACJI ---
if 'custom_playlists' not in st.session_state:
  st.session_state.custom_playlists = {
      '💖 Moje Top Hity': [
          {'artist': 'Blackpink', 'title': 'Pink Venom'},
          {'artist': 'KATSEYE', 'title': 'Touch'},
          {'artist': 'Jennie (Blackpink)', 'title': 'SOLO'},
      ],
      '🔥 Bieber & Tini Vibe': [
          {'artist': 'Tini', 'title': 'Mi Mientes'},
          {'artist': 'Justin Bieber', 'title': 'Peaches'},
      ],
  }

if 'song_ratings' not in st.session_state:
  st.session_state.song_ratings = {}

if 'battle_game' not in st.session_state:
  st.session_state.battle_game = {
      'in_room': False,
      'room_code': 'KPOP1',
      'user_nick': 'MłodyG',
      'pool': [],
      'current_a': None,
      'current_b': None,
      'votes_a': 0,
      'votes_b': 0,
  }

# -----------------------------------------------------------------------------
# NAGŁÓWEK APLIKACJI
# -----------------------------------------------------------------------------
st.title('🎵 My Music Vault & Studio 🚀')
st.caption(
    '✨ Twoja strefa muzyki: **BLACKPINK • BABYMONSTER • KATSEYE • TINI • JUSTIN'
    ' BIEBER**'
)

tab_playlists, tab_ranking, tab_battle, tab_add_custom = st.tabs([
    '🎧 MOJE PLAYLISTY',
    '🏆 ODKRYWAJ I OCENIAJ',
    '⚔️ ARENA BITWY 1v1',
    '➕ DODAJ WŁASNY KAWAŁEK',
])

# =============================================================================
# ZAKŁADKA 1: MOJE PLAYLISTY
# =============================================================================
with tab_playlists:
  st.subheader('🔥 Stwórz własny mixtape / playlistę')

  with st.container():
    c_in, c_bt = st.columns([3, 1])
    with c_in:
      new_pl_input = st.text_input(
          'Wpisz nazwę nowej playlisty:',
          placeholder='np. Vibe na wakacje 🌴, K-Pop Queens 👑...',
          label_visibility='collapsed',
      )
    with c_bt:
      if st.button(
          '✨ Stwórz playlistę', use_container_width=True, type='primary'
      ):
        clean = new_pl_input.strip()
        if clean:
          if clean not in st.session_state.custom_playlists:
            st.session_state.custom_playlists[clean] = []
            st.success(f'Utworzono playlistę: {clean} 🎉')
            st.rerun()
          else:
            st.warning('Ta nazwa już istnieje!')
        else:
          st.error('Podaj nazwę!')

  st.write('')

  if not st.session_state.custom_playlists:
    st.info(
        'Nie masz jeszcze playlist! Wpisz nazwę powyżej i kliknij Stwórz. 🚀'
    )
  else:
    for pl_name in list(st.session_state.custom_playlists.keys()):
      songs_list = st.session_state.custom_playlists[pl_name]

      st.markdown(
          f"""
          <div style="background: linear-gradient(135deg, #1f1c2c 0%, #928DAB 100%); padding: 12px 20px; border-radius: 12px; color: white; font-size: 20px; font-weight: bold; margin-top: 20px;">
              🎵 {pl_name} <span style="font-size: 14px; opacity: 0.8; font-weight: normal;">({len(songs_list)} utworów)</span>
          </div>
          """,
          unsafe_allow_html=True,
      )

      st.write('')

      col_f1, col_f2, col_f3 = st.columns([2, 3, 1])
      with col_f1:
        art_filter = st.selectbox(
            'Filtruj artystę:',
            ['Wszyscy'] + list(df['Artist'].unique()),
            key=f'f_art_{pl_name}',
        )
      with col_f2:
        sub_df = (
            df if art_filter == 'Wszyscy' else df[df['Artist'] == art_filter]
        )
        song_chosen = st.selectbox(
            'Wybierz piosenkę:',
            sub_df['Full_Name'].tolist(),
            key=f'f_s_{pl_name}',
        )
      with col_f3:
        st.write('')
        st.write('')
        if st.button(
            '➕ Dodaj', key=f'btn_add_{pl_name}', use_container_width=True
        ):
          match = df[df['Full_Name'] == song_chosen].iloc[0]
          item_dict = {'artist': match['Artist'], 'title': match['Title']}
          if item_dict not in songs_list:
            songs_list.append(item_dict)
            st.toast('Dodano do playlisty! 🎉')
            st.rerun()

      if not songs_list:
        st.caption(
            'Ta playlista jest jeszcze pusta. Dodaj swój pierwszy kawałek'
            ' powyżej! 🎶'
        )
      else:
        for idx_item, song in enumerate(songs_list):
          s_artist = (
              song.get('artist', 'Wykonawca')
              if isinstance(song, dict)
              else 'Artist'
          )
          s_title = (
              song.get('title', song) if isinstance(song, dict) else str(song)
          )

          col_t1, col_t2, col_t3, col_t4 = st.columns([4, 2, 2, 1])
          with col_t1:
            st.markdown(f'🖤 **{s_title}** — *{s_artist}*')
          with col_t2:
            st.link_button(
                '🟢 Spotify',
                get_spotify_url(s_artist, s_title),
                use_container_width=True,
            )
          with col_t3:
            st.link_button(
                '🔴 YouTube',
                get_youtube_url(s_artist, s_title),
                use_container_width=True,
            )
          with col_t4:
            if st.button('❌', key=f'del_s_{pl_name}_{idx_item}'):
              songs_list.pop(idx_item)
              st.rerun()

      with st.expander('⚙️ Opcje playlisty (Zmień nazwę / Usuń)'):
        col_r1, col_r2 = st.columns([3, 1])
        with col_r1:
          ren_val = st.text_input(
              'Nowa nazwa:', value=pl_name, key=f'ren_in_{pl_name}'
          )
          if st.button('✏️ Zapisz nową nazwę', key=f'ren_btn_{pl_name}'):
            if ren_val.strip() and ren_val.strip() != pl_name:
              st.session_state.custom_playlists[ren_val.strip()] = (
                  st.session_state.custom_playlists.pop(pl_name)
              )
              st.rerun()
        with col_r2:
          st.write('')
          st.write('')
          if st.button('🗑️ Usuń całą playlistę', key=f'del_pl_{pl_name}'):
            del st.session_state.custom_playlists[pl_name]
            st.rerun()

      st.divider()

# =============================================================================
# ZAKŁADKA 2: BAZA & RANKING
# =============================================================================
with tab_ranking:
  st.subheader('🔎 Przeglądaj i oceniaj piosenki')

  col_f, col_s = st.columns([1, 1])
  with col_f:
    selected_artist = st.selectbox(
        'Wybierz artystę:',
        ['Wszyscy wykonawcy'] + list(df['Artist'].unique()),
    )
  with col_s:
    search_q = st.text_input('Szukaj piosenki:', placeholder='Wpisz tytuł...')

  filt_df = df.copy()
  if selected_artist != 'Wszyscy wykonawcy':
    filt_df = filt_df[filt_df['Artist'] == selected_artist]
  if search_q:
    filt_df = filt_df[filt_df['Title'].str.contains(search_q, case=False)]

  st.caption(f'Znalezione utwory: {len(filt_df)}')

  for idx, row in filt_df.iterrows():
    c_info, c_rate, c_links, c_quick = st.columns([3, 2, 2, 2])

    with c_info:
      st.markdown(f"🌟 **{row['Title']}**")
      st.caption(f"{row['Artist']} • *{row['Album']}*")

    with c_rate:
      s_key = row['Full_Name']
      cur_r = st.session_state.song_ratings.get(s_key, 5)
      new_r = st.slider(
          'Ocena',
          1,
          5,
          value=cur_r,
          key=f'r_{idx}',
          label_visibility='collapsed',
      )
      st.session_state.song_ratings[s_key] = new_r

    with c_links:
      l1, l2 = st.columns(2)
      with l1:
        st.link_button(
            '🟢 Spotify',
            get_spotify_url(row['Artist'], row['Title']),
            use_container_width=True,
        )
      with l2:
        st.link_button(
            '🔴 YouTube',
            get_youtube_url(row['Artist'], row['Title']),
            use_container_width=True,
        )

    with c_quick:
      if st.session_state.custom_playlists:
        target_p = st.selectbox(
            'Wrzuć do:',
            list(st.session_state.custom_playlists.keys()),
            key=f'q_sel_{idx}',
            label_visibility='collapsed',
        )
        if st.button('➕ Dodaj', key=f'q_btn_{idx}'):
          i_dict = {'artist': row['Artist'], 'title': row['Title']}
          if i_dict not in st.session_state.custom_playlists[target_p]:
            st.session_state.custom_playlists[target_p].append(i_dict)
            st.toast('Dodano do playlisty! 🚀')
            st.rerun()

    st.divider()

# =============================================================================
# ZAKŁADKA 3: GRA 1 VS 1 NA ŻYWO (Z BARDZIEJ WIDOCZNĄ OCENĄ)
# =============================================================================
with tab_battle:
  bg = st.session_state.battle_game

  if not bg['in_room']:
    st.subheader('⚔️ Stwórz pokój pojedynków lub dołącz do znajomych')

    nick = st.text_input('Twój Nick / Imię:', value=bg['user_nick'])

    col_c, col_b = st.columns([3, 1])
    with col_c:
      room_code = st.text_input('Kod Pokoju:', value=bg['room_code'])
    with col_b:
      st.write('')
      st.write('')
      if st.button('🎲 Losuj Kod'):
        room_code = str(uuid.uuid4())[:5].upper()

    num_songs = st.selectbox('Ile piosenek w bitwie?', [2, 4, 8, 16], index=0)

    if st.button(
        '🚀 Wchodzę do Areny!', use_container_width=True, type='primary'
    ):
      bg['user_nick'] = nick
      bg['room_code'] = room_code.upper()
      pool_data = df.sample(n=min(num_songs, len(df))).to_dict(orient='records')
      bg['pool'] = pool_data
      bg['current_a'] = pool_data[0]
      bg['current_b'] = pool_data[1]
      bg['votes_a'] = 0
      bg['votes_b'] = 0
      bg['in_room'] = True
      st.rerun()

  else:
    st.markdown(
        f"### 🎮 Kod Pokoju: `{bg['room_code']}` | Grasz jako: **{bg['user_nick']}**"
    )

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
      if st.button('🎲 Następne starcie'):
        if len(bg['pool']) >= 2:
          pair = random.sample(bg['pool'], 2)
          bg['current_a'] = pair[0]
          bg['current_b'] = pair[1]
          bg['votes_a'] = 0
          bg['votes_b'] = 0
          st.rerun()
    with col_btn2:
      if st.button('🚪 Wyjdź z pokoju'):
        bg['in_room'] = False
        st.rerun()

    st.divider()

    song_a = bg['current_a']
    song_b = bg['current_b']

    # Pobieranie ocen z bazy
    full_name_a = f"{song_a['Artist']} - {song_a['Title']}"
    rating_a = st.session_state.song_ratings.get(full_name_a, 5)

    full_name_b = f"{song_b['Artist']} - {song_b['Title']}"
    rating_b = st.session_state.song_ratings.get(full_name_b, 5)

    col_a, col_b = st.columns(2)

    with col_a:
      st.markdown(f"### 🔥 {song_a['Title']}")
      st.caption(f"Wykonawca: **{song_a['Artist']}**")

      # Stylowa, duża ocena w widocznym miejscu
      st.markdown(
          f"""
          <div style="background: rgba(255, 255, 255, 0.1); border-left: 4px solid #ff4b4b; padding: 8px 12px; border-radius: 6px; margin-bottom: 12px;">
              <span style="font-size: 16px; font-weight: bold; color: #ffeb3b;">⭐ Ocena: {rating_a} / 5</span>
          </div>
          """,
          unsafe_allow_html=True,
      )

      st.link_button(
          '🟢 Słuchaj na Spotify',
          get_spotify_url(song_a['Artist'], song_a['Title']),
          use_container_width=True,
      )
      if st.button(
          f"❤️ Głosuj na {song_a['Title']}",
          key='btn_v_a',
          type='primary',
          use_container_width=True,
      ):
        bg['votes_a'] += 1
        st.toast('Głos oddany!')

    with col_b:
      st.markdown(f"### 🔥 {song_b['Title']}")
      st.caption(f"Wykonawca: **{song_b['Artist']}**")

      # Stylowa, duża ocena w widocznym miejscu
      st.markdown(
          f"""
          <div style="background: rgba(255, 255, 255, 0.1); border-left: 4px solid #ff4b4b; padding: 8px 12px; border-radius: 6px; margin-bottom: 12px;">
              <span style="font-size: 16px; font-weight: bold; color: #ffeb3b;">⭐ Ocena: {rating_b} / 5</span>
          </div>
          """,
          unsafe_allow_html=True,
      )

      st.link_button(
          '🟢 Słuchaj na Spotify',
          get_spotify_url(song_b['Artist'], song_b['Title']),
          use_container_width=True,
      )
      if st.button(
          f"❤️ Głosuj na {song_b['Title']}",
          key='btn_v_b',
          type='primary',
          use_container_width=True,
      ):
        bg['votes_b'] += 1
        st.toast('Głos oddany!')

    st.divider()
    tot = bg['votes_a'] + bg['votes_b']
    if tot > 0:
      p_a = int((bg['votes_a'] / tot) * 100)
      p_b = 100 - p_a
      res_text = (
          f"Wyniki: {song_a['Title']} ({p_a}%) vs {song_b['Title']} ({p_b}%)"
      )
      st.progress(p_a / 100, text=res_text)

# =============================================================================
# ZAKŁADKA 4: DODAWANIE NOWEGO UTWORU
# =============================================================================
with tab_add_custom:
  st.subheader('✨ Dodaj własną piosenkę do bazy')

  c_art = st.selectbox('Wykonawca:', df['Artist'].unique())
  c_title = st.text_input('Tytuł piosenki:')
  c_album = st.text_input('Album / Single (opcjonalnie):', 'Single')

  if st.button('✨ Dodaj piosenkę do bazy', type='primary'):
    if c_title.strip():
      new_r = pd.DataFrame([{
          'Artist': c_art,
          'Title': c_title.strip(),
          'Album': c_album.strip(),
          'Full_Name': f'{c_art} - {c_title.strip()}',
      }])
      st.session_state.db = pd.concat(
          [st.session_state.db, new_r], ignore_index=True
      )
      st.success(f'Dodano {c_art} - {c_title} do bazy!')
      st.rerun()
    else:
      st.error('Wpisz tytuł piosenki!')