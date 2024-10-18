import streamlit as st
from manga_db import MangaDB

firebase_key_path = st.secrets["textkey"]
manga_db = MangaDB(firebase_key_path)

st.header("Manage Manga Reading")

search_query = st.text_input("Search Manga by Title", value="")
st.session_state['mangas'] = manga_db.get_all_mangas()

if not search_query:
    filtered_mangas = st.session_state['mangas']
else:
    filtered_mangas = {doc_id: manga for doc_id, manga in st.session_state['mangas'].items() if search_query.lower() in manga["Title"].lower()}

num_cols = 6

cols = st.columns(num_cols)
headers = ["Title", "Date", "Link", "Actions", "", "Chapter"]
for col, header in zip(cols, headers):
    col.write(header)

@st.dialog("Update Manga")
def update_manga(index: str):
    selected_manga = st.session_state['mangas'][index]
    title = st.text_input("Title", value=selected_manga["Title"])
    dates = st.multiselect("Dates (Select multiple)", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], default=manga["Date"])
    link = st.text_input("Link", value=selected_manga["Link"])
    chapter = st.number_input("New Chapter", value=selected_manga["Chapter"])

    if st.button("Submit"):
        manga_db.update_manga(index, title, dates, link, chapter)
        st.session_state['mangas'] = manga_db.get_all_mangas()
        st.rerun()

for doc_id, manga in filtered_mangas.items():
    cols = st.columns(num_cols)
    cols[0].write(manga["Title"])
    cols[1].write(', '.join(manga["Date"]))
    cols[2].write(manga["Link"])


    if cols[3].button("Edit", key=f"edit_{doc_id}", icon=":material/edit:"):
        update_manga(doc_id)

    if cols[4].button("Delete", key=f"delete_{doc_id}", icon=":material/delete:"):
        manga_db.delete_manga(doc_id)
        del st.session_state['mangas'][doc_id]  # Xóa manga khỏi session state
        st.rerun()

    cols[5].subheader(manga["Chapter"])

# Nút thêm manga mới
if st.button("Add Manga", icon=":material/add_circle:"):
    @st.dialog("Add Manga")
    def add_manga():
        new_title = st.text_input("New Manga Title")
        new_dates = st.multiselect("Dates (Select multiple)",
                                   ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        new_link = st.text_input("New Link")
        new_chapter = st.number_input("New Chapter", value=1)
        if st.button("Submit"):
            manga_db.add_manga(new_title, new_dates, new_link, new_chapter)
            st.session_state['mangas'] = manga_db.get_all_mangas()

            st.rerun()
    add_manga()