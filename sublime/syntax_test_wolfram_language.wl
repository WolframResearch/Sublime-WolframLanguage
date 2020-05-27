(* SYNTAX TEST "WolframLanguage.sublime-syntax" *)

(*
  For information on how this file is used, see
  https://www.sublimetext.com/docs/3/syntax.html#testing
  Run tests by pressing `ctrl+shift+b` (or `cmd+b` on macOS), i.e. run the `build` command
*)

(* NUMBERS *)

   11
(* ^^ constant.numeric *)
   .11
(* ^^^ constant.numeric *)
   11.
(* ^^^ constant.numeric *)
   11.11
(* ^^^^^ constant.numeric *)
   11.11`
(* ^^^^^^ constant.numeric *)
   11.11`11.11
(* ^^^^^^^^^^^ constant.numeric *)


(* LANGUAGE CONSTANTS *)

   Catalan
(* ^ constant.language.wolfram *)
   Pi
(* ^ constant.language.wolfram *)

   True
(* ^^^^ constant.language *)
   Left
(* ^^^^ constant.language *)

(* OPERATORS *)

  +
(*^ keyword.operator.arithmetic*)
  -
(*^ keyword.operator.arithmetic*)
  /
(*^ keyword.operator.arithmetic*)
  *
(*^ keyword.operator.arithmetic*)


(* ! could be Not or Factorial, so do not mark as keyword.operator.logical *)
  !
(*^ keyword.operator*)


  &&
(*^^ keyword.operator.logical*)
  ||
(*^^ keyword.operator.logical*)

  >
(*^ keyword.operator*)
  <
(*^ keyword.operator*)
  ==
(*^^ keyword.operator*)
  >=
(*^^ keyword.operator*)
  <=
(*^^ keyword.operator*)
  ===
(*^^^ keyword.operator*)
  =!=
(*^^^ keyword.operator*)

   @
(* ^ keyword.operator *)
   @@
(* ^^ keyword.operator *)
   @@@
(* ^^^ keyword.operator *)
   @*
(* ^^ keyword.operator *)
   /*
(* ^^ keyword.operator *)
   /@
(* ^^ keyword.operator *)
   /;
(* ^^ keyword.operator *)
   //
(* ^^ keyword.operator *)
   /:
(* ^^ keyword.operator *)
   =
(* ^ keyword.operator *)
   :=
(* ^^ keyword.operator *)
   :>
(* ^^ keyword.operator *)
   ->
(* ^^ keyword.operator *)
   <->
(* ^^^ keyword.operator *)

  f'[x]
(* ^ keyword.operator.Derivative *)


(* STRINGIFYING OPERATORS *)

  >>>
(*^^^ invalid.illegal *)

  >>
(*^^ invalid.illegal *)

  <<
(*^^ invalid.illegal *)


  abc >>> def
(*^^^ variable.other.wolfram*)
(*    ^^^ keyword.operator.PutAppend.wolfram *)
(*        ^^^ string.unquoted.wolfram *)

  abc >>> "def"
(*^^^ variable.other.wolfram*)
(*    ^^^ keyword.operator.PutAppend.wolfram *)
(*        ^^^^^ string.quoted.double.wolfram *)

  abc >> def
(*^^^ variable.other.wolfram*)
(*    ^^ keyword.operator.Put.wolfram *)
(*       ^^^ string.unquoted.wolfram *)

  abc >> "def"
(*^^^ variable.other.wolfram*)
(*    ^^ keyword.operator.Put.wolfram *)
(*       ^^^^^ string.quoted.double.wolfram *)

  << qwerty
(*^^ keyword.operator.Get.wolfram *)
(*   ^^^^^^ string.unquoted.wolfram *)

  << "qwerty"
(*^^ keyword.operator.Get.wolfram *)
(*   ^^^^^^^^ string.quoted.double.wolfram *)

  abc << def
(*^^^ variable.other.wolfram*)
(*    ^^ keyword.operator.Get.wolfram *)
(*       ^^^ string.unquoted.wolfram *)

  ::
(*^^ invalid.illegal *)

  symbol::tag
(*^^^^^^ variable.other.wolfram *)
(*      ^^ keyword.operator.MessageName.wolfram *)
(*        ^^^ string.unquoted.wolfram *)

  symbol::"tag"
(*^^^^^^ variable.other.wolfram *)
(*      ^^ keyword.operator.MessageName.wolfram *)
(*        ^^^^^ string.quoted.double.wolfram *)


(* VARIABLES *)

  f[x]
(*^ variable*)
  foo$bar12
(*^^^^^^^^^ variable.other *)
  $foo
(*^^^^ variable.other *)
  my`context12`$foo
(*^^^^^^^^^^^^^^^^^ variable.other *)
  1$12foo
(*^ constant.numeric.wolfram *)
(* ^^^^^^ variable.other.wolfram *)

  System`foo
(*^^^^^^^^^^ invalid.illegal.system.wolfram *)
  URLFetch
(*^^^^^^^^ invalid.deprecated.wolfram *)
  DiskBox
(*^^^^^^^ variable.function.undocumented.wolfram *)
  BaseEncode
(*^^^^^^^^^^ variable.function.experimental.wolfram *)

  Plus
(*^^^^ variable.function *)
  System`Plus
(*^^^^^^^^^^^ variable.function *)

  Image[Red, Interleaving -> True]
(*^^^^^ variable.function.builtin.wolfram *)
(*      ^^^ constant.language.wolfram *)
(*           ^^^^^^^^^^^^ variable.function.builtin.wolfram *)
(*                        ^^ keyword.operator *)

  `foo
(*^^^^ variable.other *)

  `$desktopCacheBase
(*^^^^^^^^^^^^^^^^^^ variable.other *)

  System`\[FormalX]
(*^^^^^^^^^^^^^^^^^ constant.language.wolfram *)






(* STRINGS *)

  "This is a `string` (* this is not a comment*)"
(* ^ string.quoted *)
(*                       ^ string.quoted *)
(*                                    ^ string.quoted.double *)

  foo::bar = "message"
(*   ^^ keyword.operator.MessageName *)
(*     ^^^ string.unquoted*)
(*             ^ string.quoted *)

  "this`is`a`context"
(*^ punctuation.definition.string.begin *)
(* ^^^^^^^^^^^^^^^^^ string.quoted.double.wolfram*)


(* COMMENTS *)

(* simple comment *)
(* ^ comment.block *)

(* comment (*in a comment*) *)
(* ^^^^^^^^ comment.block.wolfram *)
(*         ^^^^^^^^^^^^^^^^ comment.block.wolfram comment.block.wolfram *)


(* BRACKETS *)

  <|   |>  foo
(*^^ meta.association.wolfram punctuation.section.association.begin.wolfram  *)
(*   ^ meta.association.wolfram  *)
(*     ^^ meta.association.wolfram punctuation.section.association.end.wolfram *)
(*         ^^^ source.wolfram variable.other *)

  [ ]
(*^ meta.brackets.wolfram punctuation.section.brackets.begin.wolfram *)
(* ^ meta.brackets.wolfram *)
(*  ^ meta.brackets.wolfram punctuation.section.brackets.end.wolfram *)

  { }
(*^ meta.braces.wolfram punctuation.section.braces.begin.wolfram *)
(* ^ meta.braces.wolfram *)
(*  ^ meta.braces.wolfram punctuation.section.braces.end.wolfram *)

  ( )
(*^ meta.parens.wolfram punctuation.section.parens.begin.wolfram *)
(* ^ meta.parens.wolfram *)
(*  ^ meta.parens.wolfram punctuation.section.parens.end.wolfram *)

  [ [ ]]
(*^^^ meta.parts.wolfram punctuation.section.parts.begin.wolfram *)
(*   ^ meta.parts.wolfram *)
(*    ^^ meta.parts.wolfram punctuation.section.parts.end.wolfram *)

  [[ ]]
(*^^ meta.parts.wolfram punctuation.section.parts.begin.wolfram *)
(*  ^ meta.parts.wolfram *)
(*   ^^ meta.parts.wolfram punctuation.section.parts.end.wolfram *)




(* Out[] syntax*)


  %
(*^ keyword.other.Out.wolfram *)

  %%
(*^^ keyword.other.Out.wolfram *)

  %%%
(*^^^ keyword.other.Out.wolfram *)

  %%%%
(*^^^^keyword.other.Out.wolfram *)

  %1
(*^^ keyword.other.Out.wolfram *)

  %2
(*^^ keyword.other.Out.wolfram *)

  %123
(*^^^^ keyword.other.Out.wolfram *)

  %9999
(*^^^^^ keyword.other.Out.wolfram *)





(* Slot[] and SlotSequence[] syntax *)

  #
(*^ keyword.other.Slot.wolfram *)

  ##
(*^^ keyword.other.SlotSequence.wolfram *)

  #1
(*^^ keyword.other.Slot.wolfram *)

  ##1
(*^^^ keyword.other.SlotSequence.wolfram *)

  #123
(*^^^^ keyword.other.Slot.wolfram *)

  ##123
(*^^^^^ keyword.other.SlotSequence.wolfram *)

  #abc
(*^^^^ keyword.other.Slot.wolfram *)

  #Sin
(*^^^^ keyword.other.Slot.wolfram *)

  #abc123
(*^^^^^^^ keyword.other.Slot.wolfram *)






(* Function Definitions *)

  foo[] := xxx
(*^^^ entity.name.function.wolfram *)

  foo[g[], h[]] := xxx
(*^^^ entity.name.function.wolfram *)

  foo[1, 2, a__, b__, c__, g[h[j[]]]] := xxx
(*^^^ entity.name.function.wolfram *)




(* Constant definitions *)

  a = 1
(*^ entity.name.constant.wolfram *)

Module[{}, a = 1]
(*         ^ variable.other.wolfram *)

  $constant := 3 + 4
(*^^^^^^^^^ entity.name.constant.wolfram *)






















