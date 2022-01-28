import sublime_plugin
from .plugin.open import open_file

class SideBarEditorOpenCommand(sublime_plugin.WindowCommand):
    
    def run(self, paths = []):
        for path in paths:
            open_file(path)

    def is_enabled(self, paths = []):
        for path in paths:
            if not path.endswith((".nb", ".cdf", ".wl", ".m", ".wls")):
                return False

        return True
