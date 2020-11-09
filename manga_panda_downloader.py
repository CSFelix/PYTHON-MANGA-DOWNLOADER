###########
# Imports #
###########
import re
import urllib.request
from bs4 import BeautifulSoup
import requests
from google.colab import files

#############
# Functions #
#############
def GetUrlPages(img_list, manga_title, chapter):
	"""
		Get the URL pages and store in a list
	"""
	for number_page in range(1, 200):
		URL = 'http://www.mangapanda.com/{}/{}/{}'.format(manga_title, chapter, number_page)

		# check if the link exists and it's working
		request = requests.get(URL)

		if request.status_code == 200:
			page = requests.get(URL) # html page's link
			page_content = BeautifulSoup(page.content, 'html.parser') # get the content of the page
			row_data = []

			# get the script text image
			for row in page_content.findAll('script',
						attrs={'type': 'text/javascript'}):
				row_data.append(row.text)

			# get only the image's link
			img_list.append(re.findall('[^.]ttps.*jpg', row_data[2]))

		else: break

def RemoveNullPages(img_list):
	"""
		Remove all null pages in the image's list
	"""
	for i,x in enumerate(img_list):
		if x == []: img_list.remove([])

def DownloadPages(img_list, manga_title, chapter):
	"""
		Download the Pages
	"""
	for page in range(len(img_list)):
		image_url = ''.join(map(str, img_list[page]))
		response = requests.get(image_url)

		if response.status_code == 200:
			file = open(f"{manga_title} - {chapter} - {page+1}.jpg", "wb")
			file.write(response.content)
			files.download(f"{manga_title} - {chapter} - {page+1}.jpg")
			file.close()

############
# Proccess #
############

if __name__ == '__main__':
	try:
		img_list = []
		manga_title = input('Manga Name: ')
		manga_chapter = int(input('Chapter: '))
		print('\n')

		GetUrlPages(img_list, manga_title, manga_chapter)
		RemoveNullPages(img_list)
		DownloadPages(img_list, manga_title, manga_chapter)

	except ValueError: print('The manga chapter needa be an integer number.')
	except: print('The page does not exist or it is not working now!')