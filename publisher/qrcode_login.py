# -*- coding: utf-8 -*-
"""
扫码登录模块
支持各平台扫码登录获取 Cookie
"""

import sys
import time
from playwright.sync_api import sync_playwright


class QRCodeLogin:
    """扫码登录管理器"""
    
    # 各平台登录 URL
    LOGIN_URLS = {
        'zhihu': 'https://www.zhihu.com/signin',
        'xiaohongshu': 'https://www.xiaohongshu.com/login',
        'kuaishou': 'https://www.kuaishou.com/login',
        'douyin': 'https://www.douyin.com/login'
    }
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
    
    def start_browser(self):
        """启动浏览器"""
        self.playwright = sync_playwright().start()
        
        # 使用本地 Chromium 浏览器
        local_chrome_path = r'E:\chrome-win\chrome.exe'
        
        try:
            self.browser = self.playwright.chromium.launch(
                headless=False,
                executable_path=local_chrome_path,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
        except Exception as e:
            # 如果本地浏览器不存在，使用 Playwright 自带的
            print(f"本地浏览器启动失败：{e}，尝试使用 Playwright 浏览器...")
            self.browser = self.playwright.chromium.launch(
                headless=False,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
        
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
    
    def close_browser(self):
        """关闭浏览器"""
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except:
            pass
    
    def _filter_valid_cookies(self, cookies):
        """
        过滤有效的 Cookie（未过期）
        
        Args:
            cookies: Playwright Cookie 列表
        
        Returns:
            过滤后的 Cookie 字符串
        """
        import time
        current_time = time.time()
        valid_cookies = []
        expired_count = 0
        
        print(f'[DEBUG] 获取到原始 Cookie 数量：{len(cookies)}')
        
        for cookie in cookies:
            # 检查过期时间
            expires = cookie.get('expires', -1)
            name = cookie.get('name', 'unknown')
            
            # expires=-1 表示会话 Cookie（浏览器关闭后过期），保留
            # expires>current_time 表示未过期，保留
            # expires<=current_time 表示已过期，过滤掉
            if expires == -1 or expires > current_time:
                valid_cookies.append(f"{cookie['name']}={cookie['value']}")
                if expires == -1:
                    print(f'[DEBUG] ✓ 会话 Cookie: {name}')
                else:
                    expiry_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expires))
                    print(f'[DEBUG] ✓ 有效 Cookie: {name} (过期：{expiry_str})')
            else:
                expired_count += 1
                expiry_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expires))
                print(f'[DEBUG] ✗ 已过期 Cookie: {name} (过期：{expiry_str})')
        
        print(f'[DEBUG] 过滤后有效 Cookie 数量：{len(valid_cookies)} (过期：{expired_count})')
        return '; '.join(valid_cookies)
    
    def login_zhihu(self):
        """知乎扫码登录"""
        print('正在打开知乎登录页面...')
        try:
            self.page.goto('https://www.zhihu.com/signin', wait_until='domcontentloaded', timeout=30000)
            
            # 等待二维码出现
            print('请扫描屏幕上的二维码...')
            print('等待登录（最多 120 秒）...')
            
            # 等待登录成功（检测用户头像），设置超时
            import time
            start_time = time.time()
            max_wait = 120  # 最多等待 120 秒
            login_detected_time = None
            
            while time.time() - start_time < max_wait:
                try:
                    # 检查是否登录成功
                    if self.page.query_selector('div.TopNav-profile'):
                        login_detected_time = time.time()
                        print(f'✅ 检测到登录成功！耗时：{login_detected_time - start_time:.1f}秒')
                        
                        # 等待 5 秒让 Cookie 完全生效
                        print('⏳ 等待 Cookie 生效（5 秒）...')
                        time.sleep(5)
                        
                        cookies = self.context.cookies()
                        print(f'[DEBUG] 登录成功后获取到 {len(cookies)} 个原始 Cookie')
                        
                        # 过滤过期 Cookie
                        cookie_str = self._filter_valid_cookies(cookies)
                        valid_count = len(cookie_str.split(';')) if cookie_str else 0
                        print(f'✅ 获取到 {valid_count} 个有效 Cookie')
                        
                        if not cookie_str or valid_count == 0:
                            print('[WARNING] 过滤后没有有效 Cookie，尝试返回原始 Cookie')
                            cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
                        
                        return True, cookie_str
                    time.sleep(2)  # 每 2 秒检查一次
                except Exception as e:
                    print(f'[DEBUG] 检查登录状态时出错：{e}')
                    continue
            
            print('❌ 登录超时')
            return False, '登录超时，请重试'
            
        except Exception as e:
            print(f'❌ 登录失败：{e}')
            return False, str(e)
    
    def login_xiaohongshu(self):
        """小红书扫码登录"""
        print('正在打开小红书登录页面...')
        try:
            self.page.goto('https://www.xiaohongshu.com/login', wait_until='domcontentloaded', timeout=30000)
            
            print('请扫描屏幕上的二维码...')
            print('等待登录（最多 120 秒）...')
            
            import time
            start_time = time.time()
            max_wait = 120
            login_detected_time = None
            
            while time.time() - start_time < max_wait:
                try:
                    if self.page.query_selector('div.user-info') or self.page.query_selector('[class*="user"]'):
                        login_detected_time = time.time()
                        print(f'✅ 检测到登录成功！耗时：{login_detected_time - start_time:.1f}秒')
                        
                        # 等待 5 秒让 Cookie 完全生效
                        print('⏳ 等待 Cookie 生效（5 秒）...')
                        time.sleep(5)
                        
                        cookies = self.context.cookies()
                        print(f'[DEBUG] 登录成功后获取到 {len(cookies)} 个原始 Cookie')
                        
                        # 过滤过期 Cookie
                        cookie_str = self._filter_valid_cookies(cookies)
                        valid_count = len(cookie_str.split(';')) if cookie_str else 0
                        print(f'✅ 获取到 {valid_count} 个有效 Cookie')
                        
                        if not cookie_str or valid_count == 0:
                            print('[WARNING] 过滤后没有有效 Cookie，尝试返回原始 Cookie')
                            cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
                        
                        return True, cookie_str
                    time.sleep(2)
                except Exception as e:
                    print(f'[DEBUG] 检查登录状态时出错：{e}')
                    continue
            
            print('❌ 登录超时')
            return False, '登录超时，请重试'
            
        except Exception as e:
            print(f'❌ 登录失败：{e}')
            return False, str(e)
    
    def login_kuaishou(self):
        """快手扫码登录"""
        print('正在打开快手登录页面...')
        try:
            self.page.goto('https://www.kuaishou.com/login', wait_until='domcontentloaded', timeout=30000)
            
            print('请扫描屏幕上的二维码...')
            print('等待登录（最多 120 秒）...')
            
            import time
            start_time = time.time()
            max_wait = 120
            login_detected_time = None
            
            while time.time() - start_time < max_wait:
                try:
                    cookies = self.context.cookies()
                    if any(c['name'] == 'kpn' for c in cookies):
                        login_detected_time = time.time()
                        print(f'✅ 检测到登录成功！耗时：{login_detected_time - start_time:.1f}秒')
                        print(f'[DEBUG] 检测到 kpn Cookie，数量：{len(cookies)}')
                        
                        # 等待 5 秒让 Cookie 完全生效
                        print('⏳ 等待 Cookie 生效（5 秒）...')
                        time.sleep(5)
                        
                        cookies = self.context.cookies()
                        print(f'[DEBUG] 登录成功后获取到 {len(cookies)} 个原始 Cookie')
                        
                        # 过滤过期 Cookie
                        cookie_str = self._filter_valid_cookies(cookies)
                        valid_count = len(cookie_str.split(';')) if cookie_str else 0
                        print(f'✅ 获取到 {valid_count} 个有效 Cookie')
                        
                        if not cookie_str or valid_count == 0:
                            print('[WARNING] 过滤后没有有效 Cookie，尝试返回原始 Cookie')
                            cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
                        
                        return True, cookie_str
                    time.sleep(2)
                except Exception as e:
                    print(f'[DEBUG] 检查登录状态时出错：{e}')
                    continue
            
            print('❌ 登录超时')
            return False, '登录超时，请重试'
            
        except Exception as e:
            print(f'❌ 登录失败：{e}')
            return False, str(e)
    
    def login_douyin(self):
        """抖音扫码登录"""
        print('正在打开抖音登录页面...')
        try:
            self.page.goto('https://www.douyin.com/login', wait_until='domcontentloaded', timeout=30000)
            
            print('请扫描屏幕上的二维码...')
            print('等待登录（最多 120 秒）...')
            
            import time
            start_time = time.time()
            max_wait = 120
            login_detected_time = None
            
            while time.time() - start_time < max_wait:
                try:
                    cookies = self.context.cookies()
                    if any(c['name'] in ['passport_csrf_token', 'sessionid'] for c in cookies):
                        login_detected_time = time.time()
                        print(f'✅ 检测到登录成功！耗时：{login_detected_time - start_time:.1f}秒')
                        print(f'[DEBUG] 检测到关键 Cookie: {[c["name"] for c in cookies if c["name"] in ["passport_csrf_token", "sessionid"]]}')
                        
                        # 等待 5 秒让 Cookie 完全生效
                        print('⏳ 等待 Cookie 生效（5 秒）...')
                        time.sleep(5)
                        
                        cookies = self.context.cookies()
                        print(f'[DEBUG] 登录成功后获取到 {len(cookies)} 个原始 Cookie')
                        
                        # 过滤过期 Cookie
                        cookie_str = self._filter_valid_cookies(cookies)
                        valid_count = len(cookie_str.split(';')) if cookie_str else 0
                        print(f'✅ 获取到 {valid_count} 个有效 Cookie')
                        
                        if not cookie_str or valid_count == 0:
                            print('[WARNING] 过滤后没有有效 Cookie，尝试返回原始 Cookie')
                            cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
                        
                        return True, cookie_str
                    time.sleep(2)
                except Exception as e:
                    print(f'[DEBUG] 检查登录状态时出错：{e}')
                    continue
            
            print('❌ 登录超时')
            return False, '登录超时，请重试'
            
        except Exception as e:
            print(f'❌ 登录失败：{e}')
            return False, str(e)
    
    def login(self, platform):
        """
        扫码登录
        
        Args:
            platform: 平台名称 (zhihu/xiaohongshu/kuaishou/douyin)
        
        Returns:
            (success, cookie): 是否成功，Cookie 字符串
        """
        try:
            self.start_browser()
            
            if platform == 'zhihu':
                success, cookie = self.login_zhihu()
            elif platform == 'xiaohongshu':
                success, cookie = self.login_xiaohongshu()
            elif platform == 'kuaishou':
                success, cookie = self.login_kuaishou()
            elif platform == 'douyin':
                success, cookie = self.login_douyin()
            else:
                return False, f'不支持的平台：{platform}'
            
            self.close_browser()
            return success, cookie
            
        except Exception as e:
            print(f'登录异常：{e}')
            self.close_browser()
            return False, str(e)


# 使用示例
if __name__ == '__main__':
    login_manager = QRCodeLogin()
    
    print('=== 扫码登录测试 ===')
    print('1. 知乎')
    print('2. 小红书')
    print('3. 快手')
    print('4. 抖音')
    
    choice = input('请选择平台 (1-4): ')
    
    platforms = {
        '1': 'zhihu',
        '2': 'xiaohongshu',
        '3': 'kuaishou',
        '4': 'douyin'
    }
    
    platform = platforms.get(choice)
    if not platform:
        print('无效选择')
        sys.exit(1)
    
    success, cookie = login_manager.login(platform)
    
    if success:
        print(f'\n✅ 登录成功！')
        print(f'Cookie 长度：{len(cookie)}')
        print(f'Cookie: {cookie[:100]}...')
    else:
        print(f'\n❌ 登录失败：{cookie}')
