BeginPackage["SublimeWolframLanguage`Generate`GenerateSyntax`"]

Begin["`Private`"]


Print[OutputForm["Generating Syntax..."]]

buildDirFlagPosition = FirstPosition[$CommandLine, "-buildDir"]

If[MissingQ[buildDirFlagPosition],
  Print[OutputForm["Cannot proceed; Unsupported build directory"]];
  Quit[1]
]

buildDir = $CommandLine[[buildDirFlagPosition[[1]] + 1]]

If[FileType[buildDir] =!= Directory,
  Print[OutputForm["Cannot proceed; Unsupported build directory"]];
  Quit[1]
]



setupSystemSymbols[] :=
Module[{names, documentedSymbols, allSymbols, allASCIISymbols, obsoleteNames,
  experimentalNames},

  SetDirectory[FileNameJoin[{$InstallationDirectory, "Documentation/English/System/ReferencePages/Symbols"}]];

  names = FileNames["*.nb", "", Infinity];

  documentedSymbols = StringDrop[#, -3]& /@ names;

  allSymbols = Names["System`*"];

  allASCIISymbols = Flatten[StringCases[allSymbols, RegularExpression["[a-zA-Z0-9$]+"]]];

  $undocumentedSymbols = Complement[allASCIISymbols, documentedSymbols];

  Print[OutputForm["scanning Obsolete symbols..."]];

  (*
  "OBSOLETE SYMBOL" is found in the first ~50 lines, so use 100 as a heuristic for how many lines to read
  *)
  obsoleteNames = Select[names, FindList[#, "\"OBSOLETE SYMBOL\"", 100] != {}&];

  $obsoleteSymbols = StringDrop[#, -3] & /@ obsoleteNames;

  Print[OutputForm["scanning Experimental symbols..."]];

  (*
  "EXPERIMENTAL" is found in the first ~500 lines, so use 1000 as a heuristic for how many lines to read
  *)
  experimentalNames = Select[names, FindList[#, "\"EXPERIMENTAL\"", 1000] != {}&];

  $experimentalSymbols = StringDrop[#, -3]& /@ experimentalNames;

  $builtInSymbols = Complement[documentedSymbols, $obsoleteSymbols, $experimentalSymbols];

  ResetDirectory[];
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
    "builtInFunctions" -> StringReplace[StringJoin[Riffle[$builtInSymbols, "|"]], "$" -> "\\$"],
    "undocumentedFunctions" -> StringReplace[StringJoin[Riffle[$undocumentedSymbols, "|"]], "$" -> "\\$"],
    "experimentalFunctions" -> StringReplace[StringJoin[Riffle[$experimentalSymbols, "|"]], "$" -> "\\$"],
    "obsoleteFunctions" -> StringReplace[StringJoin[Riffle[$obsoleteSymbols, "|"]], "$" -> "\\$"]
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
    "builtInFunctions" -> StringJoin[Riffle[{"    \"", #, "\""}& /@ $builtInSymbols, ",\n"]]
    |>, appliedFile];

  Print[apply];

]]

setupSystemSymbols[]

buildSyntax[]

buildCompletions[]

Print[OutputForm["Done Syntax"]]

End[]

EndPackage[]
