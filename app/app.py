import streamlit as st
import requests
import time

st.set_page_config(page_title="SA Property Investment Briefing", page_icon="🏢")
st.title("🏢 SA Property Investment Briefing Agent")
st.write("Enter your email below to receive the property briefing directly in your inbox.")

# User Inputs
api_token = st.text_input("Enter CrewAI API Token:", type="password")
recipient_email = st.text_input("Enter Your Email Address:", placeholder="lecturer@university.ac.za")

if st.button("Send Briefing to Email"):
    if not api_token or not recipient_email:
        st.warning("Please provide both the API token and your email address.")
    else:
        base_url = "https://sa-property-investment-briefing-v1-15fc6050-50e951b3.crewai.com"
        headers = {
            "Authorization": f"Bearer {api_token.strip()}",
            "Content-Type": "application/json"
        }
        
        # Pass the dynamic email to CrewAI inputs
        payload = {
            "inputs": {
                "recipient_email": recipient_email.strip()
            }
        }
        
        try:
            with st.spinner("Starting execution..."):
                kickoff_res = requests.post(f"{base_url}/kickoff", headers=headers, json=payload)
            
            if kickoff_res.status_code == 200:
                kickoff_id = kickoff_res.json().get("kickoff_id")
                st.info(f"Agent started! Sending status requests...")
                
                status_url = f"{base_url}/status/{kickoff_id}"
                
                with st.spinner("Researching and sending email..."):
                    while True:
                        time.sleep(3)
                        status_res = requests.get(status_url, headers=headers)
                        
                        if status_res.status_code == 200:
                            data = status_res.json()
                            state = str(data.get("status", "")).upper()
                            
                            if state in ["SUCCESS", "COMPLETED", "FINISHED"]:
                                st.success(f"Briefing successfully sent to **{recipient_email}**!")
                                st.markdown(data.get("result", data.get("output", "")))
                                break
                            elif state in ["FAILED", "ERROR"]:
                                st.error("Execution failed.")
                                st.json(data)
                                break
                        else:
                            st.error(f"Status check failed: {status_res.status_code}")
                            break
            else:
                st.error(f"Kickoff failed ({kickoff_res.status_code}): {kickoff_res.text}")
                
        except Exception as e:
            st.error(f"Connection error: {e}")
