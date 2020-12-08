import shutil
import os
import sublime
import sublime_plugin
import threading
import subprocess
import sys
import time
import mdpopups

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

        implicitTokens = settings.get("implicitTokens", False)
        bracketMatcher = settings.get("bracketMatcher", False)

        initialization_options = {
            "implicitTokens": implicitTokens,
            "bracketMatcher": bracketMatcher
        }

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

        command[0] = kernel
        
        base = os.path.basename(kernel)
        if not base.lower().startswith("wolframkernel"):
            sublime.message_dialog("Command for Wolfram Language Server does not start with 'WolframKernel': " + kernel)

        # start timer thread for checking that kernel initialized properly
        timer = threading.Thread(target=self.kernel_initialization_check_function, args=(command,))

        self.kernel_initialized = False

        timer.start()

        return True

    def on_initialized(self, client) -> None:

        self.kernel_initialized = True

        self._client = client

        client.on_notification("textDocument/publishImplicitTokens", self.on_implicit_tokens)

        client.on_notification("textDocument/publishHTMLSnippet", self.on_html_snippet)

    def kernel_initialization_check_function(self, command):
        
        time.sleep(10)
        
        if self.kernel_initialized:
            return

        # kill kernel, if possible

        msg = ""
        msg += "Language Server kernel did not initialize properly after 10 seconds.\n"
        msg += "\n"
        msg += "This is the command that was used:\n"
        msg += str(command) + "\n"
        msg += "\n"
        msg += "To diagnose the problem, run this in a notebook:\n"
        msg += "\n"
        msg += "Needs[\"LSPServer`\"]\n"
        msg += "LSPServer`RunServerDiagnostic[{"
        for a in command[:-1]:
            msg += "\"" + a.replace("\"", "\\\"") + "\""
            msg += ", "
        msg += "\"" + command[-1].replace("\"", "\\\"") + "\""
        msg += "}]\n"
        msg += "\n"
        msg += "Fix any problems then restart and try again."

        sublime.message_dialog(msg)


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

        tokens = params["tokens"]
        for t in tokens:
            line = t["line"]
            column = t["column"]
            c = t["character"]

            #
            # FIXME: Use the same font as the editor
            # style = font-family: xxx;
            #
            content = '<span style="color:#888888">' + implicitTokenCharToText(c) + '</span>'
            
            view.add_phantom("implicit_tokens",
                sublime.Region(view.text_point(line - 1, column - 1), view.text_point(line - 1, column - 1)),
                content,
                sublime.LAYOUT_INLINE)


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

        # view.erase_phantoms("html_snippet")
        mdpopups.erase_phantoms(view, "html_snippet")
        # view.hide_popup()
        # mdpopups.hide_popup(view)
        
        actions = params["actions"]
        for a in actions:
            href = a["href"]
            if href != "":
                self.hrefMap[href] = a

        lines = params["lines"]

        #
        # there may be multiple lines if in debug mode
        #
        for l in lines:
            line = l["line"]
            characterCount = l["characterCount"]
            content = l["content"]

            where = sublime.Region(view.text_point(line - 1, 1 - 1), view.text_point(line - 1, characterCount - 1))
            
            # view.add_phantom("html_snippet", where, content, sublime.LAYOUT_BELOW, self.on_html_snippet_navigate)
            mdpopups.add_phantom(view, "html_snippet", where, content, layout=sublime.LAYOUT_BELOW, on_navigate=self.on_html_snippet_navigate)
            # view.show_popup(content, location=view.text_point(line - 1, 1 - 1), on_navigate=self.on_html_snippet_navigate)
            # mdpopups.show_popup(view, content, location=view.text_point(line - 1, 1 - 1), on_navigate=self.on_html_snippet_navigate)

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

        # view.erase_phantoms("html_snippet")
        mdpopups.erase_phantoms(view, "html_snippet")
        # view.hide_popup()
        # mdpopups.hide_popup(view)

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


def implicitTokenCharToText(c):
    if c == "x":
        return "\xd7"
    elif c == "N":
        return "Null"
    elif c == "1":
        return "1"
    elif c == "A":
        return "All"
    elif c == "e":
        return "\u25a1"
    elif c == "f":
        return "\u25a1\xd7"
    elif c == "y":
        return "\xd71"
    elif c == "B":
        return "All\xd7"
    elif c == "C":
        return "All\xd71"
    else:
        return " "

