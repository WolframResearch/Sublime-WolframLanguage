BeginPackage["SublimeWolframLanguage`Generate`ApplyTemplates`"]

Begin["`Private`"]


Print["Applying Templates..."]

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

  (*
  Print[OutputForm["$builtInSymbols: "], OutputForm[SublimeWolframLanguage`Generate`$builtInSymbols]];
  Print[OutputForm["$undocumentedSymbols: "], OutputForm[SublimeWolframLanguage`Generate`$undocumentedSymbols]];
  Print[OutputForm["$experimentalSymbols: "], OutputForm[SublimeWolframLanguage`Generate`$experimentalSymbols]];
  Print[OutputForm["$obsoleteSymbols: "], OutputForm[SublimeWolframLanguage`Generate`$obsoleteSymbols]];
  *)
]


buildSyntax[] :=
Catch[
Module[{t, templateFile, appliedFile, apply},

  templateFile = FileNameJoin[{buildDir, "WolframLanguage.sublime-syntax.template"}];
  appliedFile = FileNameJoin[{buildDir, "package", "WolframLanguage", "WolframLanguage.sublime-syntax"}];

  t = FileTemplate[templateFile];

  If[FailureQ[t],
    Quit[1]
  ];

  apply = FileTemplateApply[t, <|
    "builtInFunctions" -> StringReplace[StringJoin[Riffle[SublimeWolframLanguage`Generate`$builtInSymbols, "|"]], "$" -> "\\$"],
    "undocumentedFunctions" -> StringReplace[StringJoin[Riffle[SublimeWolframLanguage`Generate`$undocumentedSymbols, "|"]], "$" -> "\\$"],
    "experimentalFunctions" -> StringReplace[StringJoin[Riffle[SublimeWolframLanguage`Generate`$experimentalSymbols, "|"]], "$" -> "\\$"],
    "obsoleteFunctions" -> StringReplace[StringJoin[Riffle[SublimeWolframLanguage`Generate`$obsoleteSymbols, "|"]], "$" -> "\\$"]
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
