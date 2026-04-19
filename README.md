# Video to MP3 Studio

**Notice:** This project was created with the assistance of GenAI tools. It should be carefully reviewed and independently inspected before being used in any production, security-sensitive, or otherwise critical context.

Video to MP3 Studio is a beginner-friendly local app that converts supported video URLs into MP3 files with a simple, polished web interface that runs on your own computer.

## What this app does

- Paste a supported video URL
- Choose MP3 bitrate: 128, 192, 256, or 320 kbps
- Rename the output file before converting
- See clear status updates during download and conversion
- Save finished MP3 files into a local `downloads/` folder

## Lawful use note

Only download or convert content you have the legal right to use. Copyright law and each platform's terms of service still apply. Some platforms may block downloads, change their site behavior, or stop working with download tools at any time.

## Recommended stack

- Python 3
- Flask
- yt-dlp
- FFmpeg
- HTML, CSS, and JavaScript

This stack keeps the project simple:

- One backend language
- One easy web server
- No database
- No build step
- No frontend framework

## Project structure

```text
video-to-mp3-studio/
├── app.py
├── downloader.py
├── validators.py
├── requirements.txt
├── .gitignore
├── README.md
├── downloads/
├── static/
│   ├── app.js
│   └── styles.css
├── templates/
│   └── index.html
└── tests/
    ├── test_app.py
    └── test_validators.py
```

## Step 1: install Homebrew if needed

Check whether Homebrew is installed:

```bash
brew --version
```

If that command says `command not found`, install Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Step 2: install FFmpeg and yt-dlp

```bash
brew install ffmpeg yt-dlp
```

## Step 3: create the project environment

```bash
cd /Users/l.eatonnortheastern.edu/Documents/Music/video-to-mp3-studio
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Step 4: run the app

```bash
cd /Users/l.eatonnortheastern.edu/Documents/Music/video-to-mp3-studio
source .venv/bin/activate
python3 app.py
```

Then open this address in your browser:

```text
http://127.0.0.1:5001
```

## Build a double-clickable Mac app

This project includes a Mac launcher app that starts the local server and opens the converter in your browser.

Build and install it with:

```bash
cd /Users/l.eatonnortheastern.edu/Documents/Music/video-to-mp3-studio
source .venv/bin/activate
pip install -r requirements.txt
python3 generate_icon.py
./build_mac_app.sh
```

After the build finishes, the installed app is here:

```text
~/Applications/Video to MP3 Studio.app
```

When you use the Mac app, converted files are saved here:

```text
~/Downloads/Video to MP3 Studio
```

## Step 5: run tests

```bash
cd /Users/l.eatonnortheastern.edu/Documents/Music/video-to-mp3-studio
source .venv/bin/activate
pytest
```

## How to use the app

1. Open the app in your browser.
2. Paste a supported video URL.
3. Pick a bitrate.
4. Type the output file name you want.
5. For YouTube, place a cookies file at `cookies/youtube-cookies.txt`.
6. Click `Download and convert`.
7. Wait for the status box to show progress.
8. Find the MP3 in the local `downloads/` folder.

## YouTube cookies file

This app avoids Keychain access. For YouTube downloads, it reads a manual cookies file instead.

Put your file here:

```text
/Users/l.eatonnortheastern.edu/Documents/Video to MP3 Studio/youtube-cookies.txt
```

The file should be in Netscape `cookies.txt` format.

## Troubleshooting

### `ffmpeg` is missing

Install FFmpeg:

```bash
brew install ffmpeg
```

### `yt-dlp` command is missing

Install yt-dlp:

```bash
brew install yt-dlp
```

### Python packages are missing

Activate the virtual environment and reinstall packages:

```bash
cd /Users/l.eatonnortheastern.edu/Documents/Music/video-to-mp3-studio
source .venv/bin/activate
pip install -r requirements.txt
```

### `Address already in use`

Another app is already using port `5001`. Stop the other app or run Flask on another port.

### The URL is valid but the download fails

Possible causes:

- The site is not supported by yt-dlp
- The platform changed how its pages work
- The platform blocks this content
- The content is private, deleted, age-restricted, or region-locked
- For YouTube, `cookies/youtube-cookies.txt` is missing or expired

### The app says the file already exists

Choose a different output name or delete the old file from `downloads/`.

## Customization ideas

### Change the default bitrate

Edit `templates/index.html` and change which option has `selected`.

### Change the color palette

Edit the CSS variables near the top of `static/styles.css`.

### Change the app title

Update the text in `templates/index.html` and this `README.md`.

### Save files somewhere else

Edit `DOWNLOADS_DIR` in `app.py`.

## Publish to GitHub

Suggested repository name: `video-to-mp3-studio`

Create a new empty repository under the GitHub account `leaton79`, then run:

```bash
cd /Users/l.eatonnortheastern.edu/Documents/Music/video-to-mp3-studio
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/leaton79/video-to-mp3-studio.git
git push -u origin main
```
