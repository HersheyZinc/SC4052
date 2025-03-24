import streamlit as st
import github_api
import utils


st.set_page_config(layout="wide")

if "search_results" not in st.session_state:
    st.session_state["search_results"] = []


st.title("GitHub Repository Aggregator")

search_container = st.container()
results_container = st.container()


with search_container:
    if query := st.chat_input("Type in a search query."):
        st.session_state["search_results"] = []
        results = github_api.search_github(query, num_requests=30)

        for r in results:
            summary = github_api.get_repo_summary(r["full_name"])
            if not summary: continue
            created_date = utils.get_month_year(r["created_at"])
            url = r["url"]
            owner = r["owner"]["login"]
            repo_name = r["name"]
            

            st.session_state["search_results"].append({"created_date": created_date, "url":url, "repo_name":repo_name,"owner":owner,"summary":summary})

            with results_container:
                with st.container(border=True):
                    st.subheader(repo_name)
                    st.write(f"Owner: {owner} | Created: {created_date} | url: {url}")
                    st.write("Summary:")
                    st.write(summary)


with results_container:
    for r in st.session_state["search_results"]:
        with st.container(border=True):
            st.subheader(r["repo_name"])
            st.write(f"Owner: {r["owner"]} | Created: {r['created_date']} | url: {r['url']}")
            st.write("Summary:")
            st.write(r["summary"])