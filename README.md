# Wolfram System Integration with Sublime Text

Official Sublime Text package for Wolfram Language

[Developing Wolfram Language Code in Other Editors and IDEs with LSP from WTC 2021: Watch Video (youtube)](https://www.youtube.com/watch?v=nXVEOUMZbzQ)

Forked from [https://github.com/ViktorQvarfordt/Sublime-WolframLanguage](https://github.com/ViktorQvarfordt/Sublime-WolframLanguage)

Thanks Viktor!


## Features

* Syntax Highlighting
* Goto Definition
* Auto complete
* Diagnostics and suggestions for fixes
* Formatting files and selections
* Expand and shrink selection
* Color swatches
* Symbol references
* Documentation on hover
* New menu items (Open in System Editor)


### Syntax Highlighting

Support for the entire Wolfram Language syntax and all built-in functions.

![highlighting](docs/highlighting.png)


## Setup

Compatible with Sublime Text 3 and Sublime Text 4.

If the LSP package ([https://github.com/sublimelsp/LSP](https://github.com/sublimelsp/LSP)) is installed, then additional features will be available.

LSP functionality uses a Wolfram kernel to run as a language server.

This requires Wolfram System 12.1 or higher.

1. Install [Package Control](https://packagecontrol.io/installation)
2. Open Tools > Command Palette...
3. Select Package Control: Install Package
4. Install [LSP](https://github.com/sublimelsp/LSP)
5. Install [WolframLanguage](https://github.com/WolframResearch/Sublime-WolframLanguage)

The package must be installed from Wolfram Research.

The WolframLanguage package depends on [LSPServer paclet](https://github.com/WolframResearch/lspserver) to provide LSP functionality.

Install LSPServer paclet and its dependencies by running this Wolfram Language code:
```
PacletInstall["CodeParser"]
PacletInstall["CodeInspector"]
PacletInstall["CodeFormatter"]
PacletInstall["LSPServer"]
```

If properly setup, you should have syntax highlighting and linting of Wolfram Language `.wl` files.

Test this by typing this into a new `.wl` file and saving it:
```
Which[a, b, a, b]
```

You should see warnings about duplicate clauses.


### Settings

If you have Wolfram System installed in the default location on your system, you may not have to change any settings.

If Wolfram System is not in the default location, then specify the actual location:

Go to the menu item:
`Package Settings > Wolfram Language > Settings`

Add a `kernel` setting:
```
{
  …

  "kernel": "/Applications/Mathematica.app/Contents/MacOS/WolframKernel"
  …
}

```

You may also change the command that is used to start the server:
```
{
  …

  "lsp_server_command":
    [
      "`kernel`",
      "-noinit",
      "-noprompt",
      "-nopaclet",
      "-noicon",
      "-nostartuppaclets",
      "-run",
      "Needs[\"LSPServer`\"];LSPServer`StartServer[]"
    ]
  …
}
```

You may disable Wolfram language server by specifying:
```
{
  …
  "lsp_server_enabled": false
  …
}
```


#### Other Settings

You may use a special Light color scheme that emulates the syntax coloring of the notebook editor:
```
{
  …
  "color_scheme": "WolframLanguage.sublime-color-scheme"
  …
}
```


#### Experimental Settings

You can enable experimental settings. These are not supported.

`implicitTokens` controls the display of implicit tokens.
```
{
  …

  "implicitTokens": ["*", ",", ";;", "?"]
  …
}
```

* `"*"`: display implicit Times character `×`
* `","`: display `Null` around stray commas
* `;;`: display `1` and `All` around `;;`
* `;`: display `Null` after `;`
* `?`: display `□` in place of missing arguments


## Troubleshooting

[Troubleshooting LSP for Sublime Text](https://lsp.sublimetext.io/troubleshooting/)

Make sure that LSPServer paclet and its dependencies are up-to-date and can be found on your system:
```
PacletInstall["CodeParser"]
PacletInstall["CodeInspector"]
PacletInstall["CodeFormatter"]
PacletInstall["LSPServer"]

Needs["LSPServer`"]
```

If the kernel cannot start, then follow the instructions in the dialog that pops up after 10 seconds for more information.


### Server settings

Check `WolframLanguage.sublime-settings` for errors.

Turn on debug logging from the kernel by giving a string argument to `StartServer[]`.

This is a directory that kernel logs will be written to.
```
Needs["LSPServer`"];LSPServer`StartServer["/path/to/log/directory/"]
```


