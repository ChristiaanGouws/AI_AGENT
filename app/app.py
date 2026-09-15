import streamlit as st
import requests

st.set_page_config(page_title="SA Property Investment Briefing", page_icon="🏢")
st.title("🏢 SA Property Investment Briefing Agent")
st.write("Click the button below to trigger the CrewAI agent and fetch the briefing status.")

# Optional password field or hardcode your token into Streamlit Secrets
api_token = st.text_input("Enter CrewAI API Token:", type="password")

if st.button("Run Property Briefing"):
    if not api_token:
        st.warning("Please enter your API token.")
    else:
        with st.spinner("Triggering CrewAI Execution..."):
            url = "https://sa-property-investment-briefing-v1-15fc6050-50e951b3.crewai.com/kickoff"
            headers = {
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json"
            }
            payload = {"inputs": {"location": "South Africa"}}
            
            try:
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    st.success("Agent triggered successfully!")
                    st.json(response.json())
                else:
                    st.error(f"Server returned status code {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")