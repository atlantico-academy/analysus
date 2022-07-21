import streamlit as st


def home():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##")
        st.subheader(f"Predição de Internações SUS")

    with col2:
        st.image('src/view/assets/image/header.png', width = 250)

    st.image('src/view/assets/image/logo2.png', width = 200)
