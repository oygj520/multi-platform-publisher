# -*- coding: utf-8 -*-
"""
主窗口界面 - 现代化设计版本
设计风格：现代极简 + Material Design 3
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel,
    QCheckBox, QGroupBox, QFileDialog,
    QMessageBox, QProgressBar, QListWidget, QListWidgetItem,
    QSplitter, QFrame, QScrollArea, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QParallelAnimationGroup
from PyQt5.QtGui import QFont, QColor, QPalette, QBrush, QIcon, QPainter, QPixmap, QLinearGradient


class ModernButton(QPushButton):
    """现代化按钮"""
    
    def __init__(self, text, primary=False):
        super().__init__(text)
        self.primary = primary
        self.setup_style()
    
    def setup_style(self):
        """设置样式"""
        self.setFixedHeight(45)
        self.setCursor(Qt.PointingHandCursor)
        
        if self.primary:
            self.setStyleSheet('''
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #667eea, stop:1 #764ba2);
                    color: white;
                    border: none;
                    border-radius: 12px;
                    font-size: 15px;
                    font-weight: 600;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #7c90db, stop:1 #8b5fbf);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #5a6fd6, stop:1 #6a4190);
                }
            ''')
        else:
            self.setStyleSheet('''
                QPushButton {
                    background-color: #f5f5f5;
                    color: #333;
                    border: none;
                    border-radius: 12px;
                    font-size: 14px;
                    font-weight: 500;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #e8e8e8;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            ''')


class ModernCard(QFrame):
    """现代化卡片"""
    
    def __init__(self):
        super().__init__()
        self.setup_style()
    
    def setup_style(self):
        """设置样式"""
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('''
            QFrame {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #e8e8e8;
            }
            QFrame:hover {
                border: 1px solid #667eea;
            }
        ''')
        
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)


class ModernEditor(QTextEdit):
    """现代化编辑器"""
    
    def __init__(self):
        super().__init__()
        self.setup_style()
    
    def setup_style(self):
        """设置样式"""
        self.setStyleSheet('''
            QTextEdit {
                background-color: #fafafa;
                border: 2px solid #e8e8e8;
                border-radius: 12px;
                padding: 15px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 14px;
                line-height: 1.6;
            }
            QTextEdit:focus {
                border: 2px solid #667eea;
            }
            QTextEdit:hover {
                border: 2px solid #a0a0a0;
            }
        ''')
        
        # 设置占位符样式
        self.setPlaceholderText('开始创作你的内容...\n\n# 标题\n\n正文内容支持 Markdown 格式')


class ModernTitleInput(QLineEdit):
    """现代化标题输入框"""
    
    def __init__(self):
        super().__init__()
        self.setup_style()
    
    def setup_style(self):
        """设置样式"""
        self.setPlaceholderText('输入吸引人的标题...')
        self.setStyleSheet('''
            QLineEdit {
                background-color: white;
                border: 2px solid #e8e8e8;
                border-radius: 12px;
                padding: 15px 20px;
                font-size: 16px;
                font-weight: 500;
                font-family: 'Microsoft YaHei', sans-serif;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
            }
            QLineEdit:hover {
                border: 2px solid #a0a0a0;
            }
        ''')


class PlatformCard(QCheckBox):
    """平台选择卡片"""
    
    def __init__(self, name, icon, color):
        super().__init__()
        self.name = name
        self.icon = icon
        self.color = color
        self.setup_ui()
    
    def setup_ui(self):
        """设置 UI"""
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f'''
            QCheckBox {{
                background-color: white;
                border: 2px solid #e8e8e8;
                border-radius: 16px;
                padding: 20px;
                font-size: 15px;
                font-weight: 600;
                color: #333;
            }}
            QCheckBox:hover {{
                border: 2px solid {self.color};
                background-color: #fafafa;
            }}
            QCheckBox:checked {{
                background-color: {self.color};
                color: white;
                border: 2px solid {self.color};
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #ccc;
            }}
            QCheckBox::indicator:checked {{
                background-color: white;
                border: 2px solid white;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHZpZXdCb3g9IjAgMCAyMCAyMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNNy41IDE0LjVMMy41IDEwLjVMNSA4LjVMNy41IDExTDE1IDMuNUwxNi41IDVMMTQuNSA3TDEyLjUgOUw3LjUgMTQuNVoiIGZpbGw9IiM2NjdlZWEiLz48L3N2Zz4=);
            }}
        ''')
        
        # 设置文本
        self.setText(f'{self.icon}  {self.name}')


class ModernProgressBar(QProgressBar):
    """现代化进度条"""
    
    def __init__(self):
        super().__init__()
        self.setup_style()
    
    def setup_style(self):
        """设置样式"""
        self.setFixedHeight(8)
        self.setStyleSheet('''
            QProgressBar {
                background-color: #e8e8e8;
                border-radius: 4px;
                border: none;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 4px;
            }
        ''')


class EditorWidget(QWidget):
    """编辑器组件"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # 标题
        self.title_input = ModernTitleInput()
        layout.addWidget(self.title_input)
        
        # 编辑器
        self.editor = ModernEditor()
        layout.addWidget(self.editor, stretch=1)
        
        # 封面图
        cover_card = ModernCard()
        cover_layout = QHBoxLayout(cover_card)
        cover_layout.setContentsMargins(20, 15, 20, 15)
        
        cover_label = QLabel('📷 封面图片')
        cover_label.setFont(QFont('Microsoft YaHei', 12, QFont.Bold))
        self.cover_path = QLabel('未选择图片')
        self.cover_path.setStyleSheet('color: #888; font-size: 13px;')
        
        self.cover_btn = ModernButton('选择图片')
        self.cover_btn.setFixedHeight(40)
        self.cover_btn.clicked.connect(self.select_cover)
        
        cover_layout.addWidget(cover_label)
        cover_layout.addWidget(self.cover_path, stretch=1)
        cover_layout.addWidget(self.cover_btn)
        
        layout.addWidget(cover_card)
        
        self.setLayout(layout)
    
    def select_cover(self):
        """选择封面图片"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择封面图片', '',
            '图片文件 (*.png *.jpg *.jpeg *.gif)'
        )
        if file_path:
            self.cover_path.setText(file_path)
            self.cover_path.setStyleSheet('color: #667eea; font-size: 13px; font-weight: 500;')
    
    def get_content(self):
        """获取编辑器内容"""
        return {
            'title': self.title_input.text(),
            'content': self.editor.toPlainText(),
            'cover': self.cover_path.text() if self.cover_path.text() != '未选择图片' else None
        }


class PlatformSelector(QWidget):
    """平台选择组件"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def get_selected_platforms(self):
        """获取选择的平台"""
        platforms = []
        if self.zhihu_cb.isChecked():
            platforms.append('zhihu')
        if self.xiaohongshu_cb.isChecked():
            platforms.append('xiaohongshu')
        if self.kuaishou_cb.isChecked():
            platforms.append('kuaishou')
        if self.douyin_cb.isChecked():
            platforms.append('douyin')
        return platforms
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel('🚀 选择发布平台')
        title.setFont(QFont('Microsoft YaHei', 18, QFont.Bold))
        title.setStyleSheet('color: #333; padding: 10px 0;')
        layout.addWidget(title)
        
        # 平台卡片
        platforms_layout = QVBoxLayout()
        platforms_layout.setSpacing(12)
        
        self.zhihu_cb = PlatformCard('知乎', '📝', '#0084ff')
        self.xiaohongshu_cb = PlatformCard('小红书', '📕', '#ff2442')
        self.kuaishou_cb = PlatformCard('快手', '📹', '#ff4906')
        self.douyin_cb = PlatformCard('抖音', '🎵', '#00f0ff')
        
        self.zhihu_cb.setChecked(True)
        self.xiaohongshu_cb.setChecked(True)
        
        platforms_layout.addWidget(self.zhihu_cb)
        platforms_layout.addWidget(self.xiaohongshu_cb)
        platforms_layout.addWidget(self.kuaishou_cb)
        platforms_layout.addWidget(self.douyin_cb)
        
        layout.addLayout(platforms_layout)
        
        # 发布按钮
        self.publish_btn = ModernButton('🚀 一键发布', primary=True)
        self.publish_btn.setFixedHeight(55)
        self.publish_btn.setFont(QFont('Microsoft YaHei', 16, QFont.Bold))
        layout.addWidget(self.publish_btn)
        
        # 进度条
        self.progress = ModernProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # 状态标签
        self.status_label = QLabel('✨ 准备就绪')
        self.status_label.setFont(QFont('Microsoft YaHei', 13))
        self.status_label.setStyleSheet('color: #666; padding: 10px 0;')
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)


class PublishHistory(QWidget):
    """发布历史组件"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # 标题
        title = QLabel('📜 发布历史')
        title.setFont(QFont('Microsoft YaHei', 18, QFont.Bold))
        title.setStyleSheet('color: #333; padding: 10px 0;')
        layout.addWidget(title)
        
        # 历史记录列表
        self.history_list = QListWidget()
        self.history_list.setStyleSheet('''
            QListWidget {
                background-color: white;
                border: 2px solid #e8e8e8;
                border-radius: 12px;
                padding: 10px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 15px;
                border-radius: 8px;
                margin: 5px 0;
                border: 1px solid #f0f0f0;
            }
            QListWidget::item:selected {
                background-color: #667eea;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
        ''')
        layout.addWidget(self.history_list)
        
        # 清空按钮
        clear_btn = ModernButton('🗑️ 清空历史')
        clear_btn.clicked.connect(self.history_list.clear)
        layout.addWidget(clear_btn)
        
        self.setLayout(layout)
    
    def add_record(self, title, platforms, status):
        """添加发布记录"""
        item_text = f"📄 {title}"
        item_detail = f"平台：{', '.join(platforms)}  |  状态：{status}"
        
        item = QListWidgetItem(f"{item_text}\n{item_detail}")
        item.setSizeHint(self.history_list.visualItemRect(item).size())
        self.history_list.addItem(item)


class SettingsWidget(QWidget):
    """设置页面"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel('⚙️ 平台配置')
        title.setFont(QFont('Microsoft YaHei', 18, QFont.Bold))
        title.setStyleSheet('color: #333; padding: 10px 0;')
        layout.addWidget(title)
        
        # 说明卡片
        info_card = ModernCard()
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(25, 20, 25, 20)
        
        info_text = QLabel('''
        <h3 style="color: #667eea; margin-bottom: 15px;">📌 如何配置 Cookie</h3>
        <ol style="line-height: 2; color: #555;">
            <li>登录对应平台（知乎/小红书/快手/抖音）</li>
            <li>按 F12 打开浏览器开发者工具</li>
            <li>找到 Application → Cookies</li>
            <li>复制 Cookie 值粘贴到下方输入框</li>
        </ol>
        <p style="color: #ff6b6b; margin-top: 15px;">⚠️ 注意：Cookie 包含账号信息，请妥善保管</p>
        ''')
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_card)
        
        # Cookie 输入框（占位符）
        layout.addWidget(QLabel('<b>知乎 Cookie</b>'))
        self.zhihu_cookie = ModernEditor()
        self.zhihu_cookie.setFixedHeight(80)
        self.zhihu_cookie.setPlaceholderText('粘贴知乎 Cookie...')
        layout.addWidget(self.zhihu_cookie)
        
        layout.addWidget(QLabel('<b>小红书 Cookie</b>'))
        self.xiaohongshu_cookie = ModernEditor()
        self.xiaohongshu_cookie.setFixedHeight(80)
        self.xiaohongshu_cookie.setPlaceholderText('粘贴小红书 Cookie...')
        layout.addWidget(self.xiaohongshu_cookie)
        
        # 保存按钮
        save_btn = ModernButton('💾 保存配置', primary=True)
        layout.addWidget(save_btn)
        
        # 占位提示
        layout.addStretch()
        todo = QLabel('🚧 更多配置功能开发中...')
        todo.setAlignment(Qt.AlignCenter)
        todo.setStyleSheet('color: #888; font-size: 14px; padding: 30px;')
        layout.addWidget(todo)
        
        self.setLayout(layout)


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('多平台发布助手 v1.0')
        self.setMinimumSize(1400, 900)
        self.setStyleSheet('background-color: #f8f9fa;')
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)
        
        # 顶部标题
        header = QLabel('📝 多平台发布助手')
        header.setFont(QFont('Microsoft YaHei', 28, QFont.Bold))
        header.setStyleSheet('color: #333; padding: 10px 0;')
        main_layout.addWidget(header)
        
        # 副标题
        subtitle = QLabel('一键发布到知乎、小红书、快手、抖音')
        subtitle.setFont(QFont('Microsoft YaHei', 14))
        subtitle.setStyleSheet('color: #666; padding-bottom: 20px;')
        main_layout.addWidget(subtitle)
        
        # 标签页
        from PyQt5.QtWidgets import QTabWidget
        tabs = QTabWidget()
        tabs.setStyleSheet('''
            QTabWidget::pane {
                border: none;
                background-color: transparent;
            }
            QTabBar::tab {
                background-color: white;
                border: 2px solid #e8e8e8;
                border-bottom: none;
                border-radius: 12px 12px 0 0;
                padding: 12px 25px;
                margin-right: 5px;
                font-size: 15px;
                font-weight: 500;
                color: #666;
            }
            QTabBar::tab:selected {
                background-color: #667eea;
                color: white;
                border: 2px solid #667eea;
            }
            QTabBar::tab:hover {
                background-color: #f5f5f5;
            }
        ''')
        
        # 发布标签页
        publish_widget = QWidget()
        publish_layout = QHBoxLayout(publish_widget)
        publish_layout.setSpacing(25)
        
        # 左侧：编辑器
        self.editor = EditorWidget()
        publish_layout.addWidget(self.editor, stretch=2)
        
        # 右侧：平台选择
        self.platform_selector = PlatformSelector()
        publish_layout.addWidget(self.platform_selector, stretch=1)
        
        tabs.addTab(publish_widget, '  发布内容')
        
        # 历史标签页
        self.history = PublishHistory()
        tabs.addTab(self.history, '  发布历史')
        
        # 设置标签页
        self.settings = SettingsWidget()
        tabs.addTab(self.settings, '  设置')
        
        main_layout.addWidget(tabs)
        
        # 连接信号
        self.platform_selector.publish_btn.clicked.connect(self.start_publish)
    
    def start_publish(self):
        """开始发布"""
        content = self.editor.get_content()
        platforms = self.platform_selector.get_selected_platforms()
        
        if not content['title']:
            QMessageBox.warning(self, '⚠️ 提示', '请输入标题', QMessageBox.Ok)
            return
        
        if not content['content']:
            QMessageBox.warning(self, '⚠️ 提示', '请输入内容', QMessageBox.Ok)
            return
        
        if not platforms:
            QMessageBox.warning(self, '⚠️ 提示', '请至少选择一个平台', QMessageBox.Ok)
            return
        
        # 显示进度
        self.platform_selector.progress.setVisible(True)
        self.platform_selector.status_label.setText('⏳ 正在发布...')
        self.platform_selector.status_label.setStyleSheet('color: #667eea; font-weight: 600;')
        
        # 模拟发布
        self.simulate_publish(content, platforms)
    
    def simulate_publish(self, content, platforms):
        """模拟发布过程"""
        self.platform_selector.progress.setMaximum(len(platforms))
        
        for i, platform in enumerate(platforms):
            self.platform_selector.progress.setValue(i + 1)
            self.platform_selector.status_label.setText(f'⏳ 正在发布到 {platform}...')
        
        # 发布完成
        self.platform_selector.status_label.setText('✅ 发布完成！')
        self.platform_selector.status_label.setStyleSheet('color: #10b981; font-weight: 600;')
        
        # 添加到历史
        self.history.add_record(
            content['title'],
            platforms,
            '成功'
        )
        
        QMessageBox.information(
            self,
            '✅ 发布完成',
            f'成功发布到 {len(platforms)} 个平台！\n\n标题：{content["title"]}\n平台：{", ".join(platforms)}',
            QMessageBox.Ok
        )
