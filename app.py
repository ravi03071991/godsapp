import streamlit as st
import openai

st.set_page_config(page_title="Headline Generation",
                   page_icon=":guardsman:", layout="wide")
st.header("Headline Generation")
st.write("This app will generate headlines based on text with limits on number of characters and words you need in the headline.")


def generate(text, num_chars, num_words):

    openai.api_key = "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"
    query = f"Generate a news headline that will attract users attention strict to maximum of {num_chars} characters and {num_words} words without : based on the context of the following text. Don't hallicunate."

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=query + "\n\n" + text + "\n\n",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    if response['choices'][0]["text"] != '':
        return response['choices'][0]["text"]

    return text


text = st.text_input(
    'Enter Your Text', max_chars=1000)
charlimit = st.text_input(
    'Enter Number of Characters')
wordlimit = st.text_input(
    'Enter Number of Words Text')
if st.button('Submit'):
    st.write("Processing. Please wait.")
    answer = generate(text, charlimit, wordlimit)
    st.subheader('Generated Headline')
    st.write(answer)
