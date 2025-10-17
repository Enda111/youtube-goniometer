# How to Share Your YouTube Goniometer on GitHub

## Step 1: Create a GitHub Repository

1. Go to https://github.com and sign in (create account if needed)
2. Click the green "New" button to create a repository
3. Name it: `youtube-goniometer`
4. Make it public (so others can download)
5. Click "Create repository"

## Step 2: Upload Your Files

### Option A: Use GitHub Web Interface (Easiest)
1. Click "uploading an existing file"
2. Drag and drop ALL your files from the Goniometer folder
3. Write commit message: "Initial release of YouTube Goniometer"
4. Click "Commit changes"

### Option B: Use Git Command Line
```bash
cd "C:\Users\endao\OneDrive\Documents\Goniometer"
git init
git add .
git commit -m "Initial release of YouTube Goniometer"
git branch -M main
git remote add origin https://github.com/yourusername/youtube-goniometer.git
git push -u origin main
```

## Step 3: Create a Release

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Tag version: `v1.0.0`
4. Release title: `YouTube Goniometer v1.0.0`
5. Description:
   ```
   🎵 Professional YouTube Audio Analysis Tool
   
   ## Download Options:
   - **Windows Users**: Download `YouTube-Goniometer.exe` (no Python needed!)
   - **Developers**: Download source code or install via pip
   
   ## Features:
   - Real-time goniometer visualization
   - YouTube audio streaming
   - Professional phase correlation analysis
   - Broadcast-quality audio tools
   
   ## Requirements:
   - FFmpeg (for YouTube audio)
   - Audio device connected
   ```

6. Upload these files by dragging them:
   - `dist/YouTube-Goniometer.exe`
   - `dist/youtube_goniometer-1.0.0.tar.gz`
   - `dist/youtube_goniometer-1.0.0-py3-none-any.whl`

7. Click "Publish release"

## Step 4: Share the Link

Your app will be available at:
`https://github.com/yourusername/youtube-goniometer/releases`

Users can:
- Download the `.exe` file and run it immediately
- Clone the repository for development
- Install via pip (if you publish to PyPI later)