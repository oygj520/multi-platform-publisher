# -*- coding: utf-8 -*-
"""
配置管理模块
"""

import os
import json
from pathlib import Path


class Config:
    """配置管理类"""
    
    def __init__(self):
        self.config_dir = Path.home() / '.multi_platform_publisher'
        self.config_file = self.config_dir / 'config.json'
        self.data_file = self.config_dir / 'data.db'
        
        # 确保配置目录存在
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载配置
        self.config = self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # 默认配置
        return {
            'platforms': {
                'zhihu': {'enabled': True, 'cookie': ''},
                'xiaohongshu': {'enabled': True, 'cookie': ''},
                'kuaishou': {'enabled': True, 'cookie': ''},
                'douyin': {'enabled': True, 'cookie': ''},
            },
            'editor': {
                'default_title': '',
                'auto_save': True,
            },
            'publish': {
                'auto_close': False,
                'show_notification': True,
            }
        }
    
    def save(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def get(self, key, default=None):
        """获取配置项"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    def set(self, key, value):
        """设置配置项"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save()
    
    def get_platform_config(self, platform):
        """获取平台配置"""
        return self.config.get('platforms', {}).get(platform, {})
    
    def set_platform_cookie(self, platform, cookie):
        """设置平台 Cookie"""
        if 'platforms' not in self.config:
            self.config['platforms'] = {}
        if platform not in self.config['platforms']:
            self.config['platforms'][platform] = {}
        self.config['platforms'][platform]['cookie'] = cookie
        self.save()


# 全局配置实例
config = Config()
