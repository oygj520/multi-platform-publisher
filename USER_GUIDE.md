# 📖 使用手册 - 多平台发布助手 v2.0

## 🚀 快速开始

### 1. 安装依赖

**首次使用需要安装依赖**：

```batch
cd E:\openclaw-projects\multi-platform-publisher
pip install -r requirements.txt
```

### 2. 准备浏览器

确保 Chromium 浏览器在以下路径：
```
E:\chrome-win\chrome.exe
```

如果还没有，可以：
- 手动下载 Chromium 到该位置
- 或使用 Playwright 自动下载：`playwright install chromium`

### 3. 启动应用

```batch
run.bat
```

或：
```batch
python app.py
```

### 4. 配置 Cookie

**首次使用必须配置 Cookie**：

1. 进入「Cookie 管理」标签页
2. 点击对应平台的「编辑」按钮
3. 粘贴 Cookie 数据
4. 点击「保存 Cookie」

### 5. 发布内容

1. **编写内容**
   - 输入标题
   - 使用 Markdown 编写正文
   - 选择封面图片（可选）

2. **选择平台**
   - 勾选要发布的平台

3. **一键发布**
   - 点击「🚀 一键发布」
   - 等待发布完成

---

## ⚙️ 功能说明

### Markdown 编辑器

支持标准 Markdown 语法：

```markdown
# 一级标题
## 二级标题

**粗体** *斜体*

- 列表项 1
- 列表项 2

[链接](https://example.com)

![图片](image.jpg)
```

### Cookie 管理

#### 如何获取 Cookie

**知乎**:
1. 访问 https://www.zhihu.com
2. 登录账号
3. F12 打开开发者工具
4. Application → Cookies → https://www.zhihu.com
5. 右键 → Copy All

**小红书**:
1. 访问 https://www.xiaohongshu.com
2. 登录账号
3. F12 → Application → Cookies
4. 复制 Cookie 值

**快手**:
1. 访问 https://www.kuaishou.com
2. 登录账号
3. F12 → Application → Cookies
4. 复制 Cookie 值

**抖音**:
1. 访问 https://www.douyin.com
2. 登录账号
3. F12 → Application → Cookies
4. 复制 Cookie 值

#### Cookie 格式

支持两种格式：

1. **字符串格式**:
```
key1=value1; key2=value2; key3=value3
```

2. **JSON 格式**:
```json
[
  {"name": "key1", "value": "value1", "domain": ".zhihu.com"},
  {"name": "key2", "value": "value2", "domain": ".zhihu.com"}
]
```

### 发布流程

1. **启动浏览器** - 自动打开 Chromium
2. **加载 Cookie** - 使用配置的 Cookie 登录
3. **访问创作中心** - 导航到对应平台
4. **填写内容** - 自动填写标题和正文
5. **上传图片** - 上传封面图片（如有）
6. **点击发布** - 提交发布
7. **等待完成** - 确认发布成功

---

## ⚠️ 注意事项

### 1. Cookie 安全

- ✅ Cookie 使用 Fernet 加密存储
- ✅ 存储位置：`~/.multi_platform_publisher/cookies.db`
- ✅ 加密密钥：`~/.multi_platform_publisher/.key`
- ❌ 不要分享 Cookie 给他人
- ❌ 不要在公共电脑上使用

### 2. 发布限制

| 平台 | 建议间隔 | 注意事项 |
|-----|---------|---------|
| 知乎 | 5-10 分钟 | 避免短时间大量发布 |
| 小红书 | 10-15 分钟 | 注意内容质量 |
| 快手 | 10-15 分钟 | 视频内容优先 |
| 抖音 | 10-15 分钟 | 视频内容优先 |

### 3. 内容规范

- 遵守各平台内容规范
- 不要发布违规内容
- 注意版权问题
- 避免敏感话题

### 4. 网络要求

- 需要稳定的网络连接
- 建议使用国内网络
- 某些平台可能需要特殊网络环境

---

## 🐛 常见问题

### Q1: 应用无法启动？

**检查 Python 环境**:
```bash
python --version
pip list | findstr PyQt5
pip list | findstr playwright
```

**重新安装依赖**:
```bash
pip install -r requirements.txt --force-reinstall
```

### Q2: 发布失败？

**检查 Cookie**:
1. 进入 Cookie 管理页面
2. 检查 Cookie 是否有效
3. 重新获取并保存 Cookie

**检查网络**:
1. 确认网络连接正常
2. 尝试访问对应平台网站

**查看日志**:
- 控制台会输出详细错误信息
- 截图保存错误信息便于排查

### Q3: 浏览器无法启动？

**检查 Chromium 路径**:
```
E:\chrome-win\chrome.exe
```

**确认文件存在**:
- 打开文件资源管理器
- 导航到 E:\chrome-win\
- 确认 chrome.exe 存在

**重新下载 Chromium**:
```bash
playwright install chromium
```

### Q4: Cookie 保存后仍然发布失败？

**可能原因**:
1. Cookie 已过期 - 重新获取 Cookie
2. Cookie 格式错误 - 检查格式
3. 平台要求额外验证 - 手动登录一次

**解决方法**:
1. 删除旧 Cookie
2. 重新登录平台
3. 获取新的 Cookie
4. 保存并测试

### Q5: 发布过程中浏览器被关闭？

**可能原因**:
- 网络超时
- 平台检测到自动化操作
- 系统资源不足

**解决方法**:
1. 检查网络连接
2. 降低发布频率
3. 关闭其他占用资源的程序

### Q6: 如何清空所有数据？

**删除配置目录**:
```
~/.multi_platform_publisher/
```

Windows 路径：
```
C:\Users\<用户名>\.multi_platform_publisher\
```

---

## 📞 技术支持

### 日志位置

- **Cookie 数据库**: `~/.multi_platform_publisher/cookies.db`
- **加密密钥**: `~/.multi_platform_publisher/.key`
- **截图文件**: `~/.multi_platform_publisher/screenshots/`

### 获取帮助

1. 查看测试报告：`TEST_REPORT_V2.md`
2. 查看项目说明：`README.md`
3. 检查控制台输出

---

## 📊 版本信息

| 项目 | 信息 |
|-----|------|
| 版本 | v2.0 |
| 更新日期 | 2026-03-01 |
| Python | 3.9+ |
| PyQt5 | 5.15.11 |
| Playwright | 1.58.0 |

---

**提示**: 首次使用建议先用测试账号进行发布测试，熟悉流程后再使用正式账号。
