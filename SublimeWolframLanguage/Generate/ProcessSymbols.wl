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



SublimeWolframLanguage`Generate`$constants =
{"Above", "After", "All", "Anonymous", "Automatic", "Axis", "Back", \
"Backward", "Baseline", "Before", "Below", "Black", "Blue", "Bold", \
"Bottom", "Brown", "Byte", "Catalan", "CellStyle", "Center", \
"Character", "ComplexInfinity", "Constant", "Cyan", "Dashed", \
"Decimal", "DefaultAxesStyle", "DefaultBaseStyle", "DefaultBoxStyle", \
"DefaultFaceGridsStyle", "DefaultFieldHintStyle", \
"DefaultFrameStyle", "DefaultFrameTicksStyle", \
"DefaultGridLinesStyle", "DefaultLabelStyle", "DefaultMenuStyle", \
"DefaultTicksStyle", "DefaultTooltipStyle", "Degree", "Delimiter", \
"DigitCharacter", "DotDashed", "Dotted", "DragAndDrop", "E", \
"EndOfBuffer", "EndOfFile", "EndOfLine", "EndOfString", "EulerGamma", \
"Expression", "False", "Flat", "FontProperties", "Forward", \
"ForwardBackward", "Friday", "Front", "FrontEndDynamicExpression", \
"Full", "General", "Generic", "Glaisher", "GoldenAngle", \
"GoldenRatio", "Gray", "Green", "Here", "HexadecimalCharacter", \
"HoldAll", "HoldAllComplete", "HoldFirst", "HoldRest", "I", \
"Indeterminate", "Infinity", "Inherited", "Integer", "Italic", "K", \
"Khinchin", "Large", "Larger", "Launch", "Left", "LetterCharacter", \
"LightBlue", "LightBrown", "LightCyan", "LightGray", "LightGreen", \
"LightMagenta", "LightOrange", "LightPink", "LightPurple", \
"LightRed", "LightYellow", "Listable", "Listen", "Locked", \
"Loopback", "MachinePrecision", "Magenta", "Manual", "Medium", \
"MeshCellCentroid", "MeshCellMeasure", "MeshCellQuality", "Modular", \
"Monday", "NHoldAll", "NHoldFirst", "NHoldRest", "NonAssociative", \
"None", "Now", "NoWhitespace", "Null", "Number", "NumberString", \
"Orange", "ParentForm", "Pi", "Pink", "Plain", "Protected", \
"PunctuationCharacter", "Purple", "ReadProtected", "Real", "Record", \
"Red", "Right", "Saturday", "SequenceHold", "Small", "Smaller", \
"SpanFromAbove", "SpanFromBoth", "SpanFromLeft", "StartOfLine", \
"StartOfString", "String", "Stub", "Sunday", "Temporary", "Thick", \
"Thin", "ThisLink", "Thursday", "Tiny", "Today", "Tomorrow", "Top", \
"Transparent", "True", "Tuesday", "Undefined", "Underlined", \
"Wednesday", "White", "Whitespace", "WhitespaceCharacter", "Word", \
"WordBoundary", "WordCharacter", "Yellow", "Yesterday", "$Aborted", \
"$AllowExternalChannelFunctions", "$AssertFunction", "$Assumptions", \
"$AsynchronousTask", "$AudioInputDevices", "$AudioOutputDevices", \
"$BaseDirectory", "$BatchInput", "$BatchOutput", "$BlockchainBase", \
"$BoxForms", "$ByteOrdering", "$CacheBaseDirectory", "$Canceled", \
"$ChannelBase", "$CharacterEncoding", "$CharacterEncodings", \
"$CloudBase", "$CloudConnected", "$CloudCreditsAvailable", \
"$CloudEvaluation", "$CloudExpressionBase", "$CloudRootDirectory", \
"$CloudSymbolBase", "$CloudUserID", "$CloudUserUUID", \
"$CloudVersion", "$CommandLine", "$CompilationTarget", \
"$ConfiguredKernels", "$Context", "$ContextPath", \
"$ControlActiveSetting", "$Cookies", "$CookieStore", "$CreationDate", \
"$CurrentLink", "$DateStringFormat", "$DefaultAudioInputDevice", \
"$DefaultAudioOutputDevice", "$DefaultFont", "$DefaultImagingDevice", \
"$DefaultLocalBase", "$DefaultNetworkInterface", "$DefaultPath", \
"$Display", "$DisplayFunction", "$DistributedContexts", \
"$DynamicEvaluation", "$Echo", "$EmbedCodeEnvironments", \
"$EmbeddableServices", "$EntityStores", "$Epilog", \
"$EvaluationCloudBase", "$EvaluationCloudObject", \
"$EvaluationEnvironment", "$ExportFormats", "$Failed", \
"$FontFamilies", "$FormatType", "$FrontEnd", "$FrontEndSession", \
"$GeoLocation", "$GeoLocationCity", "$GeoLocationCountry", \
"$GeoLocationSource", "$HistoryLength", "$HomeDirectory", \
"$HTTPCookies", "$IgnoreEOF", "$ImageFormattingWidth", \
"$ImagingDevice", "$ImagingDevices", "$ImportFormats", \
"$IncomingMailSettings", "$InitialDirectory", \
"$InitializationContexts", "$Input", "$InputFileName", \
"$InputStreamMethods", "$Inspector", "$InstallationDate", \
"$InstallationDirectory", "$InterpreterTypes", "$IterationLimit", \
"$KernelCount", "$KernelID", "$Language", "$LibraryPath", \
"$LicenseExpirationDate", "$LicenseID", "$LicenseProcesses", \
"$LicenseServer", "$LicenseSubprocesses", "$Line", "$Linked", \
"$LinkSupported", "$LocalBase", "$LocalSymbolBase", \
"$MachineAddresses", "$MachineDomain", "$MachineDomains", \
"$MachineEpsilon", "$MachineID", "$MachineName", "$MachinePrecision", \
"$MachineType", "$MaxExtraPrecision", "$MaxLicenseProcesses", \
"$MaxLicenseSubprocesses", "$MaxMachineNumber", "$MaxNumber", \
"$MaxPiecewiseCases", "$MaxPrecision", "$MaxRootDegree", \
"$MessageGroups", "$MessagePrePrint", "$MinMachineNumber", \
"$MinNumber", "$MinPrecision", "$MobilePhone", "$ModuleNumber", \
"$NetworkConnected", "$NetworkInterfaces", "$NetworkLicense", \
"$NewMessage", "$NewSymbol", "$Notebooks", "$NumberMarks", \
"$OperatingSystem", "$Output", "$OutputForms", "$OutputSizeLimit", \
"$OutputStreamMethods", "$Packages", "$ParentLink", \
"$ParentProcessID", "$PasswordFile", "$Path", "$PathnameSeparator", \
"$PerformanceGoal", "$Permissions", "$PersistenceBase", \
"$PersistencePath", "$PipeSupported", "$PlotTheme", "$Post", "$Pre", \
"$PrePrint", "$PreRead", "$PrintForms", "$Printout3DPreviewer", \
"$ProcessID", "$ProcessorCount", "$ProcessorType", \
"$ProductInformation", "$ProgramName", "$PublisherID", \
"$RandomState", "$RecursionLimit", "$ReleaseNumber", \
"$RequesterAddress", "$RequesterWolframID", "$RequesterWolframUUID", \
"$RootDirectory", "$ScheduledTask", "$ScriptCommandLine", \
"$ScriptInputString", "$ServiceCreditsAvailable", "$Services", \
"$SessionID", "$SharedFunctions", "$SharedVariables", \
"$SoundDisplayFunction", "$SourceLink", "$SummaryBoxDataSizeLimit", \
"$SuppressInputFormHeads", "$SynchronousEvaluation", \
"$SyntaxHandler", "$System", "$SystemCharacterEncoding", "$SystemID", \
"$SystemShell", "$SystemTimeZone", "$SystemWordLength", \
"$TemplatePath", "$TemporaryDirectory", "$TemporaryPrefix", \
"$TextStyle", "$TimedOut", "$TimeUnit", "$TimeZone", \
"$TimeZoneEntity", "$TracePattern", "$TracePostAction", \
"$TracePreAction", "$UnitSystem", "$Urgent", "$UserAgentString", \
"$UserBaseDirectory", "$UserDocumentsDirectory", "$UserName", \
"$UserURLBase", "$Version", "$VersionNumber", "$VoiceStyles", \
"$WolframID", "$WolframUUID"}



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

  Print["scanning Obsolete symbols... \[WatchIcon]"];

  (*
  "OBSOLETE SYMBOL" is found in the first ~50 lines, so use 100 as a heuristic for how many lines to read
  *)
  obsoleteNames = Select[names, FindList[#, "\"OBSOLETE SYMBOL\"", 100] != {}&];

  SublimeWolframLanguage`Generate`$obsoleteSymbols = StringDrop[#, -3]& /@ obsoleteNames;

  Print["scanning Experimental symbols... \[WatchIcon]"];

  (*
  "EXPERIMENTAL" is found in the first ~500 lines, so use 1000 as a heuristic for how many lines to read
  *)
  experimentalNames = Select[names, FindList[#, "\"EXPERIMENTAL\"", 1000] != {}&];

  SublimeWolframLanguage`Generate`$experimentalSymbols = StringDrop[#, -3]& /@ experimentalNames;

  SublimeWolframLanguage`Generate`$builtInFunctions =
    Complement[documentedSymbols,
      SublimeWolframLanguage`Generate`$constants,
      SublimeWolframLanguage`Generate`$obsoleteSymbols,
      SublimeWolframLanguage`Generate`$experimentalSymbols];

  ResetDirectory[];
]

dumpSystemSymbols[] :=
Module[{dumpFile},

  dumpFile = FileNameJoin[{buildDir, "processedSymbols.mx"}];

  DumpSave[dumpFile, {
    SublimeWolframLanguage`Generate`$builtInFunctions,
    SublimeWolframLanguage`Generate`$constants,
    SublimeWolframLanguage`Generate`$undocumentedSymbols,
    SublimeWolframLanguage`Generate`$experimentalSymbols,
    SublimeWolframLanguage`Generate`$obsoleteSymbols}]
]

setupSystemSymbols[]

dumpSystemSymbols[]

Print["Done Processing Symbols"]

End[]

EndPackage[]
