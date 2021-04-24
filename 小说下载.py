import requests
from lxml import etree
import os
from time import sleep


class DownloadNovel:
    """
    用于下载笔趣阁小说
    """
    def __init__(self, keyword):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
        }
        self.url = 'https://www.tianxiabachang.cn/cse/search?'
        self.params = {
            'q': keyword
        }
        #用来保存小说的名称和地址作者
        self.name_url_anthor = []
    
    def get_html(self, url, params=None):
        """获取网页源码"""
        if params is None:
            response = requests.get(url, headers=self.headers)
        else:
            response = requests.get(url, headers=self.headers, params=params)
        response.encoding = response.apparent_encoding
        return response.text

    def option_menu(self):
        """显示一个选择菜单"""
        tree = etree.HTML(self.get_html(self.url, self.params))

        #获取搜索页面的内容
        index = 0
        print("{:4}{:^40}{:>10}".format('索引', "作品名称", "作者"))
        for li in tree.xpath("//div[@id='main']/div[@class='novelslist2']/ul/li")[1:]:
            name = li.xpath("./span[@class='s2']/a/text()")[0]
            name_url = 'https://www.tianxiabachang.cn' + li.xpath("./span[@class='s2']/a/@href")[0]
            anthor = li.xpath("./span[@class='s4']/text()")[0]
            self.name_url_anthor.append([name, name_url, anthor])
            print("{:4}{:^40}{:>10}".format(index ,name, anthor))
            index += 1
    
    def choose_download(self):
        """根据用户选择下载"""
        choose_index = int(input("输入作品对应的索引即可下载："))
        choose_name = self.name_url_anthor[choose_index][0]
        choose_url = self.name_url_anthor[choose_index][1]
        choose_anthor = self.name_url_anthor[choose_index][2]

        # 开始下载
        print("开始下载作者{}的《{}》......".format(choose_anthor,choose_name))
        novel_tree = etree.HTML(self.get_html(choose_url))
        with open(choose_name + '.txt', 'w', encoding='utf-8') as f:
            for dd in novel_tree.xpath("//div[@id='list']/dl/dd")[9:]:
                title = dd.xpath('./a/text()')[0]
                chapter_url = 'http://www.tianxiabachang.cn' + dd.xpath("./a/@href")[0]
                chapter_tree = etree.HTML(self.get_html(chapter_url))
                chapter = chapter_tree.xpath("string(//div[@id='content'])")
                f.write(title +'\n' + chapter + '\n')
                print(title, "下载成功！")
                sleep(0.1)
        print("下载完成！")

def main():
    keyword = input("输入作品名称：")
    downloadnovel = DownloadNovel(keyword)
    downloadnovel.option_menu()
    downloadnovel.choose_download()

main()
    

