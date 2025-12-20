let currentColor = { r: 255, g: 255, b: 255 };
let eyeDropper = null;

const pickBtn = document.getElementById('pickBtn');
const colorPreview = document.getElementById('colorPreview');
const hexValue = document.getElementById('hexValue');
const rgbValue = document.getElementById('rgbValue');
const hslValue = document.getElementById('hslValue');
const hexItem = document.getElementById('hexItem');
const rgbItem = document.getElementById('rgbItem');
const hslItem = document.getElementById('hslItem');
const shortcutHint = document.getElementById('shortcutHint');

// 按钮
const pinBtn = document.getElementById('pinBtn');
const compactBtn = document.getElementById('compactBtn');
const minimizeBtn = document.getElementById('minimizeBtn');
const maximizeBtn = document.getElementById('maximizeBtn');
const closeBtn = document.getElementById('closeBtn');

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    // updateColorDisplay();
    setTimeout(() => {
        shortcutHint.classList.add('show');
        setTimeout(() => {
            shortcutHint.classList.remove('show');
            shortcutHint.classList.add('hide');
            setTimeout(() => {
                shortcutHint.style.display = 'none';
            }, 500);
        }, 3000);
    }, 500); 

    if (!window.EyeDropper) {
        alert('您的浏览器不支持EyeDropper API');
        pickBtn.disabled = true;
        pickBtn.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
        pickBtn.title = '浏览器不支持EyeDropper API';
        return;
    }
    
    eyeDropper = new EyeDropper();
    
    // 事件监听器
    pickBtn.addEventListener('click', startColorPicker);
    
    hexItem.addEventListener('click', () => copyColorValue('hex'));
    rgbItem.addEventListener('click', () => copyColorValue('rgb'));
    hslItem.addEventListener('click', () => copyColorValue('hsl'));
    
    // 点击快捷键提示卡片可以手动关闭
    shortcutHint.addEventListener('click', function() {
        shortcutHint.classList.remove('show');
        shortcutHint.classList.add('hide');
        setTimeout(() => {
            shortcutHint.style.display = 'none';
        }, 500);
    });
    setupTitleBarButtons();
});
// 开始取色器
async function startColorPicker() {
    if (!eyeDropper) return;
    try {
        // 防止重复
        pickBtn.disabled = true;
        pickBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        // 启动EyeDropper
        const result = await eyeDropper.open();
        const colorHex = result.sRGBHex;

        const rgb = hexToRgb(colorHex);
        if (rgb) {
            updateColor(rgb.r, rgb.g, rgb.b);
        }
        
    } catch (err) {
        // 用户取消
        if (err.name !== 'AbortError') {
            console.error('取色失败:', err);
            alert('取色失败: ' + err.message);
        }
    } finally {
        // 恢复按钮状态
        pickBtn.disabled = false;
        pickBtn.innerHTML = '<i class="fas fa-eye-dropper"></i>';
    }
}

// 更新颜色
function updateColor(r, g, b) {
    currentColor = { r, g, b };
    updateColorDisplay();
}

// 更新颜色显示
function updateColorDisplay() {
    const { r, g, b } = currentColor;
    const hex = rgbToHex(r, g, b);
    const rgb = `rgb(${r}, ${g}, ${b})`;
    const hsl = rgbToHsl(r, g, b);
    // 更新显示
    hexValue.textContent = hex;
    rgbValue.textContent = rgb;
    hslValue.textContent = hsl;
    // 更新预览
    colorPreview.style.backgroundColor = hex;
    updateGlassEffectBackground(hex);

    
}

// // 更新背景
// function updatBackgroundcolor(color) {
//     document.body.style.backgroundColor = color;
// }

// 更新玻璃效果背景
function updateGlassEffectBackground(color) {
    const oldStyle = document.getElementById('glass-effect-style');
    if (oldStyle) {
        oldStyle.remove();
    }
    const style = document.createElement('style');
    style.id = 'glass-effect-style';
    style.textContent = `
        .color-preview::before {
            background: ${color} !important;
        }
    `;
    document.head.appendChild(style);
    document.body.style.backgroundColor = color;
}

// 复制颜色值
function copyColorValue(format) {
    let textToCopy = '';
    
    switch(format) {
        case 'hex':
            textToCopy = hexValue.textContent;
            break;
        case 'rgb':
            textToCopy = rgbValue.textContent;
            break;
        case 'hsl':
            textToCopy = hslValue.textContent;
            break;
    }
    
    navigator.clipboard.writeText(textToCopy).then(() => {
        const item = document.getElementById(`${format}Item`);
        const originalBgColor = item.style.backgroundColor;
        const originalBorderColor = item.style.borderColor;
        
        item.style.backgroundColor = '#d4edda';
        item.style.borderColor = '#c3e6cb';
        
        setTimeout(() => {
            item.style.backgroundColor = originalBgColor;
            item.style.borderColor = originalBorderColor;
        }, 300);
    }).catch(err => {
        console.error('复制失败:', err);
        fallbackCopyText(textToCopy, format);
    });
}

// 备用复制法
function fallbackCopyText(text, format) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            const item = document.getElementById(`${format}Item`);
            const originalBgColor = item.style.backgroundColor;
            const originalBorderColor = item.style.borderColor;
            
            item.style.backgroundColor = '#d4edda';
            item.style.borderColor = '#c3e6cb';
            
            setTimeout(() => {
                item.style.backgroundColor = originalBgColor;
                item.style.borderColor = originalBorderColor;
            }, 300);
        } else {
            alert('复制失败' + text);
        }
    } catch (err) {
        console.error('复制失败:', err);
        alert('复制失败' + text);
    }
    document.body.removeChild(textArea);
}
// 十六转RGB
function hexToRgb(hex) {
    hex = hex.replace('#', '');
    if (hex.length === 3) {
        const r = parseInt(hex.charAt(0) + hex.charAt(0), 16);
        const g = parseInt(hex.charAt(1) + hex.charAt(1), 16);
        const b = parseInt(hex.charAt(2) + hex.charAt(2), 16);
        return { r, g, b };
    } else if (hex.length === 6) {
        const r = parseInt(hex.substring(0, 2), 16);
        const g = parseInt(hex.substring(2, 4), 16);
        const b = parseInt(hex.substring(4, 6), 16);
        return { r, g, b };
    }
    return null;
}

// RGB转十六
function rgbToHex(r, g, b) {
    return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1).toUpperCase()}`;
}

// RGB转HSL
function rgbToHsl(r, g, b) {
    r /= 255;
    g /= 255;
    b /= 255;
    
    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    let h, s, l = (max + min) / 2;
    
    if (max === min) {
        h = s = 0; 
    } else {
        const d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        
        switch (max) {
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        
        h /= 6;
    }
    
    h = Math.round(h * 360);
    s = Math.round(s * 100);
    l = Math.round(l * 100);
    
    return `hsl(${h}, ${s}%, ${l}%)`;
}

// 生成随机颜色（备用功能）
function generateRandomColor() {
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    updateColor(r, g, b);
}

// 添加右键菜单生成随机颜色
pickBtn.addEventListener('contextmenu', function(e) {
    e.preventDefault();
    generateRandomColor();
});

//快捷键
document.addEventListener('keydown', function(e) {
    if (e.key === 'r' && e.ctrlKey) {
        e.preventDefault();
        generateRandomColor();
    }
    
    if (e.key === 'c' && e.ctrlKey && !e.shiftKey) {
        e.preventDefault();
        copyColorValue('hex');
    }
    
    if (e.key === 'C' && e.ctrlKey && e.shiftKey) {
        e.preventDefault();
        copyColorValue('rgb');
    }
});

//标题栏按钮
function setupTitleBarButtons() {
    // 置顶
    let isPinned = false;
    pinBtn.addEventListener('click', function() {
        isPinned = !isPinned;
        if (isPinned) {
            pinBtn.innerHTML = '<i class="fas fa-thumbtack" style="color: #4dabf7;"></i>';
            pinBtn.title = '取消置顶';
            try {
                window.pywebview.api.set_always_on_top(true);
            } catch (e) {

            }
        } else {
            pinBtn.innerHTML = '<i class="fas fa-thumbtack"></i>';
            pinBtn.title = '置顶';
            try {
                window.pywebview.api.set_always_on_top(false);
            } catch (e) {

            }
        }
    });
    
    // 模式
    let isCompactMode = false;
    compactBtn.addEventListener('click', function() {
        isCompactMode = !isCompactMode;
        const body = document.body;
        
        if (isCompactMode) {
            // 切换迷你
            body.classList.remove('standard-mode');
            body.classList.add('compact-mode');
            compactBtn.innerHTML = '<i class="fas fa-expand"></i>';
            compactBtn.title = '标准模式';
            try {
                window.pywebview.api.resize_window(330, 160);
            } catch (e) {

            }
        } else {
            // 切换标准
            body.classList.remove('compact-mode');
            body.classList.add('standard-mode');
            compactBtn.innerHTML = '<i class="fas fa-compress"></i>';
            compactBtn.title = '精简模式';
            try {
                window.pywebview.api.resize_window(800, 500);
            } catch (e) {

            }
        }
    });
    
    // 最小化
    minimizeBtn.addEventListener('click', function() {
        try {
            window.pywebview.api.minimize_window();
        } catch (e) {

        }
    });
    
    // 最大化
    let isMaximized = false;
    maximizeBtn.addEventListener('click', function() {
        isMaximized = !isMaximized;
        if (isMaximized) {
            maximizeBtn.innerHTML = '<i class="fas fa-window-restore"></i>';
            maximizeBtn.title = '还原';
            try {
                window.pywebview.api.maximize_window();
            } catch (e) {

            }
        } else {
            maximizeBtn.innerHTML = '<i class="fas fa-window-maximize"></i>';
            maximizeBtn.title = '最大化';
            try {
                window.pywebview.api.restore_window();
            } catch (e) {

            }
        }
    });
    
    // 关闭
    closeBtn.addEventListener('click', function() {
        try {
            window.pywebview.api.close_window();
        } catch (e) {
            alert('在桌面程序中，此按钮将关闭窗口。在浏览器中，请手动关闭标签页。\n In the desktop application, this button will close the window. In the browser, please close the tab manually.');
        }
    });
    
    //拖动
    const titleBar = document.getElementById('customTitleBar');
    if (titleBar) {
        titleBar.addEventListener('mousedown', function(e) {
            if (e.target.closest('.title-bar-buttons')) {
                return;
            }
            
            try {
                window.pywebview.api.start_drag();
            } catch (e) {

            }
        });
    }
}

