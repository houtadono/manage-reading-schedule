import pandas as pd
import streamlit as st

from manga_db import scan_preview_manga_chapter, URL_IMAGE
from utils import get_all_mangas

header_col, button_col = st.columns([2, 1])
with header_col:
    st.header("Manage Manga Reading", anchor=False)

with button_col:
    if st.button("Add Manga", icon=":material/add_circle:", type="primary", key='add_manga'):
        @st.dialog("Add Manga")
        def add_manga():
            st.html('''
            <style>
            .stHorizontalBlock:has(.st-key-btn_preview) {
                align-items: flex-end;
            }
            </style>
            ''')
            t_cols = st.columns([4,1])
            with t_cols[0]:
                new_title = st.text_input("New Manga Title")
            with t_cols[1]:
                btn_preview =  st.button("Preview", key='btn_preview')
            if btn_preview:
                cols = st.columns([2, 3], vertical_alignment='center')
                new_chapter, new_date, doc_id, title = scan_preview_manga_chapter(new_title)

                with cols[0]:
                    st.image(f'{URL_IMAGE}/{doc_id}.jpg')
                with cols[1]:
                    with st.container(height=200, border=None, key='preview_chapter_infor'):
                        st.write(f"New Chapter: :blue-background[{new_chapter}]")
                        st.write(f"Update at: :orange[{new_date}]")
                        st.write("")
                        st.write(f"Current chapter: :green[]")
                        st.button("Reset")

                new_chapter = st.number_input("New Chapter", value=1)
                if st.button("Submit"):
                    # st.session_state.db.add_manga(new_title, new_dates, new_chapter)
                    st.rerun()

        add_manga()

with st.spinner('Loading search'):
    st.html('''
            <style>
            .stHorizontalBlock:has(.st-key-add_manga) {
                align-items: baseline;
            }
            .stSidebar {z-index:999993;}
            .stVerticalBlock {gap:0;}
            .stVerticalBlock .stVerticalBlock{gap:1rem;}
            .stMainBlockContainer{
                padding-top: 3rem;
            } 
            .st-key-search .stTextInput {height:0;}
            .st-key-search div[data-testid="stTextInputRootElement"] {
                position: fixed;
                top: 1rem;
                z-index: 999992;
                width: 45%;
            }
            .st-key-search div[data-testid="stTextInputRootElement"] input {
                background-color: #adc8c873;
            }
    
            div[data-testid="stVerticalBlockBorderWrapper"] {
                padding: 0;
                width: 100%;
                overflow: hidden;
            }       
            div[role="dialog"] div[data-testid="stVerticalBlockBorderWrapper"] {
                border: none;
            }
            /* dialog */
            div[role="dialog"] .stColumn {
                min-width: 0;
                align-items: center;
                margin-top: 0;
            }
            div[role="dialog"] .stColumn button {
                padding: 6px;
                width: 100%;
            }
            div[role="dialog"] div[data-testid="stImageContainer"] {
                align-items: center;
            }
            div[role="dialog"] img {
                height: 220px;
                margin: 0 90px;
            }
    
            button[title="View fullscreen"]{
                visibility: hidden;
            }
            @media screen and (max-width: 768px) {
                .st-key-search div[data-testid="stTextInputRootElement"] {
                    left: 75px;
                }
                div[role="dialog"] img {
                    height: 180px;
                    margin: 0 60px;
                }
            }
            .stImage, .stElementContainer, .stButton, .stMarkdown {
                width: auto !important;
            }
            </style>
    ''')
    search_query = st.text_input("Search", label_visibility="hidden",placeholder="Search...", value="", key='search')

@st.dialog("Update Manga")
def update_manga(index: str):
    selected_manga = st.session_state['mangas'][index]
    title = st.text_input("Title", value=selected_manga["Title"])
    dates = st.multiselect("Dates (Select multiple)", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], default=selected_manga["Date"])
    chapter = st.number_input("Chapter", value=selected_manga["Chapter"])

    if st.button("Submit", type='primary'):
        st.session_state.db.update_manga(index, title, dates, chapter)
        st.rerun()

    if st.button("Delete"):
        st.session_state.db.delete_manga(index)
        st.rerun()

with st.spinner('Loading mangas'):
    if 'mangas' not in st.session_state:
        st.session_state.mangas = get_all_mangas()

if not search_query:
    filtered_mangas = st.session_state['mangas']
else:
    filtered_mangas = {doc_id: manga for doc_id, manga in st.session_state['mangas'].items() if search_query.lower() in manga["Title"].lower()}

filtered_mangas = sorted(filtered_mangas.items())
home, follow, history = st.tabs(["Home", "Follow", "History"])

MANGA_PER_PAGE = 8

def show_list_manga(tab_name):
    num_columns = 2
    lst_manga = filtered_mangas[(st.session_state.page_number-1) * MANGA_PER_PAGE: st.session_state.page_number * MANGA_PER_PAGE]

    for i in range(0, len(lst_manga), num_columns):
        cols = st.columns(num_columns)
        for j in range(num_columns):
            if i + j < len(lst_manga):
                with cols[j]:
                    st.html(f'''
                    <style>
                    .st-key-{tab_name}container{i + j}1 {{
                        gap: 4px !important;
                        padding: 0;
                        display: flex;
                        flex-direction: row;
                        justify-content: flex-start;
                    }}
                    

                    .st-key-{tab_name}container{i + j}1 img {{
                        height: 100px !important;
                        max-width: 72px !important;
                    }}

                    .st-key-{tab_name}container{i + j}1 button {{
                        border: none !important;
                        background: none !important;
                    }}
                    .st-key-{tab_name}container{i + j}2 {{
                        height: 100px !important;
                        padding:0;
                        display: flex;
                        gap: 0 !important;
                        flex-direction: column;
                        justify-content: space-around;
                    }}
                    .st-key-{tab_name}container{i + j}3 > .stElementContainer > .stButton > button {{
                        padding: 0;
                        text-align: left;
                        overflow: hidden;
                    }}

                    .st-key-{tab_name}container{i + j}3 > .stElementContainer > .stButton > button p {{
                        font-size: 16px;
                        font-weight: bold;
                        font-family:  sans-serif, system-ui;
                    }}
                    
                    .st-key-{tab_name}container{i + j}1 > div[data-testid="stVerticalBlockBorderWrapper"] > div:first-child {{
                        height:100%;
                    }}
                    .st-key-{tab_name}container{i + j}3, .st-key-{tab_name}container{i + j}4 {{
                        padding:0;
                        overflow: hidden;
                        flex-shrink: 1;
                        display: flex;
                        flex-direction: row;
                        align-items: center;
                    }}
                    .st-key-{tab_name}container{i + j}3 {{
                        justify-content: space-between;
                        padding-right: 10px;
                    }}
                    .st-key-{tab_name}container{i + j}4 {{
                        justify-content: space-between;
                    }}
                    </style>''')
                    doc_id, manga = lst_manga[i + j]
                    with st.container(border=True, key=f'{tab_name}container{i + j}1', height=100):
                        st.image(manga['Image'])
                        with st.container(key=f'{tab_name}container{i + j}2'):
                            with st.container(key=f'{tab_name}container{i + j}3'):
                                if st.button(manga['Title'], key=f'{tab_name}btn-{i + j}-1'):
                                    @st.dialog(title=f"Truyện tranh: {manga['Title']}")
                                    def open_manga_dialog():
                                        cols = st.columns([2,3], vertical_alignment='center')
                                        scaner = st.session_state.db.scan_manga(doc_id, all_chapter=True)
                                        new_chapter, new_date = next(scaner)

                                        with cols[0]:
                                            st.image(manga['Image'])
                                        with cols[1]:
                                            with st.container(height=200, border=None, key='chapter_infor'):
                                                st.write(f"New Chapter: :blue-background[{new_chapter}]")
                                                st.write(f"Update at: :orange[{new_date}]")
                                                st.write("")
                                                st.write(f"Current chapter: :green[{manga['Chapter']}]")
                                                st.button("Reset")

                                        button_placeholder = st.empty()
                                        table_placeholder = st.empty()
                                        scaner = st.session_state.db.scan_manga(doc_id, all_chapter=True)
                                        new_chapter, new_date = next(scaner)
                                        if new_chapter:
                                            with button_placeholder:
                                                row2 = st.columns([2.2, 2.5, 2])
                                                row2[0].button("Đọc từ đầu")
                                                row2[1].button("Đọc mới nhất")
                                                row2[2].button("Đọc tiếp", type='primary')

                                            with table_placeholder:
                                                data = next(scaner)
                                                df = pd.DataFrame(data)
                                                st.data_editor(df, width=1000, hide_index=True)

                                    open_manga_dialog()
                                    # st.session_state['current_manga'] = doc_id
                                    # st.session_state['current_chapter'] = None
                                    # st.switch_page('app_pages/read.py')

                                if st.button("", icon=":material/cached:", key=f'{tab_name}btn-{i + j}-2'):
                                    toast = st.toast(f"**Scan:** {manga['Title']}")
                                    st.session_state.db.scan_manga(doc_id)

                            with st.container(key=f'{tab_name}container{i + j}4'):
                                st.write(f"Chap {manga['Chapter']}")
                                if st.button("Edit", icon=":material/edit:", key=f'{tab_name}btn-{i + j}-3'):
                                    update_manga(doc_id)

                                if st.button("Read", key=f'{tab_name}btn-{i + j}-4'):
                                    st.session_state['current_manga'] = doc_id
                                    st.session_state['current_chapter'] = manga['Chapter']
                                    st.switch_page('app_pages/read.py')

# footer
with st.container(key='footer'):
    st.html('''
    <style>
    .st-key-footer {
        margin-top: 1rem;
        flex-direction: row;
        justify-content: space-between;
    }
    .st-key-footer .stRadio{
        width: auto!important;
    }
    .st-key-footer button{
        width: 100%;
    }
    .st-key-footer div[role="radiogroup"] {
        flex-direction: row;
        flex-wrap: nowrap;
    }
    .st-key-footer label[data-baseweb="radio"] {
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
        border: 1px solid rgba(250, 250, 250, 0.2);
    }
    .st-key-footer label[data-baseweb="radio"]:has(input[tabindex="0"]) {
        background-color: red;
    }
    .st-key-footer label[data-baseweb="radio"]:hover {
        border-color: rgb(255, 75, 75);
    }
    .st-key-footer label[data-baseweb="radio"] div:first-child {
        width: 0;
        margin:0;
    }
    .st-key-footer label[data-baseweb="radio"]:last-child {
        margin-right: 0;
    }
    .st-key-footer div[role="radiogroup"] div[data-testid="stMarkdownContainer"] {
        padding-right: 16px;
    }
    .st-key-page_number {
        position: absolute;
        top: 2px;
        left: 50%;
        transform: translateX(-50%);
    }
    </style>
    ''')

    last_page = int((len(filtered_mangas)-1)//MANGA_PER_PAGE)+ 1
    if last_page > 9:
        last_page = 9
        MANGA_PER_PAGE = len(filtered_mangas)//last_page + 1

    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1

    if st.button("", icon=':material/chevron_left:'):
        if st.session_state.page_number - 1 < 1:
            st.session_state.page_number = 1
        else:
            st.session_state.page_number -= 1

    if st.button("", icon=':material/chevron_right:'):
        if st.session_state.page_number + 1 > last_page:
            st.session_state.page_number = last_page
        else:
            st.session_state.page_number += 1

    st.radio(
        "Choose Option",
        list(range(1, last_page+1)),
        key='page_number',
        label_visibility='collapsed',
    )

with home:
    with st.spinner('Show mangas'):
        show_list_manga(tab_name='home')

with follow:
    with st.spinner('Show mangas 1'):
        filtered_mangas =  filtered_mangas[:4]
        show_list_manga(tab_name='follow')