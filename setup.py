from setuptools import setup


APP = ["desktop_app.py"]
DATA_FILES = ["templates", "static"]
OPTIONS = {
    "argv_emulation": False,
    "plist": {
        "CFBundleName": "Video to MP3 Studio",
        "CFBundleDisplayName": "Video to MP3 Studio",
        "CFBundleIdentifier": "com.leaton79.videotomp3studio",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
        "LSMinimumSystemVersion": "12.0",
    },
    "packages": ["flask", "jinja2", "werkzeug", "yt_dlp"],
    "includes": ["tkinter"],
}


setup(
    app=APP,
    name="Video to MP3 Studio",
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
