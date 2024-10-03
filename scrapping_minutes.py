import os
import requests
from bs4 import BeautifulSoup

result = requests.get('https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm')
content = result.text
soup = BeautifulSoup(content,'lxml')

#scrappe pdf minutes 
usable_links = []
pdf_links = soup.find_all('a', href=lambda x: x and 'fomcminutes' in x and x.endswith('.pdf'))
for link in pdf_links:
    pdf_url = link.get('href')
    usable_links.append('https://www.federalreserve.gov/'+pdf_url)

pdf_minutes = 'pdfs'
if not os.path.exists(pdf_minutes):
    os.makedirs(pdf_minutes)

for pdf_link in usable_links:
    pdf_name = pdf_link.split('/')[-1]  # Extract the PDF file name from the URL
    pdf_path = os.path.join(pdf_minutes, pdf_name)
    response = requests.get(pdf_link)
    with open(pdf_path, 'wb') as f:
        f.write(response.content)