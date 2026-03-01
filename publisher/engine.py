# -*- coding: utf-8 -*-
"""
发布引擎模块
负责实际的内容发布
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
import random
from typing import Dict, Optional, Callable
from pathlib import Path

# 本地 Chromium 路径
CHROMIUM_PATH = r"E:\chrome-win\chrome.exe"


class PublishError(Exception):
    """发布异常"""
    pass


class Publisher:
    """发布器基类"""
    
    def __init__(self, cookie: str = None):
        self.cookie = cookie
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.max_retries = 2
        self.retry_delay = 2
        self.status_callback = None
    
    def set_status_callback(self, callback: Callable):
        """设置状态回调"""
        self.status_callback = callback
    
    def emit_status(self, message: str, level: str = 'info'):
        """发送状态更新"""
        if self.status_callback:
            self.status_callback(message, level)
        else:
            print(f'[{level.upper()}] {message}')
    
    def start(self, headless: bool = False):
        """启动浏览器"""
        try:
            self.emit_status('正在启动浏览器...')
            self.playwright = sync_playwright().start()
            
            self.browser = self.playwright.chromium.launch(
                headless=headless,
                executable_path=CHROMIUM_PATH,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--window-size=1920,1080'
                ]
            )
            
            # 创建上下文
            context_args = {
                'viewport': {'width': 1920, 'height': 1080},
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            if self.cookie:
                context_args['storage_state'] = self._parse_cookie(self.cookie)
            
            self.context = self.browser.new_context(**context_args)
            self.page = self.context.new_page()
            
            self.emit_status('浏览器启动成功')
            return True
        except Exception as e:
            self.emit_status(f'浏览器启动失败：{e}', 'error')
            raise PublishError(f'启动浏览器失败：{e}')
    
    def _parse_cookie(self, cookie_str: str) -> Dict:
        """解析 Cookie 字符串为 storage_state 格式"""
        try:
            # 尝试解析为 JSON 格式
            import json
            if cookie_str.startswith('{'):
                return json.loads(cookie_str)
        except:
            pass
        
        # 字符串格式，返回 None 让浏览器使用当前登录状态
        return None
    
    def close(self):
        """关闭浏览器"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            self.emit_status('浏览器已关闭')
        except Exception as e:
            self.emit_status(f'关闭浏览器出错：{e}', 'warning')
    
    def _human_delay(self, min_ms: int = 500, max_ms: int = 1500):
        """模拟人类操作延迟"""
        delay = random.uniform(min_ms, max_ms) / 1000
        time.sleep(delay)
    
    def _wait_for_element(self, selector: str, timeout: int = 10000):
        """等待元素出现"""
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            return True
        except PlaywrightTimeout:
            return False
    
    def _screenshot(self, name: str):
        """截图调试"""
        try:
            screenshot_dir = Path.home() / '.multi_platform_publisher' / 'screenshots'
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            self.page.screenshot(path=str(screenshot_dir / f'{name}.png'))
        except:
            pass
    
    def publish(self, content: Dict) -> bool:
        """发布内容（子类实现）"""
        raise NotImplementedError
    
    def publish_with_retry(self, content: Dict) -> bool:
        """带重试的发布"""
        for attempt in range(self.max_retries + 1):
            try:
                if attempt > 0:
                    self.emit_status(f'第 {attempt} 次重试...', 'warning')
                    time.sleep(self.retry_delay)
                
                result = self.publish(content)
                if result:
                    return True
            except Exception as e:
                self.emit_status(f'发布出错：{e}', 'error')
                if attempt == self.max_retries:
                    return False
        
        return False


class ZhihuPublisher(Publisher):
    """知乎发布器"""
    
    def publish(self, content: Dict) -> bool:
        """发布到知乎专栏"""
        try:
            self.start(headless=False)
            
            title = content.get('title', '')
            text_content = content.get('content', '')
            cover = content.get('cover')
            
            self.emit_status('正在访问知乎创作中心...')
            self.page.goto('https://zhuanlan.zhihu.com/write', wait_until='networkidle')
            
            # 等待页面加载
            time.sleep(3)
            
            # 检查是否已登录
            if 'login' in self.page.url.lower():
                self.emit_status('需要登录知乎，请手动登录', 'warning')
                self.emit_status('等待手动登录...（60 秒超时）', 'warning')
                try:
                    self.page.wait_for_url('https://zhuanlan.zhihu.com/write*', timeout=60000)
                except PlaywrightTimeout:
                    self.emit_status('登录超时', 'error')
                    return False
            
            self.emit_status('正在填写标题...')
            title_selector = 'input[placeholder*="标题"]'
            if self._wait_for_element(title_selector, 5000):
                title_input = self.page.query_selector(title_selector)
                if title_input:
                    title_input.fill('')
                    self._human_delay()
                    title_input.fill(title)
                    self._human_delay(1000, 2000)
            
            self.emit_status('正在填写内容...')
            editor_selector = 'div[contenteditable="true"]'
            if self._wait_for_element(editor_selector, 5000):
                editor = self.page.query_selector(editor_selector)
                if editor:
                    editor.click()
                    self._human_delay(500, 1000)
                    self.page.keyboard.press('Control+A')
                    self._human_delay(200, 500)
                    self.page.keyboard.press('Delete')
                    self._human_delay(500, 1000)
                    
                    paragraphs = text_content.split('\n\n')
                    for i, para in enumerate(paragraphs[:10]):
                        if para.strip():
                            self.page.keyboard.type(para.strip())
                            self._human_delay(100, 300)
                            if i < len(paragraphs) - 1:
                                self.page.keyboard.press('Enter')
                                self.page.keyboard.press('Enter')
                                self._human_delay(200, 500)
            
            if cover:
                self.emit_status('正在上传封面图...')
                cover_selector = 'input[type="file"][accept*="image"]'
                if self._wait_for_element(cover_selector, 5000):
                    file_input = self.page.query_selector(cover_selector)
                    if file_input:
                        file_input.set_input_files(cover)
                        self._human_delay(2000, 3000)
            
            self.emit_status('等待内容保存...')
            time.sleep(2)
            
            publish_selector = 'button:has-text("发布"), button:has-text("发表")'
            if self._wait_for_element(publish_selector, 5000):
                publish_btn = self.page.query_selector(publish_selector)
                if publish_btn:
                    self.emit_status('正在发布...')
                    publish_btn.click()
                    self._human_delay(2000, 3000)
                    time.sleep(3)
                    
                    if 'write' not in self.page.url.lower():
                        self.emit_status('知乎发布成功！', 'success')
                        return True
                    else:
                        self.emit_status('发布按钮已点击，等待跳转...', 'info')
                        time.sleep(2)
                        return True
            
            self.emit_status('未找到发布按钮', 'error')
            self._screenshot('zhihu_no_publish_btn')
            return False
            
        except Exception as e:
            self.emit_status(f'知乎发布失败：{e}', 'error')
            self._screenshot('zhihu_error')
            return False
        finally:
            self.close()


class XiaohongshuPublisher(Publisher):
    """小红书发布器"""
    
    def publish(self, content: Dict) -> bool:
        """发布到小红书"""
        try:
            self.start(headless=False)
            
            title = content.get('title', '')
            text_content = content.get('content', '')
            cover = content.get('cover')
            
            self.emit_status('正在访问小红书创作中心...')
            self.page.goto('https://creator.xiaohongshu.com/', wait_until='networkidle')
            time.sleep(3)
            
            if 'login' in self.page.url.lower() or '登录' in self.page.content():
                self.emit_status('需要登录小红书，请手动登录', 'warning')
                self.emit_status('等待手动登录...（60 秒超时）', 'warning')
                try:
                    self.page.wait_for_url('https://creator.xiaohongshu.com/*', timeout=60000)
                    time.sleep(2)
                except PlaywrightTimeout:
                    self.emit_status('登录超时', 'error')
                    return False
            
            self.emit_status('正在进入发布页面...')
            publish_link = 'a[href*="/publish"], button:has-text("发布"), button:has-text("创作")'
            if self._wait_for_element(publish_link, 10000):
                self.page.click(publish_link)
                time.sleep(3)
            
            time.sleep(2)
            
            if cover:
                self.emit_status('正在上传图片...')
                file_input = 'input[type="file"][accept*="image"]'
                if self._wait_for_element(file_input, 5000):
                    self.page.set_input_files(file_input, cover)
                    self._human_delay(3000, 5000)
            
            self.emit_status('正在填写标题...')
            title_input = 'input[placeholder*="标题"], input[placeholder*="填写标题"]'
            if self._wait_for_element(title_input, 5000):
                self.page.fill(title_input, title)
                self._human_delay(500, 1000)
            
            self.emit_status('正在填写内容...')
            content_input = 'div[contenteditable="true"], textarea[placeholder*="正文"]'
            if self._wait_for_element(content_input, 5000):
                editor = self.page.query_selector(content_input)
                if editor:
                    editor.click()
                    self._human_delay(500, 1000)
                    self.page.keyboard.type(text_content[:1000])
                    self._human_delay(1000, 2000)
            
            self.emit_status('等待内容保存...')
            time.sleep(2)
            
            publish_btn = 'button:has-text("发布笔记"), button:has-text("发表")'
            if self._wait_for_element(publish_btn, 5000):
                self.emit_status('正在发布...')
                self.page.click(publish_btn)
                self._human_delay(3000, 5000)
                time.sleep(3)
                self.emit_status('小红书发布完成！', 'success')
                return True
            
            self.emit_status('未找到发布按钮', 'error')
            self._screenshot('xiaohongshu_no_publish_btn')
            return False
            
        except Exception as e:
            self.emit_status(f'小红书发布失败：{e}', 'error')
            self._screenshot('xiaohongshu_error')
            return False
        finally:
            self.close()


class KuaishouPublisher(Publisher):
    """快手发布器"""
    
    def publish(self, content: Dict) -> bool:
        """发布到快手"""
        try:
            self.start(headless=False)
            
            title = content.get('title', '')
            text_content = content.get('content', '')
            
            self.emit_status('正在访问快手创作者平台...')
            self.page.goto('https://cp.kuaishou.com/', wait_until='networkidle')
            time.sleep(3)
            
            if 'login' in self.page.url.lower() or '登录' in self.page.content():
                self.emit_status('需要登录快手，请手动登录', 'warning')
                self.emit_status('等待手动登录...（60 秒超时）', 'warning')
                try:
                    self.page.wait_for_url('https://cp.kuaishou.com/*', timeout=60000)
                    time.sleep(2)
                except PlaywrightTimeout:
                    self.emit_status('登录超时', 'error')
                    return False
            
            self.emit_status('正在进入发布页面...')
            publish_link = 'a:has-text("发布作品"), button:has-text("发布"), button:has-text("上传")'
            if self._wait_for_element(publish_link, 10000):
                self.page.click(publish_link)
                time.sleep(3)
            
            time.sleep(2)
            
            self.emit_status('正在填写标题...')
            title_input = 'input[placeholder*="标题"], input[placeholder*="填写标题"]'
            if self._wait_for_element(title_input, 5000):
                self.page.fill(title_input, title[:50])
                self._human_delay(500, 1000)
            
            self.emit_status('正在填写描述...')
            desc_input = 'textarea[placeholder*="描述"], textarea[placeholder*="说说"]'
            if self._wait_for_element(desc_input, 5000):
                self.page.fill(desc_input, text_content[:500])
                self._human_delay(500, 1000)
            
            self.emit_status('等待内容保存...')
            time.sleep(2)
            
            publish_btn = 'button:has-text("发布"), button:has-text("发表"), button:has-text("下一步")'
            if self._wait_for_element(publish_btn, 5000):
                self.emit_status('正在发布...')
                self.page.click(publish_btn)
                self._human_delay(3000, 5000)
                time.sleep(2)
                
                confirm_btn = 'button:has-text("确认发布"), button:has-text("确定")'
                if self._wait_for_element(confirm_btn, 3000):
                    self.page.click(confirm_btn)
                    self._human_delay(2000, 3000)
                
                time.sleep(3)
                self.emit_status('快手发布完成！', 'success')
                return True
            
            self.emit_status('未找到发布按钮', 'error')
            self._screenshot('kuaishou_no_publish_btn')
            return False
            
        except Exception as e:
            self.emit_status(f'快手发布失败：{e}', 'error')
            self._screenshot('kuaishou_error')
            return False
        finally:
            self.close()


class DouyinPublisher(Publisher):
    """抖音发布器"""
    
    def publish(self, content: Dict) -> bool:
        """发布到抖音"""
        try:
            self.start(headless=False)
            
            title = content.get('title', '')
            text_content = content.get('content', '')
            
            self.emit_status('正在访问抖音创作者平台...')
            self.page.goto('https://creator.douyin.com/', wait_until='networkidle')
            time.sleep(3)
            
            if 'login' in self.page.url.lower() or '登录' in self.page.content():
                self.emit_status('需要登录抖音，请手动登录', 'warning')
                self.emit_status('等待手动登录...（60 秒超时）', 'warning')
                try:
                    self.page.wait_for_url('https://creator.douyin.com/*', timeout=60000)
                    time.sleep(2)
                except PlaywrightTimeout:
                    self.emit_status('登录超时', 'error')
                    return False
            
            self.emit_status('正在进入发布页面...')
            publish_link = 'a:has-text("发布视频"), button:has-text("发布"), button:has-text("上传")'
            if self._wait_for_element(publish_link, 10000):
                self.page.click(publish_link)
                time.sleep(3)
            
            time.sleep(2)
            
            self.emit_status('正在填写描述...')
            desc_input = 'textarea[placeholder*="填写标题"], textarea[placeholder*="作品描述"], textarea[placeholder*="说说"]'
            if self._wait_for_element(desc_input, 5000):
                self.page.fill(desc_input, f'{title}\n{text_content[:500]}')
                self._human_delay(500, 1000)
            
            self.emit_status('等待内容保存...')
            time.sleep(2)
            
            publish_btn = 'button:has-text("发布视频"), button:has-text("发布"), button:has-text("下一步")'
            if self._wait_for_element(publish_btn, 5000):
                self.emit_status('正在发布...')
                self.page.click(publish_btn)
                self._human_delay(3000, 5000)
                time.sleep(2)
                
                confirm_btn = 'button:has-text("确认发布"), button:has-text("确定"), button:has-text("发表")'
                if self._wait_for_element(confirm_btn, 3000):
                    self.page.click(confirm_btn)
                    self._human_delay(2000, 3000)
                
                time.sleep(3)
                self.emit_status('抖音发布完成！', 'success')
                return True
            
            self.emit_status('未找到发布按钮', 'error')
            self._screenshot('douyin_no_publish_btn')
            return False
            
        except Exception as e:
            self.emit_status(f'抖音发布失败：{e}', 'error')
            self._screenshot('douyin_error')
            return False
        finally:
            self.close()


def get_publisher(platform: str, cookie: str = None) -> Publisher:
    """获取发布器实例"""
    publishers = {
        'zhihu': ZhihuPublisher,
        'xiaohongshu': XiaohongshuPublisher,
        'kuaishou': KuaishouPublisher,
        'douyin': DouyinPublisher,
    }
    
    publisher_class = publishers.get(platform)
    if publisher_class:
        return publisher_class(cookie)
    else:
        raise ValueError(f'不支持的平台：{platform}')
