# 🚀 多平台发布助手 v2.0

> 一键发布内容到知乎、小红书、快手、抖音的桌面级工具

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/oygj520/multi-platform-publisher)
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-stable-green.svg)]()

---

## ✨ 功能特性

### 🎯 V2.0 核心功能

| 功能 | 状态 | 说明 |
|------|------|------|
| **扫码登录** | ✅ 新增 | 手机扫码快速获取 Cookie，无需手动操作 |
| Playwright 自动化 | ✅ 已完成 | 基于本地 Chromium 的浏览器自动化 |
| Cookie 加密存储 | ✅ 已完成 | Fernet 加密，SQLite 存储 |
| Cookie 在线验证 | ✅ 已完成 | 实时验证 Cookie 有效性 |
| 错误重试机制 | ✅ 已完成 | 自动重试 3 次，智能错误处理 |
| 实时状态反馈 | ✅ 已完成 | 发布进度实时显示 |

### 📋 平台支持

| 平台 | 类型 | 状态 | 备注 |
|------|------|------|------|
| 知乎 | 专栏文章 | ✅ 完全支持 | 支持标题、内容、封面 |
| 小红书 | 图文笔记 | ✅ 完全支持 | 支持标题、内容、图片 |
| 快手 | 图文/视频 | 🟡 部分支持 | 主要以视频为主 |
| 抖音 | 图文/视频 | 🟡 部分支持 | 主要以视频为主 |

### 基础功能

- ✅ **扫码登录** - 手机扫码快速获取 Cookie（新增 ⭐）
- ✅ **Markdown 编辑器** - 支持实时预览
- ✅ **封面图上传** - 拖拽选择图片
- ✅ **多平台选择** - 知乎、小红书、快手、抖音
- ✅ **一键发布** - 自动发布到多个平台
- ✅ **发布记录** - 历史记录查看

---

## 🛠️ 安装

### 1. 安装 Python 3.9+

```bash
python --version
```

### 2. 克隆项目

```bash
cd E:\openclaw-projects
git clone <repository-url> multi-platform-publisher
cd multi-platform-publisher
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 准备 Chromium 浏览器

下载 Chromium 到 `E:\chrome-win\chrome.exe`

或使用 Playwright 自动下载：
```bash
playwright install chromium
```

### 5. 运行应用

```bash
python app.py
```

或双击 `run.bat`

---

## 📖 使用说明

### 快速开始

1. **打开应用**
   - 运行 `run.bat` 或 `python app.py`

2. **配置 Cookie**（两种方式）
   
   **方式一：扫码登录（推荐 ⭐）**
   - 进入「Cookie 管理」标签页
   - 选择对应平台
   - 点击「扫码登录」按钮
   - 使用手机 APP 扫描二维码
   - 等待登录成功提示
   
   **方式二：手动配置**
   - 进入「Cookie 管理」标签页
   - 点击对应平台的「编辑」按钮
   - 粘贴 Cookie 数据并保存

3. **编写内容**
   - 在编辑器中输入标题和内容
   - 选择封面图片（可选）

4. **选择平台**
   - 勾选要发布的平台

5. **一键发布**
   - 点击「🚀 一键发布」按钮
   - 等待发布完成

### 📱 扫码登录

**支持平台**：知乎、小红书、快手、抖音

**使用步骤**：
```
1. 点击「扫码登录」按钮
         ↓
2. 等待浏览器弹出，显示二维码
         ↓
3. 用手机 APP 扫描二维码
         ↓
4. 在手机上确认登录
         ↓
5. Cookie 自动保存，完成！
```

**各平台扫码入口**：
| 平台 | 手机 APP 扫码入口 |
|------|-----------------|
| 知乎 | 知乎 APP → 首页右上角扫一扫 |
| 小红书 | 小红书 APP → 首页左上角扫一扫 |
| 快手 | 快手 APP → 首页左上角扫一扫 |
| 抖音 | 抖音 APP → 首页右上角扫一扫 |

> 💡 **优势**：无需手动复制 Cookie，30 秒内完成，新手友好

### 🔧 手动获取 Cookie

如果扫码登录不可用，可以手动获取：

1. 使用浏览器登录对应平台
2. 按 F12 打开开发者工具
3. 切换到 Application/存储 → Cookies
4. 复制 Cookie 值（或整个 JSON）
5. 粘贴到应用的 Cookie 管理界面

详细步骤请参考 `USER_GUIDE.md`

---

## 📁 项目结构

```
multi-platform-publisher/
├── app.py                      # 主程序入口
├── config.py                   # 配置管理
├── requirements.txt            # 依赖列表
├── run.bat                     # 启动脚本
├── build.py                    # 打包脚本
├── test_engine.py              # 测试脚本
├── README.md                   # 本文件
├── USER_GUIDE.md               # 使用手册
├── TEST_REPORT_V2.md           # 测试报告
├── publisher/
│   ├── engine.py               # 发布引擎
│   └── cookie_manager.py       # Cookie 管理
├── ui/
│   └── main_window.py          # 主窗口界面
└── dist/                       # 打包输出
```

---

## 🔧 技术栈

- **Python 3.9+** - 编程语言
- **PyQt5** - GUI 框架
- **Playwright** - 浏览器自动化
- **cryptography** - Cookie 加密
- **SQLite3** - 数据存储

---

## ⚠️ 注意事项

1. **Cookie 安全**
   - Cookie 使用 Fernet 加密存储
   - 请妥善保管，不要分享给他人
   - 定期更新 Cookie

2. **发布限制**
   - 各平台有发布频率限制
   - 请勿短时间内频繁发布
   - 建议间隔 5-10 分钟

3. **内容规范**
   - 遵守各平台内容规范
   - 不要发布违规内容
   - 注意版权问题

4. **浏览器要求**
   - 需要 Chromium 浏览器
   - 路径：`E:\chrome-win\chrome.exe`
   - 或使用 Playwright 自动下载

---

## 🐛 常见问题

### 📱 扫码登录相关

### Q1: 扫码登录按钮点击后无反应？
**A**: 
1. 检查 Playwright 是否正确安装：`playwright install chromium`
2. 确认浏览器路径正确：`E:\chrome-win\chrome.exe`
3. 重启应用后重试

### Q2: 二维码不显示？
**A**: 
1. 检查网络连接是否正常
2. 尝试手动访问平台网站
3. 关闭浏览器窗口，重新扫码
4. 如仍不行，使用手动配置 Cookie 方式

### Q3: 扫码后提示登录超时？
**A**: 
1. 二维码有效期约 60 秒，超时请刷新
2. 扫码后及时在手机上确认
3. 检查手机和电脑的网络连接

### Q4: 如何切换账号？
**A**: 
1. 进入 Cookie 管理页面
2. 点击对应平台的「扫码登录」
3. 使用新账号扫码即可

---

### 🔧 其他问题

### Q5: 应用无法启动？
**A**: 检查 Python 和依赖是否安装
```bash
python --version
pip install -r requirements.txt
```

### Q6: 发布失败？
**A**: 
1. 检查 Cookie 是否有效
2. 检查网络连接
3. 查看错误日志

### Q7: Cookie 如何获取？
**A**: 
**方式一（推荐）**：使用扫码登录功能

**方式二**：
1. 浏览器登录平台
2. F12 打开开发者工具
3. Application → Cookies
4. 复制 Cookie 值

### Q8: 浏览器无法启动？
**A**: 确认 Chromium 路径正确
```
E:\chrome-win\chrome.exe
```

### Q9: 打包成 EXE？
**A**: 
```bash
python build.py
```

---

**更多问题**请参考 `USER_GUIDE.md` 和 `QR_CODE_LOGIN.md`

---

## 📝 更新日志

### v2.1 (2026-03-01)
- ✨ **新增扫码登录功能** - 支持知乎/小红书/快手/抖音
- ✨ 自动获取并保存 Cookie
- ✨ 手机扫码，无需手动操作
- ✨ 新增快速入门指南
- ✨ 新增功能说明文档

### v2.0 (2026-03-01)
- ✨ 实现实际发布逻辑（知乎/小红书/快手/抖音）
- ✨ Cookie 加密存储和管理
- ✨ 可视化 Cookie 配置界面
- ✨ 错误处理和重试机制
- ✨ 实时状态反馈
- ✨ 完善测试套件

### v1.0 (2026-03-01)
- ✨ 项目创建
- ✨ Markdown 编辑器
- ✨ 多平台选择
- ✨ 一键发布功能（模拟）
- ✨ 发布记录

---

## 📄 许可证

MIT License

---

**开发时间**: 2026-03-01  
**版本**: v2.1  
**测试状态**: ✅ 所有测试通过

**相关文档**:
- 📖 使用手册：`USER_GUIDE.md`
- 🚀 快速入门：`QUICK_START.md`
- 📱 扫码登录说明：`QR_CODE_LOGIN.md`
