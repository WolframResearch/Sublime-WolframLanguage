
execute_process(
  COMMAND
    ${WOLFRAMKERNEL} -noinit -noprompt -nopaclet -script ${GENERATESYNTAX_WL_SCRIPT} -buildDir ${BUILDDIR}
  TIMEOUT
    # this can take a while
    600
  RESULT_VARIABLE
    APPLYSYNTAXTEMPLATE_RESULT
)

if(NOT ${APPLYSYNTAXTEMPLATE_RESULT} EQUAL "0")
  message(WARNING "Bad exit code from ApplySyntaxTemplate script: ${APPLYSYNTAXTEMPLATE_RESULT}; Continuing")
endif()
