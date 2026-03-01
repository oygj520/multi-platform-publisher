# -*- coding: utf-8 -*-
"""
多平台发布助手 - 测试脚本
测试各模块功能
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from publisher.cookie_manager import cookie_manager
from publisher.engine import get_publisher, Publisher
import time


def test_cookie_manager():
    """测试 Cookie 管理器"""
    print('=' * 60)
    print('测试 Cookie 管理器')
    print('=' * 60)
    
    # 测试保存 Cookie
    print('\n[1] 测试保存 Cookie...')
    test_cookie = 'test_key=test_value; another_key=another_value'
    success = cookie_manager.save_cookie('zhihu', test_cookie)
    print(f'    保存结果：[OK] 成功' if success else '    保存结果：[FAIL] 失败')
    
    # 测试获取 Cookie
    print('\n[2] 测试获取 Cookie...')
    retrieved = cookie_manager.get_cookie('zhihu')
    print(f'    获取结果：[OK] 成功' if retrieved else '    获取结果：[FAIL] 失败')
    if retrieved:
        print(f'    Cookie 内容：{retrieved[:50]}...')
    else:
        print('    无内容')
    
    # 测试 Cookie 状态
    print('\n[3] 测试 Cookie 状态...')
    status = cookie_manager.get_cookie_status('zhihu')
    print(f'    状态：{status}')
    
    # 测试验证格式
    print('\n[4] 测试 Cookie 格式验证...')
    valid = cookie_manager.validate_cookie_format(test_cookie)
    print(f'    格式验证：[OK] 有效' if valid else '    格式验证：[FAIL] 无效')
    
    # 测试获取所有状态
    print('\n[5] 测试获取所有平台状态...')
    all_status = cookie_manager.get_all_status()
    for platform, status in all_status.items():
        has_cookie = '[OK]' if status.get('has_cookie') else '[FAIL]'
        is_valid = '[OK]' if status.get('is_valid') else '[FAIL]'
        print(f'    {platform}: 有 Cookie={has_cookie}, 有效={is_valid}')
    
    # 清理测试数据
    print('\n[6] 清理测试数据...')
    cookie_manager.delete_cookie('zhihu')
    print('    测试 Cookie 已删除')
    
    print('\n[OK] Cookie 管理器测试完成')
    return True


def test_publisher_initialization():
    """测试发布器初始化"""
    print('\n' + '=' * 60)
    print('测试发布器初始化')
    print('=' * 60)
    
    platforms = ['zhihu', 'xiaohongshu', 'kuaishou', 'douyin']
    
    for platform in platforms:
        print(f'\n[{platform}] 测试初始化...')
        try:
            publisher = get_publisher(platform)
            print(f'    [OK] {platform} 发布器创建成功')
            print(f'    类型：{type(publisher).__name__}')
            print(f'    基类：{Publisher.__name__}')
        except Exception as e:
            print(f'    [FAIL] {platform} 发布器创建失败：{e}')
    
    print('\n[OK] 发布器初始化测试完成')
    return True


def test_browser_launch():
    """测试浏览器启动（可选，需要确认 Chromium 路径）"""
    print('\n' + '=' * 60)
    print('测试浏览器启动')
    print('=' * 60)
    
    chromium_path = r"E:\chrome-win\chrome.exe"
    
    # 检查 Chromium 是否存在
    if not os.path.exists(chromium_path):
        print(f'\n[WARN] Chromium 路径不存在：{chromium_path}')
        print('    请确认 Chromium 已下载到该位置')
        return False
    
    print(f'\n[OK] Chromium 路径存在：{chromium_path}')
    
    # 尝试启动浏览器
    print('\n尝试启动浏览器...')
    try:
        publisher = get_publisher('zhihu')
        
        def status_callback(msg, level):
            print(f'    [{level}] {msg}')
        
        publisher.set_status_callback(status_callback)
        publisher.start(headless=False)
        
        print('\n[OK] 浏览器启动成功')
        
        # 测试导航
        print('\n测试导航到知乎...')
        publisher.page.goto('https://www.zhihu.com', wait_until='domcontentloaded', timeout=30000)
        print(f'    当前 URL: {publisher.page.url}')
        
        # 截图
        print('\n测试截图...')
        publisher.page.screenshot(path='test_screenshot.png')
        print('    截图已保存到：test_screenshot.png')
        
        publisher.close()
        print('\n[OK] 浏览器测试完成')
        return True
        
    except Exception as e:
        print(f'\n[FAIL] 浏览器测试失败：{e}')
        return False


def run_all_tests():
    """运行所有测试"""
    print('\n')
    print('=' * 60)
    print(' ' * 15 + '多平台发布助手 - 测试套件' + ' ' * 15)
    print('=' * 60)
    print()
    
    results = []
    
    # 测试 1: Cookie 管理器
    try:
        result = test_cookie_manager()
        results.append(('Cookie 管理器', result))
    except Exception as e:
        print(f'\n[FAIL] Cookie 管理器测试异常：{e}')
        results.append(('Cookie 管理器', False))
    
    # 测试 2: 发布器初始化
    try:
        result = test_publisher_initialization()
        results.append(('发布器初始化', result))
    except Exception as e:
        print(f'\n[FAIL] 发布器初始化测试异常：{e}')
        results.append(('发布器初始化', False))
    
    # 测试 3: 浏览器启动（可选）
    try:
        result = test_browser_launch()
        results.append(('浏览器启动', result))
    except Exception as e:
        print(f'\n[FAIL] 浏览器启动测试异常：{e}')
        results.append(('浏览器启动', False))
    
    # 汇总结果
    print('\n' + '=' * 60)
    print('测试结果汇总')
    print('=' * 60)
    
    for name, result in results:
        status = '[PASS]' if result else '[FAIL]'
        print(f'    {name}: {status}')
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f'\n总计：{passed}/{total} 测试通过')
    
    if passed == total:
        print('\n[SUCCESS] 所有测试通过！')
    else:
        print(f'\n[WARN] 有 {total - passed} 个测试失败')
    
    return passed == total


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
