import json
import requests
import os


def getHTML(url, code='utf-8'):
    '''
    用requests库下载html文件
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/51.0.2704.63 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        r.encoding = code
        return r
    except:
        return ''


def getPICInfo(url):
    '''
    找到json中图片的url，和名字
    '''
    try:
        img_response = getHTML(url).text
        img_json = json.loads(img_response[18:-30])
        img = img_json['images'][0]
        img_url = img['url'].split('&')[0]
        img_name = img['copyright']
        return img_url, img_name
    except:
        pass


def down_img(url, path):
    bin_url = 'https://www.bing.com'
    img_info = getPICInfo(url)
    img_url = bin_url + img_info[0]
    print(img_url)
    cpright = img_info[1]
    # 因为原来copy right包含特殊字符
    img_name = cpright.split('(')[0][:-2] + '.jpg'
    print(cpright)
    file_dir = path  # enter the file location
    file_name = img_name
    file = os.path.join(file_dir, file_name)
    try:
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        if not os.path.exists(file):
            content = getHTML(img_url).content
            with open(file, 'wb') as f:
                f.write(content)
                print('load success')
        else:
            print('file exist')
    except:
        pass


def main():
    path = 'C:\\Users\\User\\Desktop\\project\\bing_image'  # 路径
    for i in range(8):  # bing 7天更新的壁纸
        url = 'https://www.bing.com/HPImageArchive.aspx?format=hp&idx={}&n=1'.format(i)
        down_img(url, path)


if __name__ == '__main__':
    main()
