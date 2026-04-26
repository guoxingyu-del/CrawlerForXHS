#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书网页版爬虫
功能：
1. 用户登录（手机号+验证码）
2. 爬取首页前10条帖子的文字内容
3. 将结果输出到文件
"""

import sys
import time

from browser_controller import BrowserController
from login_handler import LoginHandler
from content_crawler import ContentCrawler
from result_writer import ResultWriter


class XHSCrawler:
    def __init__(self, headless=False, output_dir="results"):
        self.browser = BrowserController(headless=headless)
        self.login_handler = None
        self.content_crawler = None
        self.result_writer = ResultWriter(output_dir=output_dir)
        self.xiaohongshu_url = "https://www.xiaohongshu.com"

    def start(self):
        print("=" * 80)
        print("小红书网页版爬虫启动")
        print("=" * 80)

        try:
            print("\n[1/5] 初始化浏览器...")
            self.browser.init_browser()
            print("浏览器初始化完成。")

            print("\n[2/5] 打开小红书网站...")
            self.browser.open_url(self.xiaohongshu_url)
            print(f"已打开: {self.xiaohongshu_url}")
            time.sleep(3)

            print("\n[3/5] 处理登录流程...")
            self.login_handler = LoginHandler(self.browser)
            login_success = self.login_handler.handle_login()

            if not login_success:
                print("登录失败，程序终止。")
                return False

            print("\n[4/5] 爬取首页帖子内容...")
            time.sleep(3)
            self.content_crawler = ContentCrawler(self.browser)
            posts = self.content_crawler.crawl_homepage_posts()

            if not posts:
                print("未能爬取到任何帖子内容。")
                return False

            print("\n[5/5] 将结果写入文件...")
            output_file = self.result_writer.write_posts_to_file(posts, format="txt")
            if output_file:
                print(f"结果已保存到: {output_file}")
            
            output_file_json = self.result_writer.write_posts_to_file(posts, format="json")
            if output_file_json:
                print(f"JSON格式结果已保存到: {output_file_json}")

            print("\n" + "=" * 80)
            print("爬虫任务完成！")
            print("=" * 80)

            return True

        except Exception as e:
            print(f"\n爬虫过程中出现错误: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            print("\n正在关闭浏览器...")
            try:
                self.browser.close_browser()
                print("浏览器已关闭。")
            except:
                pass

    def run_interactive(self):
        print("\n欢迎使用小红书网页版爬虫！")
        print("本程序将帮助您：")
        print("1. 登录小红书账号")
        print("2. 爬取首页前10条帖子的文字内容")
        print("3. 将结果保存到文件中\n")

        print("注意事项：")
        print("- 请确保您的网络连接正常")
        print("- 请准备好您的手机号用于登录")
        print("- 登录过程中需要您输入收到的验证码")
        print("- 爬虫过程中请勿关闭浏览器窗口\n")

        input("按回车键开始...")

        return self.start()


def main():
    import argparse

    parser = argparse.ArgumentParser(description='小红书网页版爬虫')
    parser.add_argument('--headless', action='store_true', help='使用无头模式（不显示浏览器界面）')
    parser.add_argument('--output', '-o', default='results', help='输出目录路径')
    parser.add_argument('--interactive', '-i', action='store_true', help='使用交互模式')

    args = parser.parse_args()

    crawler = XHSCrawler(headless=args.headless, output_dir=args.output)

    if args.interactive:
        success = crawler.run_interactive()
    else:
        success = crawler.start()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
