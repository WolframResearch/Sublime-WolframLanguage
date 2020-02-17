BeginPackage["SublimeWolframLanguage`Generate`ApplyTemplates`"]

Begin["`Private`"]


Print["Applying Templates..."]

srcDirFlagPosition = FirstPosition[$CommandLine, "-srcDir"]

If[MissingQ[srcDirFlagPosition],
  Print["Cannot proceed; Unsupported src directory"];
  Quit[1]
]

srcDir = $CommandLine[[srcDirFlagPosition[[1]] + 1]]

If[FileType[srcDir] =!= Directory,
  Print["Cannot proceed; Unsupported src directory"];
  Quit[1]
]

buildDirFlagPosition = FirstPosition[$CommandLine, "-buildDir"]

If[MissingQ[buildDirFlagPosition],
  Print["Cannot proceed; Unsupported build directory"];
  Quit[1]
]

buildDir = $CommandLine[[buildDirFlagPosition[[1]] + 1]]

If[FileType[buildDir] =!= Directory,
  Print["Cannot proceed; Unsupported build directory"];
  Quit[1]
]



getSystemSymbols[] :=
Module[{dumpFile},

  dumpFile = FileNameJoin[{buildDir, "processedSymbols.mx"}];

  Get[dumpFile];
]


buildSyntax[] :=
Catch[
Module[{t, templateFile, appliedFile, apply, longNameFile},

  templateFile = FileNameJoin[{buildDir, "WolframLanguage.sublime-syntax.template"}];
  appliedFile = FileNameJoin[{buildDir, "package", "WolframLanguage", "WolframLanguage.sublime-syntax"}];

  Print["scanning Long Names..."];

  longNameFile = FileNameJoin[{srcDir, "SublimeWolframLanguage", "Data", "LongNames.wl"}];

  longNamesAssoc = Get[longNameFile];

  $longNames = Keys[longNamesAssoc];

  t = FileTemplate[templateFile];

  If[FailureQ[t],
    Quit[1]
  ];

  apply = FileTemplateApply[t, <|
    "builtInFunctions" -> StringReplace[StringJoin[Riffle[SublimeWolframLanguage`Generate`$builtInSymbols, "|"]], "$" -> "\\$"],
    "undocumentedFunctions" -> StringReplace[StringJoin[Riffle[SublimeWolframLanguage`Generate`$undocumentedSymbols, "|"]], "$" -> "\\$"],
    "experimentalFunctions" -> StringReplace[StringJoin[Riffle[SublimeWolframLanguage`Generate`$experimentalSymbols, "|"]], "$" -> "\\$"],
    "obsoleteFunctions" -> StringReplace[StringJoin[Riffle[SublimeWolframLanguage`Generate`$obsoleteSymbols, "|"]], "$" -> "\\$"],
    "longNames" -> StringJoin[Riffle[$longNames, "|"]]
    |>, appliedFile];

  Print[apply];

]]



buildCompletions[] :=
Catch[
Module[{t, templateFile, appliedFile, apply},

  templateFile = FileNameJoin[{buildDir, "WolframLanguage.sublime-completions.template"}];
  appliedFile = FileNameJoin[{buildDir, "package", "WolframLanguage", "WolframLanguage.sublime-completions"}];

  t = FileTemplate[templateFile];

  If[FailureQ[t],
    Quit[1]
  ];

  apply = FileTemplateApply[t, <|
    "builtInFunctions" -> StringJoin[Riffle[{"    \"", #, "\""}& /@ SublimeWolframLanguage`Generate`$builtInSymbols, ",\n"]]
    |>, appliedFile];

  Print[apply];

]]

getSystemSymbols[]

buildSyntax[]

buildCompletions[]

Print["Done Applying Templates"]

End[]

EndPackage[]
