import streamlit as st

# The station labels in language 'en' and 'sp'
stations = {"en": ['en_A', 'en_B'],
            "sp": ['sp_A', 'sp_B']}


# Function for the form submit button - to show what was selected
def form_callback():
    st.title("Form submitted")
    st.write(st.session_state.station_selector)


# Buttons on the sidebar for language selection
with st.sidebar:
    st.header("Select language:")
    st.button(label='EN', key='en')
    st.button(label='SP', key='sp')

# The form changes depending on the language
with st.form(key='map_properties'):
    if st.session_state.sp:
        station_choice = stations["sp"]
    else:
        station_choice = stations["en"]

    st.multiselect(
        label='ams_selector',
        options=station_choice,
        default=station_choice,
        key='station_selector'
    )

    submit_button = st.form_submit_button(label="Submit", on_click=form_callback)

# Display the session state for debugging purposes
st.header("Session State Variables:")
st.write(st.session_state)