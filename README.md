# Sublime-WolframLanguage

Sublime Text 3 support for the [Wolfram Language](https://en.wikipedia.org/wiki/Wolfram_Language), the language used in Mathematica.

- Syntax highlighting.
- Auto completion for built-in functions.
- Requires Sublime Text 3 Build 3103 or later. This package uses the new syntax format `sublime-syntax`.


## Setup

Sublime-WolframLanguage depends on the CodeParser, CodeInspector, CodeFormatter, and LSPServer paclets. Make sure that the paclets can be found on your system:
```
Needs["CodeParser`"]
Needs["CodeInspector`"]
Needs["CodeFormatter`"]
Needs["LSPServer`"]
```

[CodeParser on github.com](https://github.com/<<TODO_placeholder_for_actual_link>>)
[CodeInspector on github.com](https://github.com/<<TODO_placeholder_for_actual_link>>)
[CodeFormatter on github.com](https://github.com/<<TODO_placeholder_for_actual_link>>)
[LSPServer on github.com](https://github.com/<<TODO_placeholder_for_actual_link>>)

Install LSPServer and dependencies from the CodeTools paclet server:
```
PacletInstall["CodeParser"]
PacletInstall["CodeInspector"]
PacletInstall["CodeFormatter"]
PacletInstall["LSPServer"]
```

If you haven't already, [install Package Control](https://packagecontrol.io/installation), then select `WolframLanguage` from the `Package Control: Install Package` dropdown list in the Command Palette.


In the Command Palette: LSP: Enable Language Server Globally, and select wolfram


Restart Sublime

You should now have syntax highlighting and linting of Wolfram `.m` and `.wl` files working.

Test this by typing this into a new `.m` file and saving it:
```
Which[a, b, a, b]
```

You should see warnings about duplicate clauses.


### Settings

If you have `Mathematica` installed in the default location on your system, you may not have to change any settings.

If `Mathematica` is not in the default location, then change the location by going to:

`Package Settings > Wolfram Language > Settings`

and adding a `kernel` setting:

```
{
  "kernel": "/Applications/Mathematica121.app/Contents/MacOS/WolframKernel"
}

```

There are other settings such as `lsp_server_command` that specifies the command to run for the server:

```
{
  "lsp_server_command":
    [
      "`kernel`",
      "-noinit",
      "-noprompt",
      "-nopaclet",
      "-noicon",
      "-run",
      "Needs[\"LSPServer`\"];LSPServer`StartServer[]"
    ]
}
```

#### Experimental Settings

You can enable experimental settings. These are not supported.

`implicitTokens` controls the display of implicit tokens such as `Null` after `;` and implicit Times character `×`.

`bracketMatcher` controls the experimental ML-based bracket matching recommendation system and UI.

Note: `bracketMatcher` requires the `ML4Code` package to be installed.

```
{
  "lsp_server_initialization_options": {
      "implicitTokens": true,
      "bracketMatcher": true
    }
}
```




## Using LSPServer paclet WITHOUT the Sublime-WolframLanguage package

It is possible to use the LSPServer paclet without using the Sublime-WolframLanguage package.

Add a `wolfram` client to `LSP.sublime-settings`:
```
{
  "clients":
  {
    "wolfram":
    {
      "enabled": true,

      "command":
        [
          "<<Path to WolframKernel>>",
          "-noinit",
          "-noprompt",
          "-nopaclet",
          "-noicon",
          "-run",
          "Needs[\"LSPServer`\"];LSPServer`StartServer[]"
        ],
  
      "scopes": ["source.wolfram"],
 
      "syntaxes": ["<<Path to Wolfram sublime-syntax>>"]

      "languageId": "wolfram",
  
      "initializationOptions": { }
    }
  }
}
```


## Troubleshooting


Make sure that the required packages are up-to-date:
sublime-wolframlanguage
LSP package

make sure older versions are not present

Package Control > List Packages


LSP with URL https://github.com/tomv564/LSP
Remove Package


WolframLanguage with URL https://github.com/ViktorQvarfordt/Sublime-WolframLanguage
Remove Package

### Debugging

Turn on debug LSP settings


LSP > Settings

```
{
  "log_debug": true,
  "log_server": true,
  "log_payloads": true,
  "log_stderr": true
}
```

### Windows

You may need to double-up quotations marks in the command:

``"Needs[\"\"LSPServer`\"\"];LSPServer`StartServer[]"``



