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

from LSP.plugin.core.settings import ClientConfig
from LSP.plugin import register_plugin, unregister_plugin, AbstractPlugin, WorkspaceFolder
from LSP.plugin.core.typing import Tuple, List, Optional

settings_file = "WolframLanguage.sublime-settings"

class LspWolframLanguagePlugin(AbstractPlugin):

    hrefMap = {}
    kernel_initialized = False

    @classmethod
    def name(cls) -> str:
        return "wolfram"

    @classmethod
    def configuration(cls) -> Tuple[sublime.Settings, str]:
        filepath = "Packages/WolframLanguage/{}".format(settings_file)
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
        # Related lines: https://github.com/sublimelsp/LSP/blob/main/plugin/core/types.py#L657
        #
        command = list(
            arg.replace("$", "\\[RawDollar]")
            for arg in command
        )

        implicitTokens = settings.get("implicitTokens", [])
        bracketMatcher = settings.get("bracketMatcher", False)

        initialization_options = {
            "implicitTokens": implicitTokens,
            "bracketMatcher": bracketMatcher
        }

        settings.set("command", command)
        settings.set("initializationOptions", initialization_options)
        settings.set("selector", "source.wolfram")

        return settings, filepath

    @classmethod
    def on_pre_start(cls, window: sublime.Window, initiating_view: sublime.View, workspace_folders: List[WorkspaceFolder], configuration: ClientConfig) -> Optional[str]:
        
        command = configuration.command

        kernel = command[0]

        base = os.path.basename(kernel)
        if not base.lower().startswith("wolframkernel"):
            sublime.message_dialog("Command for Wolfram Language Server does not start with 'WolframKernel': " + kernel)

        # start timer thread for checking that kernel initialized properly
        timer = threading.Thread(target=cls.kernel_initialization_check_function, args=(command,))

        timer.start()

        return None
 
    @classmethod
    def on_post_start(cls, window: sublime.Window, initiating_view: sublime.View, workspace_folders: List[WorkspaceFolder], configuration: ClientConfig) -> None:
        cls.kernel_initialized = True

    @classmethod
    def kernel_initialization_check_function(cls, command):
        
        time.sleep(10)
        
        if cls.kernel_initialized:
            return

        # kill kernel, if possible

        msg = ""
        msg += "Language Server kernel did not initialize properly after 10 seconds.\n"
        msg += "\n"
        msg += "Ignore this message if Sublime was busy opening a large file or indexing in the background.\n"
        msg += "\n"
        msg += "This is the command that was used:\n"
        msg += str(command) + "\n"
        msg += "\n"
        msg += "To help diagnose the problem, run this in a notebook:\n"
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

    def m_textDocument_publishImplicitTokens(self, params):

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


    def m_textDocument_publishHTMLSnippet(self, params):

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
    if c == "z":
        return "&nbsp;\xd7"
    elif c == "N":
        # add a space before Null because it looks nicer
        return "&nbsp;Null"
    elif c == "1":
        return "1"
    elif c == "A":
        return "All"
    elif c == "e":
        # add space before and after \u25a1 because it looks nicer
        return "&nbsp;\u25a1&nbsp;"
    elif c == "f":
        return "\u25a1\xd7"
    elif c == "y":
        return "\xd71"
    elif c == "B":
        return "All\xd7"
    elif c == "C":
        return "All\xd71"
    elif c == "D":
        return "All1"
    else:
        return " "


def plugin_loaded():
    register_plugin(LspWolframLanguagePlugin)


def plugin_unloaded():
    unregister_plugin(LspWolframLanguagePlugin)




