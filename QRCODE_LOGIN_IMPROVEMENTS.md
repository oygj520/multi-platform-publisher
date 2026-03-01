# 扫码登录功能改进建议

**生成时间**: 2026-01-11  
**基于**: QRCODE_LOGIN_TEST_REPORT.md

---

## 一、高优先级修复

### 1.1 改进快手/抖音登录检测 (P001)

**问题**: 当前仅等待 5 秒，可能导致登录失败误判

**修复方案**:

```python
# publisher/qrcode_login.py

def login_kuaishou(self):
    """快手扫码登录 - 改进版"""
    print('正在打开快手登录页面...')
    self.page.goto('https://www.kuaishou.com/login', wait_until='networkidle')
    
    print('请扫描屏幕上的二维码...')
    print('等待登录...')
    
    try:
        # 等待登录成功（检测用户头像或昵称）
        # 尝试多种可能的成功标识
        success_selectors = [
            'div.user-avatar',
            'div.user-name',
            'div.profile-info',
            'a[href^="/profile/"]'
        ]
        
        for selector in success_selectors:
            try:
                self.page.wait_for_selector(selector, timeout=30000)
                print(f'检测到登录成功标识：{selector}')
                break
            except:
                continue
        
        # 等待一小段时间确保 Cookie 完全设置
        self.page.wait_for_timeout(3000)
        
        cookies = self.context.cookies()
        
        # 检查是否有登录态
        login_cookies = ['kpn', 'kpf', 'did']
        has_login_cookie = any(c['name'] in login_cookies for c in cookies)
        
        if has_login_cookie and len(cookies) > 5:  # 确保有足够的 Cookie
            print('✅ 登录成功！')
            cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
            return True, cookie_str
        
        print('❌ 登录超时或失败')
        return False, ''
        
    except Exception as e:
        print(f'❌ 登录异常：{e}')
        return False, str(e)


def login_douyin(self):
    """抖音扫码登录 - 改进版"""
    print('正在打开抖音登录页面...')
    self.page.goto('https://www.douyin.com/login', wait_until='networkidle')
    
    print('请扫描屏幕上的二维码...')
    print('等待登录...')
    
    try:
        # 等待登录成功（检测用户头像或昵称）
        success_selectors = [
            'div.user-profile',
            'span.user-nickname',
            'img.user-avatar',
            'a[href^="/user/"]'
        ]
        
        for selector in success_selectors:
            try:
                self.page.wait_for_selector(selector, timeout=30000)
                print(f'检测到登录成功标识：{selector}')
                break
            except:
                continue
        
        # 等待一小段时间确保 Cookie 完全设置
        self.page.wait_for_timeout(3000)
        
        cookies = self.context.cookies()
        
        # 检查是否有登录态
        login_cookies = ['passport_csrf_token', 'passport_sid', 'uid_tt']
        has_login_cookie = any(c['name'] in login_cookies for c in cookies)
        
        if has_login_cookie and len(cookies) > 5:
            print('✅ 登录成功！')
            cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
            return True, cookie_str
        
        print('❌ 登录超时或失败')
        return False, ''
        
    except Exception as e:
        print(f'❌ 登录异常：{e}')
        return False, str(e)
```

### 1.2 添加异步登录支持 (P002)

**问题**: 扫码登录时 UI 可能阻塞

**修复方案**:

```python
# ui/main_window_v2.py

from PyQt5.QtCore import QThread, pyqtSignal

class QRCodeLoginWorker(QThread):
    """扫码登录工作线程"""
    
    status_signal = pyqtSignal(str)  # 状态消息
    finished_signal = pyqtSignal(bool, str)  # 成功标志，结果
    
    def __init__(self, platform: str):
        super().__init__()
        self.platform = platform
    
    def run(self):
        """执行扫码登录"""
        try:
            from publisher.qrcode_login import QRCodeLogin
            
            self.status_signal.emit('正在启动浏览器...')
            login_manager = QRCodeLogin()
            
            self.status_signal.emit('正在打开登录页面...')
            success, result = login_manager.login(self.platform)
            
            if success:
                self.status_signal.emit('登录成功，正在保存 Cookie...')
            else:
                self.status_signal.emit(f'登录失败：{result}')
            
            self.finished_signal.emit(success, result)
            
        except Exception as e:
            self.status_signal.emit(f'登录异常：{str(e)}')
            self.finished_signal.emit(False, str(e))


# 在 CookieStatusCard 类中修改 qrcode_login 方法
def qrcode_login(self):
    """扫码登录 - 异步版本"""
    from publisher.qrcode_login import QRCodeLogin
    
    print(f'\n========== 开始扫码登录：{self.platform} ==========')
    
    # 显示提示
    reply = QMessageBox.question(
        self,
        '扫码登录',
        f'即将打开浏览器窗口，请使用手机{self.platform_names.get(self.platform, self.platform)}扫码登录。\n\n点击「确定」继续',
        QMessageBox.Ok | QMessageBox.Cancel
    )
    
    if reply == QMessageBox.Cancel:
        return
    
    # 显示登录中状态
    self.status_text.setText('📱 正在启动浏览器...')
    self.status_text.setStyleSheet('color: #667eea; font-weight: 600;')
    self.qrcode_btn.setEnabled(False)
    self.validate_btn.setEnabled(False)
    self.edit_btn.setEnabled(False)
    
    # 创建工作线程
    self.login_worker = QRCodeLoginWorker(self.platform)
    self.login_worker.status_signal.connect(self.on_login_status)
    self.login_worker.finished_signal.connect(self.on_login_finished)
    self.login_worker.start()

def on_login_status(self, message: str):
    """登录状态更新"""
    self.status_text.setText(message)

def on_login_finished(self, success: bool, result: str):
    """登录完成"""
    # 恢复按钮
    self.qrcode_btn.setEnabled(True)
    self.validate_btn.setEnabled(True)
    self.edit_btn.setEnabled(True)
    
    if success:
        # 保存 Cookie
        from config import config
        from publisher.cookie_manager import cookie_manager
        
        config.set_platform_cookie(self.platform, result)
        cookie_manager.save_cookie(self.platform, result)
        
        # 更新状态
        status = cookie_manager.get_cookie_status(self.platform)
        self.update_status(status)
        
        QMessageBox.information(
            self,
            '登录成功',
            f'✅ {self.platform_names.get(self.platform, self.platform)} 登录成功！\n\nCookie 已自动保存。'
        )
    else:
        QMessageBox.warning(
            self,
            '登录失败',
            f'❌ 登录失败：{result}\n\n请重试。'
        )
```

---

## 二、中优先级优化

### 2.1 添加登录进度提示 (P003)

```python
# publisher/qrcode_login.py

def login_with_progress(self, platform, progress_callback=None):
    """
    带进度回调的扫码登录
    
    Args:
        platform: 平台名称
        progress_callback: 进度回调函数 (message: str)
    """
    def log(message):
        print(message)
        if progress_callback:
            progress_callback(message)
    
    try:
        log('正在启动浏览器...')
        self.start_browser()
        
        log('正在打开登录页面...')
        self.page.goto(self.LOGIN_URLS.get(platform), wait_until='networkidle')
        
        log('请扫描屏幕上的二维码...')
        log('等待登录确认...')
        
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
        
        log('正在关闭浏览器...')
        self.close_browser()
        
        return success, cookie
        
    except Exception as e:
        log(f'登录异常：{e}')
        self.close_browser()
        return False, str(e)
```

### 2.2 增强错误信息 (P004)

```python
# publisher/qrcode_login.py

def start_browser(self):
    """启动浏览器 - 增强错误处理"""
    try:
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=False,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
    except Exception as e:
        error_msg = f'浏览器启动失败：{str(e)}\n\n可能原因：\n'
        error_msg += '1. Playwright 未正确安装\n'
        error_msg += '2. 浏览器驱动缺失\n'
        error_msg += '3. 系统权限不足\n\n'
        error_msg += '请运行：playwright install chromium'
        raise Exception(error_msg)


def login_zhihu(self):
    """知乎扫码登录 - 增强错误处理"""
    print('正在打开知乎登录页面...')
    
    try:
        self.page.goto('https://www.zhihu.com/signin', wait_until='networkidle', timeout=30000)
    except Exception as e:
        if 'timeout' in str(e).lower():
            return False, '页面加载超时，请检查网络连接'
        elif 'net::ERR' in str(e):
            return False, '网络错误，无法访问知乎'
        else:
            return False, f'页面加载失败：{str(e)}'
    
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
    except Exception as e:
        if 'timeout' in str(e).lower():
            return False, '登录超时，请重新扫码'
        else:
            return False, f'登录失败：{str(e)}'
```

### 2.3 改进浏览器窗口显示 (P005)

```python
# publisher/qrcode_login.py

def start_browser(self):
    """启动浏览器 - 确保窗口可见"""
    try:
        self.playwright = sync_playwright().start()
        
        # 确保浏览器窗口可见
        self.browser = self.playwright.chromium.launch(
            headless=False,  # 必须为 False
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--start-maximized'  # 最大化窗口
            ]
        )
        
        self.context = self.browser.new_context(
            viewport={'width': 1280, 'height': 800}  # 设置合适的窗口大小
        )
        self.page = self.context.new_page()
        
        # 设置页面缩放
        self.page.set_viewport_size({'width': 1280, 'height': 800})
        
    except Exception as e:
        error_msg = f'浏览器启动失败：{str(e)}\n\n可能原因：\n'
        error_msg += '1. Playwright 未正确安装\n'
        error_msg += '2. 浏览器驱动缺失\n'
        error_msg += '3. 系统权限不足\n\n'
        error_msg += '请运行：playwright install chromium'
        raise Exception(error_msg)
```

---

## 三、低优先级改进

### 3.1 添加重试机制 (P008)

```python
# publisher/qrcode_login.py

def login(self, platform, max_retries=2):
    """
    扫码登录 - 带重试机制
    
    Args:
        platform: 平台名称
        max_retries: 最大重试次数
    
    Returns:
        (success, cookie): 是否成功，Cookie 字符串
    """
    retry_count = 0
    
    while retry_count <= max_retries:
        try:
            if retry_count > 0:
                print(f'\n重试第 {retry_count} 次...')
            
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
                self.close_browser()
                return False, f'不支持的平台：{platform}'
            
            self.close_browser()
            
            if success:
                return success, cookie
            else:
                # 登录失败，尝试重试
                retry_count += 1
                if retry_count <= max_retries:
                    print(f'登录失败，准备重试...')
                    time.sleep(2)
                else:
                    return False, cookie
                    
        except Exception as e:
            print(f'登录异常：{e}')
            self.close_browser()
            retry_count += 1
            if retry_count > max_retries:
                return False, str(e)
            time.sleep(2)
    
    return False, '多次重试后仍失败'
```

### 3.2 添加取消登录检测

```python
# publisher/qrcode_login.py

def login_zhihu(self):
    """知乎扫码登录 - 带取消检测"""
    print('正在打开知乎登录页面...')
    self.page.goto('https://www.zhihu.com/signin', wait_until='networkidle')
    
    # 等待二维码出现
    print('请扫描屏幕上的二维码...')
    print('等待登录...')
    print('提示：关闭浏览器窗口将取消登录')
    
    # 等待登录成功或取消
    try:
        # 使用 wait_for_function 检测页面是否关闭
        while True:
            # 检查页面是否还存活
            if not self.page.context:
                print('❌ 登录已取消')
                return False, '用户取消登录'
            
            # 检查是否登录成功
            if self.page.query_selector('div.TopNav-profile'):
                print('✅ 登录成功！')
                cookies = self.context.cookies()
                cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
                return True, cookie_str
            
            # 等待一小段时间
            self.page.wait_for_timeout(1000)
            
    except Exception as e:
        if 'closed' in str(e).lower() or 'target closed' in str(e).lower():
            print('❌ 登录已取消')
            return False, '用户取消登录'
        print('❌ 登录超时或失败')
        return False, str(e)
```

---

## 四、测试验证

### 4.1 单元测试

```python
# test_qrcode_login_unit.py

import unittest
from publisher.qrcode_login import QRCodeLogin


class TestQRCodeLogin(unittest.TestCase):
    
    def setUp(self):
        self.login_manager = QRCodeLogin()
    
    def tearDown(self):
        self.login_manager.close_browser()
    
    def test_browser_start(self):
        """测试浏览器启动"""
        self.login_manager.start_browser()
        self.assertIsNotNone(self.login_manager.browser)
        self.assertIsNotNone(self.login_manager.page)
    
    def test_login_urls(self):
        """测试登录 URL 配置"""
        expected_urls = {
            'zhihu': 'https://www.zhihu.com/signin',
            'xiaohongshu': 'https://www.xiaohongshu.com/login',
            'kuaishou': 'https://www.kuaishou.com/login',
            'douyin': 'https://www.douyin.com/login'
        }
        self.assertEqual(self.login_manager.LOGIN_URLS, expected_urls)
    
    def test_cookie_format(self):
        """测试 Cookie 格式"""
        # 这个测试需要实际登录，暂时跳过
        self.skipTest('需要实际登录')


if __name__ == '__main__':
    unittest.main()
```

### 4.2 手动测试清单

- [ ] 启动应用
- [ ] 进入设置页面
- [ ] 测试知乎扫码登录
  - [ ] 浏览器窗口正常打开
  - [ ] 登录页面正常加载
  - [ ] 扫码后正确获取 Cookie
  - [ ] Cookie 正确保存
  - [ ] 验证成功
- [ ] 测试小红书扫码登录
  - [ ] 同上
- [ ] 测试快手扫码登录
  - [ ] 同上
- [ ] 测试抖音扫码登录
  - [ ] 同上
- [ ] 测试取消登录
  - [ ] 关闭浏览器窗口
  - [ ] 应显示取消提示
- [ ] 测试登录超时
  - [ ] 不扫码等待超时
  - [ ] 应显示超时提示
- [ ] 测试网络异常
  - [ ] 断开网络
  - [ ] 应显示网络错误提示

---

## 五、实施计划

### 第一阶段（立即）
- [ ] 修复快手/抖音登录检测逻辑
- [ ] 确保浏览器窗口正确显示

### 第二阶段（本周）
- [ ] 添加异步登录支持
- [ ] 增强错误信息
- [ ] 添加登录进度提示

### 第三阶段（下周）
- [ ] 添加重试机制
- [ ] 添加取消登录检测
- [ ] 完善单元测试

### 第四阶段（长期）
- [ ] 集成 CI/CD
- [ ] 添加端到端测试
- [ ] 性能优化

---

*本改进建议基于代码审查和测试报告生成*  
*最后更新：2026-01-11*
