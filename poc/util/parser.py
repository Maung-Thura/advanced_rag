import requests
from bs4 import BeautifulSoup
import PyPDF2
import io
import pdfplumber
import boto3

def count_paper_titles_and_extract_text(url):
    extracted_text = []
    #s3 = boto3.client('s3')
    # Send a GET request to the URL
    response = requests.get(url)
    n = 0
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all elements containing paper titles
        paper_titles = soup.find_all('div', class_='title')

        # Print the count of paper titles
        print("Number of paper titles:", len(paper_titles))

        # Find all elements containing "Download PDF" links
        download_links = soup.find_all('a', string='Download PDF')

        # Iterate over each "Download PDF" link
        for link in download_links:
            pdf_url = link['href']
            # Access the PDF file
            pdf_response = requests.get(pdf_url)

            # Check if the request was successful
            if pdf_response.status_code == 200:
                # Extract text from the PDF
                pdf_content = io.BytesIO(pdf_response.content)
                # pdf_reader = PyPDF2.PdfReader(pdf_content)
                # text = ""
                # for page_num in range(len(pdf_reader.pages)):
                #     text += pdf_reader.pages[page_num].extract_text()
                with pdfplumber.open(pdf_content) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text()

                # Print the extracted text
                #print("Text from PDF:", text)
                extracted_text.append(text)
            else:
                print(f"Failed to retrieve PDF from {pdf_url}")

                #s3.put_object(Body = text, Bucket = bucekt_name, Key=f'extracted_text_{n}.txt')
                #s3.put_object(Body=pdf_response.content, Bucket=bucket_name, Key=f'pdf_file_{n}.pdf')

            n += 1
            if n == 2:
              break
    else:
        print("Failed to retrieve the webpage")
    print("parser worked")
    return extracted_text

# Example usage:
url = "https://proceedings.mlr.press/v222/"
#bucket_name = "your-s3-bucket-name"
#count_paper_titles_and_extract_text(url)
