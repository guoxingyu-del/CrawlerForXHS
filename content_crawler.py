from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class ContentCrawler:
    def __init__(self, browser_controller):
        self.browser = browser_controller
        self.driver = browser_controller.driver
        self.wait = browser_controller.wait
        self.max_posts = 10

    def crawl_homepage_posts(self):
        print(f"开始爬取首页前 {self.max_posts} 条帖子...")
        
        try:
            self._wait_for_homepage_load()
            posts = self._get_post_links()
            posts_content = []
            
            for i, post in enumerate(posts[:self.max_posts]):
                print(f"\n正在处理第 {i+1}/{self.max_posts} 条帖子...")
                try:
                    post_content = self._crawl_single_post(post, i)
                    if post_content:
                        posts_content.append(post_content)
                        print(f"第 {i+1} 条帖子爬取完成。")
                except Exception as e:
                    print(f"爬取第 {i+1} 条帖子失败: {e}")
                    continue
                
                if len(posts_content) >= self.max_posts:
                    break
            
            print(f"\n共成功爬取 {len(posts_content)} 条帖子。")
            return posts_content
            
        except Exception as e:
            print(f"爬取过程中出现错误: {e}")
            import traceback
            traceback.print_exc()
            return []

    def _wait_for_homepage_load(self):
        print("等待首页加载完成...")
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'note-item')] | //a[contains(@href, '/explore/')]"))
            )
            print("首页加载完成。")
            time.sleep(2)
        except Exception as e:
            print(f"等待首页加载超时: {e}")
            raise

    def _get_post_links(self):
        print("获取帖子链接...")
        try:
            post_links = self.driver.find_elements(
                By.XPATH, 
                "//a[contains(@href, '/explore/') or contains(@href, '/note/')]"
            )
            
            unique_links = []
            seen_hrefs = set()
            
            for link in post_links:
                href = link.get_attribute('href')
                if href and href not in seen_hrefs and ('/explore/' in href or '/note/' in href):
                    seen_hrefs.add(href)
                    unique_links.append(link)
            
            print(f"找到 {len(unique_links)} 条不同的帖子链接。")
            return unique_links
            
        except Exception as e:
            print(f"获取帖子链接失败: {e}")
            raise

    def _crawl_single_post(self, post_element, index):
        try:
            main_window = self.driver.current_window_handle
            href = post_element.get_attribute('href')
            
            if not href:
                print("帖子链接为空，跳过。")
                return None
            
            print(f"打开帖子: {href}")
            self.driver.execute_script(f"window.open('{href}', '_blank');")
            time.sleep(2)
            
            all_windows = self.driver.window_handles
            new_window = [w for w in all_windows if w != main_window][0]
            self.driver.switch_to.window(new_window)
            
            content = self._extract_post_content(href)
            
            self.driver.close()
            self.driver.switch_to.window(main_window)
            time.sleep(1)
            
            return content
            
        except Exception as e:
            print(f"处理帖子失败: {e}")
            try:
                all_windows = self.driver.window_handles
                if len(all_windows) > 1:
                    for window in all_windows[1:]:
                        self.driver.switch_to.window(window)
                        self.driver.close()
                    self.driver.switch_to.window(all_windows[0])
            except:
                pass
            return None

    def _extract_post_content(self, url):
        print("提取帖子内容...")
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'note-content') or contains(@class, 'detail')]"))
            )
            time.sleep(2)
            
            title = self._extract_title()
            content = self._extract_text_content()
            author = self._extract_author()
            
            post_data = {
                "url": url,
                "title": title,
                "author": author,
                "content": content
            }
            
            print(f"帖子标题: {title}")
            print(f"帖子作者: {author}")
            
            return post_data
            
        except Exception as e:
            print(f"提取帖子内容失败: {e}")
            return {
                "url": url,
                "title": "提取失败",
                "author": "未知",
                "content": f"提取内容时出错: {str(e)}"
            }

    def _extract_title(self):
        try:
            title_selectors = [
                "//div[contains(@class, 'title')]//h1 | //h1[contains(@class, 'title')]",
                "//div[contains(@class, 'note-title')]",
                "//h1"
            ]
            
            for selector in title_selectors:
                try:
                    title_element = self.driver.find_element(By.XPATH, selector)
                    title = title_element.text.strip()
                    if title:
                        return title
                except:
                    continue
            
            return "无标题"
        except:
            return "无标题"

    def _extract_text_content(self):
        try:
            content_selectors = [
                "//div[contains(@class, 'note-content')]//div[contains(@class, 'content')]",
                "//div[contains(@class, 'detail-content')]",
                "//div[contains(@class, 'note')]//div[not(contains(@class, 'title'))]",
                "//article//div[contains(@class, 'content')]"
            ]
            
            all_text = []
            
            for selector in content_selectors:
                try:
                    content_elements = self.driver.find_elements(By.XPATH, selector)
                    for element in content_elements:
                        text = element.text.strip()
                        if text and text not in all_text:
                            all_text.append(text)
                except:
                    continue
            
            if not all_text:
                try:
                    paragraph_elements = self.driver.find_elements(By.XPATH, "//p")
                    for p in paragraph_elements:
                        text = p.text.strip()
                        if text and len(text) > 10:
                            all_text.append(text)
                except:
                    pass
            
            return "\n\n".join(all_text) if all_text else "无内容"
        except Exception as e:
            return f"内容提取失败: {str(e)}"

    def _extract_author(self):
        try:
            author_selectors = [
                "//div[contains(@class, 'author')]//span[contains(@class, 'name')]",
                "//div[contains(@class, 'user-info')]//span[contains(@class, 'name')]",
                "//a[contains(@class, 'author')]//span",
                "//div[contains(@class, 'nickname')]"
            ]
            
            for selector in author_selectors:
                try:
                    author_element = self.driver.find_element(By.XPATH, selector)
                    author = author_element.text.strip()
                    if author:
                        return author
                except:
                    continue
            
            return "未知作者"
        except:
            return "未知作者"
