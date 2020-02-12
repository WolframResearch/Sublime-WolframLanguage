
cmake_minimum_required(VERSION 3.0)

project(sublime-wolframlanguage)

set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})
include(WolframKernel)

set(WOLFRAMKERNEL ${WOLFRAMKERNEL_DEFAULT} CACHE FILEPATH "Path to WolframKernel")

message(STATUS "WOLFRAMKERNEL: ${WOLFRAMKERNEL}")

set(STATIC_PACKAGE_SOURCES
  ${CMAKE_SOURCE_DIR}/sublime/Main.sublime-menu
  ${CMAKE_SOURCE_DIR}/sublime/plugin.py
  ${CMAKE_SOURCE_DIR}/sublime/WolframLanguage.sublime-color-scheme
  ${CMAKE_SOURCE_DIR}/sublime/WolframLanguage.sublime-settings
)

set(SYNTAX_TEMPLATE_SOURCE
  ${CMAKE_SOURCE_DIR}/sublime/WolframLanguage.sublime-syntax.template
)

set(COMPLETIONS_TEMPLATE_SOURCE
  ${CMAKE_SOURCE_DIR}/sublime/WolframLanguage.sublime-completions.template
)

set(WL_GENERATE_SOURCES
  ${CMAKE_SOURCE_DIR}/SublimeWolframLanguage/Generate/GenerateSyntax.wl
)

#
# Set VERSION_NUMBER, SYSTEMID
#
CheckWolframKernel()


file(MAKE_DIRECTORY
  ${CMAKE_BINARY_DIR}/package/WolframLanguage
)


#
# Copy source files
#

set(COPIED_SYNTAX_TEMPLATE ${CMAKE_BINARY_DIR}/WolframLanguage.sublime-syntax.template)
set(APPLIED_SYNTAX_TEMPLATE ${CMAKE_BINARY_DIR}/package/WolframLanguage/WolframLanguage.sublime-syntax)

set(COPIED_COMPLETIONS_TEMPLATE ${CMAKE_BINARY_DIR}/WolframLanguage.sublime-completions.template)
set(APPLIED_COMPLETIONS_TEMPLATE ${CMAKE_BINARY_DIR}/package/WolframLanguage/WolframLanguage.sublime-completions)

add_custom_command(
  OUTPUT
    ${APPLIED_SYNTAX_TEMPLATE}
    ${APPLIED_COMPLETIONS_TEMPLATE}
  COMMAND
    ${CMAKE_COMMAND} -E copy ${SYNTAX_TEMPLATE_SOURCE} ${COPIED_SYNTAX_TEMPLATE}
  COMMAND
    ${CMAKE_COMMAND} -E copy ${COMPLETIONS_TEMPLATE_SOURCE} ${COPIED_COMPLETIONS_TEMPLATE}
  COMMAND
    ${CMAKE_COMMAND} -DGENERATESYNTAX_WL_SCRIPT=${CMAKE_SOURCE_DIR}/SublimeWolframLanguage/Generate/GenerateSyntax.wl -DBUILDDIR=${CMAKE_BINARY_DIR} -DWOLFRAMKERNEL=${WOLFRAMKERNEL} -P ${PROJECT_SOURCE_DIR}/cmake/ApplyTemplates.cmake
  DEPENDS
    ${SYNTAX_TEMPLATE_SOURCE}
    ${COMPLETIONS_TEMPLATE_SOURCE}
    ${WL_GENERATE_SOURCES}
)

foreach(SRC ${STATIC_PACKAGE_SOURCES})
  get_filename_component(BARE_SRC ${SRC} NAME)
  add_custom_command(
    OUTPUT
      ${CMAKE_BINARY_DIR}/package/WolframLanguage/${BARE_SRC}
    COMMAND
      ${CMAKE_COMMAND} -E copy ${SRC} ${CMAKE_BINARY_DIR}/package/WolframLanguage/${BARE_SRC}
    DEPENDS
      ${SRC}
  )
  list(APPEND COPIED_PACKAGE_SOURCES ${CMAKE_BINARY_DIR}/package/WolframLanguage/${BARE_SRC})
endforeach()





#
# platform settings files
#
# The spaces and parentheses in the file names screw-up simple copying
#

add_custom_command(
  OUTPUT
    ${CMAKE_BINARY_DIR}/package/WolframLanguage/WolframLanguage\ \(Linux\).sublime-settings
  COMMAND
    ${CMAKE_COMMAND} -E copy ${CMAKE_SOURCE_DIR}/sublime/WolframLanguage\ \\\(Linux\\\).sublime-settings ${CMAKE_BINARY_DIR}/package/WolframLanguage/WolframLanguage\ \\\(Linux\\\).sublime-settings
  DEPENDS
    ${CMAKE_SOURCE_DIR}/sublime/WolframLanguage\ \(Linux\).sublime-settings
)
list(APPEND COPIED_PACKAGE_SOURCES ${CMAKE_BINARY_DIR}/package/WolframLanguage/WolframLanguage\ \(Linux\).sublime-settings)

add_custom_command(
  OUTPUT
    ${CMAKE_BINARY_DIR}/package/WolframLanguage/WolframLanguage\ \(OSX\).sublime-settings
  COMMAND
    ${CMAKE_COMMAND} -E copy ${CMAKE_SOURCE_DIR}/sublime/WolframLanguage\ \\\(OSX\\\).sublime-settings ${CMAKE_BINARY_DIR}/package/WolframLanguage/WolframLanguage\ \\\(OSX\\\).sublime-settings
  DEPENDS
    ${CMAKE_SOURCE_DIR}/sublime/WolframLanguage\ \(OSX\).sublime-settings
)
list(APPEND COPIED_PACKAGE_SOURCES ${CMAKE_BINARY_DIR}/package/WolframLanguage/WolframLanguage\ \(OSX\).sublime-settings)

add_custom_command(
  OUTPUT
    ${CMAKE_BINARY_DIR}/package/WolframLanguage/WolframLanguage\ \(Windows\).sublime-settings
  COMMAND
    ${CMAKE_COMMAND} -E copy ${CMAKE_SOURCE_DIR}/sublime/WolframLanguage\ \\\(Windows\\\).sublime-settings ${CMAKE_BINARY_DIR}/package/WolframLanguage/WolframLanguage\ \\\(Windows\\\).sublime-settings
  DEPENDS
    ${CMAKE_SOURCE_DIR}/sublime/WolframLanguage\ \(Windows\).sublime-settings
)
list(APPEND COPIED_PACKAGE_SOURCES ${CMAKE_BINARY_DIR}/package/WolframLanguage/WolframLanguage\ \(Windows\).sublime-settings)







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
