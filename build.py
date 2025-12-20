#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H5颜色选择器 - 打包脚本
将Python后端程序打包成独立的exe文件
直接在当前目录打包
"""
import os
import sys
import subprocess

def build_exe():
    if not os.path.exists('color_picker_app.py'):
        print("错误: color_picker_app.py 文件不存在")
        return 1
    main_files = ['index.html', 'style.css', 'script.js']
    missing_files = []
    for file in main_files:
        if not os.path.exists(file):
            missing_files.append(file)
    if missing_files:
        print(f"error: 以下文件不存在: {', '.join(missing_files)}")
        print("  打包将继续，但应用程序可能无法正常工作")
    
    css_dir = 'css'
    if not os.path.exists(css_dir):
        print(f"error: CSS目录不存在: {css_dir}")
    
    webfonts_dir = 'webfonts'
    if not os.path.exists(webfonts_dir):
        print(f"error: webfonts目录不存在: {webfonts_dir}")

    icon_param = []
    if os.path.exists('icon.ico'):
        icon_param = ['--icon', 'icon.ico']
        print(f"使用图标文件: icon.ico")
    else:
        print("未找到图标文件，将使用默认图标")

    # 构建PyInstaller命令 - 使用--windowed隐藏控制台窗口
    # 直接在当前目录打包，使用相对路径
    cmd = [
        'pyinstaller',
        '--onefile',  # 单文件exe
        '--windowed',  # 隐藏控制台窗口
        '--name', '取色工具',  # 使用中文名称
        '--version-file', 'version_info.txt', 

        '--collect-all=webview',   # 仅收集webview核心依赖
        '--hidden-import=win32gui',
        '--hidden-import=win32con',

        
        '--exclude-module=tkinter',
        '--exclude-module=unittest',
        '--exclude-module=numpy',
        '--exclude-module=pandas',
        '--exclude-module=matplotlib',
        '--exclude-module=scipy',
        '--exclude-module=PIL',    # 如果你没用到PIL/ Pillow，保留这行
        '--exclude-module=requests',# 没用到网络请求就保留
        '--optimize=1',  # 代码优化级别，减少体积同时提升运行速度
    ] + icon_param + [
        '--add-data', 'index.html;.',  # 添加index.html
        '--add-data', 'style.css;.',   # 添加style.css
        '--add-data', 'script.js;.',   # 添加script.js
        '--add-data', 'css;css',       # 添加css目录
        '--add-data', 'webfonts;webfonts',  # 添加webfonts目录
        '--add-data', 'LICENSE.txt;.',  # 开源协议文件
        '--hidden-import', 'webview',
        '--hidden-import', 'webview.platforms.win32',  # 补充win32平台依赖
        '--hidden-import', 'pythonnet',
        '--clean',  # 清理临时文件
        'color_picker_app.py'
    ]
    print(f"正在执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"打包失败:")
        print(f"标准输出: {result.stdout}")
        print(f"标准错误: {result.stderr}")
        return 1
    
    print("打包成功!")
    
    dist_dir = 'dist'
    if os.path.exists(dist_dir):
        exe_files = [f for f in os.listdir(dist_dir) if f.endswith('.exe')]
        if exe_files:
            exe_file = exe_files[0]
            exe_path = os.path.join(dist_dir, exe_file)
            
            print(f"\nEXE文件已生成: {exe_path}")
            print(f"   大小: {os.path.getsize(exe_path) / (1024*1024):.2f} MB")
            return 0
        else:
            print("错误: 没有找到生成的exe文件")
            return 1
    else:
        print("错误: dist目录不存在")
        return 1

def main():
    """主函数"""
    return build_exe()

if __name__ == '__main__':
    sys.exit(main())
