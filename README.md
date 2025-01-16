<div align="center">
  <div align="center">
    <h1><b>🕷️ Baidu Image Crawling</b></h1>
  </div>

<a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.12-aff.svg"></a>
<a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
<a href="https://pypi.org/project/baidu_image_crawling/"><img alt="PyPI" src="https://img.shields.io/pypi/v/baidu_image_crawling"></a>
<a href="https://pepy.tech/project/baidu_image_crawling"><img src="https://static.pepy.tech/personalized-badge/baidu_image_crawling?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
<a href="https://github.com/SWHL/BaiduImageCrawling/stargazers"><img src="https://img.shields.io/github/stars/SWHL/BaiduImageCrawling?color=ccf"></a>
<a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

</div>

### 简介

一个超级轻量的百度图片爬虫, modified from <https://github.com/kong36088/BaiduImageCrawling>

### 安装

```bash
pip install baidu_image_crawling
```

### Python使用

```python
from baidu_image_crawling.main import Crawler

crawler = Crawler(0.05, save_dir="outputs")  # 抓取延迟为 0.05

# 抓取关键词为 “美女”，总数为2页，开始页码为1，每页 30 张, 即总共2*30=60张
crawler(word="美女", total_page=2, start_page=1, per_page=30)
```

### 终端使用

```bash
baidu_image_crawling -w 美女 -tp 1 -sp 1 -pp 2
```

查看参数文档：

```bash
$ baidu_image_crawling -h
usage: baidu_image_crawling [-h] -w WORD -tp TOTAL_PAGE -sp START_PAGE [-pp [PER_PAGE]] [-sd SAVE_DIR] [-d DELAY]

options:
  -h, --help            show this help message and exit
  -w WORD, --word WORD  抓取关键词
  -tp TOTAL_PAGE, --total_page TOTAL_PAGE
                        需要抓取的总页数
  -sp START_PAGE, --start_page START_PAGE
                        起始页数
  -pp [PER_PAGE], --per_page [PER_PAGE]
                        每页大小
  -sd SAVE_DIR, --save_dir SAVE_DIR
                        图片保存目录
  -d DELAY, --delay DELAY
                        抓取延时（间隔）
```
