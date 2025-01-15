# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
import json
import re
import socket
import time
import urllib
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from fake_useragent import UserAgent

timeout = 5
socket.setdefaulttimeout(timeout)


class Crawler:
    __amount = 0
    __start_amount = 0
    __counter = 0
    headers = {"User-Agent": str(UserAgent().random), "Cookie": ""}
    __per_page = 30

    def __init__(
        self, time_sleep: float = 0.1, save_dir: Union[str, Path, None] = None
    ):
        self.time_sleep = time_sleep
        self.save_dir = Path(save_dir) if save_dir is not None else Path("./")

    def __call__(self, word, total_page=1, start_page=1, per_page=30):
        """
        爬虫入口
        :param word: 抓取的关键词
        :param total_page: 需要抓取数据页数 总抓取图片数量为 页数 x per_page
        :param start_page:起始页码
        :param per_page: 每页数量
        :return:
        """
        self.__per_page = per_page
        self.__start_amount = (start_page - 1) * self.__per_page
        self.__amount = total_page * self.__per_page + self.__start_amount
        self.get_images(word)

    def get_images(self, word: str):
        search = urllib.parse.quote(word)
        page_num = self.__start_amount
        while page_num < self.__amount:
            url = (
                "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%s&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word=%s&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn=%s&rn=%d&gsm=1e&1594447993172="
                % (search, search, str(page_num), self.__per_page)
            )
            try:
                time.sleep(self.time_sleep)
                req = urllib.request.Request(url=url, headers=self.headers)
                with urllib.request.urlopen(req) as page:
                    self.headers["Cookie"] = self.handle_baidu_cookie(
                        self.headers["Cookie"], page.info().get_all("Set-Cookie")
                    )
                    rsp = page.read()
            except UnicodeDecodeError as e:
                print(e)
                print("-----UnicodeDecodeErrorurl:", url)
            except urllib.error.URLError as e:
                print(e)
                print("-----urlErrorurl:", url)
            except socket.timeout as e:
                print(e)
                print("-----socket timout:", url)
            else:
                rsp_data = json.loads(rsp, strict=False)
                if "data" not in rsp_data:
                    print("触发了反爬机制，自动重试！")
                else:
                    self.save_image(rsp_data, word)
                    print("下载下一页")
                    page_num += self.__per_page
        print("下载任务结束")

    @staticmethod
    def handle_baidu_cookie(original_cookie, cookies):
        """
        :param string original_cookie:
        :param list cookies:
        :return string:
        """
        if not cookies:
            return original_cookie

        result = original_cookie
        for cookie in cookies:
            result += cookie.split(";")[0] + ";"
        result.rstrip(";")
        return result

    def save_image(self, rsp_data: Dict[str, Any], word: str):
        save_img_dir = self.save_dir / word
        if not save_img_dir.exists():
            save_img_dir.mkdir(parents=True, exist_ok=True)

        self.__counter = len(list(Path(save_img_dir).iterdir())) + 1
        for image_info in rsp_data["data"]:
            try:
                if "replaceUrl" not in image_info or len(image_info["replaceUrl"]) < 1:
                    continue

                obj_url = image_info["replaceUrl"][0]["ObjUrl"]
                thumb_url = image_info["thumbURL"]
                url = (
                    "https://image.baidu.com/search/down?tn=download&ipn=dwnl&word=download&ie=utf8&fr=result&url=%s&thumburl=%s"
                    % (urllib.parse.quote(obj_url), urllib.parse.quote(thumb_url))
                )
                time.sleep(self.time_sleep)
                suffix = self.get_suffix(obj_url)

                # 指定UA和referrer，减少403
                opener = urllib.request.build_opener()
                opener.addheaders = [("User-agent", str(UserAgent().random))]
                urllib.request.install_opener(opener)

                save_img_path = save_img_dir / f"{self.__counter}{suffix}"
                urllib.request.urlretrieve(url, save_img_path)
                if save_img_path.stat().st_size < 5:
                    print("下载到了空文件，跳过!")
                    save_img_path.unlink()
                    continue
            except urllib.error.HTTPError as urllib_err:
                print(urllib_err)
                continue
            except Exception as err:
                time.sleep(1)
                print(err)
                print("产生未知错误，放弃保存")
                continue
            else:
                print("下载图+1,已有" + str(self.__counter) + "张图")
                self.__counter += 1

    @staticmethod
    def get_suffix(name):
        m = re.search(r"\.[^\.]*$", str(name))
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        return ".jpeg"


def parse_args(arg_list: Optional[List[str]] = None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--word", type=str, help="抓取关键词", required=True)
    parser.add_argument("-tp", "--total_page", type=int, help="需要抓取的总页数", required=True)
    parser.add_argument("-sp", "--start_page", type=int, help="起始页数", required=True)
    parser.add_argument(
        "-pp",
        "--per_page",
        type=int,
        help="每页大小",
        default=10,
        nargs="?",
    )
    parser.add_argument("-sd", "--save_dir", type=str, help="图片保存目录", default=None)
    parser.add_argument("-d", "--delay", type=float, help="抓取延时（间隔）", default=0.05)
    args = parser.parse_args(arg_list)
    return args


def main(arg_list: Optional[List[str]] = None):
    args = parse_args(arg_list)

    crawler = Crawler(args.delay, save_dir=args.save_dir)

    # 抓取关键词为 “美女”，总数为 1 页（即总共 1*60=60 张），开始页码为 2
    crawler(args.word, args.total_page, args.start_page, args.per_page)


if __name__ == "__main__":
    main()
