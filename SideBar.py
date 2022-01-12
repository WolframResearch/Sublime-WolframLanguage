import os
import subprocess
import sublime
import sublime_plugin



def open_file(filepath):
    if sublime.platform() == "osx":
        subprocess.Popen(('open', filepath))
    elif sublime.platform() == "windows":
        os.startfile(filepath)
    elif sublime.platform() == "linux":
        subprocess.Popen(('xdg-open', filepath))

class NotebookEditorOpenCommand(sublime_plugin.WindowCommand):
    def run(self, paths = []):
        for path in paths:
            if path.endswith((".nb", ".cdf", ".wl", ".m", ".wls")):
                open_file(path)


    def is_enabled(self):
        if self.window.active_view():
            return self.window.active_view().file_name() is not None
        else:
            return False


