# Packaging and Distribution Guide for YouTube Goniometer

This guide explains different distribution methods for making your app available to others.

## Distribution Methods

### 1. Python Package (PyPI) - Best for Developers
Upload to Python Package Index for easy `pip install` installation.

### 2. Standalone Executables - Best for End Users
Create single-file executables that don't require Python installation.

### 3. GitHub Releases - Best for Open Source
Distribute through GitHub with downloadable packages.

### 4. Windows Installer - Best for Windows Users
Create MSI/NSIS installers for professional deployment.

## Step-by-Step Instructions

### Method 1: PyPI Distribution

1. **Prepare the package:**
   ```bash
   pip install build twine
   python -m build
   ```

2. **Test on TestPyPI first:**
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

3. **Upload to PyPI:**
   ```bash
   python -m twine upload dist/*
   ```

4. **Users install with:**
   ```bash
   pip install youtube-goniometer
   ```

### Method 2: Standalone Executables (PyInstaller) ✅ **COMPLETED**

**Already created!** Check the `dist/` folder for `YouTube-Goniometer.exe`

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Create executable:**
   ```bash
   pyinstaller --onefile --windowed --name="YouTube-Goniometer" app.py
   ```

3. **Advanced options (used for this build):**
   ```bash
   pyinstaller --onefile --windowed \
     --name="YouTube-Goniometer" \
     --add-data="README.md;." \
     --hidden-import=PySide6.QtCore \
     --hidden-import=PySide6.QtWidgets \
     --hidden-import=PySide6.QtGui \
     --hidden-import=pyqtgraph \
     app.py
   ```

**Result:** 118 MB executable that runs without Python installation!

### Method 3: GitHub Releases

1. **Create release assets:**
   ```bash
   # Create source distribution
   python -m build --sdist
   
   # Create wheel
   python -m build --wheel
   
   # Create executable
   pyinstaller --onefile --windowed app.py
   ```

2. **Upload to GitHub:**
   - Go to your repository
   - Click "Releases" → "Create a new release"
   - Upload: `dist/*.tar.gz`, `dist/*.whl`, `dist/app.exe`

### Method 4: Windows Installer (NSIS)

1. **Install NSIS:**
   Download from https://nsis.sourceforge.io/

2. **Create installer script** (install.nsi):
   ```nsis
   !define APP_NAME "YouTube Goniometer"
   !define APP_VERSION "1.0.0"
   
   OutFile "YouTube-Goniometer-Setup.exe"
   InstallDir "$PROGRAMFILES\${APP_NAME}"
   
   Section "MainSection" SEC01
     SetOutPath "$INSTDIR"
     File "dist\app.exe"
     File "README.md"
     CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\app.exe"
   SectionEnd
   ```

## Recommended Deployment Strategy

### For Maximum Reach:
1. **PyPI** - For Python developers
2. **GitHub Releases** - With executables for each platform
3. **Windows Installer** - For non-technical Windows users

### Files to Include in Releases:
- Source code (`youtube-goniometer-1.0.0.tar.gz`)
- Python wheel (`youtube_goniometer-1.0.0-py3-none-any.whl`)
- Windows executable (`YouTube-Goniometer-Windows.exe`)
- macOS app bundle (`YouTube-Goniometer-macOS.app`)
- Linux executable (`YouTube-Goniometer-Linux`)

## Pre-Distribution Checklist

- [ ] All dependencies listed in `requirements.txt`
- [ ] Version number updated in `pyproject.toml`
- [ ] README.md has clear installation instructions
- [ ] LICENSE file included
- [ ] All code tested on target platforms
- [ ] No hardcoded paths or personal information
- [ ] Error handling for missing dependencies
- [ ] Clear user documentation