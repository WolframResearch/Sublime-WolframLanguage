import shutil
import os
import sublime
import sublime_plugin
import threading
import subprocess
import sys

from LSP.plugin.core.handlers import LanguageHandler
from LSP.plugin.core.settings import ClientConfig, LanguageConfig, read_client_config
from LSP.plugin.core.protocol import Request

settings_file = 'WolframLanguage.sublime-settings'

class LspWolframLanguagePlugin(LanguageHandler):
    @property
    def name(self) -> str:
        return 'lsp-wolfram'

    @property
    def config(self) -> ClientConfig:
        settings = sublime.load_settings(settings_file)
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
        settings = sublime.load_settings(settings_file)
        client_configuration = settings.get('lsp_server')

        command = client_configuration.get('command')
        kernel_path = command[0]

        if not os.path.isfile(kernel_path):
            sublime.message_dialog("Cannot find kernel: " + kernel_path)
            return False

        if sys.platform == "win32":
            base = os.path.basename(kernel_path)
            if base.lower() == 'wolframkernel.exe' or base.lower() == 'wolframkernel':
                sublime.message_dialog('WolframKernel.exe cannot be used because it opens a separate window and hangs on stdin. Please use wolfram.exe')
                return False

        return True

    def on_initialized(self, client) -> None:

        active_window   = sublime.active_window()
        panel = active_window.create_output_panel("wolfram")

        #request = Request('wolfram/versions')

        #result = client.execute_request(request)

        #panel.run_command("append", {"characters": 'result: ' + str(result) + '\n'})

        client.on_notification("wolfram/versions", self.on_wolfram_versions)

        client.on_notification("textDocument/publishImplicitTimes", self.on_implicit_times)

    def on_wolfram_versions(self, params):

        if not sublime:
            return

        # active_window = sublime.active_window()

        # panel = active_window.create_output_panel("wolfram")

        # panel.run_command("append", {"characters": 'params: ' + str(params) + '\n'})

        wolfram_version = params['wolframVersion']
        codeparser_version = params['codeParserVersion']
        codeinspector_version = params['codeInspectorVersion']
        lspserver_version = params['lspServerVersion']

        if not wolfram_version or wolfram_version == 'bad':
            sublime.message_dialog('Cannot detect Wolfram version.')

        if not codeparser_version or codeparser_version == 'bad':
            sublime.message_dialog('Cannot detect CodeParser paclet version.')

        if not codeinspector_version or codeinspector_version == 'bad':
            sublime.message_dialog('Cannot detect CodeInspector paclet version.')

        if not lspserver_version or lspserver_version == 'bad':
            sublime.message_dialog('Cannot detect LSPServer paclet version.')

    def on_implicit_times(self, params):

        #
        # Currently grabbing the active view
        # There is no current way to obtain the view that corresponds to the file
        # Related issues: https://github.com/sublimelsp/LSP/issues/641
        #
        
        if not sublime:
            return

        active_window = sublime.active_window()

        view = active_window.active_view()

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
            index = 0
            for c in joined:
                if c == ' ':
                    replaced.append('&nbsp;')
                elif c == '\t':
                    replaced.append('&nbsp;')
                elif c == '\xd7':
                    replaced.append(c)
                    view.add_phantom("implicit_times",
                        sublime.Region(view.text_point(line - 1, index), view.text_point(line - 1, index + 1)),
                        '<span style="color:#aaaaff">' + c + '</span>',
                        sublime.LAYOUT_INLINE)
                else:
                    replaced.append(c)
                index = index + 1

            # joined = ''.join(replaced)
            # view.add_phantom("implicit_times",
            #     sublime.Region(view.text_point(line - 1, 1 - 1), view.text_point(line - 1, len(replaced) - 1)),
            #     '<span style="color:#7777ff">' + joined + '</span>',
            #     sublime.LAYOUT_BELOW)

