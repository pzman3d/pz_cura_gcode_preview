# pz_cura_gcode_preview

一個強大的Cura插件，提供即時GCODE圖層預覽和分析功能，專為3D列印愛好者和專業人士設計。**完美用於驗證ARC運動指令（G2/G3）和監控GCODE檔案中的溫度/流量調整。**

## 🌐 語言支援

- 🇺🇸 [English](README.md)
- 🇹🇼 [繁體中文](README_zh_TW.md) (目前語言)
- 🇯🇵 [日本語](README_ja.md)

## 🎥 示範影片

觀看插件實際操作：

[![pz_cura_gcode_preview 示範](https://img.youtube.com/vi/m4raWx0PiOg/maxresdefault.jpg)](https://youtu.be/m4raWx0PiOg)

*點擊上方影片觀看完整功能示範*

## 📋 功能特色

- **即時圖層預覽**：即時監控當前列印圖層和步驟
- **GCODE指令分析**：查看每個圖層和步驟的詳細GCODE指令
- **ARC運動驗證**：**檢查G2/G3弧線指令是否正確實作圓形運動**
- **溫度與流量監控**：**即時監控溫度調整和流量變化**
- **自動滾動控制**：切換自動滾動到當前圖層指令
- **暫存GCODE儲存**：將當前Cura GCODE儲存為暫存檔案
- **檔案管理**：輕鬆選擇和管理GCODE檔案
- **多語言支援**：繁體中文介面，使用微軟正黑體字型
- **專業介面**：簡潔現代的介面設計，直觀易用

## 🚀 安裝說明

### 系統需求
- Creality Slicer 4.8 或相容的Cura切片軟體
- Python 3.x（Cura內建）
- PyQt5（Cura內建）

### 安裝步驟

1. **下載插件**
   ```bash
   git clone https://github.com/pzman3d/pz_cura_gcode_preview.git
   ```

2. **複製到Cura插件目錄**
   - 導航到您的Cura插件目錄：
     - **Windows**: `%APPDATA%\Creality Slicer\4.8\plugins\`
     - **macOS**: `~/Library/Application Support/Creality Slicer/4.8/plugins/`
     - **Linux**: `~/.local/share/cura/4.8/plugins/`

3. **安裝插件**
   - 將 `LayerPreviewPlugin` 資料夾複製到您的插件目錄
   - 重新啟動 Creality Slicer

4. **驗證安裝**
   - 開啟 Creality Slicer
   - 前往 `擴充功能` → `pz_cura_gcode_preview` → `顯示圖層預覽`
   - 插件視窗應成功開啟

## 📖 使用指南

### 快速開始

> **💡 提示**：觀看上方[示範影片](https://youtu.be/m4raWx0PiOg)了解所有功能的視覺化操作！

### 基本使用

1. **開啟插件**
   - 啟動 Creality Slicer
   - 載入您的3D模型並進行切片
   - 前往 `擴充功能` → `pz_cura_gcode_preview` → `顯示圖層預覽`

2. **查看圖層資訊**
   - 插件顯示當前圖層、步驟和總圖層數
   - 資訊每500毫秒自動更新

3. **載入GCODE檔案**
   - 點擊 `選擇GCODE檔案` 載入GCODE檔案
   - 或使用 `儲存暫存GCODE` 儲存當前Cura GCODE

### 進階功能

#### 自動滾動控制
- **啟用自動滾動**：自動跳轉到當前圖層指令
- **停用自動滾動**：凍結顯示，允許手動滾動
- 使用 `自動滾動` 核取方塊切換

#### 暫存GCODE管理
- **儲存暫存GCODE**：將當前Cura GCODE儲存到 `GCODE_temp` 資料夾
- **刪除暫存GCODE**：刪除所有暫存GCODE檔案
- 檔案儲存後會自動載入

#### GCODE指令分析
- 查看每個圖層的詳細GCODE指令
- 當前步驟的指令會高亮顯示
- 格式：`( 圖層 X / 步驟 Y ) GCODE_指令`
- 顯示範圍顯示指令數量和範圍

#### 🔍 ARC運動驗證
- **G2/G3弧線指令**：驗證圓形運動指令是否正確生成
- **平滑曲線**：檢查切片器是否使用弧線指令而非線性線段
- **列印品質**：確保平滑曲面無可見圖層線
- **檔案大小**：使用高效弧線指令減少GCODE檔案大小

#### 🌡️ 溫度與流量監控
- **溫度變化**：監控M104/M109溫度設定指令
- **流量調整**：追蹤M221流量修改指令
- **圖層轉換**：識別圖層間的溫度變化
- **列印優化**：分析溫度和流量模式以獲得更好結果

### 介面元素

| 元素 | 說明 |
|------|------|
| **當前圖層資訊** | 顯示當前圖層、步驟和總圖層數 |
| **GCODE檔案路徑** | 顯示當前載入的GCODE檔案路徑 |
| **選擇GCODE檔案** | 瀏覽和載入GCODE檔案 |
| **儲存暫存GCODE** | 將當前Cura GCODE儲存為暫存檔案 |
| **刪除暫存GCODE** | 刪除所有暫存GCODE檔案 |
| **自動滾動** | 切換自動滾動到當前指令 |
| **GCODE指令** | 可滾動的GCODE指令顯示 |
| **狀態列** | 顯示當前操作狀態 |

## 🔧 設定

### 自動滾動設定
- **啟用**：自動滾動到當前圖層指令
- **停用**：凍結顯示，允許手動導航
- 狀態在會話間保持

### 檔案管理
- 暫存檔案儲存在 `GCODE_temp` 資料夾
- 檔案以時間戳命名：`GCODE_temp_YYYYMMDD_HHMMSS.gcode`
- 可透過 `刪除暫存GCODE` 按鈕自動清理

## 🐛 故障排除

### 常見問題

**插件未出現在擴充功能選單中**
- 確保插件在正確目錄中
- 重新啟動 Creality Slicer
- 檢查檔案權限

**GCODE顯示未更新**
- 驗證GCODE檔案已載入
- 檢查自動滾動是否啟用
- 確保Cura已完成切片

**暫存檔案無法儲存**
- 檢查插件目錄的寫入權限
- 確保有足夠的磁碟空間
- 驗證Cura已生成GCODE

**ARC指令未顯示**
- 在Cura中啟用"Arc Welder"插件
- 檢查模型是否有曲面
- 驗證切片器設定中的弧線生成

**溫度指令不可見**
- 確保GCODE包含M104/M109指令
- 檢查Cura中是否啟用溫度設定
- 驗證材料配置檔案有溫度設定

### 除錯資訊
- 在Cura中啟用除錯記錄
- 檢查控制台輸出的錯誤訊息
- 插件記錄所有操作以便故障排除

## 📁 檔案結構

```
LayerPreviewPlugin/
├── LayerPreviewPlugin.py    # 主要插件檔案
├── __init__.py              # 插件初始化
├── plugin.json              # 插件元資料
├── GCODE_temp/              # 暫存GCODE儲存
│   └── GCODE_temp_*.gcode   # 暫存檔案
└── README_zh_TW.md          # 此檔案
```

## 🤝 貢獻

歡迎貢獻！請遵循以下步驟：

1. Fork 儲存庫
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的變更 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

### 開發設定
1. 複製儲存庫
2. 安裝開發依賴
3. 進行您的變更
4. 徹底測試
5. 提交 pull request

## 📄 授權

此專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案。

## 👨‍💻 作者

**pzman3d**
- 電子郵件：pzman3d@gmail.com
- GitHub：[@pzman3d](https://github.com/pzman3d)

## 🙏 致謝

- Cura開發團隊提供優秀的切片引擎
- Creality提供使用者友善的介面
- 3D列印社群提供回饋和建議

## 📞 技術支援

如果您遇到任何問題或有疑問：

1. 觀看[示範影片](https://youtu.be/m4raWx0PiOg)獲得視覺指導
2. 查看[故障排除](#-故障排除)章節
3. 搜尋現有[Issues](https://github.com/pzman3d/pz_cura_gcode_preview/issues)
4. 建立新問題並提供詳細描述
5. 聯絡：pzman3d@gmail.com

## 🔄 版本歷史

### v1.0.0
- 初始版本
- 即時圖層預覽
- GCODE指令分析
- **ARC運動驗證（G2/G3指令）**
- **溫度與流量監控**
- 自動滾動控制
- 暫存檔案管理
- 繁體中文介面
- 微軟正黑體字型支援

---

**為3D列印社群而製作 ❤️**
