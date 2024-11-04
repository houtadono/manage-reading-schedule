import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup

from app_pages.setting import title


@st.dialog('Test')
def test_dialog():
    st.write('This is a test dialog')
    a = scan_manga_chapter('https://nettruyenviet.com/truyen-tranh/ban-hoc-cua-toi-la-linh-danh-thue')


st.html('''
<style>
.stColumn {
    min-width: 0;
    align-items: center;
}
.stColumn button {
    padding: 6px;
    width: 100%;
}
</style> 
''')


import streamlit as st
import json


@st.cache_data
def load_translations(file_path='translations.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# st.session_state.translations = load_translations()

# with st.sidebar:
#     if 'lang' not in st.session_state:
#         st.session_state.lang = 'Tiếng Việt'
#     with st.expander(
#             f"{st.session_state.translations[st.session_state['lang']]['lang_label']}: :rainbow[**{st.session_state.lang}**]"):
#         lang_option = st.radio(
#             "Choose Option",
#             ["English", "Tiếng Việt"],
#             horizontal=True,
#             key='lang',
#             label_visibility='collapsed',
#         )

        # if lang_option == "English":
        #     st.session_state['lang'] = 'en'
        # else:
        #     st.session_state['lang'] = 'vi'

st.title(st.session_state.translations[st.session_state['lang']]['welcome'])
st.write(st.session_state.translations[st.session_state['lang']]['greeting'])
st.button(st.session_state.translations[st.session_state['lang']]['submit'])

if st.button('start'):
    # test_dialog()
    @st.dialog(f"{st.session_state['lang']}")
    def test_dialog():
        st.write('This is a test dialog')
        a = scan_manga_chapter('https://nettruyenviet.com/truyen-tranh/ban-hoc-cua-toi-la-linh-danh-thue')


    test_dialog()



# Tạo nút chuông
st.html('''
<style>
.stPopover{
    position: fixed;
    top: 1.25rem;
    z-index: 999990;
    right: 3rem;
    height: 3.75rem;
}
.stPopover button {
    border: none;
    margin-right: 1rem;
    background: none;
}
div[data-baseweb="popover"]{
    overflow-y: scroll;
}
</style>
''')

count_page = 6

prev, cols ,next = st.columns([1, count_page, 1])
last_page = 10
st.session_state.page_number= 0
if next.button("", icon=':material/chevron_right:'):
    if st.session_state.page_number + 1 > last_page:
        st.session_state.page_number = 0
    else:
        st.session_state.page_number += 1
with cols:
    for index, i in enumerate(st.columns(count_page)):
        i.button(f"{index}")

if prev.button("", icon=':material/chevron_left:'):

    if st.session_state.page_number - 1 < 0:
        st.session_state.page_number = last_page
    else:
        st.session_state.page_number -= 1