import sublime_plugin
from .plugin.open import open_file

class ContextEditorOpenCommand(sublime_plugin.TextCommand):
    
    def run(self, edit):
        name = self.view.file_name()
        open_file(name)

    def is_enabled(self):
        name = self.view.file_name()
        if name == None:
            return False
        if name.endswith((".nb", ".cdf", ".wl", ".m", ".wls")):
            return True
        return False
