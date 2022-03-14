#-*-coding:utf-8-*-
import requests
from lxml import etree
import pandas as pd
import time


class NiaoWang_Spider(object):
    def __init__(self, keyword):
        # self.base_url='https://www.baidu.com/s?wd={}'
        self.base_url = 'https://www.cnniao.com/search/{}'
        # 传入的keyword参数，例如：spider = NiaoWang_Spider(keyWord)
        self.keyword = keyword
        # self.url=self.base_url.format(self.keyword)+'&ie=utf-8'
        self.url = self.base_url.format(self.keyword)
        # print("self.url: ", self.url)

    def get_html(self):
        print("get_html...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.106 Safari/537.36 '
        }
        try:
            r = requests.get(self.url.format(), headers=headers)
            r.encoding = 'utf-8'
            res = etree.HTML(r.text)
            # print("res: ", res)
            # selector=res.xpath('//div[@id="content_left"]/div[@class="result c-container new-pmd"]')
            # 浏览器中按F12找到HTML中，显示搜索结果对应的标签
            # 对于本网站来说，发现所有的目标元素都在class="entry-wrapper"这个div标签里，单个搜过结果显示在class="entry-header"
            # 的header中， 我们要的鸟名字显示在./h2/a/的title里。下面for循环中再写./h2/a/@title
            selector = res.xpath('//div[@class="entry-wrapper"]/header[@class="entry-header"]')
            print("selector: ", selector)
            # 如果 selecotor 为空，返回 NAN
            # TODO

            # data_list=[]
            name = ""
            for data in selector:
                # item={}
                # item['title']=''.join(data.xpath('./h3/a/text()'))
                # item['link']=''.join(data.xpath('./h3/a/@href'))
                # title = ''.join(data.xpath('./h3/a/text()'))
                # print("title: ", title)
                name = ''.join(data.xpath('./h2/a/@title'))
                print("name: ", name)
            return name

        except:
            pass

    # def save_data(self,item):
    #     with open(crawl_result,'a',encoding='utf-8')as f:
    #         data=item['title']+'\t'+item['link']
    #         print(data)
    #         f.write(data+'\n')


def main():
    # read the labelmap (downloaded from: https://tfhub.dev/google/aiy/vision/classifier/birds_V1/1)
    # 把.csv中的数据放到df中，方面后续使用
    df = pd.read_csv('aiy_birds_V1_labelmap.csv')
    # 第0条不用翻译，强制写入
    df.at[0, 'chinese_name'] = '背景'
    keyWord = 'Dryobates minor'
    # keyWord = 'Anser anser domesticus'
    # spider = NiaoWang_Spider(keyWord)
    # bird_name = spider.get_html()
    # print("bird_name: ", bird_name)
    # bird_chinese_name = bird_name.split("/")[0]
    # print("bird_chinese_name: ", bird_chinese_name)
    # df.at[1, 'chinese_name'] = bird_chinese_name

    # 遍历整个df，依次查询每个鸟
    for index in range(1, len(df)):
    # for index in range(1, 3):  # 怕鸟网崩了，测试用的
        # 拿到搜索关键字，这里拿表格中的name，也就是鸟的拉丁文学名去搜索
        keyWord = df.name[index]
        print("keyWord: ", index, ",", keyWord)
        # 把关键字传入类
        spider = NiaoWang_Spider(keyWord)
        # 搜索
        bird_name = spider.get_html()
        time.sleep(30)
        print("bird_name: ", bird_name)
        if bird_name is None:
            continue

        # 如果 bird_name 为NAN，则记录这条数据（方便后续手动添加），并跳出本次循环
        # TODO

        # 拿到第一个'/'前面的字符串即为我们所要的中文名
        bird_chinese_name = bird_name.split("/")[0]
        print("bird_chinese_name: ", bird_chinese_name)
        # 放到 df 中
        df.at[index, 'chinese_name'] = bird_chinese_name

    # 把整个搜索结果连带原来的数据写入到一个新的.csv文件中
    df.to_csv('aiy_birds_V1_labelmap_amended.csv', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    main()
