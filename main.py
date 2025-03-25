from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile
from urllib.parse import urljoin

load_dotenv()

url = os.environ['URL_GOV']

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

pdf_links = []

try:
    for link in soup.find_all('a', href=True):
        href = link['href']
        if ("Anexo" in href or "anexo" in href) and href.endswith('.pdf'):
            pdf_links.append(urljoin(url, href))

    pdf_files = []
    for pdf_url in pdf_links:
        pdf_name = pdf_url.split('/')[-1]
        pdf_path = os.path.join(os.getcwd(), pdf_name)

        pdf_response = requests.get(pdf_url)

        with open(pdf_path, 'wb') as f:
            f.write(pdf_response.content)
        pdf_files.append(pdf_path)
except Exception as err:
    print(f'Error pdf: {err}')

try:
    zip_filename = 'compact_pdf.zip'

    with ZipFile(zip_filename, 'w') as zipf:
        for pdf_file in pdf_files:
            zipf.write(pdf_file, os.path.basename(pdf_file))

    for pdf_file in pdf_files:
        os.remove(pdf_file)
except Exception as err:
    print(f'Error zipfile: {err}')