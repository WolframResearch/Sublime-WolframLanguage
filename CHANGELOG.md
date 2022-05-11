
## 1.6.0 - XX May, 2022

Add "Download Wolfram Engine" links to main menu and command palette

support new 13.1 syntax `"PackedArray"::["Real64"]`


## 1.5.0 - 7 Mar, 2022

Open notebooks support.

Ensure an empty directory to use as working directory

Should try new versions as well as older versions

Increase timeout to 15 seconds and add timeout_warning_enabled setting

Syntax error for invalid `\|XXXXXX` character syntax

Reorganize the "Open in Notebook Editor" menu items

Add context menu item

Rename "Open in Notebook Editor" -> "Open in System Editor"

13.0.1 syntax updates


### Fixes

Fix 419286: "Open in Notebook Editor" opens other files than recognized by FE

Fix logic for resolving kernel paths


## 1.4.0 - 25 Oct, 2021

Fix 415574: unrecognized symbol followed by `[` should have scope `variable.function`

Also recognize `f @ x` syntax for function call, but do NOT recognize `a ~f~ b` or `a // f`


## 1.3.3 - 11 Oct, 2021

Treat mdpopups module as optional

If a kernel cannot be started, then do not also show the timeout dialog after 10 seconds, that is just extra noise.

`lsp_server_enabled` setting: Allow selectively disabling Wolfram Language LSP


## 1.3.2 - 27 Sep, 2021

Fixed problem with dialog saying `"Language Server kernel did not initialize properly after 10 seconds."`

The kernel actually did start correctly, but the timeout for the dialog was not being handled properly.


## 1.3.1 - 23 Sep, 2021

First release from official Wolfram Research GitHub repo

[https://github.com/WolframResearch/Sublime-WolframLanguage](https://github.com/WolframResearch/Sublime-WolframLanguage)

Forked and major rewrite from [https://github.com/ViktorQvarfordt/Sublime-WolframLanguage](https://github.com/ViktorQvarfordt/Sublime-WolframLanguage)


## 1.3.0 - 30 Aug, 2021

Now supporting Sublime 4


## 0.12 - 5 Aug, 2019

Start relying on the WolframLanguage Sublime package. There is no longer a sublime-wolfram package to install. Please read the README for changes.
