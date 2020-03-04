# -*-coding:utf-8 -*-
# @File  : StarSpider.py
# @Author: MoxuanYang
# @Date  : 2020/3/4
# @Desc  :
# ********************
import requests
import os
import re

os.system('PYTHONIOENCODING=utf-8')


class StarSpider(object):
    def __init__(self, save_dir):
        self.save_dir = save_dir
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'Referer': 'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&fm=index&pos=history&word=%E6%9D%8E%E6%99%A8'
        }

    def getStarList(self, star_number):
        star_list = []
        page_number = star_number // 12 + 1 if star_number % 12 else star_number // 12
        for i in range(page_number):
            url = f'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=28266&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=%E6%98%8E%E6%98%9F&sort_key=&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn={i * 12}&rn=12&cb=jQuery110204606451277705128_1583291728784&_=1583291728809'
            content = requests.get(url).content.decode('unicode_escape')
            star = re.findall(r'"ename":".{2,3}"', content)
            star = list(map(lambda x: x.replace('"', '').replace(':', '').replace('ename', ''), star))
            star_list += star[1:]
        return star_list[:star_number]

    def getImgUrls(self, star_name, img_number):
        img_urls = []
        page_number = img_number // 30 + 1 if img_number % 30 else img_number // 30
        for i in range(page_number):
            url = f'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={star_name}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word={star_name}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&cg=star&pn={i * 30}&rn=30&gsm=3c&1583292375944='
            content = requests.get(url).content.decode('unicode_escape')
            urls = re.findall(r'"thumbURL":".*?jpg"', content)
            urls = list(map(lambda x: x.replace('"thumbURL":"', '').replace('"', ''), urls))
            img_urls += urls
        return img_urls[:img_number]

    def getImgs(self, imge_url, save_path):
        with open(save_path, 'wb') as f:
            f.write(requests.get(imge_url, headers=self.headers).content)
        print(f'save to {save_path}.')

    def run(self, star_number, img_number_per_star):
        star_list = self.getStarList(star_number)
        for star in star_list:
            img_urls = self.getImgUrls(star, img_number_per_star)
            for index, img_url in enumerate(img_urls):
                self.getImgs(img_url, f'{self.save_dir}/{star}_{index}.jpg')


if __name__ == '__main__':
    star_spider = StarSpider('./imgs')
    star_spider.run(2, 10)
