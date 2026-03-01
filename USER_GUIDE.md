# 📖 使用手册 - 多平台发布助手

## 🚀 快速开始

### 1. 安装依赖

**首次使用需要安装依赖**，有两种方式：

#### 方式一：自动安装（推荐）
```batch
cd E:\openclaw-projects\multi-platform-publisher
setup.bat
```

#### 方式二：手动安装
```batch
pip install -r requirements.txt
playwright install chromium
```

### 2. 启动应用

#### 方式一：直接运行
```batch
run.bat
```

#### 方式二：Python 运行
```batch
python app.py
```

### 3. 发布内容

1. **编写内容**
   - 输入标题
   - 使用 Markdown 编写正文
   - 点击「预览」查看效果

2. **选择封面**（可选）
   - 点击「选择图片」
   - 选择封面图片

3. **选择平台**
   - 勾选要发布的平台
   - 支持：知乎、小红书、快手、抖音

4. **一键发布**
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

### 平台选择

- **知乎** - 知乎专栏
- **小红书** - 小红书笔记
- **快手** - 快手作品
- **抖音** - 抖音作品

### 发布记录

- 查看历史发布记录
- 显示发布平台和时间
- 点击「清空历史」清除记录

---

## ⚠️ 注意事项

### 1. Cookie 配置

**当前版本需要手动配置各平台 Cookie**

1. 进入「⚙️ 设置」标签页
2. 填写对应平台的 Cookie
3. 保存配置

**如何获取 Cookie**：
- 登录对应平台
- 打开浏览器开发者工具（F12）
- 找到 Cookie 并复制

### 2. 发布限制

- 各平台有发布频率限制
- 请勿短时间内频繁发布
- 建议间隔 5-10 分钟

### 3. 内容规范

- 遵守各平台内容规范
- 不要发布违规内容
- 注意版权问题

---

## 🐛 常见问题

### Q1: 应用无法启动？
**A**: 检查 Python 是否安装，依赖是否完整
```batch
python --version
pip install -r requirements.txt
```

### Q2: 发布失败？
**A**: 检查 Cookie 是否有效，网络是否正常

### Q3: Markdown 预览不显示？
**A**: 检查 markdown 库是否安装
```batch
pip install markdown
```

### Q4: 打包成 EXE？
**A**: 运行打包脚本
```batch
python build.py
```

---

## 📞 技术支持

如有问题，请查看：
- README.md - 项目说明
- TEST_REPORT.md - 测试报告

---

**版本**: v1.0  
**更新日期**: 2026-03-01
