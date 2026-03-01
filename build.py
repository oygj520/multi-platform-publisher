# -*- coding: utf-8 -*-
"""
构建脚本 - 使用 PyInstaller 打包成 exe
"""

import os
import sys
import subprocess


def main():
    # 获取项目根目录
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    print("=" * 60)
    print("Multi-Platform Publisher - Build Script")
    print("=" * 60)
    
    # 清理旧的构建文件
    print("\n[1/3] Cleaning old build files...")
    build_dir = os.path.join(project_dir, 'build')
    dist_dir = os.path.join(project_dir, 'dist')
    
    if os.path.exists(build_dir):
        import shutil
        shutil.rmtree(build_dir)
        print(f"[OK] Deleted {build_dir}")
    
    if os.path.exists(dist_dir):
        import shutil
        shutil.rmtree(dist_dir)
        print(f"[OK] Deleted {dist_dir}")
    
    # 运行 PyInstaller
    print("\n[2/3] Starting build...")
    cmd = [
        sys.executable,
        '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
        '--windowed',
        '--name', 'MultiPlatformPublisher',
        '--add-data', 'ui;ui',
        '--add-data', 'publisher;publisher',
        'app.py'
    ]
    
    print(f"Command: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, cwd=project_dir)
    
    if result.returncode == 0:
        exe_path = os.path.join(dist_dir, 'MultiPlatformPublisher.exe')
        if os.path.exists(exe_path):
            print("\n" + "=" * 60)
            print("[SUCCESS] Build completed!")
            print(f"[SUCCESS] EXE file: {exe_path}")
            print("=" * 60)
            return True
        else:
            print("\n[ERROR] Build completed but EXE not found")
            return False
    else:
        print("\n[ERROR] Build failed")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
