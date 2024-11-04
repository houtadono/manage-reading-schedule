import streamlit as st
from utils import load_cache, get_trans

st.set_page_config(layout="wide")
load_cache()

with st.sidebar:
    if 'lang' not in st.session_state:
        st.session_state.lang = "Tiếng Việt"
    with st.expander(
            f"{st.session_state.translations[st.session_state['lang']]['lang_label']}: :rainbow[**{st.session_state.lang}**]"):
        lang_option = st.radio(
            "Choose Option",
            ["English", "Tiếng Việt"],
            horizontal=True,
            key='lang',
            label_visibility='collapsed',
        )

st.html('''
<style>
.stPopover{
    position: fixed;
    top: 1rem;
    z-index: 999990;
    right: 3rem;
    height: 3.75rem;
}
.stPopover button {
    border: none;
    margin-right: 1rem;
    background: none;
    padding: 0;
}
div[aria-expanded="true"] button{
    background: rgb(255, 75, 75);
}
div[aria-expanded="true"] svg{
    color: white;
}
.stPopover button:active {
    background: none;
}
div[data-baseweb="popover"]{
    overflow-y: scroll;
}
</style>
''')
# Danh sách thông báo giả lập
notifications = [
    "Thông báo 1: Hệ thống sẽ bảo trì lúc 10:00.",
    "Thông báo 2: Có cập nhật mới cho ứng dụng.",
    "Thông báo 3: Hãy kiểm tra lại dữ liệu của bạn."
]

with st.popover("🔔", use_container_width=True):
    for notification in notifications:
        st.write(f"- {notification}")
    for notification in notifications:
        st.write(f"- {notification}")
    for notification in notifications:
        st.write(f"- {notification}")
    for notification in notifications:
        st.write(f"- {notification}")

# home = st.Page("pages/home.py", title="Home", icon=":material/home:", default=True)
# read = st.Page("pages/read.py", title="Reading", icon=":material/book:")
# test = st.Page("pages/test_page.py", title="Test", icon=":material/book:")
# setting = st.Page("pages/setting.py", title="Setting", icon=":material/settings:")
#
# pg = st.navigation({
#     f"{get_trans('page/home')}": [home],
#     f"{get_trans('page/read')}": [read, test],
#     f"{get_trans('page/setting')}": [setting],
# })
st.html( """
    <style>
    .stAppDeployButton {
            visibility: hidden;
        }
    </style>
    """
)
home = st.Page("app_pages/home.py", title=get_trans('page/home'), icon=":material/home:", default=True)
read = st.Page("app_pages/read.py", title=get_trans('page/read'), icon=":material/book:")
test = st.Page("app_pages/test_page.py", title="Test", icon=":material/book:")
setting = st.Page("app_pages/setting.py", title=get_trans('page/setting'), icon=":material/settings:")

pg = st.navigation([home, read, test, setting])

pg.run()
