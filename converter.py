import requests
from bs4 import BeautifulSoup
import os

file_location = 'C:\\Users\\Yoon\\Desktop\\Lyrics\\'
file_list = os.listdir(file_location) # Lyrics 폴더 모든 파일 리스트

# 리스트에서 Lyrics 파일만 남기기
n3 = 0
while n3 < len(file_list):
    if file_list[n3].find('.MSL') == -1:
        file_list.pop(n3)
    else:
        file_list[n3] = file_list[n3].replace('.MSL','') # @@@.MSL을 @@@으로
    n3 = n3 + 1
if file_list[n3-1].find('.MSL') == -1: # 마지막 요소 안되서 추가
    file_list.pop(n3-1)

print(file_list)
# lyrics_list = file_list(0)[0:-4]
# print(lyrics_list)

n4 = 0
while n4 < len(file_list):
    song_id = file_list[n4] # https://www.genie.co.kr/detail/songInfo?xgnm='song_id'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'} # 크롤링 차단 우회
    url = 'https://www.genie.co.kr/detail/songInfo?xgnm='+ song_id # 지니 뮤직 URL

    resp = requests.get(url, headers = headers)
    soup = BeautifulSoup(resp.text, 'html.parser')

    song_name = soup.find("h2", {"class":"name"}).text
    song_name = song_name[14:-6] # 공백 제거
    song_artist = soup.find("span", {"class":"value"}).text
    # full_lirycs = soup.find("pre", {"id":"pLyrics"}).text

    print(song_name)
    print(song_artist)
    # print(full_lirycs)

    Lyrics_lacation = 'C:\\Users\\Yoon\\Desktop\\Lyrics\\' + song_id + '.MSL'
    print(Lyrics_lacation)
    f = open(Lyrics_lacation, 'r', encoding='utf-8')
    data = f.read()

    # data 가공
    data = data.replace('{','') # { 제거
    data = data.replace(':','') # : 제거
    data = data.replace(',','')
    data = data.replace('""','"')

    n = 0
    time = ''
    lyrics = ''
    mode = 1
    print(data)

    while data[n] != '}':
        if data[n] =='"':
            mode = -1 * mode
        # 시간/가사 모드 변환

        if mode == 1:
            lyrics = lyrics + data[n]
        else:
            time = time + data[n]

        n=n+1

    time = time.split('"') # 리스트로 변환
    lyrics = lyrics.split('"') # 리스트로 변환

    time = list(filter(None, time)) # 빈 요소 제거
    lyrics = list(filter(None, lyrics)) # 빈 요소 제거

    # print(time)
    print(lyrics)

    # ms > 초분으로 변환
    m = [] # minutes
    s = [] # seconds
    time_m = []
    time_s = []
    time_float = []
    n1 = 0
    while n1 < len(time):
        ms = int(time[n1])
        time_m.append(format(int( ms / ( 1000 * 60 )),'02')) # 자릿수 00 맞추기
        second = int( ms / 1000 )
        if second <= 60:
            second = format((int(ms / 1000 )) - 0, '02') 
        elif second <= 120 :
            second = format((int(ms / 1000 )) - 60, '02')
        elif second <= 180:
            second = format((int(ms / 1000 )) - 120, '02')
        elif second <= 240:
            second = format((int(ms / 1000 )) - 180, '02')   
        elif second <= 300:
            second = format((int(ms / 1000 )) - 240, '02')
        elif second <= 360:
            second = format((int(ms / 1000 )) - 300, '02')   
        time_s.append(second)
        time_float.append( format(int(100 * (round(( ms / 1000 ) % 1, 2 ))), '02'))
        n1 = n1 + 1

    print(time_m)
    print(time_s)
    print(time_float)

    output_lacation = 'C:\\Users\\Yoon\\Desktop\\Lyrics\\Output\\'
    #output 폴더 없을 시 생성
    def createFolder(directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print ('Error: Creating directory. ' + directory)
            # 에러 메시지 출력

    createFolder(output_lacation)
    output = open(output_lacation + song_artist + ' - ' + song_name + '.lrc', 'w')
    n2 = 0
    while n2 < len(time_m):
        timestamp = '[' + str(time_m[n2]) + ':' + str(time_s[n2]) + '.' + str(time_float[n2]) + ']' + lyrics[n2] + '\n'
        output.write(timestamp)
        n2 = n2 + 1

    f.close() # 파일 객체를 닫아 주는 역할
    n4 = n4 + 1



    # https://www.genie.co.kr/search/searchMain?query="URL encode 된 한글 또는 영어"로 검색 가능
    # https://namu.wiki/w/URL%20escape%20code 참고````