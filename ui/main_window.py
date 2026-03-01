# -*- coding: utf-8 -*-
"""
主窗口界面
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel,
    QTabWidget, QCheckBox, QGroupBox, QFileDialog,
    QMessageBox, QProgressBar, QListWidget, QListWidgetItem,
    QSplitter, QToolBar, QAction, QStatusBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap

import os
import markdown


class EditorWidget(QWidget):
    """Markdown 编辑器组件"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 标题输入
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText('输入标题...')
        self.title_input.setFont(QFont('Microsoft YaHei', 14))
        layout.addWidget(self.title_input)
        
        # 分割器（编辑器 + 预览）
        splitter = QSplitter(Qt.Horizontal)
        
        # Markdown 编辑器
        self.editor = QTextEdit()
        self.editor.setPlaceholderText('使用 Markdown 格式编写内容...\n\n# 标题\n## 副标题\n\n正文内容...')
        self.editor.setFont(QFont('Consolas', 11))
        splitter.addWidget(self.editor)
        
        # 预览区域
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setFont(QFont('Microsoft YaHei', 11))
        splitter.addWidget(self.preview)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)
        
        # 封面图
        cover_layout = QHBoxLayout()
        cover_label = QLabel('封面图:')
        self.cover_path = QLabel('未选择')
        self.cover_btn = QPushButton('选择图片')
        self.cover_btn.clicked.connect(self.select_cover)
        cover_layout.addWidget(cover_label)
        cover_layout.addWidget(self.cover_path)
        cover_layout.addWidget(self.cover_btn)
        layout.addLayout(cover_layout)
        
        self.setLayout(layout)
    
    def select_cover(self):
        """选择封面图片"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择封面图片', '',
            '图片文件 (*.png *.jpg *.jpeg *.gif)'
        )
        if file_path:
            self.cover_path.setText(file_path)
    
    def get_content(self):
        """获取编辑器内容"""
        return {
            'title': self.title_input.text(),
            'content': self.editor.toPlainText(),
            'html': markdown.markdown(self.editor.toPlainText()),
            'cover': self.cover_path.text() if self.cover_path.text() != '未选择' else None
        }
    
    def preview_content(self):
        """预览内容"""
        content = self.get_content()
        html = f'''
        <html>
        <head>
            <style>
                body {{ font-family: Microsoft YaHei; padding: 20px; }}
                h1 {{ color: #1e88e5; }}
                h2 {{ color: #43a047; }}
                img {{ max-width: 100%; }}
            </style>
        </head>
        <body>
            <h1>{content['title']}</h1>
            {content['html']}
        </body>
        </html>
        '''
        self.preview.setHtml(html)


class PlatformSelector(QWidget):
    """平台选择组件"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        group = QGroupBox('选择发布平台')
        group_layout = QVBoxLayout(group)
        
        # 平台复选框
        self.zhihu_cb = QCheckBox('知乎')
        self.xiaohongshu_cb = QCheckBox('小红书')
        self.kuaishou_cb = QCheckBox('快手')
        self.douyin_cb = QCheckBox('抖音')
        
        self.zhihu_cb.setChecked(True)
        self.xiaohongshu_cb.setChecked(True)
        
        group_layout.addWidget(self.zhihu_cb)
        group_layout.addWidget(self.xiaohongshu_cb)
        group_layout.addWidget(self.kuaishou_cb)
        group_layout.addWidget(self.douyin_cb)
        
        layout.addWidget(group)
        
        # 发布按钮
        self.publish_btn = QPushButton('🚀 一键发布')
        self.publish_btn.setStyleSheet('''
            QPushButton {
                background-color: #1e88e5;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        ''')
        layout.addWidget(self.publish_btn)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # 状态标签
        self.status_label = QLabel('就绪')
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
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


class PublishHistory(QWidget):
    """发布历史组件"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 历史记录列表
        self.history_list = QListWidget()
        layout.addWidget(self.history_list)
        
        # 清空按钮
        clear_btn = QPushButton('清空历史')
        clear_btn.clicked.connect(self.history_list.clear)
        layout.addWidget(clear_btn)
        
        self.setLayout(layout)
    
    def add_record(self, title, platforms, status):
        """添加发布记录"""
        item_text = f"{title}\n平台：{', '.join(platforms)} | 状态：{status}"
        item = QListWidgetItem(item_text)
        self.history_list.addItem(item)


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('多平台发布助手 v1.0')
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 标签页
        tabs = QTabWidget()
        
        # 发布标签页
        publish_widget = QWidget()
        publish_layout = QHBoxLayout(publish_widget)
        
        # 左侧：编辑器
        self.editor = EditorWidget()
        publish_layout.addWidget(self.editor, stretch=2)
        
        # 右侧：平台选择
        self.platform_selector = PlatformSelector()
        publish_layout.addWidget(self.platform_selector, stretch=1)
        
        tabs.addTab(publish_widget, '📝 发布内容')
        
        # 历史标签页
        self.history = PublishHistory()
        tabs.addTab(self.history, '📜 发布历史')
        
        # 设置标签页
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        settings_layout.addWidget(QLabel('平台配置（Cookie 管理）'))
        settings_layout.addWidget(QLabel('TODO: 实现 Cookie 配置界面'))
        tabs.addTab(settings_widget, '⚙️ 设置')
        
        main_layout.addWidget(tabs)
        
        # 状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('就绪 - 请选择平台并点击发布')
        
        # 连接信号
        self.platform_selector.publish_btn.clicked.connect(self.start_publish)
    
    def start_publish(self):
        """开始发布"""
        content = self.editor.get_content()
        platforms = self.platform_selector.get_selected_platforms()
        
        if not content['title']:
            QMessageBox.warning(self, '警告', '请输入标题')
            return
        
        if not content['content']:
            QMessageBox.warning(self, '警告', '请输入内容')
            return
        
        if not platforms:
            QMessageBox.warning(self, '警告', '请至少选择一个平台')
            return
        
        # 显示进度
        self.platform_selector.progress.setVisible(True)
        self.platform_selector.status_label.setText('正在发布...')
        
        # TODO: 实现实际发布逻辑
        # 这里先模拟发布过程
        self.simulate_publish(content, platforms)
    
    def simulate_publish(self, content, platforms):
        """模拟发布过程（后续替换为实际发布）"""
        self.platform_selector.progress.setMaximum(len(platforms))
        
        for i, platform in enumerate(platforms):
            self.platform_selector.progress.setValue(i + 1)
            self.platform_selector.status_label.setText(f'正在发布到 {platform}...')
        
        # 发布完成
        self.platform_selector.status_label.setText('发布完成！')
        self.statusBar.showMessage(f'已发布到 {len(platforms)} 个平台')
        
        # 添加到历史
        self.history.add_record(
            content['title'],
            platforms,
            '成功'
        )
        
        QMessageBox.information(
            self,
            '发布完成',
            f'成功发布到 {len(platforms)} 个平台！\n\n注意：当前是演示版本，实际发布功能需要配置各平台 Cookie。'
        )
