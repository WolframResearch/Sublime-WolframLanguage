BeginPackage["SublimeWolframLanguage`Generate`ProcessSymbols`"]

Begin["`Private`"]


Print["Processing Symbols..."]

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



setupSystemSymbols[] :=
Module[{names, documentedSymbols, allSymbols, allASCIISymbols, obsoleteNames,
  experimentalNames},

  SetDirectory[FileNameJoin[{$InstallationDirectory, "Documentation/English/System/ReferencePages/Symbols"}]];

  Print["scanning Documented symbols..."];

  names = FileNames["*.nb", "", Infinity];

  documentedSymbols = StringDrop[#, -3]& /@ names;

  allSymbols = Names["System`*"];

  allASCIISymbols = Flatten[StringCases[allSymbols, RegularExpression["[a-zA-Z0-9$]+"]]];

  SublimeWolframLanguage`Generate`$undocumentedSymbols = Complement[allASCIISymbols, documentedSymbols];

  Print["scanning Obsolete symbols..."];

  (*
  "OBSOLETE SYMBOL" is found in the first ~50 lines, so use 100 as a heuristic for how many lines to read
  *)
  obsoleteNames = Select[names, FindList[#, "\"OBSOLETE SYMBOL\"", 100] != {}&];

  SublimeWolframLanguage`Generate`$obsoleteSymbols = StringDrop[#, -3] & /@ obsoleteNames;

  Print["scanning Experimental symbols..."];

  (*
  "EXPERIMENTAL" is found in the first ~500 lines, so use 1000 as a heuristic for how many lines to read
  *)
  experimentalNames = Select[names, FindList[#, "\"EXPERIMENTAL\"", 1000] != {}&];

  SublimeWolframLanguage`Generate`$experimentalSymbols = StringDrop[#, -3]& /@ experimentalNames;

  SublimeWolframLanguage`Generate`$builtInSymbols = Complement[documentedSymbols, SublimeWolframLanguage`Generate`$obsoleteSymbols, SublimeWolframLanguage`Generate`$experimentalSymbols];

  ResetDirectory[];
]

dumpSystemSymbols[] :=
Module[{dumpFile},

  dumpFile = FileNameJoin[{buildDir, "processedSymbols.mx"}];

  DumpSave[dumpFile, {SublimeWolframLanguage`Generate`$builtInSymbols, SublimeWolframLanguage`Generate`$undocumentedSymbols, SublimeWolframLanguage`Generate`$experimentalSymbols, SublimeWolframLanguage`Generate`$obsoleteSymbols}]
]

setupSystemSymbols[]

dumpSystemSymbols[]

Print["Done Processing Symbols"]

End[]

EndPackage[]
