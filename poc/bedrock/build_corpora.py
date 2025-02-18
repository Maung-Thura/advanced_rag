import os

import requests
from bs4 import BeautifulSoup


def create_corpora_dir():
	if not os.path.isdir('./corpora'):
		os.mkdir('./corpora')

	return


def build_corpora():
	response = requests.get('https://proceedings.mlr.press/v222/')

	if not response.text or not response.status_code == 200:
		return

	main_html = BeautifulSoup(response.text, 'html.parser')
	href_tags = main_html.find_all('a')
	pdf_links = [tag['href'].strip() for tag in href_tags if '.pdf' in tag['href']]

	for link in pdf_links:
		response = requests.get(link)

		if not response.content or not response.status_code == 200:
			continue

		file_name = link.split('/')[-1]
		file = open(f'./corpora/{file_name}', 'wb')
		file.write(response.content)
		file.close()

		print(f'Saved file ./corpora/{file_name}')

	return


if __name__ == '__main__':
	create_corpora_dir()
	build_corpora()
