import shutil
import os
import sublime
import sublime_plugin
import threading
import subprocess
import sys

import webbrowser

from LSP.plugin.core.handlers import LanguageHandler
from LSP.plugin.core.settings import ClientConfig, LanguageConfig, read_client_config
from LSP.plugin.core.protocol import Notification

settings_file = 'WolframLanguage.sublime-settings'

class LspWolframLanguagePlugin(LanguageHandler):
    @property
    def name(self) -> str:
        return 'wolfram'

    @property
    def config(self) -> ClientConfig:
        settings = sublime.load_settings(settings_file)

        command = settings.get("lsp_server_command")

        kernel_path = command[0]

        if kernel_path == '`kernel`':
            kernel = settings.get("kernel")
            command[0] = kernel

        initialization_options = settings.get("lsp_server_initialization_options")

        config = {
            "languageId": "wolfram",
            "scopes": ["source.wolfram"],
            "syntaxes": ["Packages/WolframLanguage/WolframLanguage.sublime-syntax"]
        }

        config['command'] = command
        config['initializationOptions'] = initialization_options

        return read_client_config('wolfram', config)

    def on_start(self, window) -> bool:
        settings = sublime.load_settings(settings_file)

        command = settings.get("lsp_server_command")

        kernel_path = command[0]

        #
        # if not using `kernel` syntax in command, then just return now
        #
        if not kernel_path == '`kernel`':
            return True

        #
        # Check that kernel specified by `kernel` actually exists
        #
        kernel = settings.get("kernel")

        if not os.path.isfile(kernel):
            sublime.message_dialog("Cannot find Wolfram Kernel: " + kernel)
            return False

        if sys.platform == "win32":
            base = os.path.basename(kernel)
            if base.lower() == 'wolframkernel.exe' or base.lower() == 'wolframkernel':
                sublime.message_dialog('WolframKernel.exe cannot be used because it opens a separate window and hangs on stdin. Please use wolfram.exe')
                return False

        return True

    def on_initialized(self, client) -> None:

        self._client = client

        active_window   = sublime.active_window()
        panel = active_window.create_output_panel("wolfram")

        #request = Request('wolfram/versions')

        #result = client.execute_request(request)

        #panel.run_command("append", {"characters": 'result: ' + str(result) + '\n'})

        client.on_notification("wolfram/versions", self.on_wolfram_versions)

        client.on_notification("textDocument/publishImplicitTimes", self.on_implicit_times)

        client.on_notification("textDocument/publishHTMLSnippet", self.on_html_snippet)

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

            index = 0
            for c in joined:
                if c == '\xd7':
                    view.add_phantom("implicit_times",
                        sublime.Region(view.text_point(line - 1, index), view.text_point(line - 1, index + 1)),
                        '<span style="color:#888888">' + c + '</span>',
                        sublime.LAYOUT_INLINE)
                index = index + 1


    def on_html_snippet(self, params):

        #
        # Currently grabbing the active view
        # There is no current way to obtain the view that corresponds to the file
        # Related issues: https://github.com/sublimelsp/LSP/issues/641
        #
        
        if not sublime:
            return

        active_window = sublime.active_window()

        view = active_window.active_view()

        view.erase_phantoms("html_snippet")

        lines = params['lines']
        for l in lines:
            line = l['line']
            characters = l['characters']

            joined = ''.join(characters)

            view.add_phantom("html_snippet",
                sublime.Region(view.text_point(line - 1, 1 - 1), view.text_point(line - 1, len(characters) - 1)),
                joined,
                sublime.LAYOUT_BELOW, self.on_navigate)

    def on_navigate(self, href):
        
        # if not sublime:
        #     return

        # active_window = sublime.active_window()

        # panel = active_window.create_output_panel("wolfram")

        #panel.run_command("append", {"characters": 'clicked on: ' + href + '\n'})

        req = Notification("htmlSnippetClick", {'href': href})

        self._client.send_notification(req)


class WolframLanguageOpenSiteCommand(sublime_plugin.ApplicationCommand):
    """Open site links."""

    def run(self, url):
        """Open the URL."""

        webbrowser.open_new_tab(url)
