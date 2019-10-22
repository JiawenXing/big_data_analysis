# 利用循环语句，爬取豆瓣前100名影片

import requests
from bs4 import BeautifulSoup

url = "https://movie.douban.com/top250"
movie_names = []
number = 100 # 想爬取的电影数目

while len(movie_names) < number:
    res = requests.get(url)
    html = res.text
    mysoup = BeautifulSoup(html,'lxml')
    movie_list = mysoup.find('ol').find_all('li')
    for movie in movie_list:
        name = movie.find('span',attrs = {'class':'title'}).getText()  #<span class='title'>...</span>，
        movie_names.append(name)
    nextpage = mysoup.find('span',attrs = {'class':'next'}).find('a')  #None
    if nextpage:
        href = nextpage['href']
        url = url + href
    else:
        print('Reach the last page! URL=',url)
        break

with open('/Users/xingjiawen/OneDrive/文档/SJTU/2019-2020Autumn/大数据分析/hw4/movie_names_douban.txt','w') as f:
    for name in movie_names:
        f.write(name+'\n')
print('Finished.', len(movie_names),'movies crawled.')

# 尝试用同样的方法获取猫眼电影前100影片

u = 'https://maoyan.com/board/4'
url = u
movie_names = []
number = 100 # 想爬取的电影数目
page = 10 # page = 10 对应网页第二页，20 对应第三页，etc，直到90
headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'


while len(movie_names) < number:
    if page <= 100:
        res = requests.get(url,headers=headers)
        if res.status_code == 200:
            html = res.text
            mysoup = BeautifulSoup(html,'html5lib')
            movie_para = mysoup.find_all('p', attrs={'class': 'name'})
            for movie in movie_para:
                name = movie.getText()
                movie_names.append(name) # 爬第n页之后，把movie_names加上该页所爬取内容
            url = u + '?offset=' + str(page) # 再把url更新为第n+1页的，该url是下次循环使用的url
            page = page + 10 # 再把page更新为第n+2页的，该page是对应的url是下下次循环使用的url
        else:
            print (res.status_code)
            break
    else:
        print(html) # 我发现爬得比较频繁会有验证操作。。如果需要验证（html的title是'验证页面'），就在浏览器打开猫眼网站手动验证
        break

with open('/Users/xingjiawen/OneDrive/文档/SJTU/2019-2020Autumn/大数据分析/hw4/movie_names_maoyanclass.txt','w') as f:
    for name in movie_names:
        f.write(name+'\n')
print('Finished.', number,'movies crawled.')
