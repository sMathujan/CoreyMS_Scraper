from bs4 import BeautifulSoup
import requests
import csv
import logging

logging.basicConfig(filename = 'scraper.log', level = logging.DEBUG, format = '%(asctime)s %(levelname)s %(message)s')

csv_file = open('cms_scrape.csv', 'w')
logging.info('Creating csv file to store scraped data')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline', 'summary', 'video_link'])

for page in range(1, 18):
    source = requests.get(f'https://coreyms.com/page/{page}').text
    logging.info('Fetching url : ', f'https://coreyms.com/page/{page}')

    soup = BeautifulSoup(source, 'lxml')

    for article in soup.find_all('article'):
        try:
            headline = article.h2.a.text
        except Exception as e:
            headline = None
            logging.exception('Exception occured ' + str(e))
        print(headline)

        try:
            summary = article.find('div', class_='entry-content').p.text
        except Exception as e:
            summary = None
            logging.exception('Exception occured ' + str(e))
        print(summary)

        try:
            vid_src = article.find('iframe', class_='youtube-player')['src']

            vid_id = vid_src.split('/')[4]
            vid_id = vid_id.split('?')[0]

            yt_link = f'https://youtube.com/watch?v={vid_id}'
        except Exception as e:
            yt_link = None
            logging.exception('Exception occured ' + str(e))
        print(yt_link)

        csv_writer.writerow([headline, summary, yt_link])


csv_file.close()


