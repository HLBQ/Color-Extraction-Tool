#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
取色工具 - 桌面应用程序
使用pywebview将H5颜色选择器嵌入到窗口中
隐藏原生标题栏，使用自定义标题栏
Color Picker Tool - Desktop Application
Embed an H5 color picker into the window using pywebview
Hide the native title bar and use a custom title bar
"""
import os
import sys
import tempfile
from pathlib import Path
import webview
import win32gui
import win32con
WEBVIEW_AVAILABLE = True
PYWIN32_AVAILABLE = True

def force_topmost(hwnd, topmost=True):
    """强制设置窗口置顶状态"""
  
    try:
        if topmost:
            # 设置窗口置顶
            win32gui.SetWindowPos(
                hwnd,
                win32con.HWND_TOPMOST,
                0, 0, 0, 0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW
            )
        else:
            # 取消窗口置顶
            win32gui.SetWindowPos(
                hwnd,
                win32con.HWND_NOTOPMOST,
                0, 0, 0, 0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW
            )
        return True
    except Exception as e:
        print(f"error:窗口置顶时出错: {e}")
        return False

class ColorPickerApp:
    """颜色选择器应用程序"""
    
    def __init__(self):
        self.window = None
        self.html_content = None
        self.temp_dir = None
        self.temp_html_file = None
        self.is_compact_mode = False
        self.is_pinned = False
        self.is_maximized = False
        
    def load_html_content(self):
        """加载HTML内容"""
        # 检查是否在PyInstaller打包的exe中运行
        if getattr(sys, 'frozen', False):
            # 在exe中运行，从临时目录或数据目录读取文件
            base_path = sys._MEIPASS
        else:
            # 正常Python运行，从当前目录读取
            base_path = '.'
        
        # 读取HTML文件
        html_path = os.path.join(base_path, 'index.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # 读取CSS文件
        css_path = os.path.join(base_path, 'style.css')
        with open(css_path, 'r', encoding='utf-8') as f:
            css = f.read()
        
        # 读取JavaScript文件
        js_path = os.path.join(base_path, 'script.js')
        with open(js_path, 'r', encoding='utf-8') as f:
            js = f.read()
        
        # 创建完整的HTML文档
        full_html = f'''
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>取色工具</title>
            <style>{css}</style>
            <link rel="stylesheet" href="css/all.min.css">
        </head>
        <body class="standard-mode">
            <!-- 自定义标题栏 -->
            <div id="customTitleBar" class="custom-title-bar">
                <div class="title-bar-title">取色工具</div>
                <div class="title-bar-buttons">
                    <button class="title-bar-btn" id="pinBtn" title="置顶">
                        <i class="fas fa-thumbtack"></i>
                    </button>
                    <button class="title-bar-btn" id="compactBtn" title="精简模式">
                        <i class="fas fa-compress"></i>
                    </button>
                    <button class="title-bar-btn" id="minimizeBtn" title="最小化">
                        <i class="fas fa-window-minimize"></i>
                    </button>
                    <button class="title-bar-btn" id="maximizeBtn" title="最大化">
                        <i class="fas fa-window-maximize"></i>
                    </button>
                    <button class="title-bar-btn close-btn" id="closeBtn" title="关闭">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>

            <div class="main-container">
                <div class="color-box">
                    <div class="color-preview" id="colorPreview">
                        <button class="pick-btn" id="pickBtn">
                            <i class="fas fa-eye-dropper"></i>
                        </button>
                    </div>
                    
                    <div class="color-info">
                        <div class="info-item" id="hexItem" data-value="hex">
                            <div class="info-label">HEX</div>
                            <div class="info-value" id="hexValue">#FFFFFF</div>
                        </div>
                        
                        <div class="info-item" id="rgbItem" data-value="rgb">
                            <div class="info-label">RGB</div>
                            <div class="info-value" id="rgbValue">rgb(255, 255, 255)</div>
                        </div>
                        
                        <div class="info-item" id="hslItem" data-value="hsl">
                            <div class="info-label">HSL</div>
                            <div class="info-value" id="hslValue">hsl(0, 0%, 100%)</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 提示 -->
            <div id="shortcutHint" class="shortcut-hint">
                <div>Tips:</div>
                <div>Esc: 退出取色状态</div>
                <div>Ctrl+R: 随机颜色</div>
                <div>点击右侧代码可复制</div>
            </div>

            <script>{js}</script>
        </body>
        </html>
        '''
        
        return full_html
    
    def create_temp_html_file(self, html_content):
        """创建临时HTML文件"""
        self.temp_dir = tempfile.mkdtemp(prefix='color_picker_')
        self.temp_html_file = os.path.join(self.temp_dir, 'index.html')
        
        with open(self.temp_html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 检查是否在PyInstaller打包的exe中运行
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = '.'
        
        # 复制CSS和字体文件到临时目录
        for item in ['css', 'webfonts']:
            source_dir = os.path.join(base_path, item)
            if os.path.exists(source_dir):
                import shutil
                dest_dir = os.path.join(self.temp_dir, item)
                shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
        
        return f'file://{self.temp_html_file}'
    
    def on_closed(self):
        """窗口关闭时的回调"""
        print("窗口已关闭")
        
    def on_shown(self):
        """窗口显示时的回调"""
        print("窗口已显示")
        
    def on_loaded(self):
        """页面加载完成时的回调"""
        print("页面加载完成")
    
    # JavaScript API方法
    def set_always_on_top(self, always_on_top):
        """设置窗口置顶"""
        if not self.window:
            return False
        
        # 使用win32gui查找窗口
        print(f"设置窗口置顶状态: {bool(always_on_top)}")
        try:
            hwnd = None
            try:
                # 通过窗口标题查找窗口句柄
                def enum_windows_callback(hwnd_enum, extra):
                    if win32gui.IsWindowVisible(hwnd_enum):
                        window_text = win32gui.GetWindowText(hwnd_enum)
                        # 查找包含"取色工具"的窗口
                        if '取色工具' in window_text:
                            nonlocal hwnd
                            hwnd = hwnd_enum
                            return False  # 停止枚举
                    return True  # 继续枚举
                
                win32gui.EnumWindows(enum_windows_callback, None)
            except Exception as e:
                print(f"error:查找窗口时出错: {e}")
                return False
            
            if hwnd:
                # 使用pywin32 API强制置顶
                success = force_topmost(hwnd, bool(always_on_top))
                if success:
                    print(f"窗口置顶设置成功: {bool(always_on_top)}")
                    self.is_pinned = bool(always_on_top)
                    return True
                else:
                    print(f"窗口置顶设置失败")
                    return False
            else:
                print("无法找到取色工具窗口")
                return False
                
        except Exception as e:
            print(f"设置窗口置顶时出错: {e}")
            return False
    
    def resize_window(self, width, height):
        """调整窗口大小"""
        if self.window:
            self.window.resize(width, height)
            self.is_compact_mode = (width == 330 and height == 160)
            return True
        return False
    
    def minimize_window(self):
        """最小化窗口"""
        if self.window:
            self.window.minimize()
            return True
        return False
    
    def maximize_window(self):
        """最大化窗口"""
        if self.window:
            self.window.maximize()
            self.is_maximized = True
            return True
        return False
    
    def restore_window(self):
        """还原窗口"""
        if self.window:
            self.window.restore()
            self.is_maximized = False
            return True
        return False
    
    def close_window(self):
        """关闭窗口"""
        if self.window:
            self.window.destroy()
            return True
        return False
    
    def start_drag(self):
        """开始拖动窗口"""
        return True
    
    def run(self):
        """运行应用程序"""
        # 检查是否在PyInstaller打包的exe中运行
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = '.'
        
        # 检查必要文件
        required_files = ['index.html', 'style.css', 'script.js']
        missing_files = []
        
        for file in required_files:
            file_path = os.path.join(base_path, file)
            if not os.path.exists(file_path):
                missing_files.append(file)
        
        if missing_files:
            print("error: 缺少必要的文件:")
            for file in missing_files:
                print(f"  - {file}")
            print(f"搜索路径: {base_path}")
            print("请确保所有H5文件都在正确目录中。")
            return 1
        
        # 加载HTML内容
        self.html_content = self.load_html_content()
        
        # 创建临时HTML文件
        url = self.create_temp_html_file(self.html_content)
        
        # 创建窗口 - 隐藏原生标题栏，使用自定义标题栏
        try:
            self.window = webview.create_window(
                title='取色工具',
                url=url,
                width=800,
                height=500,
                resizable=False,  # 不允许更改大小，通过自定义按钮控制
                fullscreen=False,
                frameless=True,  # 隐藏原生标题栏
                easy_drag=True,  # 启用拖动
                background_color='#2d2d2d',
                js_api=self
            )
            
            # 设置事件回调
            self.window.events.closed += self.on_closed
            self.window.events.shown += self.on_shown
            self.window.events.loaded += self.on_loaded
            
            # 启动窗口
            webview.start(debug=False, http_server=False)
            
            print("取色工具已关闭")
            
            # 清理临时文件
            if self.temp_dir and os.path.exists(self.temp_dir):
                import shutil
                shutil.rmtree(self.temp_dir)
                print("已清理临时文件")
            
            return 0
            
        except Exception as e:
            print("=" * 50)
            print(f"error启动失败: {e}")
            import traceback
            traceback.print_exc()
            return 1

def main():
    """主函数"""
    app = ColorPickerApp()
    return app.run()

if __name__ == '__main__':
    sys.exit(main())
