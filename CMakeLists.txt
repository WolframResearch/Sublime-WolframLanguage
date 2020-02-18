
cmake_minimum_required(VERSION 3.0)

project(sublime-wolframlanguage)

set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})
include(WolframKernel)

set(WOLFRAMKERNEL ${WOLFRAMKERNEL_DEFAULT} CACHE FILEPATH "Path to WolframKernel")

message(STATUS "WOLFRAMKERNEL: ${WOLFRAMKERNEL}")

set(STATIC_PACKAGE_SOURCES
  ${PROJECT_SOURCE_DIR}/sublime/Main.sublime-menu
  ${PROJECT_SOURCE_DIR}/sublime/plugin.py
  ${PROJECT_SOURCE_DIR}/sublime/syntax_test_wolfram_language.wl
  ${PROJECT_SOURCE_DIR}/sublime/WolframLanguage.sublime-color-scheme
  ${PROJECT_SOURCE_DIR}/sublime/WolframLanguage.sublime-settings
)

set(SYNTAX_TEMPLATE_SOURCE
  ${PROJECT_SOURCE_DIR}/sublime/WolframLanguage.sublime-syntax.template
)

set(COMPLETIONS_TEMPLATE_SOURCE
  ${PROJECT_SOURCE_DIR}/sublime/WolframLanguage.sublime-completions.template
)

#
# Set VERSION_NUMBER, SYSTEMID
#
CheckWolframKernel()


file(MAKE_DIRECTORY
  ${PROJECT_BINARY_DIR}/package/WolframLanguage
)


#
# Copy source files
#

set(PROCESSED_SYMBOLS_DUMP ${PROJECT_BINARY_DIR}/processedSymbols.mx)

set(COPIED_SYNTAX_TEMPLATE ${PROJECT_BINARY_DIR}/WolframLanguage.sublime-syntax.template)
set(APPLIED_SYNTAX_TEMPLATE ${PROJECT_BINARY_DIR}/package/WolframLanguage/WolframLanguage.sublime-syntax)

set(COPIED_COMPLETIONS_TEMPLATE ${PROJECT_BINARY_DIR}/WolframLanguage.sublime-completions.template)
set(APPLIED_COMPLETIONS_TEMPLATE ${PROJECT_BINARY_DIR}/package/WolframLanguage/WolframLanguage.sublime-completions)

add_custom_command(
  OUTPUT
    ${PROCESSED_SYMBOLS_DUMP}
  COMMAND
    ${CMAKE_COMMAND} -DSCRIPT=${PROJECT_SOURCE_DIR}/SublimeWolframLanguage/Generate/ProcessSymbols.wl -DSRCDIR=${PROJECT_SOURCE_DIR} -DBUILDDIR=${PROJECT_BINARY_DIR} -DWOLFRAMKERNEL=${WOLFRAMKERNEL} -P ${PROJECT_SOURCE_DIR}/cmake/WolframScript.cmake
  DEPENDS
    ${PROJECT_SOURCE_DIR}/SublimeWolframLanguage/Generate/ProcessSymbols.wl
    ${PROJECT_SOURCE_DIR}/cmake/WolframScript.cmake
)

add_custom_command(
  OUTPUT
    ${APPLIED_SYNTAX_TEMPLATE}
    ${APPLIED_COMPLETIONS_TEMPLATE}
  COMMAND
    ${CMAKE_COMMAND} -E copy ${SYNTAX_TEMPLATE_SOURCE} ${COPIED_SYNTAX_TEMPLATE}
  COMMAND
    ${CMAKE_COMMAND} -E copy ${COMPLETIONS_TEMPLATE_SOURCE} ${COPIED_COMPLETIONS_TEMPLATE}
  COMMAND
    ${CMAKE_COMMAND} -DSCRIPT=${PROJECT_SOURCE_DIR}/SublimeWolframLanguage/Generate/ApplyTemplates.wl -DSRCDIR=${PROJECT_SOURCE_DIR} -DBUILDDIR=${PROJECT_BINARY_DIR} -DWOLFRAMKERNEL=${WOLFRAMKERNEL} -P ${PROJECT_SOURCE_DIR}/cmake/WolframScript.cmake
  DEPENDS
    ${SYNTAX_TEMPLATE_SOURCE}
    ${COMPLETIONS_TEMPLATE_SOURCE}
    ${PROJECT_SOURCE_DIR}/SublimeWolframLanguage/Generate/ApplyTemplates.wl
    ${PROJECT_SOURCE_DIR}/cmake/WolframScript.cmake
    ${PROCESSED_SYMBOLS_DUMP}
)

foreach(SRC ${STATIC_PACKAGE_SOURCES})
  get_filename_component(BARE_SRC ${SRC} NAME)
  add_custom_command(
    OUTPUT
      ${PROJECT_BINARY_DIR}/package/WolframLanguage/${BARE_SRC}
    COMMAND
      ${CMAKE_COMMAND} -E copy ${SRC} ${PROJECT_BINARY_DIR}/package/WolframLanguage/${BARE_SRC}
    DEPENDS
      ${SRC}
  )
  list(APPEND COPIED_PACKAGE_SOURCES ${PROJECT_BINARY_DIR}/package/WolframLanguage/${BARE_SRC})
endforeach()





#
# platform settings files
#
# The spaces and parentheses in the file names screw-up simple copying
#

add_custom_command(
  OUTPUT
    ${PROJECT_BINARY_DIR}/package/WolframLanguage/WolframLanguage\ \(Linux\).sublime-settings
  COMMAND
    ${CMAKE_COMMAND} -E copy ${PROJECT_SOURCE_DIR}/sublime/WolframLanguage\ \\\(Linux\\\).sublime-settings ${PROJECT_BINARY_DIR}/package/WolframLanguage/WolframLanguage\ \\\(Linux\\\).sublime-settings
  DEPENDS
    ${PROJECT_SOURCE_DIR}/sublime/WolframLanguage\ \(Linux\).sublime-settings
)
list(APPEND COPIED_PACKAGE_SOURCES ${PROJECT_BINARY_DIR}/package/WolframLanguage/WolframLanguage\ \(Linux\).sublime-settings)

add_custom_command(
  OUTPUT
    ${PROJECT_BINARY_DIR}/package/WolframLanguage/WolframLanguage\ \(OSX\).sublime-settings
  COMMAND
    ${CMAKE_COMMAND} -E copy ${PROJECT_SOURCE_DIR}/sublime/WolframLanguage\ \\\(OSX\\\).sublime-settings ${PROJECT_BINARY_DIR}/package/WolframLanguage/WolframLanguage\ \\\(OSX\\\).sublime-settings
  DEPENDS
    ${PROJECT_SOURCE_DIR}/sublime/WolframLanguage\ \(OSX\).sublime-settings
)
list(APPEND COPIED_PACKAGE_SOURCES ${PROJECT_BINARY_DIR}/package/WolframLanguage/WolframLanguage\ \(OSX\).sublime-settings)

add_custom_command(
  OUTPUT
    ${PROJECT_BINARY_DIR}/package/WolframLanguage/WolframLanguage\ \(Windows\).sublime-settings
  COMMAND
    ${CMAKE_COMMAND} -E copy ${PROJECT_SOURCE_DIR}/sublime/WolframLanguage\ \\\(Windows\\\).sublime-settings ${PROJECT_BINARY_DIR}/package/WolframLanguage/WolframLanguage\ \\\(Windows\\\).sublime-settings
  DEPENDS
    ${PROJECT_SOURCE_DIR}/sublime/WolframLanguage\ \(Windows\).sublime-settings
)
list(APPEND COPIED_PACKAGE_SOURCES ${PROJECT_BINARY_DIR}/package/WolframLanguage/WolframLanguage\ \(Windows\).sublime-settings)







#
# package target
#

set(PACKAGE_SOURCES
  ${COPIED_PACKAGE_SOURCES}
  ${APPLIED_SYNTAX_TEMPLATE}
  ${APPLIED_COMPLETIONS_TEMPLATE}
)

add_custom_target(package
  DEPENDS ${PACKAGE_SOURCES}
)
