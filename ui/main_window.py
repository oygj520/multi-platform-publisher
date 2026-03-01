# -*- coding: utf-8 -*-
"""
主窗口界面 - 完整版
包含 Cookie 管理、发布引擎集成
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel,
    QCheckBox, QGroupBox, QFileDialog,
    QMessageBox, QProgressBar, QListWidget, QListWidgetItem,
    QSplitter, QFrame, QScrollArea, QGraphicsDropShadowEffect,
    QTabWidget, QGridLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QIcon

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from publisher.engine import get_publisher, PublishError
from publisher.cookie_manager import cookie_manager


class ModernButton(QPushButton):
    """现代化按钮"""
    
    def __init__(self, text, primary=False, danger=False):
        super().__init__(text)
        self.primary = primary
        self.danger = danger
        self.setup_style()
    
    def setup_style(self):
        """设置样式"""
        self.setFixedHeight(45)
        self.setCursor(Qt.PointingHandCursor)
        
        if self.danger:
            self.setStyleSheet('''
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #ff6b6b, stop:1 #ee5a5a);
                    color: white;
                    border: none;
                    border-radius: 12px;
                    font-size: 15px;
                    font-weight: 600;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #ff5252, stop:1 #e04545);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #ff4040, stop:1 #d03535);
                }
            ''')
        elif self.primary:
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


class CookieStatusCard(QFrame):
    """Cookie 状态卡片"""
    
    def __init__(self, platform, icon, color):
        super().__init__()
        self.platform = platform
        self.icon = icon
        self.color = color
        self.setup_ui()
    
    def setup_ui(self):
        """设置 UI"""
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f'''
            QFrame {{
                background-color: white;
                border-radius: 12px;
                border: 2px solid #e8e8e8;
                padding: 15px;
            }}
            QFrame:hover {{
                border: 2px solid {self.color};
            }}
        ''')
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # 平台名称
        title_layout = QHBoxLayout()
        self.title_label = QLabel(f'{self.icon} {self.platform_display()}')
        self.title_label.setFont(QFont('Microsoft YaHei', 14, QFont.Bold))
        self.title_label.setStyleSheet('color: #333;')
        title_layout.addWidget(self.title_label)
        
        # 状态指示器
        self.status_indicator = QLabel('●')
        self.status_indicator.setFont(QFont('Arial', 16))
        self.status_indicator.setStyleSheet('color: #ccc;')
        title_layout.addStretch()
        title_layout.addWidget(self.status_indicator)
        
        layout.addLayout(title_layout)
        
        # 状态文本
        self.status_label = QLabel('未配置 Cookie')
        self.status_label.setFont(QFont('Microsoft YaHei', 12))
        self.status_label.setStyleSheet('color: #888;')
        layout.addWidget(self.status_label)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        
        self.edit_btn = ModernButton('编辑')
        self.edit_btn.setFixedHeight(35)
        self.edit_btn.clicked.connect(self.edit_cookie)
        btn_layout.addWidget(self.edit_btn)
        
        self.test_btn = ModernButton('测试')
        self.test_btn.setFixedHeight(35)
        self.test_btn.clicked.connect(self.test_cookie)
        btn_layout.addWidget(self.test_btn)
        
        self.delete_btn = ModernButton('删除', danger=True)
        self.delete_btn.setFixedHeight(35)
        self.delete_btn.clicked.connect(self.delete_cookie)
        btn_layout.addWidget(self.delete_btn)
        
        layout.addLayout(btn_layout)
    
    def platform_display(self):
        """平台显示名称"""
        names = {
            'zhihu': '知乎',
            'xiaohongshu': '小红书',
            'kuaishou': '快手',
            'douyin': '抖音'
        }
        return names.get(self.platform, self.platform)
    
    def update_status(self, status: dict):
        """更新状态显示"""
        if status.get('has_cookie'):
            if status.get('is_valid'):
                self.status_label.setText('Cookie 有效')
                self.status_label.setStyleSheet('color: #10b981; font-weight: 600;')
                self.status_indicator.setStyleSheet('color: #10b981;')
            else:
                self.status_label.setText('Cookie 可能已失效')
                self.status_label.setStyleSheet('color: #f59e0b; font-weight: 600;')
                self.status_indicator.setStyleSheet('color: #f59e0b;')
        else:
            self.status_label.setText('未配置 Cookie')
            self.status_label.setStyleSheet('color: #888;')
            self.status_indicator.setStyleSheet('color: #ccc;')
    
    def edit_cookie(self):
        """编辑 Cookie"""
        # 信号由外部处理
        pass
    
    def test_cookie(self):
        """测试 Cookie"""
        pass
    
    def delete_cookie(self):
        """删除 Cookie"""
        reply = QMessageBox.question(
            None, '确认删除',
            f'确定要删除 {self.platform_display()} 的 Cookie 吗？',
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            cookie_manager.delete_cookie(self.platform)
            self.update_status(cookie_manager.get_cookie_status(self.platform))


class PublishWorker(QThread):
    """发布工作线程"""
    
    status_signal = pyqtSignal(str, str)  # message, level
    finished_signal = pyqtSignal(bool, str)  # success, message
    
    def __init__(self, platform, content, cookie):
        super().__init__()
        self.platform = platform
        self.content = content
        self.cookie = cookie
    
    def run(self):
        """执行发布任务"""
        try:
            publisher = get_publisher(self.platform, self.cookie)
            publisher.set_status_callback(self.emit_status)
            
            success = publisher.publish_with_retry(self.content)
            
            if success:
                self.finished_signal.emit(True, f'{self.platform} 发布成功')
            else:
                self.finished_signal.emit(False, f'{self.platform} 发布失败')
        except Exception as e:
            self.finished_signal.emit(False, f'{self.platform} 发布异常：{str(e)}')
    
    def emit_status(self, message, level='info'):
        """发送状态更新"""
        self.status_signal.emit(message, level)


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
    
    def clear(self):
        """清空编辑器"""
        self.title_input.clear()
        self.editor.clear()
        self.cover_path.setText('未选择图片')
        self.cover_path.setStyleSheet('color: #888; font-size: 13px;')


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
        from datetime import datetime
        item_text = f"📄 {title}"
        item_detail = f"平台：{', '.join(platforms)}  |  状态：{status}  |  时间：{datetime.now().strftime('%H:%M:%S')}"
        
        item = QListWidgetItem(f"{item_text}\n{item_detail}")
        self.history_list.addItem(item)


class CookieManagerWidget(QWidget):
    """Cookie 管理组件"""
    
    def __init__(self):
        super().__init__()
        self.cookie_editors = {}
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel('🔐 Cookie 管理')
        title.setFont(QFont('Microsoft YaHei', 18, QFont.Bold))
        title.setStyleSheet('color: #333; padding: 10px 0;')
        layout.addWidget(title)
        
        # 说明卡片
        info_card = ModernCard()
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(25, 20, 25, 20)
        
        info_text = QLabel('''
        <h3 style="color: #667eea; margin-bottom: 15px;">📌 如何获取 Cookie</h3>
        <ol style="line-height: 2; color: #555;">
            <li>使用浏览器登录对应平台（知乎/小红书/快手/抖音）</li>
            <li>按 F12 打开开发者工具</li>
            <li>切换到 Application/存储 → Cookies</li>
            <li>复制所有 Cookie 值（或整个 JSON）</li>
            <li>粘贴到下方对应平台的输入框中</li>
        </ol>
        <p style="color: #ff6b6b; margin-top: 15px;">⚠️ 注意：Cookie 包含账号登录信息，请妥善保管，不要分享给他人</p>
        ''')
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_card)
        
        # Cookie 状态卡片网格
        status_grid = QGridLayout()
        status_grid.setSpacing(15)
        
        self.cookie_cards = {}
        platforms = [
            ('zhihu', '知乎', '📝', '#0084ff'),
            ('xiaohongshu', '小红书', '📕', '#ff2442'),
            ('kuaishou', '快手', '📹', '#ff4906'),
            ('douyin', '抖音', '🎵', '#00f0ff')
        ]
        
        for i, (key, name, icon, color) in enumerate(platforms):
            card = CookieStatusCard(key, icon, color)
            self.cookie_cards[key] = card
            row = i // 2
            col = (i % 2) * 2
            status_grid.addWidget(card, row, col, 1, 2)
        
        layout.addLayout(status_grid)
        
        # Cookie 编辑区域（默认隐藏）
        self.edit_area = QFrame()
        self.edit_area.setFrameShape(QFrame.StyledPanel)
        self.edit_area.setStyleSheet('''
            QFrame {
                background-color: #fafafa;
                border-radius: 12px;
                border: 2px dashed #ccc;
                padding: 20px;
            }
        ''')
        edit_layout = QVBoxLayout(self.edit_area)
        
        self.edit_area_label = QLabel('')
        self.edit_area_label.setFont(QFont('Microsoft YaHei', 14, QFont.Bold))
        edit_layout.addWidget(self.edit_area_label)
        
        self.cookie_editor = QTextEdit()
        self.cookie_editor.setPlaceholderText('粘贴 Cookie 数据...')
        self.cookie_editor.setStyleSheet('''
            QTextEdit {
                background-color: white;
                border: 2px solid #e8e8e8;
                border-radius: 8px;
                padding: 10px;
                font-family: 'Consolas', monospace;
                font-size: 13px;
            }
        ''')
        self.cookie_editor.setFixedHeight(150)
        edit_layout.addWidget(self.cookie_editor)
        
        edit_btn_layout = QHBoxLayout()
        self.save_cookie_btn = ModernButton('💾 保存 Cookie', primary=True)
        self.save_cookie_btn.clicked.connect(self.save_cookie)
        edit_btn_layout.addWidget(self.save_cookie_btn)
        
        self.cancel_edit_btn = ModernButton('取消')
        self.cancel_edit_btn.clicked.connect(self.hide_edit_area)
        edit_btn_layout.addWidget(self.cancel_edit_btn)
        
        edit_layout.addLayout(edit_btn_layout)
        edit_layout.addStretch()
        
        layout.addWidget(self.edit_area)
        self.edit_area.setVisible(False)
        
        # 刷新按钮
        refresh_btn = ModernButton('🔄 刷新状态')
        refresh_btn.clicked.connect(self.refresh_all_status)
        layout.addWidget(refresh_btn)
        
        layout.addStretch()
        
        self.setLayout(layout)
        
        # 初始加载状态
        QTimer.singleShot(500, self.refresh_all_status)
    
    def refresh_all_status(self):
        """刷新所有 Cookie 状态"""
        all_status = cookie_manager.get_all_status()
        for platform, status in all_status.items():
            if platform in self.cookie_cards:
                self.cookie_cards[platform].update_status(status)
    
    def show_edit_area(self, platform):
        """显示编辑区域"""
        self.current_platform = platform
        names = {
            'zhihu': '知乎',
            'xiaohongshu': '小红书',
            'kuaishou': '快手',
            'douyin': '抖音'
        }
        self.edit_area_label.setText(f'编辑 {names.get(platform, platform)} Cookie')
        
        # 加载现有 Cookie
        existing = cookie_manager.get_cookie(platform)
        if existing:
            self.cookie_editor.setText(existing)
        else:
            self.cookie_editor.clear()
        
        self.edit_area.setVisible(True)
    
    def hide_edit_area(self):
        """隐藏编辑区域"""
        self.edit_area.setVisible(False)
        self.current_platform = None
    
    def save_cookie(self):
        """保存 Cookie"""
        if not hasattr(self, 'current_platform') or not self.current_platform:
            return
        
        cookie_data = self.cookie_editor.toPlainText().strip()
        
        if not cookie_data:
            QMessageBox.warning(self, '⚠️ 提示', 'Cookie 不能为空', QMessageBox.Ok)
            return
        
        if not cookie_manager.validate_cookie_format(cookie_data):
            reply = QMessageBox.warning(
                self, '⚠️ 格式警告',
                'Cookie 格式可能不正确，确定要保存吗？',
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
        
        success = cookie_manager.save_cookie(self.current_platform, cookie_data)
        
        if success:
            QMessageBox.information(
                self, '✅ 保存成功',
                f'{self.current_platform} Cookie 已保存',
                QMessageBox.Ok
            )
            self.hide_edit_area()
            self.refresh_all_status()
        else:
            QMessageBox.critical(
                self, '❌ 保存失败',
                '保存 Cookie 时出错，请重试',
                QMessageBox.Ok
            )


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.publish_workers = []
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('多平台发布助手 v2.0')
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
        subtitle = QLabel('一键发布到知乎、小红书、快手、抖音 | v2.0 完整版')
        subtitle.setFont(QFont('Microsoft YaHei', 14))
        subtitle.setStyleSheet('color: #666; padding-bottom: 20px;')
        main_layout.addWidget(subtitle)
        
        # 标签页
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
        
        # Cookie 管理标签页
        self.cookie_manager = CookieManagerWidget()
        tabs.addTab(self.cookie_manager, '  Cookie 管理')
        
        # 历史标签页
        self.history = PublishHistory()
        tabs.addTab(self.history, '  发布历史')
        
        main_layout.addWidget(tabs)
        
        # 连接信号
        self.platform_selector.publish_btn.clicked.connect(self.start_publish)
        
        # 连接 Cookie 卡片编辑信号
        for platform, card in self.cookie_manager.cookie_cards.items():
            card.edit_btn.clicked.connect(lambda checked, p=platform: self.cookie_manager.show_edit_area(p))
    
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
        
        # 检查 Cookie
        missing_cookies = []
        for platform in platforms:
            cookie = cookie_manager.get_cookie(platform)
            if not cookie:
                missing_cookies.append(platform)
        
        if missing_cookies:
            names = {'zhihu': '知乎', 'xiaohongshu': '小红书', 'kuaishou': '快手', 'douyin': '抖音'}
            missing_names = [names.get(p, p) for p in missing_cookies]
            reply = QMessageBox.warning(
                self, '⚠️ Cookie 缺失',
                f'以下平台未配置 Cookie：{", ".join(missing_names)}\n\n'
                f'是否继续？（可能需要手动登录）',
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
        
        # 显示进度
        self.platform_selector.progress.setVisible(True)
        self.platform_selector.progress.setMaximum(len(platforms))
        self.platform_selector.progress.setValue(0)
        self.platform_selector.status_label.setText('⏳ 正在发布...')
        self.platform_selector.status_label.setStyleSheet('color: #667eea; font-weight: 600;')
        
        # 禁用发布按钮
        self.platform_selector.publish_btn.setEnabled(False)
        
        # 开始发布任务
        self.current_platform_index = 0
        self.platforms_to_publish = platforms
        self.content = content
        self.publish_results = []
        
        self.publish_next_platform()
    
    def publish_next_platform(self):
        """发布下一个平台"""
        if self.current_platform_index >= len(self.platforms_to_publish):
            # 所有平台发布完成
            self.on_publish_complete()
            return
        
        platform = self.platforms_to_publish[self.current_platform_index]
        cookie = cookie_manager.get_cookie(platform)
        
        self.platform_selector.status_label.setText(f'⏳ 正在发布到 {self.platform_name(platform)}...')
        
        # 创建工作线程
        worker = PublishWorker(platform, self.content, cookie)
        worker.status_signal.connect(self.on_publish_status)
        worker.finished_signal.connect(self.on_publish_finished)
        
        self.publish_workers.append(worker)
        worker.start()
    
    def on_publish_status(self, message, level):
        """处理发布状态更新"""
        print(f'[{level.upper()}] {message}')
    
    def on_publish_finished(self, success, message):
        """处理发布完成"""
        platform = self.platforms_to_publish[self.current_platform_index]
        self.publish_results.append({
            'platform': platform,
            'success': success,
            'message': message
        })
        
        # 更新进度
        self.current_platform_index += 1
        self.platform_selector.progress.setValue(self.current_platform_index)
        
        # 发布下一个
        QTimer.singleShot(1000, self.publish_next_platform)
    
    def on_publish_complete(self):
        """所有发布完成"""
        success_count = sum(1 for r in self.publish_results if r['success'])
        total = len(self.publish_results)
        
        if success_count == total:
            self.platform_selector.status_label.setText(f'✅ 全部发布成功！({success_count}/{total})')
            self.platform_selector.status_label.setStyleSheet('color: #10b981; font-weight: 600;')
            
            # 添加到历史
            platforms_names = [self.platform_name(p) for p in self.platforms_to_publish]
            self.history.add_record(
                self.content['title'],
                platforms_names,
                '成功'
            )
            
            QMessageBox.information(
                self,
                '✅ 发布完成',
                f'成功发布到 {success_count} 个平台！\n\n标题：{self.content["title"]}\n平台：{", ".join(platforms_names)}',
                QMessageBox.Ok
            )
        else:
            self.platform_selector.status_label.setText(f'⚠️ 部分发布成功 ({success_count}/{total})')
            self.platform_selector.status_label.setStyleSheet('color: #f59e0b; font-weight: 600;')
            
            # 显示失败详情
            failed = [r for r in self.publish_results if not r['success']]
            failed_msg = '\n'.join([f"• {self.platform_name(r['platform'])}: {r['message']}" for r in failed])
            
            QMessageBox.warning(
                self,
                '⚠️ 部分发布失败',
                f'成功：{success_count}/{total}\n\n失败详情:\n{failed_msg}',
                QMessageBox.Ok
            )
        
        # 恢复按钮
        self.platform_selector.publish_btn.setEnabled(True)
        self.publish_workers.clear()
    
    def platform_name(self, platform):
        """获取平台中文名"""
        names = {
            'zhihu': '知乎',
            'xiaohongshu': '小红书',
            'kuaishou': '快手',
            'douyin': '抖音'
        }
        return names.get(platform, platform)
