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
    
    def login_zhihu(self):
        """知乎扫码登录"""
        print('正在打开知乎登录页面...')
        self.page.goto('https://www.zhihu.com/signin', wait_until='networkidle')
        
        # 等待二维码出现
        print('请扫描屏幕上的二维码...')
        print('等待登录...')
        
        # 等待登录成功（检测用户头像）
        try:
            self.page.wait_for_selector('div.TopNav-profile', timeout=120000)
            print('✅ 登录成功！')
            
            # 获取 Cookie
            cookies = self.context.cookies()
            cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
            
            return True, cookie_str
        except:
            print('❌ 登录超时或失败')
            return False, ''
    
    def login_xiaohongshu(self):
        """小红书扫码登录"""
        print('正在打开小红书登录页面...')
        self.page.goto('https://www.xiaohongshu.com/login', wait_until='networkidle')
        
        # 等待二维码出现
        print('请扫描屏幕上的二维码...')
        print('等待登录...')
        
        # 等待登录成功（检测用户信息）
        try:
            self.page.wait_for_selector('div.user-info', timeout=120000)
            print('✅ 登录成功！')
            
            # 获取 Cookie
            cookies = self.context.cookies()
            cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
            
            return True, cookie_str
        except:
            print('❌ 登录超时或失败')
            return False, ''
    
    def login_kuaishou(self):
        """快手扫码登录"""
        print('正在打开快手登录页面...')
        self.page.goto('https://www.kuaishou.com/login', wait_until='networkidle')
        
        print('请扫描屏幕上的二维码...')
        print('等待登录...')
        
        try:
            # 等待登录成功
            self.page.wait_for_timeout(5000)  # 等待 5 秒
            cookies = self.context.cookies()
            
            # 检查是否有登录态
            if any(c['name'] == 'kpn' for c in cookies):
                print('✅ 登录成功！')
                cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
                return True, cookie_str
            
            print('❌ 登录超时或失败')
            return False, ''
        except:
            return False, ''
    
    def login_douyin(self):
        """抖音扫码登录"""
        print('正在打开抖音登录页面...')
        self.page.goto('https://www.douyin.com/login', wait_until='networkidle')
        
        print('请扫描屏幕上的二维码...')
        print('等待登录...')
        
        try:
            # 等待登录成功
            self.page.wait_for_timeout(5000)
            cookies = self.context.cookies()
            
            # 检查是否有登录态
            if any(c['name'] == 'passport_csrf_token' for c in cookies):
                print('✅ 登录成功！')
                cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
                return True, cookie_str
            
            print('❌ 登录超时或失败')
            return False, ''
        except:
            return False, ''
    
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
