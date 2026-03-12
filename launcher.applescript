on run
	set projectDir to "/Users/l.eatonnortheastern.edu/Documents/Music/video-to-mp3-studio"
	set pythonBin to "/Users/l.eatonnortheastern.edu/Documents/Music/video-to-mp3-studio/.venv/bin/python3"
	set appScript to "/Users/l.eatonnortheastern.edu/Documents/Music/video-to-mp3-studio/app.py"
	set downloadsDir to POSIX path of (path to downloads folder) & "Video to MP3 Studio"
	set cookiesDir to POSIX path of (path to documents folder) & "Video to MP3 Studio"
	set appURL to "http://127.0.0.1:5001"
	
	do shell script "mkdir -p " & quoted form of downloadsDir
	
	try
		do shell script "curl -sf " & quoted form of appURL & " >/dev/null"
	on error
		set launchCommand to "cd " & quoted form of projectDir & " && VIDEO_TO_MP3_DOWNLOADS_DIR=" & quoted form of downloadsDir & " VIDEO_TO_MP3_COOKIES_DIR=" & quoted form of cookiesDir & " " & quoted form of pythonBin & space & quoted form of appScript
		tell application "Terminal"
			do script launchCommand
			activate
		end tell
		
		repeat 20 times
			delay 1
			try
				do shell script "curl -sf " & quoted form of appURL & " >/dev/null"
				exit repeat
			end try
		end repeat
	end try
	
	open location appURL
end run
