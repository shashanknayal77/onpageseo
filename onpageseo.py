import streamlit as st
import requests
from bs4 import BeautifulSoup
import trafilatura
import re

st.title("On-Page SEO Analysis")

url = st.text_input("Enter a URL")

def validate_url(url):
    url_pattern = re.compile(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+")
    return bool(url_pattern.match(url))

if url!="":
    if not validate_url(url):
        st.error("Please enter a valid URL")
    else:
        def get_title(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string
                return title
            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL: {e}")
            except AttributeError:
                print("Title tag not found")
            return None

        title = get_title(url)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("**Title**")
        with col2:
            st.write(f"{title}")
        if title is not None:
                st.write(f"{len(title)} characters")

        # st.markdown("---")
        def find_meta_description(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                meta_description_tag = soup.find('meta', attrs={'name': 'description'})
                if meta_description_tag:
                    content = meta_description_tag.get('content', '')
                    return content
                else:
                    return 0
            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL: {e}")
                return None
            
        meta= find_meta_description(url)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("**Meta Description**")
        with col2:
            st.write(f"{meta}")
        if meta is not None:
            st.write(f"{len(meta)} characters")

        # st.markdown("---")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("**Url**")
        with col2:
            st.write(f"{url}")
        # st.markdown("---")    
        def canonical_tag(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                canonical_tags = soup.find('link', rel='canonical')
                return canonical_tags
            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL: {e}")
                return None

        canonical_tag = canonical_tag(url)
        if canonical_tag is not None:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader("**Canonical**")
            with col2:
                st.write(f"{canonical_tag.get('href')}")
        else:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader("**Canonical**")
            with col2:
                st.write(f"Not Specified")
        def check_lang_tag(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                html_tag = soup.find('html')
                lang_attribute = html_tag.get('lang') if html_tag else None
                return lang_attribute
            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL: {e}")
                return None

        has_lang_tag = check_lang_tag(url)
        if has_lang_tag is not None:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader("**Lang**")
            with col2:
                st.write("This page has lang tag")
        else:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader("**Lang**")
            with col2:
                st.write(f"Not Specified")

        def check_meta_robots(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                meta_robots_tag = soup.find('meta', attrs={'name': 'robots'})
                print(meta_robots_tag)
                if meta_robots_tag:
                    return meta_robots_tag.get('content', '')
                else:
                    return None
            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL: {e}")
                return None
        robots_content = check_meta_robots(url)
        if robots_content is not None:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader("**Meta Robots**")
            with col2:
                st.write(f"{robots_content}")
        else:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader("**Meta Robots**")
            with col2:
                st.write(f"Not Specified")
        st.subheader("Header Tags Analysis")
        def check(url,tag):
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                heading_tags = soup.find_all(tag)
                return heading_tags
            except requests.RequestException as e:
                print(f"Failed to fetch {url}: {e}")

        h1_tag=check(url,'h1')
        h2_tag=check(url,'h2')
        h3_tag=check(url,'h3')
        h4_tag=check(url,'h4')
        h5_tag=check(url,'h5')
        h6_tag=check(url,'h6')
        col1,col2,col3,col4,col5,col6= st.columns([1,1,1,1,1,1])
        with col1:
            st.subheader("_h1_")
            st.write(f"{len(h1_tag)}")
        with col2:
            st.subheader("_h2_")
            st.write(f"{len(h2_tag)}")
        with col3:
            st.subheader("_h3_")
            st.write(f"{len(h3_tag)}")
        with col4:
            st.subheader("_h4_")
            st.write(f"{len(h4_tag)}")
        with col5:
            st.subheader("_h5_")
            st.write(f"{len(h5_tag)}") 
        with col6:
            st.subheader("_h6_")
            st.write(f"{len(h6_tag)}")  
        def count_total_words(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()
                words = re.findall(r'\b\w+\b', text.lower())
                return len(words)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL: {e}")
                return None

        total_words = count_total_words(url)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("**Word Count**")
        with col2:
            st.write(f"{total_words}")
        def check_alt_tags(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                img_tags = soup.find_all('img')
                count = sum(1 for img_tag in img_tags if not img_tag.get('alt'))
                return count
            except requests.RequestException as e:
                print(f"Failed to fetch {url}: {e}")
                return None

        alt_tag_count = check_alt_tags(url)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("**Images without alt attributes**")
        with col2:
            st.write(f"{alt_tag_count}")
        # st.markdown("---")
        # st.subheader("Robots.txt Analysis")
        def check_robots_txt(url):
            robots_url = url + '/robots.txt'
            try:
                robots_txt = trafilatura.fetch_url(robots_url)
                if robots_txt:
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.subheader("**Robots.txt**")
                    with col2:
                        st.write(f"{robots_url}")
                elif url!="":
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.subheader("**Robots.txt**")
                    with col2:
                        st.write(f"Not Specified")
            except requests.exceptions.RequestException as e:
                print("Error:", e)

        check_robots_txt(url)
        def check_sitemap(url):
            sitemap_url = url + '/sitemap.xml'
            try:
                sitemap = trafilatura.fetch_url(sitemap_url)
                if sitemap:
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.subheader("**Sitemap.xml**")
                    with col2:
                        st.write(f"{sitemap_url}")
                elif url!="":
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.subheader("**Sitemap.xml**")
                    with col2:
                        st.write(f"Not Specified")
            except requests.exceptions.RequestException as e:
                print("Error:", e)

        check_sitemap(url)
        # st.subheader("Text to HTML Ratio Analysis")
        def get_text_to_html_ratio(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                text_length = len(soup.get_text())
                html_length = len(response.text)
                ratio = text_length / html_length
                return ratio*100
            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL: {e}")
                return None

        text_to_html_ratio = get_text_to_html_ratio(url)
        # if text_to_html_ratio is not None:
        #     st.write(f"Text to HTML ratio for {url}: {text_to_html_ratio:.2f}")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("**Text To Html Ratio**")
        with col2:
            st.write(f"{text_to_html_ratio:.2f}")
        # st.markdown("---")
        # st.subheader("URL Length Analysis")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("**Url length**")
        with col2:
            st.write(f"{len(url)}")
else:
    st.info("Enter a URL to analyze")
