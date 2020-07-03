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

settings_file = "WolframLanguage.sublime-settings"

class LspWolframLanguagePlugin(LanguageHandler):
    @property
    def name(self) -> str:
        return "wolfram"

    @property
    def config(self) -> ClientConfig:
        settings = sublime.load_settings(settings_file)

        command = settings.get("lsp_server_command")

        kernel_path = command[0]

        if kernel_path == "`kernel`":
            kernel = settings.get("kernel")
            command[0] = kernel

        #
        # Any dollar sign characters $ will be treated as the beginning of an
        # environment variable to be expanded, so must use \\[RawDollar]
        #
        # Related lines: https://github.com/sublimelsp/LSP/blob/24cee140fd7d02a29e82a139b918bef77d89f6fb/plugin/core/clients.py#L16
        #
        command = list(
            arg.replace("$", "\\[RawDollar]")
            for arg in command
        )

        initialization_options = settings.get("lsp_server_initialization_options")

        config = {
            "languageId": "wolfram",
            "scopes": ["source.wolfram"],
            "syntaxes": ["Packages/WolframLanguage/WolframLanguage.sublime-syntax"]
        }

        config["command"] = command
        config["initializationOptions"] = initialization_options

        return read_client_config("wolfram", config)

    def on_start(self, window) -> bool:

        self.hrefMap = {}

        settings = sublime.load_settings(settings_file)

        command = settings.get("lsp_server_command")

        kernel_path = command[0]

        #
        # if not using `kernel` syntax in command, then just return now
        #
        if not kernel_path == "`kernel`":
            return True

        #
        # Check that kernel specified by `kernel` is WolframKernel
        #
        kernel = settings.get("kernel")

        base = os.path.basename(kernel)
        if not base.lower().startswith("wolframkernel"):
            sublime.message_dialog("Command for Wolfram Language Server does not start with 'WolframKernel': " + kernel)

        return True

    def on_initialized(self, client) -> None:

        self._client = client

        client.on_notification("wolfram/versions", self.on_wolfram_versions)

        client.on_notification("textDocument/publishImplicitTokens", self.on_implicit_tokens)

        client.on_notification("textDocument/publishHTMLSnippet", self.on_html_snippet)

    def on_wolfram_versions(self, params):

        if not sublime:
            return

        wolfram_version = params["wolframVersion"]
        codeparser_version = params["codeParserVersion"]
        codeinspector_version = params["codeInspectorVersion"]
        codeformatter_version = params["codeFormatterVersion"]
        lspserver_version = params["lspServerVersion"]

        if not wolfram_version or wolfram_version == "bad":
            sublime.message_dialog("Cannot detect Wolfram version.")

        if not codeparser_version or codeparser_version == "bad":
            sublime.message_dialog("Cannot detect CodeParser paclet version.")

        if not codeinspector_version or codeinspector_version == "bad":
            sublime.message_dialog("Cannot detect CodeInspector paclet version.")

        if not codeformatter_version or codeformatter_version == "bad":
            sublime.message_dialog("Cannot detect CodeFormatter paclet version.")

        if not lspserver_version or lspserver_version == "bad":
            sublime.message_dialog("Cannot detect LSPServer paclet version.")

    def on_implicit_tokens(self, params):

        #
        # Currently grabbing the active view
        # There is no current way to obtain the view that corresponds to the file
        # Related issues: https://github.com/sublimelsp/LSP/issues/641
        #
        
        if not sublime:
            return

        active_window = sublime.active_window()

        view = active_window.active_view()

        view.erase_phantoms("implicit_tokens")

        lines = params["lines"]
        for l in lines:
            line = l["line"]
            characters = l["characters"]

            joined = "".join(characters)

            #
            # Must replace spaces with &nbsp;
            # Sublime minihtml does not support <pre>, <code>, etc.
            # Related issues: https://forum.sublimetext.com/t/does-minihtml-support-the-pre-tag/46267/3
            #

            index = 0
            for c in joined:
                if c == "x":
                    view.add_phantom("implicit_tokens",
                        sublime.Region(view.text_point(line - 1, index), view.text_point(line - 1, index + 1)),
                        '<span style="color:#888888">' + '\xd7' + '</span>',
                        sublime.LAYOUT_INLINE)
                elif c == "N":
                    view.add_phantom("implicit_tokens",
                        sublime.Region(view.text_point(line - 1, index), view.text_point(line - 1, index + 1)),
                        '<span style="color:#888888">' + 'Null' + '</span>',
                        sublime.LAYOUT_INLINE)
                elif c == "1":
                    view.add_phantom("implicit_tokens",
                        sublime.Region(view.text_point(line - 1, index), view.text_point(line - 1, index + 1)),
                        '<span style="color:#888888">' + '1' + '</span>',
                        sublime.LAYOUT_INLINE)
                elif c == "A":
                    view.add_phantom("implicit_tokens",
                        sublime.Region(view.text_point(line - 1, index), view.text_point(line - 1, index + 1)),
                        '<span style="color:#888888">' + 'All' + '</span>',
                        sublime.LAYOUT_INLINE)
                elif c == "y":
                    view.add_phantom("implicit_tokens",
                        sublime.Region(view.text_point(line - 1, index), view.text_point(line - 1, index + 1)),
                        '<span style="color:#888888">' + '\xd7' + '</span>',
                        sublime.LAYOUT_INLINE)
                    view.add_phantom("implicit_tokens",
                        sublime.Region(view.text_point(line - 1, index), view.text_point(line - 1, index + 1)),
                        '<span style="color:#888888">' + '1' + '</span>',
                        sublime.LAYOUT_INLINE)
                elif c == "B":
                    view.add_phantom("implicit_tokens",
                        sublime.Region(view.text_point(line - 1, index), view.text_point(line - 1, index + 1)),
                        '<span style="color:#888888">' + 'All' + '</span>',
                        sublime.LAYOUT_INLINE)
                    view.add_phantom("implicit_tokens",
                        sublime.Region(view.text_point(line - 1, index), view.text_point(line - 1, index + 1)),
                        '<span style="color:#888888">' + '\xd7' + '</span>',
                        sublime.LAYOUT_INLINE)
                elif c == "C":
                    view.add_phantom("implicit_tokens",
                        sublime.Region(view.text_point(line - 1, index), view.text_point(line - 1, index + 1)),
                        '<span style="color:#888888">' + 'All' + '</span>',
                        sublime.LAYOUT_INLINE)
                    view.add_phantom("implicit_tokens",
                        sublime.Region(view.text_point(line - 1, index), view.text_point(line - 1, index + 1)),
                        '<span style="color:#888888">' + '\xd7' + '</span>',
                        sublime.LAYOUT_INLINE)
                    view.add_phantom("implicit_tokens",
                        sublime.Region(view.text_point(line - 1, index), view.text_point(line - 1, index + 1)),
                        '<span style="color:#888888">' + '1' + '</span>',
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

        actions = params["actions"]
        for a in actions:
            href = a["href"]
            if href != "":
                self.hrefMap[href] = a

        lines = params["lines"]
        for l in lines:
            line = l["line"]
            characterCount = l["characterCount"]
            content = l["content"]

            view.add_phantom("html_snippet",
                sublime.Region(view.text_point(line - 1, 1 - 1), view.text_point(line - 1, characterCount - 1)),
                content,
                sublime.LAYOUT_BELOW, self.on_html_snippet_navigate)

    def on_html_snippet_navigate(self, href):
        
        if href == "":
            return

        #
        # Currently grabbing the active view
        # There is no current way to obtain the view that corresponds to the file
        # Related issues: https://github.com/sublimelsp/LSP/issues/641
        #

        if not sublime:
            return

        active_window = sublime.active_window()

        view = active_window.active_view()

        action = self.hrefMap[href]

        command = action["command"]

        if command == "insert":
            view.run_command("click_insert", {"line": action["line"], "column": action["column"], "insertionText": action["insertionText"]})
        elif command == "delete":
            view.run_command("click_delete", {"line": action["line"], "column": action["column"], "deletionText": action["deletionText"]})
        else:
            raise ValueError("unrecognized command: " + command)

        del self.hrefMap[href]


class ClickInsertCommand(sublime_plugin.TextCommand):
    def run(self, edit, line, column, insertionText):
        self.view.insert(edit, self.view.text_point(line - 1, column - 1), insertionText)


class ClickDeleteCommand(sublime_plugin.TextCommand):
    def run(self, edit, line, column, deletionText):
        self.view.erase(edit, sublime.Region(self.view.text_point(line - 1, column - 1), self.view.text_point(line - 1, column + len(deletionText) - 1)))


class WolframLanguageOpenSiteCommand(sublime_plugin.ApplicationCommand):
    """Open site links."""

    def run(self, url):
        """Open the URL."""

        webbrowser.open_new_tab(url)
