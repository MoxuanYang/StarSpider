# -*-coding:utf-8 -*-
# @File  : StarSpider.py
# @Author: MoxuanYang
# @Date  : 2020/3/4
# @Desc  :
# ********************
import requests
import os
import re

# os.system('PYTHONIOENCODING=utf-8')


class StarSpider(object):
    def __init__(self, save_dir):
        self.save_dir = save_dir
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'Referer': 'https://www.1905.com/mdb/star/'
        }

    def getStarUrls(self, url):
        content = requests.get(url, headers=self.headers).content.decode('utf-8')
        urls = re.findall(r'/mdb/star/\d+/', content)
        return list(set(urls))

    def getImgUrls(self, url):
        content = requests.get(f'https://www.1905.com{url}', headers=self.headers).content.decode('utf-8')
        content = re.findall(r'<img class="poster" src=".*\.jpg" alt=".*"/>', content)[0]
        img = re.findall(r'src=".*\.jpg"', content)[0].split('"')[-2]
        name = re.findall(r'alt=".*"', content)[0].split('"')[-2]
        return img, name

    def getImgs(self, imge_url, save_path):
        with open(save_path, 'wb') as f:
            f.write(requests.get(imge_url, headers=self.headers).content)
        print(f'save to {save_path}.')

    def run(self, star_number):
        urls = []
        page_number = star_number // 16 + 1 if star_number % 16 else star_number // 16
        for i in range(1, page_number + 1):
            url = f'https://www.1905.com/mdb/star/m1p{i}.html'
            for star_url in self.getStarUrls(url):
                if star_url in urls:
                    continue
                urls.append(star_url)
                image_url, star_name = self.getImgUrls(star_url)
                self.getImgs(image_url, f'./imgs/{star_name}.jpg')


if __name__ == '__main__':
    star_spider = StarSpider('./imgs')
    star_spider.run(32)
