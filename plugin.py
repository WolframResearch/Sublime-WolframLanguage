import shutil
import os
import sublime
import sublime_plugin
import threading
import subprocess
import sys
import time
import datetime
import tempfile

import webbrowser

try:
    from LSP.plugin.core.settings import ClientConfig
    from LSP.plugin import register_plugin, unregister_plugin, AbstractPlugin, WorkspaceFolder
    #
    # mdpopups may not be available, but LSP depends on mdpopups, so if LSP is installed, then mdpopups is also installed
    #
    # Do not add a dependency on mdpopups to WolframLanguage
    #
    # verify that LSP depends on mdpopups: https://github.com/sublimelsp/LSP/blob/main/dependencies.json
    #
    import mdpopups
except ImportError:
    #
    # if there is an ImportError, then that means that LSP is not installed
    #
    # we want to keep LSP as optional, so handle this by mocking the bare minimum needed to simply load the plugin
    #
    # nothing in the plugin will run, we just want to guarantee that it does not crash when loading because of
    # ImportError, TypeError, etc.
    #
    #
    # Relatedly, we also want to continue to support older versions of Sublime with older versions of Python
    # So, do not yet include any special type hint syntax that was introduced in Python 3.5
    #
    class AbstractPlugin:
        pass
    def register_plugin(cls):
        pass
    def unregister_plugin(cls):
        pass

settings_file = "WolframLanguage.sublime-settings"

ping_pong_counter = 0
start_time = datetime.datetime(2020,1,1,0,0,0,0)

class LspWolframLanguagePlugin(AbstractPlugin):

    kernel_initialized = False

    #
    # AbstractPlugin is created after the server has responded, so __init__
    # can be used as a kind of on_post_initialize
    #
    # Related issues: https://github.com/sublimelsp/LSP/issues/1860
    #
    def __init__(self, weaksession):
        super().__init__(weaksession)
        self.hrefMap = {}
        cls = type(self)
        cls.kernel_initialized = True

    @classmethod
    def name(cls):
        return "wolfram"

    @classmethod
    def configuration(cls):
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

        enabled = settings.get("lsp_server_enabled", True)
        if enabled:
            #
            # if LSP settings have disabled wolfram client, then respect that
            #
            # Being disabled is "poison": if disabled is specified anywhere, then client is disabled
            #
            lsp_settings = sublime.load_settings("LSP.sublime-settings")
            clients = lsp_settings.get("clients")
            wolfram_client = clients.get("wolfram", {})
            wolfram_client_enabled = wolfram_client.get("enabled", True)
            if not wolfram_client_enabled:
                enabled = False

        settings.set("command", command)
        settings.set("initializationOptions", initialization_options)
        settings.set("selector", "source.wolfram")
        settings.set("enabled", enabled)

        return settings, filepath

    @classmethod
    def on_pre_start(cls, window, initiating_view, workspace_folders, configuration):
        
        command = configuration.command

        kernel = command[0]

        base = os.path.basename(kernel)
        if not base.lower().startswith("wolframkernel"):
            sublime.message_dialog("Command for Wolfram Language Server does not start with 'WolframKernel': " + kernel)

        #
        # Check kernel initialization after 10 seconds
        #
        sublime.set_timeout(lambda: cls.check_kernel_initialization(command), 10000)

        #
        # Ensure an empty directory to use as working directory
        #
        cls.wolfram_tmp_dir = os.path.join(tempfile.gettempdir(), "Wolfram-LSPServer")

        try:
            os.mkdir(cls.wolfram_tmp_dir)
        except FileExistsError:
            pass

        #
        # :returns:   A desired working directory, or None if you don't care
        #
        return cls.wolfram_tmp_dir

    @classmethod
    def check_kernel_initialization(cls, command):
        
        if cls.kernel_initialized:
            return
        
        kernel = command[0]

        #
        # Users knows that the kernel did not start properly, so do not also display timeout error
        #
        if not os.path.exists(kernel):
            return

        # TODO: kill kernel, if possible

        msg = ""
        msg += "Language server kernel did not respond after 10 seconds.\n"
        msg += "\n"
        msg += "The most likely cause is that required paclets are not installed.\n"
        msg += "\n"
        msg += "The language server kernel process is hanging and may need to be killed manually.\n"
        msg += "\n"
        msg += "Ignore this message if Sublime was busy opening a large file or indexing in the background.\n"
        msg += "\n"
        msg += "This is the command that was used:\n"
        msg += str(command) + "\n"
        msg += "\n"
        msg += "To ensure that required paclets are installed and up-to-date, run this in a notebook:\n"
        msg += "\n"
        msg += "PacletInstall[\"CodeParser\"]\n"
        msg += "PacletInstall[\"CodeInspector\"]\n"
        msg += "PacletInstall[\"CodeFormatter\"]\n"
        msg += "PacletInstall[\"LSPServer\"]\n"
        msg += "\n"
        msg += "To help diagnose the problem, run this in a notebook:\n"
        msg += "\n"
        msg += "Needs[\"LSPServer`\"]\n"
        msg += "LSPServer`RunServerDiagnostic[{"
        for a in command[:-1]:
            #
            # important to replace \ -> \\ before replacing " -> \"
            #
            msg += "\"" + a.replace("\\", "\\\\").replace("\"", "\\\"") + "\""
            msg += ", "
        msg += "\"" + command[-1].replace("\\", "\\\\").replace("\"", "\\\"") + "\""
        msg += "}, ProcessDirectory -> \""
        msg += cls.wolfram_tmp_dir.replace("\\", "\\\\")
        msg += "\"]\n"
        msg += "\n"
        msg += "Fix any problems then restart and try again."

        sublime.message_dialog(msg)

    def m_roundTripTest(self, params):

        if not sublime:
            return

        active_window = sublime.active_window()

        view = active_window.active_view()

        delT = datetime.datetime.now() - start_time

        print("Roundtrip timing test executed.")
        print("==========================================")
        
        sublime.message_dialog('Roundtrip Timing = '+(str(round(delT.total_seconds()*1000, 2)) + ' ms'))

    
    def m_pingPongTest(self, params):

        
        if not sublime:
            return     

        global ping_pong_counter
        ping_pong_counter = ping_pong_counter - 1

                           
        if ping_pong_counter == 0:
            delT = datetime.datetime.now() - start_time
            delT.total_seconds()
            print("Pingpong test executed.")
            print("==========================================")
            
            sublime.message_dialog('Pingpong Timing = '+(str(round(delT.total_seconds()*100, 2)) + ' ms'))
            return
        
        active_window = sublime.active_window()

        view = active_window.active_view()

        view.run_command("lsp_execute", 
                {
                    "session_name": "wolfram",
                    "command_name": "ping_pong_responsiveness_test", 
                    "command_args":{}
                }
            )

    def m_payloadTest(self, params):

        
        if not sublime:
            return     

        
        global ping_pong_counter
        ping_pong_counter = ping_pong_counter - 1

                           
        if ping_pong_counter == 0:
            delT = datetime.datetime.now() - start_time
            delT.total_seconds()

            print("Payload timing test executed.")
            print("==========================================")

            sublime.message_dialog('Payload (2.6MB) Timing = '+(str(round(delT.total_seconds()/3, 2)) + ' sec'))
            return
        
        active_window = sublime.active_window()

        view = active_window.active_view()

        view.run_command("lsp_execute", 
                {
                    "session_name": "wolfram",
                    "command_name": "payload_responsiveness_test", 
                    "command_args":{}
                    }
                )


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

class RoundTripTimingCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        global start_time
        start_time = datetime.datetime.now()
        print("Roundtrip timing test started ...")
        active_window = sublime.active_window()
        view = active_window.active_view()

        view.run_command("lsp_execute", 
            {
            "session_name": "wolfram",
            "command_name": "roundtrip_responsiveness_test", 
            "command_args":{}
            }
        )


class PingPongCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        global ping_pong_counter
        ping_pong_counter = 10

        global start_time
        start_time = datetime.datetime.now()
        print("Pingpong test started ...")
        active_window = sublime.active_window()
        view = active_window.active_view()

        view.run_command("lsp_execute", 
            {
                "session_name": "wolfram",
                "command_name": "ping_pong_responsiveness_test",
                "command_args":{}
            }
        )

class PayloadTimingCommand(sublime_plugin.ApplicationCommand):
    def run(self):

        global ping_pong_counter
        ping_pong_counter = 3

        global start_time
        start_time = datetime.datetime.now()

        print("Payload timing test started ...")

        active_window = sublime.active_window()
        view = active_window.active_view()

        view.run_command("lsp_execute", 
            {
                "session_name": "wolfram",
                "command_name": "payload_responsiveness_test", 
                "command_args":{}
            }
        )


# class OpenInFrontendCommand(sublime_plugin.WindowCommand):

#     def run(self, path=None, then_close=False):
#         view = self.window.active_view()
#         path = path or view.file_name()
#         print(path)
#         if path:
#             open_file(path)
#             if then_close:
#                 if hasattr(view, "close"):
#                     view.close()
#                 else:
#                     self.window.run_command("close")
#         else:
#             view.set_status(
#                 "NTFiles", "Cannot open file with external application")
#             sublime.set_timeout(lambda: view.erase_status("NTFiles"), 10000)

#     def is_enabled(self):
#         if self.window.active_view():
#             return self.window.active_view().file_name() is not None
#         else:
#             return False

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


# def open_file(filepath):
#     if sublime.platform() == "osx":
#         subprocess.Popen(('open', filepath))
#     elif sublime.platform() == "windows":
#         os.startfile(filepath)
#     elif sublime.platform() == "linux":
#         subprocess.Popen(('xdg-open', filepath))



def plugin_loaded():
    register_plugin(LspWolframLanguagePlugin)


def plugin_unloaded():
    unregister_plugin(LspWolframLanguagePlugin)




