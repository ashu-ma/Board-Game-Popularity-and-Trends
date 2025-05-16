import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url='https://boardgamegeek.com/browse/boardgame'
board_games=[]

for page in range(1,3):
    url=f"{base_url}?page={page}"
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')

    rows=soup.select('tr#row_')

    for row in rows:
        try:
            rank=row.select_one('.collection_rank').text.strip()
            title=row.select_one('.primary').text.strip()
            year=row.select_one('.collection_objectname span.smallerfont').text.strip('()')
            rating=row.select_one('td.collection_bggrating:nth-of-type(4)').text.strip()
            avg_rating=row.select_one('td.collection_bggrating:nth-of-type(5)').text.strip()
            voters=row.select_one('td.collection_bggrating:nth-of-type(6)').text.strip()

            board_games.append({
                'Rank':rank,
                'Title':title,
                'Year':year,
                'Rating':rating,
                'Avg_Rating':avg_rating,
                'Voters':voters
            })
        except Exception as e:
            print(f"Error parsing in {e}")
            continue

    time.sleep(1)

df=pd.DataFrame(board_games)
df.to_csv('boardgames_top200.csv',index=False)