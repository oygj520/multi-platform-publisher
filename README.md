# 🚀 多平台发布助手 v2.0

一个桌面级的多平台内容发布工具，支持一键发布到知乎、小红书、快手、抖音。

## ✨ 功能特性

### v2.0 新功能

- ✅ **实际发布逻辑** - 基于 Playwright 的浏览器自动化
- ✅ **Cookie 加密存储** - 使用 Fernet 加密，安全存储
- ✅ **可视化 Cookie 管理** - 直观的 Cookie 配置界面
- ✅ **错误处理机制** - 完善的异常捕获和重试
- ✅ **实时状态反馈** - 发布进度实时显示

### 基础功能

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

2. **配置 Cookie**
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

### 如何获取 Cookie

1. 使用浏览器登录对应平台
2. 按 F12 打开开发者工具
3. 切换到 Application/存储 → Cookies
4. 复制 Cookie 值（或整个 JSON）
5. 粘贴到应用的 Cookie 管理界面

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

### Q1: 应用无法启动？
**A**: 检查 Python 和依赖是否安装
```bash
python --version
pip install -r requirements.txt
```

### Q2: 发布失败？
**A**: 
1. 检查 Cookie 是否有效
2. 检查网络连接
3. 查看错误日志

### Q3: Cookie 如何获取？
**A**: 
1. 浏览器登录平台
2. F12 打开开发者工具
3. Application → Cookies
4. 复制 Cookie 值

### Q4: 浏览器无法启动？
**A**: 确认 Chromium 路径正确
```
E:\chrome-win\chrome.exe
```

### Q5: 打包成 EXE？
**A**: 
```bash
python build.py
```

---

## 📝 更新日志

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
**版本**: v2.0  
**测试状态**: ✅ 所有测试通过
