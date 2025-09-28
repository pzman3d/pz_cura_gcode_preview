from UM.Extension import Extension
from UM.Logger import Logger
from cura.CuraApplication import CuraApplication
from PyQt5.QtCore import QTimer, pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QFileDialog, QMessageBox, QTextEdit, QScrollBar, QCheckBox
from PyQt5.QtGui import QFont, QTextCursor
import os
import shutil
from datetime import datetime

class LayerPreviewWidget(QWidget):
    """Layer Preview Window"""
    
    def __init__(self):
        super().__init__()
        self.gcode_lines = []  # Store GCODE lines
        self.setupUI()
        
        # Setup timer for updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.updatePreviewInfo)
        self.update_timer.start(500)  # Update every 500ms
        
    def setupUI(self):
        """Setup UI interface"""
        self.setWindowTitle("pz_cura_gcode_preview - Layer Preview Monitor")
        self.setMinimumSize(500, 400)
        self.resize(600, 700)
        
        # Set window properties to overlay on Cura GUI
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Window)
        self.setAttribute(Qt.WA_ShowWithoutActivating, False)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title_label = QLabel("pz_cura_gcode_preview")
        title_label.setStyleSheet("font-family: 'Microsoft JhengHei', '微軟正黑體', sans-serif; font-size: 20px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignCenter)  # Center alignment
        layout.addWidget(title_label)
        
        # Author info
        author_label = QLabel("Author: pzman3d / pzman3d@gmail.com")
        author_label.setStyleSheet("font-family: 'Microsoft JhengHei', '微軟正黑體', sans-serif; font-size: 12px; color: #6c757d; margin-bottom: 5px;")
        author_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(author_label)
        
        # Information display area
        self.info_label = QLabel("Loading...")
        self.info_label.setStyleSheet("""
            background-color: #f8f9fa; 
            border: 1px solid #dee2e6; 
            padding: 15px; 
            border-radius: 8px; 
            font-family: 'Microsoft JhengHei', '微軟正黑體', sans-serif;
            font-size: 16px; 
            line-height: 1.6;
            color: #495057;
        """)
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)
        
        # GCODE file selection area
        gcode_file_label = QLabel("GCODE Commands for Current Layer")
        gcode_file_label.setStyleSheet("font-family: 'Microsoft JhengHei', '微軟正黑體', sans-serif; font-weight: bold; margin-top: 15px; font-size: 16px;")
        layout.addWidget(gcode_file_label)
        
        # GCODE file path display
        self.gcode_path_label = QLabel("GCODE File Path: Not selected")
        self.gcode_path_label.setStyleSheet("background-color: #e9ecef; padding: 8px; border-radius: 4px; font-family: 'Microsoft JhengHei', '微軟正黑體', sans-serif; font-size: 14px; color: #6c757d;")
        self.gcode_path_label.setWordWrap(True)
        layout.addWidget(self.gcode_path_label)
        
        # Button area
        button_layout = QHBoxLayout()
        
        self.select_button = QPushButton("Select GCODE File")
        self.select_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff; 
                color: white; 
                border: none; 
                padding: 8px 16px; 
                border-radius: 4px; 
                font-family: 'Microsoft JhengHei', '微軟正黑體', sans-serif;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.select_button.clicked.connect(self.selectGcodeFile)
        button_layout.addWidget(self.select_button)
        
        self.temp_gcode_button = QPushButton("Save Temp GCODE")
        self.temp_gcode_button.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8; 
                color: white; 
                border: none; 
                padding: 8px 16px; 
                border-radius: 4px; 
                font-family: 'Microsoft JhengHei', '微軟正黑體', sans-serif;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        self.temp_gcode_button.clicked.connect(self.tempGcodeFile)
        button_layout.addWidget(self.temp_gcode_button)
        
        self.del_temp_button = QPushButton("Del Temp GCODE")
        self.del_temp_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545; 
                color: white; 
                border: none; 
                padding: 8px 16px; 
                border-radius: 4px; 
                font-family: 'Microsoft JhengHei', '微軟正黑體', sans-serif;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.del_temp_button.clicked.connect(self.delTempGcodeFiles)
        button_layout.addWidget(self.del_temp_button)
        
        layout.addLayout(button_layout)
        
        # GCODE commands display area
        gcode_commands_label = QLabel("GCODE Commands:")
        gcode_commands_label.setStyleSheet("font-family: 'Microsoft JhengHei', '微軟正黑體', sans-serif; font-weight: bold; margin-top: 10px; font-size: 16px;")
        layout.addWidget(gcode_commands_label)
        
        # Auto scroll checkbox
        checkbox_layout = QHBoxLayout()
        self.auto_scroll_checkbox = QCheckBox("Auto Scroll")
        self.auto_scroll_checkbox.setChecked(True)  # Default to checked
        self.auto_scroll_checkbox.setStyleSheet("""
            QCheckBox {
                font-family: 'Microsoft JhengHei', '微軟正黑體', sans-serif;
                font-size: 14px;
                color: #495057;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:checked {
                background-color: #007bff;
                border: 2px solid #007bff;
                border-radius: 3px;
            }
            QCheckBox::indicator:unchecked {
                background-color: white;
                border: 2px solid #ccc;
                border-radius: 3px;
            }
        """)
        self.auto_scroll_checkbox.stateChanged.connect(self.onAutoScrollChanged)
        checkbox_layout.addWidget(self.auto_scroll_checkbox)
        checkbox_layout.addStretch()  # Push checkbox to the left
        layout.addLayout(checkbox_layout)

        # Create scrollable text area
        self.gcode_display = QTextEdit()
        self.gcode_display.setReadOnly(True)
        self.gcode_display.setMinimumHeight(200)  # Set minimum height
        self.gcode_display.setStyleSheet("""
            QTextEdit {
                background-color: #f8f8f8; 
                border: 1px solid #ccc; 
                padding: 8px; 
                font-family: 'Microsoft JhengHei', '微軟正黑體', 'Courier New', monospace; 
                font-size: 12px;
                line-height: 1.4;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
        """)
        self.gcode_display.setPlainText("Please select a GCODE file first")
        layout.addWidget(self.gcode_display)
        
        # Status bar
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("background-color: #e8f5e8; padding: 5px; border-radius: 3px; font-family: 'Microsoft JhengHei', '微軟正黑體', sans-serif; font-size: 12px; color: #2e7d32;")
        layout.addWidget(self.status_label)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545; 
                color: white; 
                border: none; 
                padding: 10px 20px; 
                border-radius: 4px; 
                font-family: 'Microsoft JhengHei', '微軟正黑體', sans-serif;
                font-weight: bold; 
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
        
    def onAutoScrollChanged(self, state):
        """Handle auto scroll checkbox state change"""
        if state == Qt.Checked:
            self.status_label.setText("Auto scroll enabled - will automatically jump to current layer commands")
            Logger.log("d", "Auto scroll enabled")
            # When enabling auto scroll, trigger an immediate update
            if self.gcode_lines:
                try:
                    current_layer, current_step = self.getCurrentPreviewLayerAndStep()
                    self.updateGcodeDisplay(current_layer, current_step)
                except Exception as e:
                    Logger.log("d", "Error updating display after enabling auto scroll: {}".format(e))
        else:
            self.status_label.setText("Auto scroll disabled - GCODE display frozen at current position")
            Logger.log("d", "Auto scroll disabled")
            # When disabling auto scroll, ensure we don't have any pending scroll operations
            # by clearing any existing timers or scroll operations
            try:
                # Force the display to stay at current position
                scrollbar = self.gcode_display.verticalScrollBar()
                if scrollbar:
                    current_pos = scrollbar.value()
                    Logger.log("d", "Auto scroll disabled, maintaining current position: {}".format(current_pos))
            except Exception as e:
                Logger.log("d", "Error maintaining scroll position: {}".format(e))
    
    def updatePreviewInfo(self):
        """Update preview information"""
        try:
            app = CuraApplication.getInstance()
            if not app:
                return
                
            # Get current layer and step
            current_layer, current_step = self.getCurrentPreviewLayerAndStep()
            total_layers, total_steps = self.getTotalLayersAndSteps()
            
            # Update information display
            info_text = "Current Layer: {}\nCurrent Step: {}\nTotal Layers: {}".format(
                current_layer, current_step, total_layers)
            self.info_label.setText(info_text)
            
            # Update GCODE display only if auto scroll is enabled
            if self.gcode_lines and self.auto_scroll_checkbox.isChecked():
                self.updateGcodeDisplay(current_layer, current_step)
            elif self.gcode_lines and not self.auto_scroll_checkbox.isChecked():
                # When auto scroll is disabled, just update status without changing display
                self.status_label.setText("Auto scroll disabled - GCODE display frozen at current position")
                
        except Exception as e:
            Logger.log("e", "Error updating preview information: {}".format(e))
    
    def getCurrentPreviewLayerAndStep(self):
        """Get current preview layer and step"""
        try:
            app = CuraApplication.getInstance()
            if not app:
                return 0, 0
                
            # 嘗試從 SimulationView 獲取
            try:
                simulation_view = app.getPluginRegistry().getPluginObject("SimulationView")
                if simulation_view:
                    current_layer = simulation_view.getCurrentLayer()
                    current_step = simulation_view.getCurrentPath()
                    Logger.log("d", "從 SimulationView 獲取: 圖層={}, 步驟={}".format(current_layer, current_step))
                    return current_layer, current_step
            except Exception as e:
                Logger.log("d", "從 SimulationView 獲取失敗: {}".format(e))
            
            # 備用方法：從 activeView 獲取
            try:
                active_view = app.getController().getActiveView()
                if active_view:
                    current_layer = active_view.getCurrentLayer()
                    current_step = active_view.getCurrentStep()
                    Logger.log("d", "從 activeView 獲取: 圖層={}, 步驟={}".format(current_layer, current_step))
                    return current_layer, current_step
            except Exception as e:
                Logger.log("d", "從 activeView 獲取失敗: {}".format(e))
            
            return 0, 0
            
        except Exception as e:
            Logger.log("e", "Error getting current preview layer and step: {}".format(e))
            return 0, 0
    
    def getTotalLayersAndSteps(self):
        """Get total number of layers and steps"""
        try:
            app = CuraApplication.getInstance()
            if not app:
                return 0, 0
                
            # 嘗試從 SimulationView 獲取
            try:
                simulation_view = app.getPluginRegistry().getPluginObject("SimulationView")
                if simulation_view:
                    total_layers = simulation_view.getMaxLayers()
                    # 不計算總步驟數，節省運算資源
                    total_steps = 0
                    Logger.log("d", "從 SimulationView 獲取總數: 圖層={}, 總步驟=0 (已禁用)".format(total_layers))
                    return total_layers, total_steps
            except Exception as e:
                Logger.log("d", "從 SimulationView 獲取總數失敗: {}".format(e))
            
            # 備用方法：從 activeView 獲取
            try:
                active_view = app.getController().getActiveView()
                if active_view:
                    total_layers = active_view.getMaxLayers()
                    # 不計算總步驟數，節省運算資源
                    total_steps = 0
                    Logger.log("d", "從 activeView 獲取總數: 圖層={}, 總步驟=0 (已禁用)".format(total_layers))
                    return total_layers, total_steps
            except Exception as e:
                Logger.log("d", "從 activeView 獲取總數失敗: {}".format(e))
            
            return 0, 0
            
        except Exception as e:
            Logger.log("e", "Error getting total layers and steps: {}".format(e))
            return 0, 0
    
    def getLayerStepCount(self, layer_num):
        """獲取指定圖層的步驟數"""
        try:
            app = CuraApplication.getInstance()
            if not app:
                return 0
                
            # 方法1：從 SimulationView 獲取該層的步驟數
            try:
                simulation_view = app.getPluginRegistry().getPluginObject("SimulationView")
                if simulation_view:
                    # 先設置到指定圖層
                    simulation_view.setLayer(layer_num)
                    # 獲取該層的最大路徑數（步驟數）
                    max_paths = simulation_view.getMaxPaths()
                    Logger.log("d", "從 SimulationView 獲取圖層 {} 的步驟數: {}".format(layer_num, max_paths))
                    return max_paths
            except Exception as e:
                Logger.log("d", "從 SimulationView 獲取圖層步驟數失敗: {}".format(e))
            
            # 方法2：從場景中的切片數據獲取
            try:
                scene = app.getController().getScene()
                for node in scene.getRoot().getChildren():
                    if hasattr(node, 'callDecoration'):
                        layer_data = node.callDecoration("getLayerData")
                        if layer_data:
                            layer = layer_data.getLayer(layer_num)
                            if layer and hasattr(layer, 'lineMeshElementCount'):
                                step_count = layer.lineMeshElementCount()
                                Logger.log("d", "從切片數據獲取圖層 {} 的步驟數: {}".format(layer_num, step_count))
                                return step_count
            except Exception as e:
                Logger.log("d", "從切片數據獲取圖層步驟數失敗: {}".format(e))
            
            # 方法3：從 GCODE 分析獲取（備用方法）
            try:
                if self.gcode_lines:
                    # 尋找該層的 GCODE 指令
                    layer_commands = self.findLayerCommands(layer_num, 0)
                    if layer_commands:
                        # 根據指令類型估算步驟數
                        # 通常每個 G1 指令代表一個移動步驟
                        g1_commands = [cmd for cmd in layer_commands if cmd.strip().startswith('G1')]
                        step_count = len(g1_commands)
                        Logger.log("d", "從 GCODE 分析獲取圖層 {} 的步驟數: {}".format(layer_num, step_count))
                        return step_count
            except Exception as e:
                Logger.log("d", "從 GCODE 分析獲取圖層步驟數失敗: {}".format(e))
            
            return 0
            
        except Exception as e:
            Logger.log("e", "獲取圖層 {} 步驟數時發生錯誤: {}".format(layer_num, e))
            return 0
    
    
    def selectGcodeFile(self):
        """Select GCODE file"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, 
                "Select GCODE File", 
                "", 
                "GCODE Files (*.gcode);;All Files (*)"
            )
            
            if file_path:
                self.loadGcodeFile(file_path)
                self.gcode_path_label.setText("GCODE File Path: {}".format(file_path))
                self.status_label.setText("GCODE file loaded")
                Logger.log("i", "Loaded GCODE file: {}".format(file_path))
            else:
                self.status_label.setText("No file selected")
                
        except Exception as e:
            Logger.log("e", "Error selecting GCODE file: {}".format(e))
            QMessageBox.critical(self, "Error", "Error selecting GCODE file:\n{}".format(str(e)))
    
    def tempGcodeFile(self):
        """Save current Cura GCODE file as temporary"""
        try:
            # Get current Cura application
            app = CuraApplication.getInstance()
            if not app:
                QMessageBox.warning(self, "Warning", "Cannot connect to Cura application")
                return
            
            # Get scene and GCODE content
            scene = app.getController().getScene()
            if not hasattr(scene, "gcode_dict"):
                QMessageBox.warning(self, "Warning", "No GCODE content available, please slice first")
                return
            
            # Get current build plate GCODE
            active_build_plate = app.getMultiBuildPlateModel().activeBuildPlate
            gcode_dict = getattr(scene, "gcode_dict")
            gcode_list = gcode_dict.get(active_build_plate, None)
            
            if not gcode_list:
                QMessageBox.warning(self, "Warning", "Current build plate has no GCODE content, please slice first")
                return
            
            # Create GCODE_temp folder
            plugin_dir = os.path.dirname(os.path.abspath(__file__))
            temp_dir = os.path.join(plugin_dir, "GCODE_temp")
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
                Logger.log("i", "Created GCODE_temp folder: {}".format(temp_dir))
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_filename = "GCODE_temp_{}.gcode".format(timestamp)
            temp_file_path = os.path.join(temp_dir, temp_filename)
            
            # Save GCODE content to file
            with open(temp_file_path, 'w', encoding='utf-8') as f:
                for line in gcode_list:
                    f.write(line)
            
            Logger.log("i", "Successfully saved temporary GCODE file: {}".format(temp_file_path))
            
            # Automatically load the temporary file
            self.loadGcodeFile(temp_file_path)
            self.gcode_path_label.setText("GCODE File Path: {}".format(temp_file_path))
            self.status_label.setText("Temporary GCODE file saved and loaded")
            
            QMessageBox.information(self, "Success", "GCODE file saved to:\n{}".format(temp_file_path))
            
        except Exception as e:
            Logger.log("e", "Error saving temporary GCODE file: {}".format(e))
            QMessageBox.critical(self, "Error", "Error saving temporary GCODE file:\n{}".format(str(e)))
    
    def delTempGcodeFiles(self):
        """Delete temporary GCODE files"""
        try:
            # Get the temp directory path
            plugin_dir = os.path.dirname(os.path.abspath(__file__))
            temp_dir = os.path.join(plugin_dir, "GCODE_temp")
            
            # Check if temp directory exists
            if not os.path.exists(temp_dir):
                QMessageBox.information(self, "Info", "No temporary GCODE files found.\nTemp directory does not exist.")
                return
            
            # Get list of files in temp directory
            temp_files = []
            for file in os.listdir(temp_dir):
                if file.endswith('.gcode'):
                    temp_files.append(file)
            
            if not temp_files:
                QMessageBox.information(self, "Info", "No temporary GCODE files found in temp directory.")
                return
            
            # Show confirmation dialog
            file_list = "\n".join(temp_files)
            reply = QMessageBox.question(
                self, 
                "Confirm Delete", 
                "Are you sure you want to delete all temporary GCODE files?\n\nFiles to be deleted:\n{}".format(file_list),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                deleted_count = 0
                failed_files = []
                
                # Delete each file
                for file in temp_files:
                    try:
                        file_path = os.path.join(temp_dir, file)
                        os.remove(file_path)
                        deleted_count += 1
                        Logger.log("i", "Deleted temporary file: {}".format(file))
                    except Exception as e:
                        failed_files.append(file)
                        Logger.log("e", "Failed to delete file {}: {}".format(file, e))
                
                # Show result
                if failed_files:
                    QMessageBox.warning(
                        self, 
                        "Partial Success", 
                        "Deleted {} files successfully.\n\nFailed to delete:\n{}".format(
                            deleted_count, "\n".join(failed_files)
                        )
                    )
                else:
                    QMessageBox.information(
                        self, 
                        "Success", 
                        "Successfully deleted {} temporary GCODE files.".format(deleted_count)
                    )
                    self.status_label.setText("Deleted {} temporary GCODE files".format(deleted_count))
            else:
                self.status_label.setText("Delete operation cancelled")
                
        except Exception as e:
            Logger.log("e", "Error deleting temporary GCODE files: {}".format(e))
            QMessageBox.critical(self, "Error", "Error deleting temporary GCODE files:\n{}".format(str(e)))
    
    def loadGcodeFile(self, file_path):
        """Load GCODE file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                self.gcode_lines = f.readlines()
            
            Logger.log("i", "Successfully loaded GCODE file, {} lines".format(len(self.gcode_lines)))
            self.gcode_display.setPlainText("GCODE file loaded successfully, {} lines".format(len(self.gcode_lines)))
            
        except Exception as e:
            Logger.log("e", "Error loading GCODE file: {}".format(e))
            self.gcode_display.setPlainText("Failed to load GCODE file:\n{}".format(str(e)))
            self.status_label.setText("Failed to load GCODE file")
    
    def updateGcodeDisplay(self, current_layer, current_step):
        """根據當前圖層和步驟更新 GCODE 指令顯示"""
        try:
            if not self.gcode_lines:
                return
            
            # Check if auto scroll is enabled before updating display
            if not self.auto_scroll_checkbox.isChecked():
                Logger.log("d", "Auto scroll disabled, skipping GCODE display update")
                return
            
            # 步驟1：先讀取該層有多少 STEP
            layer_commands = self.findLayerCommands(current_layer, 0)  # 獲取該層所有指令
            if not layer_commands or len(layer_commands) == 0:
                self.gcode_display.setPlainText("No GCODE commands found for layer {}".format(current_layer))
                self.status_label.setText("No GCODE commands found for layer {}".format(current_layer))
                return
            
            # 步驟2：獲取該層的實際步驟數
            total_commands = len(layer_commands)
            total_steps = self.getLayerStepCount(current_layer)
            
            # 如果無法獲取步驟數，使用備用方法
            if total_steps <= 0:
                # 根據 GCODE 指令數量估算步驟數
                # 假設每 5-10 個指令為一個步驟
                total_steps = max(1, total_commands // 8)  # 平均每8個指令一個步驟
                Logger.log("d", "無法獲取圖層 {} 的實際步驟數，使用估算值: {}".format(current_layer, total_steps))
            
            # 計算每個步驟對應的指令範圍
            commands_per_step = max(1, total_commands // max(1, total_steps))
            
            # 步驟3：拉動時依照指令編號來高亮與跳到對應行號
            if current_step > 0 and current_step <= total_steps:
                # 計算當前步驟對應的指令範圍
                start_idx = (current_step - 1) * commands_per_step
                end_idx = min(start_idx + commands_per_step, total_commands)
            else:
                start_idx = 0
                end_idx = total_commands
            
            # 調試信息
            Logger.log("d", "圖層 {} 步驟 {} - 總指令: {}, 總步驟: {}, 每步驟指令: {}, 範圍: {}-{}".format(
                current_layer, current_step, total_commands, total_steps, commands_per_step, start_idx + 1, end_idx))
            
            # Use HTML format for display with highlighting support
            html_text = "<h3>GCODE Commands for Layer {} Step {}:</h3><br>".format(current_layer, current_step)
            
            # 添加指令，當前步驟的指令用高亮顯示
            for i, command in enumerate(layer_commands):
                command_number = i + 1  # 指令編號從1開始
                if start_idx <= i < end_idx:
                    # 當前步驟的指令 - 高亮顯示（黃色背景）
                    html_text += '<div id="highlight-{}" style="background-color: #ffff00; padding: 4px; margin: 2px; border-radius: 4px; font-weight: bold; border-left: 4px solid #ff6b00;">{}</div>'.format(i, command)
                else:
                    # 其他指令 - 正常顯示（淺灰色背景）
                    html_text += '<div style="background-color: #f0f0f0; padding: 4px; margin: 2px; border-radius: 4px; color: #666;">{}</div>'.format(command)
            
            # Add step information
            html_text += '<br><div style="background-color: #e3f2fd; padding: 8px; border-radius: 4px; font-size: 12px; color: #1976d2;">'
            html_text += 'Display range: Commands {} - {} (Total: {} commands)'.format(start_idx + 1, end_idx, total_commands)
            html_text += '</div>'
            
            # Store current scroll position if auto scroll is disabled
            current_scroll_position = 0
            if not self.auto_scroll_checkbox.isChecked():
                scrollbar = self.gcode_display.verticalScrollBar()
                if scrollbar:
                    current_scroll_position = scrollbar.value()
                    Logger.log("d", "Storing current scroll position: {}".format(current_scroll_position))
            
            self.gcode_display.setHtml(html_text)
            
            # Restore scroll position if auto scroll is disabled
            if not self.auto_scroll_checkbox.isChecked() and current_scroll_position > 0:
                def restoreScrollPosition():
                    scrollbar = self.gcode_display.verticalScrollBar()
                    if scrollbar:
                        scrollbar.setValue(current_scroll_position)
                        Logger.log("d", "Restored scroll position to: {}".format(current_scroll_position))
                from PyQt5.QtCore import QTimer
                QTimer.singleShot(100, restoreScrollPosition)  # Small delay to ensure HTML is rendered
            
            # Update status bar
            self.status_label.setText("Layer {} Step {} - Display commands {}-{} (Total: {})".format(
                current_layer, current_step, start_idx + 1, end_idx, total_commands))
            
            # Auto scroll to highlighted line only if checkbox is checked
            if self.auto_scroll_checkbox.isChecked():
                self.autoScrollToHighlight(start_idx, total_commands)
                
        except Exception as e:
            Logger.log("e", "Error updating GCODE display: {}".format(e))
            self.status_label.setText("Error updating GCODE display")
    
    def autoScrollToHighlight(self, start_idx, total_commands):
        """Auto scroll to highlighted line"""
        try:
            # Check if auto scroll is enabled before proceeding
            if not self.auto_scroll_checkbox.isChecked():
                Logger.log("d", "Auto scroll disabled, skipping scroll operation")
                return
                
            from PyQt5.QtCore import QTimer
            from PyQt5.QtGui import QTextCursor
            
            def scrollToPosition():
                try:
                    # Triple check auto scroll status before executing
                    if not self.auto_scroll_checkbox.isChecked():
                        Logger.log("d", "Auto scroll was disabled during delay, cancelling scroll")
                        return
                    
                    # Additional check to ensure the widget is still valid
                    if not hasattr(self, 'gcode_display') or self.gcode_display is None:
                        Logger.log("d", "GCODE display widget no longer valid, cancelling scroll")
                        return
                        
                    if total_commands > 0 and start_idx < total_commands:
                        # Method 1: Use scrollbar for precise scrolling
                        scrollbar = self.gcode_display.verticalScrollBar()
                        if scrollbar and self.auto_scroll_checkbox.isChecked():  # Final check
                            estimated_line_height = 35  # pixels
                            target_position = start_idx * estimated_line_height
                            max_scroll = scrollbar.maximum()
                            target_position = min(target_position, max_scroll)
                            scrollbar.setValue(target_position)
                            Logger.log("d", "Scrolled to position: {} (command index: {}, max: {})".format(target_position, start_idx, max_scroll))
                            
                            # Method 2: Use cursor as backup (only if auto scroll is still enabled)
                            if self.auto_scroll_checkbox.isChecked():
                                try:
                                    cursor = self.gcode_display.textCursor()
                                    cursor.movePosition(QTextCursor.Start)
                                    for i in range(start_idx + 2):  # +2 for title and empty line
                                        cursor.movePosition(QTextCursor.Down)
                                    self.gcode_display.setTextCursor(cursor)
                                    self.gcode_display.ensureCursorVisible()
                                    Logger.log("d", "Used cursor to scroll to line: {}".format(start_idx + 2))
                                except Exception as e:
                                    Logger.log("d", "Cursor scroll failed: {}".format(e))
                except Exception as e:
                    Logger.log("d", "Error during auto scroll: {}".format(e))
            
            # Only set up the timer if auto scroll is still enabled
            if self.auto_scroll_checkbox.isChecked():
                QTimer.singleShot(500, scrollToPosition)
            else:
                Logger.log("d", "Auto scroll disabled before timer setup, cancelling")
        except Exception as e:
            Logger.log("e", "Error setting up auto scroll: {}".format(e))
    
    
    def findLayerCommands(self, layer_num, step_num):
        """尋找指定圖層的 GCODE 指令"""
        try:
            commands = []
            layer_start_found = False
            
            # 尋找圖層開始標記
            layer_marker = ";LAYER:{}".format(layer_num)
            layer_start_index = -1
            
            for i, line in enumerate(self.gcode_lines):
                if layer_marker in line:
                    layer_start_index = i
                    layer_start_found = True
                    break
            
            if not layer_start_found:
                # 如果沒找到標準的圖層標記，嘗試其他格式
                for i, line in enumerate(self.gcode_lines):
                    if "; LAYER:{}".format(layer_num) in line or "LAYER:{}".format(layer_num) in line:
                        layer_start_index = i
                        layer_start_found = True
                        break
            
            if not layer_start_found:
                return ["No layer {} marker found".format(layer_num)]
            
            # 從圖層開始位置尋找指令
            start_line = max(0, layer_start_index)
            end_line = min(len(self.gcode_lines), layer_start_index + 200)  # 增加搜尋範圍
            
            # 收集所有 G 和 M 指令
            all_commands = []
            for i in range(start_line, end_line):
                line = self.gcode_lines[i].strip()
                
                # 跳過空行和註釋
                if not line or line.startswith(';'):
                    continue
                
                # 檢查是否到達下一個圖層
                if i > layer_start_index and (";LAYER:" in line or "; LAYER:" in line):
                    break
                
                # 收集 G 和 M 指令
                if line.startswith('G') or line.startswith('M'):
                    all_commands.append("( Layer {} / Step {} ) {}".format(layer_num, i + 1, line))
            
            if not all_commands:
                return ["No GCODE commands found in layer {}".format(layer_num)]
            
            # 如果 step_num 為 0，返回所有指令
            if step_num == 0:
                return all_commands
            
            # 如果指定了步驟數，返回該步驟的指令
            total_commands = len(all_commands)
            if step_num > 0 and total_commands > 0:
                # 計算每個步驟的指令數量
                commands_per_step = max(1, total_commands // step_num)
                start_idx = (step_num - 1) * commands_per_step
                end_idx = min(start_idx + commands_per_step, total_commands)
                
                # 返回當前步驟的指令
                return all_commands[start_idx:end_idx]
            else:
                # 如果沒有指定步驟，返回所有指令
                return all_commands
            
        except Exception as e:
            Logger.log("e", "Error finding layer commands: {}".format(e))
            return ["Error parsing GCODE: {}".format(str(e))]

class LayerPreviewPlugin(Extension):
    """Main plugin class - Simplified version"""
    
    def __init__(self):
        super().__init__()
        self._preview_widget = None
        self._current_layer = 0
        self._current_step = 0
        self._total_layers = 0
        self._total_steps = 0
        
        # Add menu item
        self.addMenuItem("Show Layer Preview", self.showPreviewWindow)
        
        # Setup timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._updatePreviewInfo)
        self.update_timer.start(500)  # Update every 500ms
        
        Logger.log("i", "pz_cura_gcode_preview plugin initialized")
    
    def _updatePreviewInfo(self):
        """Update preview information - Simplified version"""
        try:
            app = CuraApplication.getInstance()
            if not app:
                return
                
            # 獲取當前圖層和步驟
            current_layer, current_step = self._getCurrentPreviewLayerAndStep()
            total_layers, total_steps = self._getTotalLayersAndSteps()
            
            # 更新內部狀態
            self._current_layer = current_layer
            self._current_step = current_step
            self._total_layers = total_layers
            self._total_steps = total_steps
                
            # 如果預覽視窗存在且可見，更新信息
            if self._preview_widget and self._preview_widget.isVisible():
                try:
                    self._preview_widget.updateLayerInfo(
                        self._current_layer, 
                        self._current_step, 
                        self._total_layers, 
                        self._total_steps
                    )
                except Exception as e:
                    Logger.log("d", "更新UI時發生錯誤: {}".format(e))
            
        except Exception as e:
            Logger.log("e", "更新預覽信息時發生錯誤: {}".format(e))
            
    def showPreviewWindow(self):
        """Show preview window"""
        try:
            if self._preview_widget is None:
                self._preview_widget = LayerPreviewWidget()
            
            self._preview_widget.show()
            self._preview_widget.raise_()
            self._preview_widget.activateWindow()
            
            # 立即更新一次信息
            try:
                self._preview_widget.updateLayerInfo(
                    self._current_layer, 
                    self._current_step, 
                    self._total_layers, 
                    self._total_steps
                )
            except Exception as e:
                Logger.log("d", "立即更新UI時發生錯誤: {}".format(e))
            
            Logger.log("i", "顯示圖層預覽視窗")
            
        except Exception as e:
            Logger.log("e", "Show preview window時發生錯誤: {}".format(e))
            try:
                QMessageBox.critical(None, "錯誤", "Show preview window時發生錯誤：\n{}".format(str(e)))
            except:
                pass
    
    def _getCurrentPreviewLayerAndStep(self):
        """獲取當前預覽圖層和步驟 - 簡化版本"""
        try:
            app = CuraApplication.getInstance()
            if not app:
                return 0, 0
                
            # 嘗試從 SimulationView 獲取
            try:
                simulation_view = app.getPluginRegistry().getPluginObject("SimulationView")
                if simulation_view:
                    current_layer = simulation_view.getCurrentLayer()
                    current_step = simulation_view.getCurrentPath()
                    return current_layer, current_step
            except Exception as e:
                Logger.log("d", "從 SimulationView 獲取失敗: {}".format(e))
            
            return 0, 0
            
        except Exception as e:
            Logger.log("e", "Error getting current preview layer and step: {}".format(e))
            return 0, 0
    
    def _getTotalLayersAndSteps(self):
        """Get total number of layers and steps - 簡化版本"""
        try:
            app = CuraApplication.getInstance()
            if not app:
                return 0, 0
                
            # 嘗試從 SimulationView 獲取
            try:
                simulation_view = app.getPluginRegistry().getPluginObject("SimulationView")
                if simulation_view:
                    total_layers = simulation_view.getMaxLayers()
                    total_steps = simulation_view.getMaxPaths()
                    return total_layers, total_steps
            except Exception as e:
                Logger.log("d", "從 SimulationView 獲取總數失敗: {}".format(e))
            
            return 0, 0
            
        except Exception as e:
            Logger.log("e", "Error getting total layers and steps: {}".format(e))
            return 0, 0
