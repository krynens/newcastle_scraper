import scraperwiki
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"


today = datetime.today()

url = 'https://cn-web.t1cloud.com/T1PRDefault/WebApps/eProperty/P1/PublicNotices/AllPublicNotices.aspx?r=TCON.LG.WEBGUEST&f=P1.ESB.PUBNOTAL.ENQ'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'lxml')

table = soup.find('div', id='ctl00_Content_cusApplicationResultsGrid_pnlCustomisationGrid')
rows = table.find_all('table', class_='grid')

for row in rows:
    record = {}
    record['address'] = row.find_all('td')[5].text
    record['date_scraped'] = today.strftime("%Y-%m-%d")
    record['description'] = row.find_all('td')[3].text
    record['council_reference'] = row.find_all('td')[1].text
    record['info_url'] = 'https://cn-web.t1cloud.com/T1PRDefault/WebApps/eProperty/P1/PublicNotices/' + \
        str(row.find_all('td')[1]).split('"')[1]
    on_notice_to_raw = row.find_all('td')[7].text
    record['on_notice_to'] = datetime.strptime(on_notice_to_raw, '%d/%m/%Y').strftime("%Y-%m-%d")

    scraperwiki.sqlite.save(
        unique_keys=['council_reference'], data=record, table_name="data")
