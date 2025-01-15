# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from baidu_image_spider.main import Crawler

crawler = Crawler(0.05, save_dir="outputs")  # 抓取延迟为 0.05

# 抓取关键词为 “美女”，总数为2页，开始页码为1，每页 30 张, 即总共2*30=60张
crawler(word="美女", total_page=2, start_page=1, per_page=30)
