import requests
import os
from bs4 import BeautifulSoup


def getHTMLText(url, code='utf-8'):
    '''
    download the html from url
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ''


def parseHTML(url, lst, page):
    '''
    get the name, content, like and comments number from the html
    '''
    html = getHTMLText(url)
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', attrs={'class': 'col1 old-style-col1'})
    try:
        con_list = div.find_all('div', class_='article')
        for i in con_list:
            try:
                content = i.find('div', attrs={'class': 'content'}).find('span').text
                author = i.find('h2').text
                stats = i.find('div', class_='stats')
                laugh = stats.find('span', attrs={'class': 'stats-vote'}).find('i', attrs={'class': 'number'}).text
                comment = stats.find('span', attrs={'class': 'stats-comments'}).find('i',
                                                                                     attrs={'class': 'number'}).text
                lst.append([page, author, laugh, comment, content])
            except:
                continue
    except:
        pass


def save_file(lst):
    '''
    save the lst into a txt file
    '''
    output = """第{}页 作者：{} 点赞：{} 评论：{}\n{}\n------------\n"""
    file_dir = 'C:\\'  # enter the file location
    file_name = 'qiubai.txt'
    file = os.path.join(file_dir, file_name)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(file, 'w', encoding='utf-8') as f:
        for i in lst:
            page = i[0]
            author = i[1]
            laugh = i[2]
            comment = i[3]
            content = i[4]
            f.write(output.format(page, author, laugh, comment, content))


def main():
    '''
    main control loop
    '''
    contest = []
    for i in range(10):  # control the page number
        url = 'https://www.qiushibaike.com/text/page/{}'.format(i)
        parseHTML(url, contest, i)
    save_file(contest)


if __name__ == '__main__':
    main()
