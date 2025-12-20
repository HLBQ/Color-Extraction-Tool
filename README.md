# 取色工具 (Color Picker Tool)

一个简洁美观的桌面颜色提取应用程序，使用Python和pywebview构建，支持屏幕直接取色。

![应用截图](https://heilibaiqi.top/warehousetools/007/exe.png)

## 功能特性

- 🎨 **屏幕取色**：从屏幕任意位置拾取颜色
- 📋 **颜色格式转换**：支持HEX、RGB、HSL格式
- 🖱️ **一键复制**：点击颜色值即可复制到剪贴板
- 🪟 **自定义标题栏**：隐藏原生标题栏，使用美观的自定义界面
- 📌 **窗口置顶**：可将窗口保持在最前端
- 🔄 **精简模式**：切换为紧凑界面节省屏幕空间
- 🎲 **随机颜色**：按Ctrl+R生成随机颜色
- 🚀 **独立运行**：可打包为独立的exe文件，无需Python环境

## 系统要求

- **操作系统**：Windows 10/11
- **Python**：3.8+（仅开发环境需要）
- **依赖库**：pywebview, pywin32

## 快速开始

### 1. 运行Python版本

```bash

# 安装依赖
pip install pywebview pywin32

# 运行应用
python Color.Extraction.Tool.py
```

### 2. 使用打包版本

安装完库文件后运行构建build程序，打包的exe文件位于 `dist/` 目录，双击即可运行，无需安装Python环境。

## 使用方法

1. **启动应用**：运行程序后会出现颜色选择器窗口
2. **取色操作**：
   - 点击取色按钮（滴管图标）
   - 鼠标移动到屏幕任意位置
   - 点击左键选择颜色
   - 按Esc键退出取色状态
3. **颜色操作**：
   - 点击HEX、RGB或HSL值可复制到剪贴板
   - 按Ctrl+R生成随机颜色
4. **窗口控制**：
   - **置顶按钮**：将窗口保持在最前端
   - **精简模式**：切换为紧凑界面
   - **最小化**：最小化窗口
   - **关闭**：退出应用

## 项目结构

```
color-picker/
├── Color.Extraction.Tool.py    # 主应用程序（Python后端）
├── index.html             # 主界面HTML
├── style.css              # 样式表
├── script.js              # 前端交互逻辑
├── build.py               # 打包脚本
├── icon.ico               # 应用图标
├── LICENSE.txt            # MIT许可证
├── version_info.txt       # 版本信息
├── dist/                  # 打包的exe文件位于该目录
├── css/                   # FontAwesome CSS
│   └── all.min.css
├── webfonts/              # FontAwesome字体
└── build/                 # 构建输出目录
    └── 取色工具/          # PyInstaller构建文件
```

## 开发指南

### 环境设置

```bash
# 创建虚拟环境（可选）
python -m venv venv
venv\Scripts\activate  # Windows

# 安装开发依赖
pip install pywebview pywin32 pyinstaller
```

### 打包应用

```bash
# 使用构建脚本打包
python build.py

# 或直接使用PyInstaller
pyinstaller --onefile --windowed --name "取色工具" Color.Extraction.Tool.py
```

打包后的exe文件将生成在 `dist/` 目录中。

### 自定义修改

- **修改界面**：编辑 `index.html`、`style.css`、`script.js`
- **调整功能**：修改 `Color.Extraction.Tool.py` 中的Python逻辑
- **更换图标**：替换 `icon.ico` 文件
- **更新版本**：编辑 `version_info.txt`

## 快捷键

|  快捷键   | 功能        |
|----------|-------------|
| `Esc`    | 退出取色状态 |
| `Ctrl+R` | 生成随机颜色 |
| `Ctrl+C` | 复制HEX值    |

## 技术栈

- **后端**：Python 3.8+
- **GUI框架**：pywebview
- **前端**：HTML5, CSS3, JavaScript
- **打包工具**：PyInstaller
- **系统集成**：pywin32 (Windows API)

## 许可证

本项目基于 [MIT License](LICENSE.txt) 开源。

## 贡献指南

欢迎提交Issue和Pull Request！

## 常见问题

### Q: 运行时报错"ModuleNotFoundError: No module named 'webview'"
A: 请安装pywebview库：`pip install pywebview`

### Q: 打包后的exe文件很大
A: 这是PyInstaller打包Python环境的正常现象，可以使用UPX压缩进一步减小体积

### Q: 能否在macOS或Linux上运行？
A: 目前仅支持Windows，因为使用了pywin32库。如需跨平台支持，可考虑使用其他GUI框架


## 更新日志

### v1.0.0 (2025-12-20)
- 初始版本发布
---


### 下载应用最新版本
- [Windows 版](https://github.com/HLBQ/color-picker/releases/tag/v1.0)



### 在线版本
 如果您这是想使用而不下载该工具，可以使用下面的网页版本
- [网页版](https://heilibaiqi.top/warehousetools/007/tool/)



*如果这个项目对你有帮助，请给个Star⭐支持一下！*
