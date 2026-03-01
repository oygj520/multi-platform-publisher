# -*- coding: utf-8 -*-
"""
Cookie 管理模块 - V2 版本
负责 Cookie 的加密存储、验证和管理
"""

import json
import base64
import hashlib
import sqlite3
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Tuple
from cryptography.fernet import Fernet


class CookieManager:
    """Cookie 管理器"""
    
    # 各平台 Cookie 验证 URL
    PLATFORM_CHECK_URLS = {
        'zhihu': 'https://www.zhihu.com/api/v4/me',
        'xiaohongshu': 'https://edith.xiaohongshu.com/api/sns/web/v1/user/me',
        'kuaishou': 'https://api.kuaishou.com/openapi/user/info',
        'douyin': 'https://www.douyin.com/aweme/v1/web/user/profile/other/'
    }
    
    # Cookie 有效期（天）
    COOKIE_VALIDITY_DAYS = 7
    
    def __init__(self):
        self.data_dir = Path.home() / '.multi_platform_publisher'
        self.db_file = self.data_dir / 'cookies.db'
        self.key_file = self.data_dir / '.key'
        
        # 确保目录存在
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化加密密钥
        self.cipher = self._init_cipher()
        
        # 初始化数据库
        self._init_db()
    
    def _init_cipher(self) -> Fernet:
        """初始化加密密钥"""
        if self.key_file.exists():
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        
        return Fernet(key)
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()
        
        # Cookie 存储表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cookies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT UNIQUE NOT NULL,
                cookie_data TEXT NOT NULL,
                is_valid INTEGER DEFAULT 1,
                last_checked TEXT,
                check_result TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Cookie 历史表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cookie_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Cookie 验证结果表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cookie_validation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                is_valid INTEGER NOT NULL,
                username TEXT,
                user_id TEXT,
                message TEXT,
                checked_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _encrypt(self, data: str) -> str:
        """加密 Cookie 数据"""
        try:
            encrypted = self.cipher.encrypt(data.encode('utf-8'))
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception as e:
            print(f'加密失败：{e}')
            return None
    
    def _decrypt(self, encrypted_data: str) -> Optional[str]:
        """解密 Cookie 数据"""
        try:
            decoded = base64.b64decode(encrypted_data.encode('utf-8'))
            decrypted = self.cipher.decrypt(decoded)
            return decrypted.decode('utf-8')
        except Exception as e:
            print(f'解密失败：{e}')
            return None
    
    def save_cookie(self, platform: str, cookie_data: str) -> Tuple[bool, str]:
        """
        保存 Cookie
        返回：(成功标志，消息)
        """
        try:
            # 验证 Cookie 格式
            if not self.validate_cookie_format(cookie_data):
                return False, "Cookie 格式无效，请检查后重试"
            
            encrypted = self._encrypt(cookie_data)
            if not encrypted:
                return False, "Cookie 加密失败"
            
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO cookies 
                (platform, cookie_data, is_valid, last_checked, updated_at)
                VALUES (?, ?, 1, ?, ?)
            ''', (platform, encrypted, datetime.now().isoformat(), datetime.now().isoformat()))
            
            # 记录历史
            cursor.execute('''
                INSERT INTO cookie_history (platform, action, details)
                VALUES (?, ?, ?)
            ''', (platform, 'save', f'Cookie updated at {datetime.now().isoformat()}'))
            
            conn.commit()
            conn.close()
            
            # 自动验证 Cookie
            self.validate_cookie(platform)
            
            return True, "Cookie 保存成功"
        except Exception as e:
            error_msg = f'保存 Cookie 失败：{str(e)}'
            print(error_msg)
            return False, error_msg
    
    def get_cookie(self, platform: str) -> Optional[str]:
        """获取 Cookie"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            cursor.execute('SELECT cookie_data, is_valid FROM cookies WHERE platform = ?', (platform,))
            row = cursor.fetchone()
            conn.close()
            
            if row and row[0]:
                decrypted = self._decrypt(row[0])
                return decrypted
            return None
        except Exception as e:
            print(f'获取 Cookie 失败：{e}')
            return None
    
    def delete_cookie(self, platform: str) -> Tuple[bool, str]:
        """删除 Cookie"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM cookies WHERE platform = ?', (platform,))
            
            # 记录历史
            cursor.execute('''
                INSERT INTO cookie_history (platform, action, details)
                VALUES (?, ?, ?)
            ''', (platform, 'delete', f'Cookie deleted at {datetime.now().isoformat()}'))
            
            conn.commit()
            conn.close()
            return True, "Cookie 已删除"
        except Exception as e:
            error_msg = f'删除 Cookie 失败：{str(e)}'
            print(error_msg)
            return False, error_msg
    
    def get_all_cookies(self) -> Dict[str, Optional[str]]:
        """获取所有平台的 Cookie"""
        platforms = ['zhihu', 'xiaohongshu', 'kuaishou', 'douyin']
        return {platform: self.get_cookie(platform) for platform in platforms}
    
    def mark_invalid(self, platform: str) -> bool:
        """标记 Cookie 为无效"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE cookies SET is_valid = 0, last_checked = ?
                WHERE platform = ?
            ''', (datetime.now().isoformat(), platform))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f'标记 Cookie 无效失败：{e}')
            return False
    
    def is_valid(self, platform: str) -> bool:
        """检查 Cookie 是否有效（本地状态）"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT is_valid, updated_at FROM cookies WHERE platform = ?
            ''', (platform,))
            row = cursor.fetchone()
            conn.close()
            
            if not row or not row[0]:
                return False
            
            # 检查是否超过有效期
            if row[1]:
                last_update = datetime.fromisoformat(row[1])
                if datetime.now() - last_update > timedelta(days=self.COOKIE_VALIDITY_DAYS):
                    return False
            
            return True
        except Exception as e:
            print(f'检查 Cookie 有效性失败：{e}')
            return False
    
    def validate_cookie(self, platform: str) -> Tuple[bool, str, Dict]:
        """
        验证 Cookie 有效性（在线验证）
        返回：(是否有效，消息，用户信息)
        """
        try:
            cookie = self.get_cookie(platform)
            if not cookie:
                return False, "未找到 Cookie", {}
            
            # 发送验证请求
            check_url = self.PLATFORM_CHECK_URLS.get(platform)
            if not check_url:
                return False, f"不支持的平台：{platform}", {}
            
            # 解析 Cookie 为字典
            cookies_dict = self._parse_cookie_to_dict(cookie)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
            }
            
            # 根据不同平台设置不同的请求头
            if platform == 'zhihu':
                headers['Authorization'] = f'Bearer {cookies_dict.get("token", "")}'
            elif platform == 'xiaohongshu':
                headers['x-s'] = cookies_dict.get("x-s", "")
                headers['x-t'] = str(int(datetime.now().timestamp() * 1000))
            
            response = requests.get(check_url, cookies=cookies_dict, headers=headers, timeout=10)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # 解析用户信息
                    user_info = self._extract_user_info(platform, data)
                    
                    # 更新数据库
                    self._update_validation_result(platform, True, user_info)
                    self._update_cookie_status(platform, True)
                    
                    username = user_info.get('username', '用户')
                    return True, f"验证成功，欢迎 {username}", user_info
                    
                except json.JSONDecodeError:
                    # 非 JSON 响应，但状态码 200 也认为有效
                    self._update_validation_result(platform, True, {})
                    self._update_cookie_status(platform, True)
                    return True, "验证成功", {}
            else:
                # 验证失败
                self._update_validation_result(platform, False, {}, f"HTTP {response.status_code}")
                self._update_cookie_status(platform, False)
                return False, f"验证失败：HTTP {response.status_code}", {}
                
        except requests.exceptions.Timeout:
            self._update_cookie_status(platform, False)
            return False, "验证超时，请检查网络连接", {}
        except requests.exceptions.RequestException as e:
            self._update_cookie_status(platform, False)
            return False, f"网络错误：{str(e)}", {}
        except Exception as e:
            self._update_cookie_status(platform, False)
            return False, f"验证异常：{str(e)}", {}
    
    def _parse_cookie_to_dict(self, cookie_str: str) -> Dict:
        """将 Cookie 字符串解析为字典"""
        cookies = {}
        try:
            pairs = cookie_str.split(';')
            for pair in pairs:
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    cookies[key.strip()] = value.strip()
        except Exception as e:
            print(f'Cookie 解析警告：{e}')
        return cookies
    
    def _extract_user_info(self, platform: str, data: Dict) -> Dict:
        """从响应数据中提取用户信息"""
        user_info = {}
        
        try:
            if platform == 'zhihu':
                user_info['username'] = data.get('name', '知乎用户')
                user_info['user_id'] = data.get('id', '')
                user_info['avatar'] = data.get('avatar_url', '')
            
            elif platform == 'xiaohongshu':
                user_info['username'] = data.get('nickname', '小红书用户')
                user_info['user_id'] = data.get('red_id', '')
                user_info['avatar'] = data.get('images', {}).get('avatar', '')
            
            elif platform == 'kuaishou':
                user_info['username'] = data.get('user_name', '快手用户')
                user_info['user_id'] = data.get('user_id', '')
            
            elif platform == 'douyin':
                user_info['username'] = data.get('nickname', '抖音用户')
                user_info['user_id'] = data.get('sec_uid', '')
        except Exception as e:
            print(f'提取用户信息失败：{e}')
        
        return user_info
    
    def _update_validation_result(self, platform: str, is_valid: bool, user_info: Dict, message: str = ""):
        """更新验证结果到数据库"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO cookie_validation 
                (platform, is_valid, username, user_id, message, checked_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                platform,
                1 if is_valid else 0,
                user_info.get('username', ''),
                user_info.get('user_id', ''),
                message,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f'更新验证结果失败：{e}')
    
    def _update_cookie_status(self, platform: str, is_valid: bool):
        """更新 Cookie 状态"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE cookies SET is_valid = ?, last_checked = ?, check_result = ?
                WHERE platform = ?
            ''', (1 if is_valid else 0, datetime.now().isoformat(), 
                  'valid' if is_valid else 'invalid', platform))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f'更新 Cookie 状态失败：{e}')
    
    def get_cookie_status(self, platform: str) -> Dict:
        """获取 Cookie 状态信息"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT platform, is_valid, last_checked, created_at, updated_at, check_result
                FROM cookies WHERE platform = ?
            ''', (platform,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                # 获取最新验证结果
                user_info = self._get_latest_validation(platform)
                
                return {
                    'platform': row[0],
                    'is_valid': bool(row[1]),
                    'last_checked': row[2],
                    'created_at': row[3],
                    'updated_at': row[4],
                    'check_result': row[5],
                    'has_cookie': True,
                    'username': user_info.get('username', ''),
                    'days_until_expiry': self._days_until_expiry(row[4])
                }
            return {
                'platform': platform,
                'is_valid': False,
                'has_cookie': False,
                'days_until_expiry': 0
            }
        except Exception as e:
            print(f'获取 Cookie 状态失败：{e}')
            return {'platform': platform, 'is_valid': False, 'has_cookie': False, 'error': str(e)}
    
    def _get_latest_validation(self, platform: str) -> Dict:
        """获取最新验证结果"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT username, user_id FROM cookie_validation 
                WHERE platform = ? ORDER BY checked_at DESC LIMIT 1
            ''', (platform,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {'username': row[0], 'user_id': row[1]}
        except:
            pass
        return {}
    
    def _days_until_expiry(self, updated_at: str) -> int:
        """计算距离过期的天数"""
        try:
            if updated_at:
                last_update = datetime.fromisoformat(updated_at)
                expiry_date = last_update + timedelta(days=self.COOKIE_VALIDITY_DAYS)
                days_left = (expiry_date - datetime.now()).days
                return max(0, days_left)
        except:
            pass
        return 0
    
    def get_all_status(self) -> Dict[str, Dict]:
        """获取所有平台 Cookie 状态"""
        platforms = ['zhihu', 'xiaohongshu', 'kuaishou', 'douyin']
        return {platform: self.get_cookie_status(platform) for platform in platforms}
    
    def validate_cookie_format(self, cookie_str: str) -> bool:
        """验证 Cookie 格式是否基本有效"""
        if not cookie_str:
            return False
        
        cookie_str = cookie_str.strip()
        
        if len(cookie_str) < 20:
            return False
        
        # 检查是否包含有效的 Cookie 格式
        try:
            # JSON 格式
            if cookie_str.startswith('{'):
                data = json.loads(cookie_str)
                return isinstance(data, dict) and len(data) > 0
            
            # 字符串格式（键值对）
            if '=' in cookie_str:
                pairs = [p for p in cookie_str.split(';') if '=' in p]
                return len(pairs) >= 1  # 至少有一个键值对
            
            return False
        except:
            return False
    
    def get_validation_history(self, platform: str = None, limit: int = 10) -> List[Dict]:
        """获取验证历史"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            if platform:
                cursor.execute('''
                    SELECT platform, is_valid, username, message, checked_at
                    FROM cookie_validation 
                    WHERE platform = ?
                    ORDER BY checked_at DESC LIMIT ?
                ''', (platform, limit))
            else:
                cursor.execute('''
                    SELECT platform, is_valid, username, message, checked_at
                    FROM cookie_validation 
                    ORDER BY checked_at DESC LIMIT ?
                ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'platform': row[0],
                    'is_valid': bool(row[1]),
                    'username': row[2],
                    'message': row[3],
                    'checked_at': row[4]
                }
                for row in rows
            ]
        except Exception as e:
            print(f'获取验证历史失败：{e}')
            return []
    
    def clear_expired_cookies(self) -> int:
        """清除过期的 Cookie"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            expiry_date = (datetime.now() - timedelta(days=self.COOKIE_VALIDITY_DAYS)).isoformat()
            
            cursor.execute('''
                UPDATE cookies SET is_valid = 0
                WHERE updated_at < ? AND is_valid = 1
            ''', (expiry_date,))
            
            count = cursor.rowcount
            conn.commit()
            conn.close()
            
            return count
        except Exception as e:
            print(f'清除过期 Cookie 失败：{e}')
            return 0


# 全局 Cookie 管理器实例
cookie_manager = CookieManager()
