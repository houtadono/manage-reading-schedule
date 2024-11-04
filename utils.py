from datetime import datetime, timedelta
import streamlit as st
import json
from functools import reduce
from manga_db import MangaDB

@st.cache_resource
def initialize_db():
    cred, options = json.loads(st.secrets["cred"]), json.loads(st.secrets["options"])
    return MangaDB(cred, options)


@st.cache_data
def get_all_mangas():
    db = initialize_db()
    return db.get_all_mangas()

@st.cache_data
def get_site():
    db = initialize_db()
    return db.get_reading_site(), db.get_scan_site()

@st.cache_data
def load_translations(file_path='translations.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_trans(key):
    keys = key.split('/')
    try:
        return reduce(lambda d, k: d[k], keys, st.session_state.translations[st.session_state['lang']])
    except KeyError:
        return None


def load_cache():
    st.session_state.translations = load_translations()
    with st.spinner('Loading database'):
        st.session_state.db = initialize_db()

    # def check_time_difference():
    #     db = initialize_db()
    #     current_time = datetime.now().strftime("%d/%m/%Y %H:00:00")
    #
    #     time_last = db.get_time_last()
    #     time_last_dt = datetime.fromtimestamp(time_last)
    #     current_time = datetime.now()
    #     return (current_time - time_last_dt) > timedelta(hours=1)

    with st.spinner('Loading site'):
        sites = get_site()
        st.session_state.reading_site, st.session_state.scan_site = sites


