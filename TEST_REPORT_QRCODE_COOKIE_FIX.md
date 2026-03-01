# 扫码登录 Cookie 过期问题修复报告

## 📋 问题描述

用户扫码登录成功后，提示"Cookie 已失效或过期"，扫码登录功能没有正确保存 Cookie 到数据库。

## 🔍 问题分析

### 根本原因

1. **Cookie 过滤缺失**：`qrcode_login.py` 中获取 Cookie 时，没有过滤已过期的 Cookie
   - Playwright 的 `context.cookies()` 返回所有 Cookie，包括已过期的
   - 过期的 Cookie 被保存到数据库，导致验证失败

2. **保存结果未检查**：`main_window_v2.py` 中调用 `cookie_manager.save_cookie()` 后，没有检查返回值
   - 即使保存失败，仍然显示"登录成功"
   - 没有进行后续的 Cookie 验证

### 问题文件

- `publisher/qrcode_login.py` - Cookie 获取逻辑
- `ui/main_window_v2.py` - UI 扫码登录实现

## ✅ 修复方案

### 1. 添加 Cookie 过滤功能 (`qrcode_login.py`)

新增 `_filter_valid_cookies()` 方法，过滤已过期的 Cookie：

```python
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
    
    for cookie in cookies:
        # 检查过期时间
        expires = cookie.get('expires', -1)
        
        # expires=-1 表示会话 Cookie（浏览器关闭后过期），保留
        # expires>current_time 表示未过期，保留
        # expires<=current_time 表示已过期，过滤掉
        if expires == -1 or expires > current_time:
            valid_cookies.append(f"{cookie['name']}={cookie['value']}")
    
    return '; '.join(valid_cookies)
```

### 2. 更新所有平台登录方法

在以下方法中应用 Cookie 过滤：
- `login_zhihu()` - 知乎扫码登录
- `login_xiaohongshu()` - 小红书扫码登录
- `login_kuaishou()` - 快手扫码登录
- `login_douyin()` - 抖音扫码登录

修改示例：
```python
# 修改前
cookies = self.context.cookies()
cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])

# 修改后
cookies = self.context.cookies()
# 过滤过期 Cookie
cookie_str = self._filter_valid_cookies(cookies)
print(f'获取到 {len(cookie_str.split(";"))} 个有效 Cookie')
```

### 3. 增强 UI 登录流程 (`main_window_v2.py`)

改进 `qrcode_login()` 方法，增加错误处理和验证：

```python
def qrcode_login(self):
    """扫码登录"""
    from publisher.qrcode_login import QRCodeLogin
    reply = QMessageBox.question(self, "扫码登录", "请用手机扫码登录", QMessageBox.Ok | QMessageBox.Cancel)
    if reply == QMessageBox.Cancel: return
    try:
        login_manager = QRCodeLogin()
        success, result = login_manager.login(self.platform)
        if success:
            from config import config
            # 保存到配置文件
            config.set_platform_cookie(self.platform, result)
            # 保存到 Cookie 管理器并检查结果
            save_success, save_message = cookie_manager.save_cookie(self.platform, result)
            if save_success:
                # 验证 Cookie
                is_valid, validate_message, user_info = cookie_manager.validate_cookie(self.platform)
                # 更新状态显示
                self.update_status(cookie_manager.get_cookie_status(self.platform))
                if is_valid:
                    QMessageBox.information(self, "登录成功", f"✅ {validate_message}")
                else:
                    QMessageBox.warning(self, "验证失败", f"⚠️ {validate_message}\n\nCookie 已保存，但验证失败。请检查网络连接或重新登录。")
            else:
                QMessageBox.critical(self, "保存失败", f"❌ {save_message}")
        else:
            QMessageBox.warning(self, "登录失败", result)
    except Exception as e:
        QMessageBox.critical(self, "错误", str(e))
```

## 📦 重新打包

已完成 EXE 重新打包：
- 打包工具：PyInstaller 6.3.0
- Python 版本：3.9.13
- 输出文件：`E:\openclaw-projects\multi-platform-publisher\dist\MultiPlatformPublisher\MultiPlatformPublisher.exe`
- 文件大小：2.5 MB

## 🧪 测试建议

### 手动测试流程

1. **启动程序**
   ```
   E:\openclaw-projects\multi-platform-publisher\dist\MultiPlatformPublisher\MultiPlatformPublisher.exe
   ```

2. **进入设置页面**
   - 点击"设置"标签页
   - 选择任意平台（知乎/小红书/快手/抖音）

3. **扫码登录**
   - 点击"📱 扫码登录"按钮
   - 使用手机扫描屏幕上的二维码
   - 等待登录成功

4. **验证结果**
   - 检查是否显示"登录成功"消息
   - 检查 Cookie 状态是否显示为"Cookie 有效"
   - 检查是否显示用户名
   - 点击"✓ 验证"按钮进行手动验证

5. **测试发布功能**
   - 返回"发布内容"标签页
   - 输入标题和内容
   - 选择已登录的平台
   - 点击"🚀 一键发布"
   - 验证发布是否成功

### 预期结果

✅ 扫码登录后显示"登录成功"并显示用户名
✅ Cookie 状态显示为"Cookie 有效"
✅ Cookie 剩余天数显示正确（7 天内）
✅ 发布功能正常工作

## 📝 修改文件清单

| 文件 | 修改内容 | 行数变化 |
|------|----------|----------|
| `publisher/qrcode_login.py` | 新增 `_filter_valid_cookies()` 方法，更新 4 个登录方法 | +40 |
| `ui/main_window_v2.py` | 改进 `qrcode_login()` 方法，增加错误处理和验证 | +15 |

## 🎯 修复效果

1. **Cookie 质量提升**：只保存未过期的有效 Cookie
2. **用户体验改善**：明确显示登录成功/失败原因
3. **错误处理增强**：保存失败时显示具体错误信息
4. **状态同步准确**：登录后立即验证并更新状态

## ⚠️ 注意事项

1. **首次使用**：需要确保 Playwright 浏览器已安装
   ```bash
   playwright install chromium
   ```

2. **网络要求**：扫码登录和 Cookie 验证需要网络连接

3. **Cookie 有效期**：Cookie 默认有效期为 7 天，过期后需要重新登录

4. **浏览器路径**：默认使用 `E:\chrome-win\chrome.exe`，如不存在则使用 Playwright 自带浏览器

## 📅 修复时间

- 修复完成时间：2026-03-02
- 修复人员：Developer Agent
- 测试状态：待用户手动测试

---

**备注**：由于自动化测试环境限制，建议用户手动测试扫码登录功能以验证修复效果。
