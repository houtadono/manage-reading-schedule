import streamlit as st
from manga_db import MangaDB
from utils import initialize_db

db = initialize_db()

sites, sites_with_dates = db.get_all_sites()
if not sites:
    st.warning("Không có site nào được lưu trong Firestore.")
else:
    cols = st.columns(3)
    for i, title in enumerate(["Site", "Date", ""]):
        cols[i].write(title)
    for site, date in sites_with_dates:
        cols = st.columns(3)
        cols[0].write(site)
        cols[1].write(date)
        if cols[2].button("Delete", key=f"delete_{site}", icon=":material/delete:"):
            db.delete_site(site)
            if 'reading_site' in st.session_state and st.session_state['reading_site'] == site:
                db.save_reading_site(None)
                st.session_state.reading_site = None
            if 'scan_site' in st.session_state and st.session_state['scan_site'] == site:
                db.save_scan_site(None)
                st.session_state.scan_site = None
            st.rerun()

    rs = st.session_state.reading_site
    reading_site = st.selectbox("Reading Site:", sites, index=sites.index(rs) if rs in sites else None)

    ss = st.session_state.scan_site
    scan_site = st.selectbox("Scan Site:", sites, index=sites.index(ss) if ss in sites else None)

    if st.button("Save"):
        db.save_reading_site(reading_site)
        db.save_scan_site(scan_site)
        st.session_state.reading_site = reading_site
        st.session_state.scan_site = scan_site

if st.button("Add Link", icon=":material/add_circle:"):
    @st.dialog("Add site")
    def add_site(item):
        new_site = st.text_input("Nhập site mới:")
        if st.button("Submit Link"):
            new_site = new_site.rstrip('/')
            if new_site:
                db.add_site(new_site)
                st.toast('Your edited image was saved!', icon='😍')
                st.rerun()
            else:
                st.warning("Vui lòng nhập một site hợp lệ.")

    add_site(1)