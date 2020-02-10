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
        settings = sublime.load_settings("LSP-wolfram.sublime-settings")
        client_configuration = settings.get('client')
        
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
        pass

class WolframLanguageListener(sublime_plugin.EventListener):
    def on_hover(self, view, point, hover_zone):

        name = view.scope_name(point)

        win   = sublime.active_window()
        panel = win.create_output_panel("wolfram")
        panel.run_command("append", {"characters": name})
