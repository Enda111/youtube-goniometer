# Makefile for YouTube Goniometer

.PHONY: help install build test clean dist upload-test upload exe installer

help:
	@echo "YouTube Goniometer Build System"
	@echo "==============================="
	@echo ""
	@echo "Available commands:"
	@echo "  install      - Install dependencies"
	@echo "  build        - Build Python package"
	@echo "  test         - Run tests"
	@echo "  clean        - Clean build artifacts"
	@echo "  dist         - Create distribution packages"
	@echo "  exe          - Create standalone executable"
	@echo "  installer    - Create Windows installer (requires NSIS)"
	@echo "  upload-test  - Upload to TestPyPI"
	@echo "  upload       - Upload to PyPI"

install:
	pip install -r requirements.txt
	pip install build twine pyinstaller

build:
	python -m build

test:
	@echo "Running basic import test..."
	python -c "import app; print('✓ App imports successfully')"
	python -c "from visualizers import gonio; print('✓ Visualizers import successfully')"
	python -c "import config; print('✓ Config imports successfully')"

clean:
	rm -rf build/ dist/ *.egg-info/
	rm -rf __pycache__/ */__pycache__/
	rm -f *.spec
	find . -name "*.pyc" -delete

dist: clean build
	@echo "Distribution packages created in dist/"

exe: clean
	pyinstaller --onefile --windowed \
		--name="YouTube-Goniometer" \
		--add-data="README.md;." \
		--hidden-import=PySide6.QtCore \
		--hidden-import=PySide6.QtWidgets \
		--hidden-import=PySide6.QtGui \
		app.py
	@echo "Executable created: dist/YouTube-Goniometer.exe"

installer: exe
	@if command -v makensis >/dev/null 2>&1; then \
		echo "Creating Windows installer..."; \
		makensis installer.nsi; \
	else \
		echo "NSIS not found. Please install NSIS to create Windows installer."; \
	fi

upload-test: dist
	python -m twine upload --repository testpypi dist/*

upload: dist
	python -m twine upload dist/*

# Platform-specific targets
windows: exe installer

linux: build
	@echo "Linux package ready in dist/"

macos: build
	@echo "macOS package ready in dist/"