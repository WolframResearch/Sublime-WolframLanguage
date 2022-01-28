import os
import subprocess
import sublime
import sublime_plugin

def open_file(filepath):
    if sublime.platform() == "osx":
        subprocess.Popen(("open", filepath))
    elif sublime.platform() == "windows":
        os.startfile(filepath)
    elif sublime.platform() == "linux":
        subprocess.Popen(("xdg-open", filepath))
