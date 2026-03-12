on run
  set bundleLauncher to quoted form of ((POSIX path of (path to me)) & "Contents/Resources/launcher.sh")
  do shell script bundleLauncher
end run
