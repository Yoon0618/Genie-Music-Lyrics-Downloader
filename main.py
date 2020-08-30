import requests
from bs4 import BeautifulSoup
import sys
import re
import os

print("Searching")
keyword = input()
print("Result")

search_url = 'https://www.genie.co.kr/search/searchMain?query=' + keyword

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'} # 크롤링 차단 우회
resp_search = requests.get(search_url, headers = headers)
soup_search = BeautifulSoup(resp_search.text, 'html.parser')

songs = soup_search.select('table.list-wrap > tbody > tr.list')
artists = soup_search.select('table.list-wrap > tbody > tr.list')
ids = soup_search.select('table.list-wrap > tbody > tr.list')

songs_list = []
artists_list = []
ids_list = []

n7 = 0
for song in songs:
    #사이트 하단 까지 나와서 추가
    if n7+1 == len(songs):
        break
    title = song.find('td',{'class':'info'}).find('a',{'class':'title ellipsis'}).text
    title = title.replace('TITLE','')
    title = title.strip()
    n7 = n7 + 1
    songs_list.append(title)

# print(songs_list)

n8 = 0
for artist in artists:
    if n8+1 == len(songs):
        break
    artist = artist.find('td',{'class':'info'}).find('a',{'class':'artist ellipsis'}).text
    n8 = n8 + 1
    artist = artist.replace('\t','')
    artist = artist.replace('\n','')
    artists_list.append(artist)

# print(artists_list)

# ID 리스트
n10 = 0
# print(ids[4])
while True:
    if ( n10 + 1 ) == len(ids):
        break
    html_id = ids[n10]
    html_id = str(html_id)
    html_id = html_id[25:33]
    ids_list.append(html_id)
    n10 = n10 + 1

info_list = []

n11 = 0
while True:
    if n11+1 == len(ids):
        break
    info_list.append( songs_list[n11] + ' - '+ artists_list[n11] + '(' + ids_list[n11] + ')')
    n11 = n11 + 1

n11 = 1
for a in info_list:
    index = str(n11)
    print()
    print(index + '. ' + a)
    n11 = n11 + 1

print('Select 1-15')
song_id = ids_list[int(input()) - 1]
# print(song_id)

lyrics_url = "https://dn.genie.co.kr/app/purchase/get_msl.asp?path=a&songid=" + song_id
info_url = "https://www.genie.co.kr/detail/songInfo?xgnm=" + song_id

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'} # 크롤링 차단 우회

# 가사 정보 받아오기
# print(info_url)

resp_info = requests.get(info_url, headers = headers)
soup_info = BeautifulSoup(resp_info.text, 'html.parser')

song_name = soup_info.find("h2", {"class":"name"}).text
song_name = song_name[14:-6] # 공백 제거
song_artist = soup_info.find("span", {"class":"value"}).text
# full_lirycs = soup.find("pre", {"id":"pLyrics"}).text

# print(song_name)
# print(song_artist)

# 가사 받아오기
resp_lyrics = requests.get(lyrics_url, headers = headers)
lyrics = BeautifulSoup(resp_lyrics.text, 'html.parser')

# Lyrics 가공
lyrics = lyrics.text
lyrics = lyrics[7:-4] + '*'

n1 = 0
mode = 1
# mode = 1 : 타임라인
# mode = -1 : 가사
lyrics_timeline = ''
lyrics_text = ''

while True:

    if lyrics[n1] == '*':
        break

    if lyrics[n1] + lyrics[n1-1] + lyrics[n1-2] == '":"':
        mode = -1
    elif lyrics[n1] + lyrics[n1-1] + lyrics[n1-2] == '","':
        mode = 1
    
    # 타임라인/가사 분리
    if mode == 1:
        lyrics_timeline = lyrics_timeline + lyrics[n1]

    if mode == -1:
        lyrics_text = lyrics_text + lyrics[n1]
    
    n1 = n1 + 1

# *으로 구분
lyrics_text = lyrics_text[1:]
lyrics_text = lyrics_text.replace('","','*')


lyrics_timeline = lyrics_timeline.replace('":"','*')
lyrics_timeline = lyrics_timeline.replace('":','')

# 리스트로 변환
lyrics_text = lyrics_text.split('*')
lyrics_timeline = lyrics_timeline.split('*')

# print(lyrics_text)

# 분분:초초:소수 로 변환
# lyrics_time[n2] = ms 단위
n2 = 0
second_fixed_list = []
minute_list = []
float_second_list = []
while True:
    if len(lyrics_timeline) == n2:
        break

    # 스트링 타입을 인트로 변환
    ms = int(lyrics_timeline[n2])
    second = ms / 1000

    #분
    minute = second / 60
    minute = str(int(minute))
    minute = minute.zfill(2) # 자릿수 맞추기
    minute_list.append(minute)

    #초
    second_fixed = int(second)
    if int(second_fixed / 60) == 1:
        second_fixed = second_fixed - 60
    elif int(second_fixed / 60) == 2:
        second_fixed = second_fixed - 120
    elif int(second_fixed / 60) == 3:
        second_fixed = second_fixed - 180
    elif int(second_fixed / 60) == 4:
        second_fixed = second_fixed - 240
    elif int(second_fixed / 60) == 5:
        second_fixed = second_fixed - 300
    elif int(second_fixed / 60) == 6:
        second_fixed = second_fixed - 360
    elif int(second_fixed / 60) == 7:
        second_fixed = second - 420

    second_fixed = str(second_fixed).zfill(2) # 자릿수 맞추기
    second_fixed_list.append(second_fixed)

    #초:소수
    float_second = ( second % 1 ) * 100
    float_second = int(round(float_second, 2)) # 두자리수 제한, 인트 타입 변환
    float_second = str(float_second).zfill(2) # 자릿수 맞추기
    float_second_list.append(float_second)


    n2 = n2 + 1


output_location = os.path.join(os.path.expanduser('~'),'Desktop') + '\output//'# 데스크탑 경로
#output 폴더 없을 시 생성
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)
        # 에러 메시지 출력

createFolder(output_location)
output = open(os.path.join(os.path.expanduser('~'),'Desktop') + '\output' + '//' + song_artist + ' - ' + song_name + '.lrc', 'w')

# print(minute_list)
n3 = 0
while True:
    if (n3) == len(minute_list):
        break
    timestamp = '[' + str(minute_list[n3]) + ':' + str(second_fixed_list[n3]) + '.' + str(float_second_list[n3]) + ']' + lyrics_text[n3] + '\n'
    output.write(timestamp)
    n3 = n3 + 1

print('Done!')