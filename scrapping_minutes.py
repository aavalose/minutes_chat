import os
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from config import PDF_MINUTES

def check_and_download_new_minutes():
    # Get existing files
    existing_files = set(os.listdir(PDF_MINUTES))
    new_files_downloaded = False
    
    # Scrape current available minutes
    result = requests.get('https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm')
    soup = BeautifulSoup(result.text, 'lxml')
    
    # Find minutes links
    usable_links = []
    pdf_links = soup.find_all('a', href=lambda x: x and 'fomcminutes' in x and x.endswith('.pdf'))
    
    for link in pdf_links:
        pdf_url = link.get('href')
        date_match = re.search(r'minutes(\d{8})', pdf_url)
        if date_match:
            date_str = date_match.group(1)
            formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
            usable_links.append({
                'url': 'https://www.federalreserve.gov/' + pdf_url,
                'date': formatted_date
            })
    
    # Create directory if it doesn't exist
    if not os.path.exists(PDF_MINUTES):
        os.makedirs(PDF_MINUTES)
    
    # Download only new PDFs
    for pdf_info in usable_links:
        pdf_name = f"minutes_{pdf_info['date']}.pdf"
        if pdf_name not in existing_files:
            pdf_path = os.path.join(PDF_MINUTES, pdf_name)
            response = requests.get(pdf_info['url'])
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            new_files_downloaded = True
    
    return new_files_downloaded

if __name__ == "__main__":
    # This will run only if the script is run directly
    check_and_download_new_minutes()