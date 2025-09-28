# pz_cura_gcode_preview

A powerful Cura plugin for real-time GCODE layer preview and analysis with advanced features for 3D printing enthusiasts and professionals.

## 🎥 Demo Video

Watch the plugin in action:

[![pz_cura_gcode_preview Demo](https://github.com/pzman3d/pz_cura_gcode_preview/blob/main/pz_cura_gcode_preview.mp4)](https://github.com/pzman3d/pz_cura_gcode_preview/blob/main/pz_cura_gcode_preview.mp4)

*Click the video above to see the full demonstration of the plugin features*

## 📋 Features

- **Real-time Layer Preview**: Monitor current printing layer and step in real-time
- **GCODE Command Analysis**: View detailed GCODE commands for each layer and step
- **Auto Scroll Control**: Toggle automatic scrolling to current layer commands
- **Temporary GCODE Storage**: Save current Cura GCODE as temporary files
- **File Management**: Easy selection and management of GCODE files
- **Multi-language Support**: English interface with Microsoft JhengHei font
- **Professional UI**: Clean, modern interface with intuitive controls

## 🚀 Installation

### Prerequisites
- Creality Slicer 4.8 or compatible Cura-based slicer
- Python 3.x (included with Cura)
- PyQt5 (included with Cura)

### Installation Steps

1. **Download the Plugin**
   ```bash
   git clone https://github.com/pzman3d/pz_cura_gcode_preview.git
   ```

2. **Copy to Cura Plugins Directory**
   - Navigate to your Cura plugins directory:
     - **Windows**: `%APPDATA%\Creality Slicer\4.8\plugins\`
     - **macOS**: `~/Library/Application Support/Creality Slicer/4.8/plugins/`
     - **Linux**: `~/.local/share/cura/4.8/plugins/`

3. **Install the Plugin**
   - Copy the `LayerPreviewPlugin` folder to your plugins directory
   - Restart Creality Slicer/Cura

4. **Verify Installation**
   - Open Creality Slicer
   - Go to `Extensions` → `pz_cura_gcode_preview` → `Show Layer Preview`
   - The plugin window should open successfully

## 📖 Usage Guide

### Quick Start

> **💡 Tip**: Watch the [demo video](https://github.com/pzman3d/pz_cura_gcode_preview/blob/main/pz_cura_gcode_preview.mp4) above for a visual walkthrough of all features!

### Basic Usage

1. **Open the Plugin**
   - Launch Creality Slicer
   - Load your 3D model and slice it
   - Go to `Extensions` → `pz_cura_gcode_preview` → `Show Layer Preview`

2. **View Layer Information**
   - The plugin displays current layer, step, and total layers
   - Information updates automatically every 500ms

3. **Load GCODE File**
   - Click `Select GCODE File` to load a GCODE file
   - Or use `Save Temp GCODE` to save current Cura GCODE

### Advanced Features

#### Auto Scroll Control
- **Enable Auto Scroll**: Automatically jumps to current layer commands
- **Disable Auto Scroll**: Freeze display, allows manual scrolling
- Toggle using the `Auto Scroll` checkbox

#### Temporary GCODE Management
- **Save Temp GCODE**: Saves current Cura GCODE to `GCODE_temp` folder
- **Del Temp GCODE**: Deletes all temporary GCODE files
- Files are automatically loaded after saving

#### GCODE Command Analysis
- View detailed GCODE commands for each layer
- Commands are highlighted for current step
- Format: `( Layer X / Step Y ) GCODE_COMMAND`
- Display range shows command count and scope

### Interface Elements

| Element | Description |
|---------|-------------|
| **Current Layer Info** | Shows current layer, step, and total layers |
| **GCODE File Path** | Displays currently loaded GCODE file path |
| **Select GCODE File** | Browse and load GCODE files |
| **Save Temp GCODE** | Save current Cura GCODE as temporary file |
| **Del Temp GCODE** | Delete all temporary GCODE files |
| **Auto Scroll** | Toggle automatic scrolling to current commands |
| **GCODE Commands** | Scrollable display of GCODE commands |
| **Status Bar** | Shows current operation status |

## 🔧 Configuration

### Auto Scroll Settings
- **Enabled**: Automatically scrolls to current layer commands
- **Disabled**: Freezes display, allows manual navigation
- Status is preserved across sessions

### File Management
- Temporary files are stored in `GCODE_temp` folder
- Files are named with timestamp: `GCODE_temp_YYYYMMDD_HHMMSS.gcode`
- Automatic cleanup available via `Del Temp GCODE` button

## 🐛 Troubleshooting

### Common Issues

**Plugin not appearing in Extensions menu**
- Ensure plugin is in correct directory
- Restart Creality Slicer
- Check file permissions

**GCODE display not updating**
- Verify GCODE file is loaded
- Check if Auto Scroll is enabled
- Ensure Cura has completed slicing

**Temporary files not saving**
- Check write permissions in plugin directory
- Ensure sufficient disk space
- Verify Cura has generated GCODE

### Debug Information
- Enable debug logging in Cura
- Check console output for error messages
- Plugin logs all operations for troubleshooting

## 📁 File Structure

```
LayerPreviewPlugin/
├── LayerPreviewPlugin.py    # Main plugin file
├── __init__.py              # Plugin initialization
├── plugin.json              # Plugin metadata
├── GCODE_temp/              # Temporary GCODE storage
│   └── GCODE_temp_*.gcode   # Temporary files
└── README.md                # This file
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
1. Clone the repository
2. Install development dependencies
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**pzman3d**
- Email: pzman3d@gmail.com
- GitHub: [@pzman3d](https://github.com/pzman3d)

## 🙏 Acknowledgments

- Cura development team for the excellent slicing engine
- Creality for the user-friendly interface
- 3D printing community for feedback and suggestions

## 📞 Support

If you encounter any issues or have questions:

1. Watch the [demo video](https://github.com/pzman3d/pz_cura_gcode_preview/blob/main/pz_cura_gcode_preview.mp4) for visual guidance
2. Check the [Troubleshooting](#-troubleshooting) section
3. Search existing [Issues](https://github.com/pzman3d/pz_cura_gcode_preview/issues)
4. Create a new issue with detailed description
5. Contact: pzman3d@gmail.com

## 🔄 Version History

### v1.0.0
- Initial release
- Real-time layer preview
- GCODE command analysis
- Auto scroll control
- Temporary file management
- English interface
- Microsoft JhengHei font support

---

**Made with ❤️ for the 3D printing community**
