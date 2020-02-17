import shutil
import os
import sublime
import sublime_plugin
import threading
import subprocess

from LSP.plugin.core.handlers import LanguageHandler
from LSP.plugin.core.settings import ClientConfig, LanguageConfig, read_client_config

class LspWolframLanguagePlugin(LanguageHandler):
    @property
    def name(self) -> str:
        return 'lsp-wolfram'

    @property
    def config(self) -> ClientConfig:
        settings = sublime.load_settings("WolframLanguage.sublime-settings")
        client_configuration = settings.get('lsp_server')
        
        default_configuration = {
            "languages": [
                {
                    "languageId": "wolfram",
                    "scopes": ["source.wolfram"],
                    "syntaxes": ["Packages/WolframLanguage/WolframLanguage.sublime-syntax"]
                }
            ]
        }
        default_configuration.update(client_configuration)

        return read_client_config('lsp-wolfram', default_configuration)

    def on_start(self, window) -> bool:
        return True

    def on_initialized(self, client) -> None:
        client.on_notification("textDocument/publishImplicitTimes", self.on_implicit_times)

    def on_implicit_times(self, params):

        #
        # Currently grabbing the active view
        # There is no current way to obtain the view that corresponds to the file
        # Related issues: https://github.com/sublimelsp/LSP/issues/641
        #
        view = sublime.active_window().active_view()

        view.erase_phantoms("implicit_times")

        lines = params['lines']
        for l in lines:
            line = l['line']
            characters = l['characters']

            joined = ''.join(characters)

            #
            # Must replace spaces with &nbsp;
            # Sublime minihtml does not support <pre>, <code>, etc.
            # Related issues: https://forum.sublimetext.com/t/does-minihtml-support-the-pre-tag/46267/3
            #

            replaced = []
            for c in joined:
                if c == ' ':
                    replaced.append('&nbsp;')
                elif c == '\t':
                    replaced.append('&nbsp;')
                else:
                    replaced.append(c)

            joined = ''.join(replaced)
            
            view.add_phantom("implicit_times",
                sublime.Region(view.text_point(line - 1, 1 - 1), view.text_point(line - 1, len(replaced) - 1)),
                '<span style="color:#7777ff">' + joined + '</span>',
                sublime.LAYOUT_BELOW)

