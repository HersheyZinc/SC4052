import streamlit as st
import github_api
import utils


st.set_page_config(layout="wide")

# intialize empty variables
if "search_results" not in st.session_state:
    st.session_state["search_results"] = []

# Web app elements
st.title("CCDS Repository Finder")
search_container = st.container()
results_container = st.container()


with search_container:
    if query := st.chat_input("Type in a CCDS course code. E.g. SC4052"):
        st.session_state["search_results"] = []

        # Search GitHub
        results = github_api.search_github(query, num_requests=20)
        # Check for old/alternate course codes
        query = query.lower()
        if query.startswith("sc"):
            results += github_api.search_github(query.replace("sc", "cz"), num_requests=5)
        if query.startswith("ce"):
            results += github_api.search_github(query.replace("sc", "ce"), num_requests=5)

        # Get information and summary for each result
        for r in results:
            summary = github_api.get_repo_summary(r["full_name"])
            # Skip result if no summary fond
            if not summary: continue
            created_date = utils.get_month_year(r["created_at"])
            url = "https://github.com/" + r["full_name"]
            owner = r["owner"]["login"]
            repo_name = r["name"]
            
            # Store results
            st.session_state["search_results"].append({"created_date": created_date, "url":url, "repo_name":repo_name,"owner":owner,"summary":summary})

            # Dynamically show result to results page
            with results_container:
                with st.container(border=True):
                    st.subheader(repo_name)
                    st.write(f"Owner: {owner} | Created: {created_date} | url: {url}")
                    st.write("Summary:")
                    st.write(summary)

# Reshow stored results if page is refreshed
with results_container:
    for r in st.session_state["search_results"]:
        with st.container(border=True):
            st.subheader(r["repo_name"])
            st.write(f"Owner: {r["owner"]} | Created: {r['created_date']} | url: {r['url']}")
            st.write("Summary:")
            st.write(r["summary"])