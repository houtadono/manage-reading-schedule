import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.html('''
<style>
        .stMainBlockContainer, .st-key-container {
            padding:0;
        }
</style>''')
doc_id = st.session_state['current_manga']  if 'current_manga' in st.session_state else None
chapter = st.session_state['current_chapter'] if 'current_chapter' in st.session_state else None
reading_site = st.session_state['reading_site'] if 'reading_site' in st.session_state else None

if not doc_id:
    # st.warning("You have not selected a Comic to read yet.")
    pass
elif not reading_site:
    # st.warning("You have not selected a Reading Site to read yet.")
    pass
else:
    url = f'{doc_id}/chap-{chapter}' if chapter else doc_id
    url = f'{reading_site}/truyen-tranh/{url}'
    with st.container(key='container'):
        iframe_html = f'''
        <div style="position:relative;margin-top:2rem; height:120vh; z-index: 999990" >
            <button
                    style="position:absolute; z-index:1000; background-color:orange; border:none; color:white; cursor:pointer;">
                Back
            </button>
            <iframe id="myIframe" src="{url}" width="100%" height="80%" sandbox="allow-same-origin allow-scripts">
            </iframe>
        </div>
        <style>
        
        </style>
        '''
        while ( k:= streamlit_js_eval(js_expressions='screen.height')) is not None:
            st.components.v1.html(iframe_html,
                                  height=int(k * 8 / 10)
                                  , scrolling=False)
            break


