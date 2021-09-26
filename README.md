# Wolfram System Integration with Sublime Text

Official Sublime Text package for Wolfram Language

* Syntax highlighting
* [LSP](https://microsoft.github.io/language-server-protocol/) support

![highlighting](docs/highlighting.png)


Forked from [https://github.com/ViktorQvarfordt/Sublime-WolframLanguage](https://github.com/ViktorQvarfordt/Sublime-WolframLanguage)

Thanks Viktor!


## Compatibility

Compatible with Sublime Text 3 and Sublime Text 4.

If the LSP package ([https://github.com/sublimelsp/LSP](https://github.com/sublimelsp/LSP)) is installed, then additional features will be available.


## Setup

1. Install [Package Control](https://packagecontrol.io/installation)
2. Open Tools > Command Palette...
3. Select Package Control: Install Package
4. Install [LSP](https://github.com/sublimelsp/LSP)
5. Install [WolframLanguage](https://github.com/WolframResearch/Sublime-WolframLanguage)

The WolframLanguage package depends on [LSPServer paclet](https://github.com/WolframResearch/lspserver) to provide LSP functionality.

Install LSPServer and its dependencies by running this Wolfram Language code:
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

  "kernel": "/Applications/Mathematica123.app/Contents/MacOS/WolframKernel"

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

#### Experimental Settings

You can enable experimental settings. These are not supported.

`implicitTokens` controls the display of implicit tokens such as `Null` after `;` and implicit Times character `×`.

```
{
  …

  "implicitTokens": ["*", ",", ";;", "?"]

  …
}
```


## Troubleshooting

Make sure that the paclets can be found on your system:
```
Needs["LSPServer`"]
```

[Troubleshooting LSP for Sublime Text](https://lsp.sublimetext.io/troubleshooting/)
