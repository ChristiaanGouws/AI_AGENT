import streamlit as st
import requests
import time

st.set_page_config(page_title="SA Property Investment Briefing", page_icon="🏢")
st.title("🏢 SA Property Investment Briefing Agent")
st.write("Click the button below to trigger the CrewAI agent and view the generated output.")

api_token = st.text_input("Enter CrewAI API Token:", type="password")

if st.button("Run Property Briefing"):
    if not api_token:
        st.warning("Please enter your API token.")
    else:
        base_url = "https://sa-property-investment-briefing-v1-15fc6050-50e951b3.crewai.com"
        headers = {
            "Authorization": f"Bearer {api_token.strip()}",
            "Content-Type": "application/json"
        }
        
        try:
            # 1. Trigger Kickoff
            with st.spinner("Starting agent execution..."):
                kickoff_res = requests.post(f"{base_url}/kickoff", headers=headers, json={"inputs": {}})
            
            if kickoff_res.status_code == 200:
                kickoff_id = kickoff_res.json().get("kickoff_id")
                st.info(f"Agent started! (ID: {kickoff_id}) Fetching result...")
                
                # 2. Poll Status Endpoint
                status_url = f"{base_url}/status/{kickoff_id}"
                
                with st.spinner("Agent is researching & generating report..."):
                    while True:
                        time.sleep(3)
                        status_res = requests.get(status_url, headers=headers)
                        
                        if status_res.status_code == 200:
                            data = status_res.json()
                            state = str(data.get("status", "")).upper()
                            
                            if state in ["SUCCESS", "COMPLETED", "FINISHED"]:
                                st.success("Briefing Complete!")
                                # Display result output
                                result_text = data.get("result", data.get("output", data))
                                st.markdown(result_text)
                                break
                            elif state in ["FAILED", "ERROR"]:
                                st.error("Execution failed on server.")
                                st.json(data)
                                break
                        else:
                            st.error(f"Status check failed: {status_res.status_code}")
                            break
            else:
                st.error(f"Kickoff failed ({kickoff_res.status_code}): {kickoff_res.text}")
                
        except Exception as e:
            st.error(f"Connection error: {e}")