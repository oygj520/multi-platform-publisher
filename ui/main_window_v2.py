# -*- coding: utf-8 -*-
"""
主窗口界面 - 现代化设计版本 V2
集成实际发布逻辑和 Cookie 管理
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel,
    QCheckBox, QGroupBox, QFileDialog,
    QMessageBox, QProgressBar, QListWidget, QListWidgetItem,
    QSplitter, QFrame, QScrollArea, QGraphicsDropShadowEffect,
    QTabWidget, QFormLayout, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QDialog, QDialogButtonBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QDesktopServices
from PyQt5.QtCore import QUrl
import sys
import os

# 添加项目路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from publisher.engine import get_publisher, PublishError
from publisher.cookie_manager import cookie_manager
from config import config


class ModernButton(QPushButton):
    """现代化按钮"""
    
    def __init__(self, text, primary=False, danger=False):
        super().__init__(text)
        self.primary = primary
        self.danger = danger
        self.setup_style()
    
    def setup_style(self):
        """设置样式"""
        self.setMinimumHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(self.sizePolicy().horizontalPolicy(), QSizePolicy.Preferred)
        
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
                    padding: 12px 25px;
                    min-width: 120px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #ff8585, stop:1 #ff7070);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #e55a5a, stop:1 #d44a4a);
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
                    padding: 12px 25px;
                    min-width: 120px;
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
                    padding: 12px 25px;
                    min-width: 100px;
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


class PublishWorker(QThread):
    """发布工作线程"""
    
    status_signal = pyqtSignal(str, str)  # message, level
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, platform: str, content: dict, cookie: str):
        super().__init__()
        self.platform = platform
        self.content = content
        self.cookie = cookie
    
    def run(self):
        """执行发布任务"""
        try:
            def on_status_change(message: str, level: str = "info"):
                self.status_signal.emit(message, level)
            
            publisher = get_publisher(self.platform, self.cookie, on_status_change)
            success = publisher.publish(self.content)
            
            if success:
                self.finished_signal.emit(True, f"{self.platform} 发布成功")
            else:
                self.finished_signal.emit(False, f"{self.platform} 发布失败")
                
        except Exception as e:
            self.status_signal.emit(f"发布异常：{str(e)}", "error")
            self.finished_signal.emit(False, str(e))


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
        self.publish_workers = []
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
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)


class PublishHistory(QWidget):
    """发布历史组件"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_history()
    
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
        self.history_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.history_list)
        
        # 按钮布局
        btn_layout = QHBoxLayout()
        
        clear_btn = ModernButton('🗑️ 清空历史')
        clear_btn.clicked.connect(self.clear_history)
        btn_layout.addWidget(clear_btn)
        
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def load_history(self):
        """加载历史记录"""
        from config import config
        history = config.get('publish.history', [])
        
        self.history_list.clear()
        for record in reversed(history[-50:]):  # 只显示最近 50 条
            self._add_record_to_list(record)
    
    def _add_record_to_list(self, record):
        """添加记录到列表"""
        title = record.get('title', '无标题')
        platforms = record.get('platforms', [])
        status = record.get('status', '未知')
        timestamp = record.get('timestamp', '')
        
        platform_names = {
            'zhihu': '知乎',
            'xiaohongshu': '小红书',
            'kuaishou': '快手',
            'douyin': '抖音'
        }
        platform_str = ', '.join([platform_names.get(p, p) for p in platforms])
        
        status_icon = '✅' if status == '成功' else '❌'
        color = '#10b981' if status == '成功' else '#ef4444'
        
        item_text = f"{status_icon} {title}"
        item_detail = f"平台：{platform_str}  |  状态：<span style='color:{color}'>{status}</span>"
        if timestamp:
            item_detail += f"  |  时间：{timestamp}"
        
        item = QListWidgetItem(item_text)
        item.setToolTip(f"{item_text}\n{item_detail}")
        self.history_list.addItem(item)
    
    def add_record(self, title, platforms, status):
        """添加发布记录"""
        from config import config
        
        record = {
            'title': title,
            'platforms': platforms,
            'status': status,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 保存到配置
        history = config.get('publish.history', [])
        history.append(record)
        config.set('publish.history', history[-100:])  # 保留最近 100 条
        
        # 添加到列表
        self._add_record_to_list(record)
    
    def clear_history(self):
        """清空历史"""
        reply = QMessageBox.question(
            self, '确认清空',
            '确定要清空所有发布历史吗？',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            from config import config
            config.set('publish.history', [])
            self.history_list.clear()
            QMessageBox.information(self, '提示', '发布历史已清空')


# 导入 datetime
from datetime import datetime


class CookieStatusCard(QFrame):
    """Cookie 状态卡片"""
    
    def __init__(self, platform: str, parent=None):
        super().__init__(parent)
        self.platform = platform
        self.platform_names = {
            'zhihu': '知乎',
            'xiaohongshu': '小红书',
            'kuaishou': '快手',
            'douyin': '抖音'
        }
        self.platform_icons = {
            'zhihu': '📝',
            'xiaohongshu': '📕',
            'kuaishou': '📹',
            'douyin': '🎵'
        }
        self.platform_colors = {
            'zhihu': '#0084ff',
            'xiaohongshu': '#ff2442',
            'kuaishou': '#ff4906',
            'douyin': '#00f0ff'
        }
        self.init_ui()
    
    def init_ui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('''
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 2px solid #e8e8e8;
            }
        ''')
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        
        # 平台名称
        header_layout = QHBoxLayout()
        icon = self.platform_icons.get(self.platform, '📌')
        name = self.platform_names.get(self.platform, self.platform)
        
        title_label = QLabel(f'{icon} {name}')
        title_label.setFont(QFont('Microsoft YaHei', 14, QFont.Bold))
        title_label.setStyleSheet(f'color: {self.platform_colors.get(self.platform, "#333")};')
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # 状态指示器
        self.status_indicator = QLabel('●')
        self.status_indicator.setFont(QFont('Arial', 16))
        self.status_indicator.setStyleSheet('color: #ccc;')
        header_layout.addWidget(self.status_indicator)
        
        layout.addLayout(header_layout)
        
        # 状态信息
        self.status_text = QLabel('未配置 Cookie')
        self.status_text.setStyleSheet('color: #888; font-size: 13px;')
        layout.addWidget(self.status_text)
        
        # 用户名
        self.username_label = QLabel('')
        self.username_label.setStyleSheet('color: #667eea; font-size: 13px; font-weight: 500;')
        layout.addWidget(self.username_label)
        
        # 按钮
        btn_layout = QHBoxLayout()
        
        self.validate_btn = ModernButton('验证')
        self.validate_btn.setFixedHeight(35)
        self.validate_btn.clicked.connect(self.validate_cookie)
        btn_layout.addWidget(self.validate_btn)
        
        self.edit_btn = ModernButton('配置')
        self.edit_btn.setFixedHeight(35)
        self.edit_btn.clicked.connect(self.edit_cookie)
        btn_layout.addWidget(self.edit_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def update_status(self, status: dict):
        """更新状态显示"""
        if status.get('has_cookie'):
            if status.get('is_valid'):
                self.status_indicator.setStyleSheet('color: #10b981;')
                self.status_text.setText(f'Cookie 有效 · 剩余 {status.get("days_until_expiry", 0)} 天')
                self.status_text.setStyleSheet('color: #10b981; font-size: 13px;')
                
                if status.get('username'):
                    self.username_label.setText(f'👤 {status["username"]}')
            else:
                self.status_indicator.setStyleSheet('color: #ef4444;')
                self.status_text.setText('Cookie 已失效或过期')
                self.status_text.setStyleSheet('color: #ef4444; font-size: 13px;')
                self.username_label.setText('')
        else:
            self.status_indicator.setStyleSheet('color: #ccc;')
            self.status_text.setText('未配置 Cookie')
            self.status_text.setStyleSheet('color: #888; font-size: 13px;')
            self.username_label.setText('')
    
    def validate_cookie(self):
        """验证 Cookie"""
        from config import config
        
        cookie = config.get(f'platforms.{self.platform}.cookie', '')
        if not cookie:
            QMessageBox.warning(self, '提示', '请先配置 Cookie')
            return
        
        # 显示验证中状态
        self.status_text.setText('正在验证...')
        self.validate_btn.setEnabled(False)
        
        # 执行验证
        is_valid, message, user_info = cookie_manager.validate_cookie(self.platform)
        
        # 更新显示
        status = cookie_manager.get_cookie_status(self.platform)
        self.update_status(status)
        
        self.validate_btn.setEnabled(True)
        
        # 显示结果
        if is_valid:
            QMessageBox.information(self, '验证成功', message)
        else:
            QMessageBox.warning(self, '验证失败', message)
    
    def edit_cookie(self):
        """编辑 Cookie"""
        dialog = CookieEditDialog(self.platform, self)
        if dialog.exec_() == QDialog.Accepted:
            # 更新状态
            status = cookie_manager.get_cookie_status(self.platform)
            self.update_status(status)


class CookieEditDialog(QDialog):
    """Cookie 编辑对话框"""
    
    def __init__(self, platform: str, parent=None):
        super().__init__(parent)
        self.platform = platform
        self.platform_names = {
            'zhihu': '知乎',
            'xiaohongshu': '小红书',
            'kuaishou': '快手',
            'douyin': '抖音'
        }
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f'配置 {self.platform_names.get(self.platform, self.platform)} Cookie')
        self.setMinimumSize(600, 500)
        self.setStyleSheet('background-color: #f8f9fa;')
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 说明
        info_card = ModernCard()
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(25, 20, 25, 20)
        
        info_text = QLabel('''
        <h3 style="color: #667eea; margin-bottom: 15px;">📌 如何获取 Cookie</h3>
        <ol style="line-height: 2; color: #555;">
            <li>使用浏览器登录对应平台</li>
            <li>按 F12 打开开发者工具</li>
            <li>进入 Application/存储 → Cookies</li>
            <li>复制所有 Cookie 值（或关键 Cookie）</li>
            <li>粘贴到下方输入框</li>
        </ol>
        <p style="color: #ff6b6b; margin-top: 15px;">⚠️ 注意：Cookie 包含账号登录信息，请妥善保管</p>
        ''')
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_card)
        
        # Cookie 输入
        layout.addWidget(QLabel('<b>Cookie 值</b>'))
        self.cookie_input = QTextEdit()
        self.cookie_input.setPlaceholderText('粘贴 Cookie 到这里...')
        self.cookie_input.setStyleSheet('''
            QTextEdit {
                background-color: white;
                border: 2px solid #e8e8e8;
                border-radius: 12px;
                padding: 15px;
                font-family: 'Consolas', monospace;
                font-size: 13px;
            }
            QTextEdit:focus {
                border: 2px solid #667eea;
            }
        ''')
        self.cookie_input.setFixedHeight(200)
        layout.addWidget(self.cookie_input)
        
        # 加载现有 Cookie
        from config import config
        existing_cookie = config.get(f'platforms.{self.platform}.cookie', '')
        if existing_cookie:
            self.cookie_input.setPlainText(existing_cookie[:100] + '...' if len(existing_cookie) > 100 else existing_cookie)
        
        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = ModernButton('取消')
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = ModernButton('💾 保存', primary=True)
        save_btn.clicked.connect(self.save_cookie)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def save_cookie(self):
        """保存 Cookie"""
        cookie_value = self.cookie_input.toPlainText().strip()
        
        if not cookie_value:
            QMessageBox.warning(self, '提示', 'Cookie 不能为空')
            return
        
        from config import config
        
        # 保存到配置
        config.set_platform_cookie(self.platform, cookie_value)
        
        # 保存到 Cookie 管理器
        success, message = cookie_manager.save_cookie(self.platform, cookie_value)
        
        if success:
            QMessageBox.information(self, '保存成功', message)
            self.accept()
        else:
            QMessageBox.critical(self, '保存失败', message)


class SettingsWidget(QWidget):
    """设置页面 - V2 版本"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.refresh_cookie_status()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel('⚙️ 平台配置')
        title.setFont(QFont('Microsoft YaHei', 18, QFont.Bold))
        title.setStyleSheet('color: #333; padding: 10px 0;')
        layout.addWidget(title)
        
        # Cookie 状态卡片
        status_layout = QHBoxLayout()
        status_layout.setSpacing(15)
        
        self.zhihu_card = CookieStatusCard('zhihu')
        self.xiaohongshu_card = CookieStatusCard('xiaohongshu')
        self.kuaishou_card = CookieStatusCard('kuaishou')
        self.douyin_card = CookieStatusCard('douyin')
        
        status_layout.addWidget(self.zhihu_card)
        status_layout.addWidget(self.xiaohongshu_card)
        status_layout.addWidget(self.kuaishou_card)
        status_layout.addWidget(self.douyin_card)
        
        layout.addLayout(status_layout)
        
        # 刷新按钮
        refresh_btn = ModernButton('🔄 刷新状态')
        refresh_btn.clicked.connect(self.refresh_cookie_status)
        layout.addWidget(refresh_btn)
        
        # 验证历史
        history_card = ModernCard()
        history_layout = QVBoxLayout(history_card)
        history_layout.setContentsMargins(20, 15, 20, 15)
        
        history_title = QLabel('📊 最近验证记录')
        history_title.setFont(QFont('Microsoft YaHei', 14, QFont.Bold))
        history_layout.addWidget(history_title)
        
        self.validation_table = QTableWidget()
        self.validation_table.setColumnCount(4)
        self.validation_table.setHorizontalHeaderLabels(['平台', '状态', '用户', '时间'])
        self.validation_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.validation_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.validation_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.validation_table.setStyleSheet('''
            QTableWidget {
                background-color: white;
                border: none;
                gridline-color: #e8e8e8;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 10px;
                border: none;
                font-weight: 600;
            }
        ''')
        history_layout.addWidget(self.validation_table)
        
        layout.addWidget(history_card)
        
        # 说明卡片
        info_card = ModernCard()
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(25, 20, 25, 20)
        
        info_text = QLabel('''
        <h3 style="color: #667eea; margin-bottom: 15px;">💡 使用提示</h3>
        <ul style="line-height: 2; color: #555;">
            <li>Cookie 有效期为 7 天，建议定期更新</li>
            <li>如发布失败，请先验证 Cookie 是否有效</li>
            <li>不同平台需要分别登录获取 Cookie</li>
            <li>Cookie 已加密存储，请放心使用</li>
        </ul>
        ''')
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_card)
        
        self.setLayout(layout)
    
    def refresh_cookie_status(self):
        """刷新 Cookie 状态"""
        statuses = cookie_manager.get_all_status()
        
        self.zhihu_card.update_status(statuses.get('zhihu', {}))
        self.xiaohongshu_card.update_status(statuses.get('xiaohongshu', {}))
        self.kuaishou_card.update_status(statuses.get('kuaishou', {}))
        self.douyin_card.update_status(statuses.get('douyin', {}))
        
        # 加载验证历史
        self.load_validation_history()
    
    def load_validation_history(self):
        """加载验证历史"""
        history = cookie_manager.get_validation_history(limit=10)
        
        self.validation_table.setRowCount(0)
        
        platform_icons = {
            'zhihu': '📝',
            'xiaohongshu': '📕',
            'kuaishou': '📹',
            'douyin': '🎵'
        }
        
        for record in history:
            row = self.validation_table.rowCount()
            self.validation_table.insertRow(row)
            
            platform = record.get('platform', '')
            icon = platform_icons.get(platform, '📌')
            
            # 平台
            self.validation_table.setItem(row, 0, QTableWidgetItem(f'{icon} {platform}'))
            
            # 状态
            status = '✅ 有效' if record.get('is_valid') else '❌ 无效'
            status_item = QTableWidgetItem(status)
            status_item.setForeground(QColor('#10b981' if record.get('is_valid') else '#ef4444'))
            self.validation_table.setItem(row, 1, status_item)
            
            # 用户
            self.validation_table.setItem(row, 2, QTableWidgetItem(record.get('username', '-')))
            
            # 时间
            checked_at = record.get('checked_at', '')
            if checked_at:
                try:
                    dt = datetime.fromisoformat(checked_at)
                    checked_at = dt.strftime('%m-%d %H:%M')
                except:
                    pass
            self.validation_table.setItem(row, 3, QTableWidgetItem(checked_at))


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.current_workers = []
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
        subtitle = QLabel('一键发布到知乎、小红书、快手、抖音 · V2 版本')
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
        
        # 验证输入
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
        from config import config
        missing_cookies = []
        for platform in platforms:
            cookie = config.get(f'platforms.{platform}.cookie', '')
            if not cookie:
                missing_cookies.append(platform)
        
        if missing_cookies:
            platform_names = {'zhihu': '知乎', 'xiaohongshu': '小红书', 'kuaishou': '快手', 'douyin': '抖音'}
            missing_names = [platform_names.get(p, p) for p in missing_cookies]
            
            reply = QMessageBox.warning(
                self, '⚠️ Cookie 未配置',
                f'以下平台未配置 Cookie：{", ".join(missing_names)}\n\n是否继续发布？',
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                tabs = self.findChild(QTabWidget)
                tabs.setCurrentIndex(2)  # 切换到设置页
                return
        
        # 显示进度
        self.platform_selector.progress.setVisible(True)
        self.platform_selector.progress.setMaximum(len(platforms))
        self.platform_selector.progress.setValue(0)
        self.platform_selector.status_label.setText('⏳ 正在发布...')
        self.platform_selector.status_label.setStyleSheet('color: #667eea; font-weight: 600;')
        self.platform_selector.publish_btn.setEnabled(False)
        
        # 开始发布
        self.current_platforms = platforms
        self.current_content = content
        self.current_index = 0
        self.results = []
        
        self.publish_next()
    
    def publish_next(self):
        """发布下一个平台"""
        if self.current_index >= len(self.current_platforms):
            # 所有平台发布完成
            self.on_publish_complete()
            return
        
        platform = self.current_platforms[self.current_index]
        
        from config import config
        cookie = config.get(f'platforms.{platform}.cookie', '')
        
        # 创建工作线程
        worker = PublishWorker(platform, self.current_content, cookie)
        worker.status_signal.connect(self.on_publish_status)
        worker.finished_signal.connect(self.on_publish_finished)
        
        self.current_workers.append(worker)
        worker.start()
    
    def on_publish_status(self, message: str, level: str):
        """发布状态更新"""
        self.platform_selector.status_label.setText(message)
        
        if level == 'error':
            self.platform_selector.status_label.setStyleSheet('color: #ef4444; font-weight: 600;')
        elif level == 'success':
            self.platform_selector.status_label.setStyleSheet('color: #10b981; font-weight: 600;')
        else:
            self.platform_selector.status_label.setStyleSheet('color: #667eea; font-weight: 600;')
    
    def on_publish_finished(self, success: bool, message: str):
        """发布完成"""
        platform = self.current_platforms[self.current_index]
        self.results.append((platform, success))
        
        # 更新进度
        self.current_index += 1
        self.platform_selector.progress.setValue(self.current_index)
        
        # 发布下一个
        QTimer.singleShot(1000, self.publish_next)
    
    def on_publish_complete(self):
        """所有发布完成"""
        success_count = sum(1 for _, success in self.results if success)
        total = len(self.results)
        
        # 恢复按钮
        self.platform_selector.publish_btn.setEnabled(True)
        
        # 更新状态
        if success_count == total:
            self.platform_selector.status_label.setText(f'✅ 全部发布成功 ({success_count}/{total})')
            self.platform_selector.status_label.setStyleSheet('color: #10b981; font-weight: 600;')
            
            # 添加到历史
            self.history.add_record(
                self.current_content['title'],
                self.current_platforms,
                '成功'
            )
            
            QMessageBox.information(
                self,
                '✅ 发布完成',
                f'成功发布到 {success_count} 个平台！\n\n标题：{self.current_content["title"]}',
                QMessageBox.Ok
            )
        else:
            self.platform_selector.status_label.setText(f'⚠️ 部分发布成功 ({success_count}/{total})')
            self.platform_selector.status_label.setStyleSheet('color: #f59e0b; font-weight: 600;')
            
            # 添加到历史
            self.history.add_record(
                self.current_content['title'],
                self.current_platforms,
                '部分成功'
            )
            
            QMessageBox.warning(
                self,
                '⚠️ 发布完成',
                f'发布完成：{success_count} 成功，{total - success_count} 失败\n\n标题：{self.current_content["title"]}',
                QMessageBox.Ok
            )
        
        # 清空编辑器
        self.editor.clear()
        
        # 清理工作线程
        self.current_workers = []
