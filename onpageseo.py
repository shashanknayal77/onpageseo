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
        st.markdown("---")
        st.subheader("Title Analysis")
        def get_title_length(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string
                return len(title)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL: {e}")
            except AttributeError:
                print("Title tag not found")
            return None

        title_length = get_title_length(url)
        if title_length is not None:
                st.write(f"Title length of {url}: {title_length}")

        st.markdown("---")
        st.subheader("Meta Description Analysis")
        def find_meta_description_length(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                meta_description_tag = soup.find('meta', attrs={'name': 'description'})
                if meta_description_tag:
                    content = meta_description_tag.get('content', '')
                    return len(content)
                else:
                    return 0

            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL: {e}")
                return None

        length = find_meta_description_length(url)
        if length is not None:
            st.write(f"Meta description tag length: {length}")

        st.markdown("---")
        st.subheader("Canonical Tags Analysis")
        def count_canonical_tags(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                canonical_tags = soup.find_all('link', rel='canonical')

                return len(canonical_tags)

            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL: {e}")
                return None

        canonical_tag_count = count_canonical_tags(url)
        if canonical_tag_count is not None:
            st.write(f"Number of canonical tags: {canonical_tag_count}")

        st.markdown("---")
        st.subheader("Language Tag Analysis")
        def check_lang_tag(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                html_tag = soup.find('html')
                lang_attribute = html_tag.get('lang') if html_tag else None
                return lang_attribute is not None
            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL: {e}")
                return None

        has_lang_tag = check_lang_tag(url)
        if has_lang_tag is not None:
            if has_lang_tag:
                st.write("The webpage is using the lang tag.")
            else:
                st.write("The webpage is not using the lang tag.")

        st.markdown("---")
        st.subheader("Header Tags Analysis")
        def find_all_header_tags(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                header_counts = {'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0, 'h5': 0, 'h6': 0}
                for header_level in header_counts.keys():
                    header_tags = soup.find_all(header_level)
                    header_counts[header_level] = len(header_tags)
                return header_counts

            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL: {e}")
                return None

        header_counts = find_all_header_tags(url)
        if header_counts is not None:
            for header_level, count in header_counts.items():
                st.write(f"Number of {header_level} tags: {count}")

        st.markdown("---")
        st.subheader("Alt Tags Analysis")
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
        if alt_tag_count is not None:
            st.write(f"Number of img tags without alt attribute: {alt_tag_count}")

        st.markdown("---")
        st.subheader("Robots.txt Analysis")
        def check_robots_txt(url):
            robots_url = url + '/robots.txt'
            try:
                robots_txt = trafilatura.fetch_url(robots_url)
                if robots_txt:
                    st.write("robots.txt file found on the website.")
                elif url!="":
                    st.write("robots.txt file not found on the website.")
            except requests.exceptions.RequestException as e:
                print("Error:", e)

        check_robots_txt(url)

        st.markdown("---")
        st.subheader("Sitemap.xml Analysis")
        def check_sitemap(url):
            sitemap_url = url + '/sitemap.xml'
            try:
                sitemap = trafilatura.fetch_url(sitemap_url)
                if sitemap:
                    st.write("sitemap.xml file found on the website.")
                elif url !="":
                    st.write("sitemap.xml file not found on the website.")
            except requests.exceptions.RequestException as e:
                print("Error:", e)

        check_sitemap(url)

        st.markdown("---")
        st.subheader("Text to HTML Ratio Analysis")
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
        if text_to_html_ratio is not None:
            st.write(f"Text to HTML ratio for {url}: {text_to_html_ratio:.2f}")

        st.markdown("---")
        st.subheader("URL Length Analysis")
        st.write(f"The length of URL is {len(url)}")
else:
    st.info("Enter a URL to analyze")
