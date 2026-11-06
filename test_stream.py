import streamlit as st

st.title("✅ Streamlit is Working!")
st.write("If you can see this in your browser, your installation is successful.")

name = st.text_input("Enter your name:")
if name:
    st.success(f"Hello, {name}! Streamlit is running perfectly. 🎉")

st.sidebar.header("Test Sidebar")
st.sidebar.write("This is a sidebar test.")