import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)  # Configure logging

def refresh_data():
    try:
        url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }

        session = requests.session()
        data = session.get(url, headers=headers).json()['records']['data']

        option_data = []
        for i in data:
            for j, k in i.items():
                if j == "CE" or j == "PE":
                    newdata = k
                    newdata["instrumentType"] = j  # Corrected spelling mistake in "instrumentType"
                    option_data.append(k)

        df = pd.DataFrame(option_data)

        # Convert DataFrame to HTML
        html_content = df.to_html()

        # Write HTML content to a file
        with open("optionchain.html", "w") as f:
            f.write('<meta http-equiv="refresh" content="10">')  # Auto-refresh every 10 seconds
            f.write(html_content)
            
        logging.info("Data refreshed successfully.")

    except Exception as e:
        logging.error(f"Error occurred while refreshing data: {e}")

def filter_data(html_file, strike_price, expiry_date):
    try:
        with open(html_file, "r") as f:
            html_content = f.read()

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')

        # Convert HTML table to DataFrame
        df = pd.read_html(str(table))[0]

        # Filter DataFrame by strike price and expiry date
        filtered_df = df[(df['strikePrice'] == strike_price) & (df['expiryDate'] == expiry_date)]

        # Write HTML table to a file
        html_table = filtered_df.to_html(index=False)
        with open("filtered_optionchain.html", "w") as f:
            f.write(html_table)
            
        logging.info("Data filtered successfully.")

    except Exception as e:
        logging.error(f"Error occurred while filtering data: {e}")

if __name__ == "__main__":
    while True:
        refresh_data()
        filter_data("optionchain.html", 22000, '22-Feb-2024')  # Example parameters
        time.sleep(10)
