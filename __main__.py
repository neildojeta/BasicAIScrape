import streamlit as st
import asyncio

from scrape import (
    scrape_website,
    split_dom_content,
    clean_body_content,
    extract_body_content,
)

from parse import parse_with_ollama

# Streamlit App
def main():
    st.title("Web Scraping App")
    
    # Input for URL
    url = st.text_input("Enter the URL of the website you want to scrape", "")
    
    # Button to start scraping
    if st.button("Scrape Website"):
        if url:
            st.write("Scraping the Website")

            result = scrape_website(url)
            body_content = extract_body_content(result)
            cleaned_content = clean_body_content(body_content)

            st.session_state.dom_content = cleaned_content

            with st.expander("View DOM Content"):
                st.text_area("DOM Content", cleaned_content, height=300)
        else:
            st.warning("Please enter a URL!")
    
    if "dom_content" in st.session_state:
        parse_description = st.text_area("Describe what you want to parse?")

        if st.button("Parse Content"):
            if parse_description:
                st.write("Parsing the content")

                dom_chunks = split_dom_content(st.session_state.dom_content)
                result = parse_with_ollama(dom_chunks, parse_description)
                # result = asyncio.run(parse_with_ollama(dom_chunks, parse_description))
                st.write(result)

if __name__ == '__main__':
    main()