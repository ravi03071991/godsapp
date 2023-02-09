import streamlit as st
import pinecone
import utils

pinecone.init(api_key=utils.pinecone_api_key,
              environment=utils.pinecone_environment)

st.set_page_config(page_title="GodsAPP",
                   page_icon=":guardsman:", layout="wide")
st.header("GodsAPP")
st.write("GodsAPP will give answers based on Bhagwad Gita, Quran and Bible for your situation")

tab1, tab2, tab3 = st.tabs(["Bhagwad Gita", "Quran", "Bible"])

with tab1:
    st.header("Bhagwad Gita")
    title = st.text_input(
        'Enter Your Situation for Bhagwad Gita to suggest a solution')
    if st.button('Ask Gita'):
        st.write("Bhagwad Gita is thinking. Please wait.")
        answer = utils.qa("gita", title)
        answer, relevantverses = answer.split("----------------")
        st.subheader('Answer')
        st.write(answer)
        st.subheader('Relevant Verses')
        st.write(relevantverses)

with tab2:
    st.header("Quran")
    title = st.text_input(
        'Enter Your Situation for Quran to suggest a solution')
    if st.button('Ask Quran'):
        st.write("Quran is thinking. Please wait.")
        answer = utils.qa("quran", title)
        answer, relevantverses = answer.split("----------------")
        st.subheader('Answer')
        st.write(answer)
        st.subheader('Relevant Verses')
        st.write(relevantverses)

with tab3:
    st.header("Bible")
    title = st.text_input(
        'Enter Your Situation for Bible to suggest a solution')
    if st.button('Ask Bible'):
        st.write("Bible is thinking. Please wait.")
        answer = utils.qa("bible", title)
        answer, relevantverses = answer.split("----------------")
        st.subheader('Answer')
        st.write(answer)
        st.subheader('Relevant Verses')
        st.write(relevantverses)
