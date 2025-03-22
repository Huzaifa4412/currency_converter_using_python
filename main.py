import requests
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()
def get_exchange_rates():
    url = os.getenv("API_KEY_URL")
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    st.set_page_config(page_title="Currency Converter", page_icon="💱", layout="centered")
    
    st.title("🌍 Currency Converter")
    st.markdown("Convert currencies in real-time with live exchange rates.")
    
    data = get_exchange_rates()
    if data:
        currency_data = data["conversion_rates"]
        last_update = datetime.utcfromtimestamp(data["time_last_update_unix"]).strftime('%Y-%m-%d %H:%M:%S UTC')
        
        with st.container():
            st.markdown(f"#### ⏳ Last Updated: `{last_update}`")
            amount = st.number_input("Enter the Amount 💸", min_value=0.01, format="%.2f")
            
            col1 ,col2 = st.columns([4, 4])
            with col1:
                from_currency = st.selectbox("From Currency", list(currency_data.keys()), key="from_currency")

            with col2:
                to_currency = st.selectbox("To Currency", list(currency_data.keys()), key="to_currency")
            
            if st.button("Convert ♻"):
                from_rate = currency_data[from_currency]
                to_rate = currency_data[to_currency]
                converted_amount = (amount / from_rate) * to_rate
                
                st.success(f"💰 {amount} {from_currency} = {converted_amount:.2f} {to_currency}")
                
                st.info(f"Exchange Rate: 1 {from_currency} = {to_rate/from_rate:.4f} {to_currency}")
                
            st.subheader("Exchange Rate (USD) Based 💵")
            st.dataframe(
                data=currency_data,
                column_config={
                   0: "Currency",
                    1:"Rates"
                },
                use_container_width=True
            )
    else:
        st.error("Failed to fetch exchange rates. Please try again later.")

if __name__ == "__main__":
    main()
