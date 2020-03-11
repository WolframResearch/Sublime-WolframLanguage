# Sublime-WolframLanguage

Sublime Text 3 support for the [Wolfram Language](https://en.wikipedia.org/wiki/Wolfram_Language), the language used in Mathematica.

- Syntax highlighting.
- Auto completion for built-in functions.
- Requires Sublime Text 3 Build 3103 or later. This package uses the new syntax format `sublime-syntax`.


## Setup

Sublime-WolframLanguage depends on the CodeParser, CodeInspector, CodeFormatter, and LSPServer paclets. Make sure that the paclets can be found on your system:
```
In[1]:= Needs["CodeParser`"]
      Needs["CodeInspector`"]
      Needs["CodeFormatter`"]
      Needs["LSPServer`"]
```

[CodeParser on github.com](https://github.com/<<TODO_placeholder_for_actual_link>>)
[CodeInspector on github.com](https://github.com/<<TODO_placeholder_for_actual_link>>)
[CodeFormatter on github.com](https://github.com/<<TODO_placeholder_for_actual_link>>)
[CodeParser on github.com](https://github.com/<<TODO_placeholder_for_actual_link>>)

Install LSPServer and dependencies from the CodeTools paclet server:
```
In[1]:= PacletUpdate["CodeParser", "Site" -> "<<TODO_placeholder_for_actual_link>>", "UpdateSites" -> True]
      PacletUpdate["CodeInspector", "Site" -> "<<TODO_placeholder_for_actual_link>>", "UpdateSites" -> True]
      PacletUpdate["CodeFormatter", "Site" -> "<<TODO_placeholder_for_actual_link>>", "UpdateSites" -> True]
      PacletUpdate["LSPServer", "Site" -> "<<TODO_placeholder_for_actual_link>>", "UpdateSites" -> True]

Out[1]= PacletObject[CodeParser, 1.0, <>]
Out[2]= PacletObject[CodeInspector, 1.0, <>]
Out[3]= PacletObject[CodeFormatter, 1.0, <>]
Out[4]= PacletObject[LSPServer, 1.0, <>]
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

`Package Settings > Wolfram Language > Settings`

```
{
  "kernel": "/Applications/Mathematica121.app/Contents/MacOS/WolframKernel"
}

```


## Building

Sublime-WolframLanguage uses a Wolfram Language kernel to build a `.sublime-package` file.

Sublime-WolframLanguage uses CMake to generate build scripts.

Here is an example transcript using the default make generator to build Sublime-WolframLanguage:
```
cd sublime-wolframlanguage
mkdir build
cd build
cmake ..
cmake --build . --target package
```

The result is a directory named `package` that contains the WolframLanguage Sublime package.

Specify `MATHEMATICA_INSTALL_DIR` if you have Mathematica installed in a non-default location:
```
cmake -DMATHEMATICA_INSTALL_DIR=/Applications/Mathematica111.app/Contents/ ..
cmake --build . --target package
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
  "auto_show_diagnostics_panel": "never",
  "log_debug": true,
  "log_payloads": true,
  "log_stderr": true,
  "show_diagnostics_severity_level": 4
}

```









### Windows

It is recommended to specify `wolfram.exe` instead of `WolframKernel.exe`.

`WolframKernel.exe` opens a new window while it is running. But `wolfram.exe` runs inside the window that started it.

You may need to double-up quotations marks in the command:

``"Needs[\"\"LSPServer`\"\"];LSPServer`StartServer[]"``
