
cmake_minimum_required(VERSION 3.0)

project(sublime-wolframlanguage)

set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})
include(WolframKernel)
include(PacletInfo)

set(PACLET "SublimeWolframLanguage")
set(WOLFRAMKERNEL ${WOLFRAMKERNEL_DEFAULT} CACHE FILEPATH "Path to WolframKernel")
set(BUILD_DOCS OFF CACHE BOOL "Build documentation")
set(LOCAL_BUILD OFF CACHE BOOL "Local build")

message(STATUS "PACLET: ${PACLET}")
message(STATUS "WOLFRAMKERNEL: ${WOLFRAMKERNEL}")
message(STATUS "BUILD_DOCS: ${BUILD_DOCS}")
message(STATUS "LOCAL_BUILD: ${LOCAL_BUILD}")

set(STATIC_PACKAGE_SOURCES
  #
  # why still use the older-style .tmPreferences?
  # https://forum.sublimetext.com/t/toggle-comment-with-a-custom-sublime-syntax/18789
  #
  ${PROJECT_SOURCE_DIR}/sublime/Comments.tmPreferences
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

set(WL_GENERATE_CREATEPACLETARCHIVE_SOURCES
  ${PROJECT_SOURCE_DIR}/${PACLET}/Generate/CreatePacletArchive.wl
)

set(PACLETINFO_SOURCE
  ${PROJECT_SOURCE_DIR}/${PACLET}/PacletInfo.m
)

set(DOCUMENTATION_NOTEBOOK_PATHS
  English/Guides/SublimeWolframLanguage.nb
  English/Tutorials/ReleaseNotes.nb
  English/Tutorials/SublimeWolframLanguageManual.nb

)

#
# Setup documentation notebook paths
#
foreach(NB_PATH ${DOCUMENTATION_NOTEBOOK_PATHS})
  set(SRC ${PROJECT_SOURCE_DIR}/${PACLET}/Documentation/${NB_PATH})
  set(BUILT ${PROJECT_BINARY_DIR}/paclet/${PACLET}/Documentation/${NB_PATH})
  list(APPEND DOCUMENTATION_SOURCE ${SRC})
  list(APPEND BUILT_DOCUMENTATION ${BUILT})
endforeach()

#
# Set VERSION_NUMBER, SYSTEMID
#
CheckWolframKernel()
CheckPacletInfo()


file(MAKE_DIRECTORY
  ${PROJECT_BINARY_DIR}/package/WolframLanguage
)
file(MAKE_DIRECTORY
  ${PROJECT_BINARY_DIR}/paclet/${PACLET}
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





set(COPIED_PACLETINFO ${PROJECT_BINARY_DIR}/paclet/${PACLET}/PacletInfo.m)

add_custom_command(
  OUTPUT
    ${COPIED_PACLETINFO}
  COMMAND
    ${CMAKE_COMMAND} -E copy ${PROJECT_SOURCE_DIR}/${PACLET}/PacletInfo.m ${COPIED_PACLETINFO}
  COMMAND
    ${CMAKE_COMMAND} -DLOCAL_BUILD=${LOCAL_BUILD} -DCOPIED_PACLETINFO=${COPIED_PACLETINFO} -P ${PROJECT_SOURCE_DIR}/cmake/ReplacePacletInfo.cmake
  DEPENDS
    ${PROJECT_SOURCE_DIR}/${PACLET}/PacletInfo.m
    ${PROJECT_SOURCE_DIR}/cmake/ReplacePacletInfo.cmake
)
list(APPEND COPIED_WL_PACLET_SOURCES ${PROJECT_BINARY_DIR}/paclet/${PACLET}/PacletInfo.m)

set(PACLET_SOURCES
  ${COPIED_WL_PACLET_SOURCES}
  ${WL_GENERATE_CREATEPACLETARCHIVE_SOURCES}
)

if(BUILD_DOCS)

list(APPEND PACLET_SOURCES
  ${BUILT_DOCUMENTATION}
)

endif(BUILD_DOCS)










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







#
# docs target
#

if(BUILD_DOCS)

add_custom_target(docs
  DEPENDS
    ${BUILT_DOCUMENTATION}
)

set(DOCS_APPPATH /Applications/Eclipse.app/Contents/Eclipse/configuration/org.eclipse.osgi/525/0/.cp/MathematicaSource/ CACHE PATH "Path of MathematicaSource inside Workbench installation")

message(STATUS "DOCS_APPPATH: ${DOCS_APPPATH}")

if (NOT IS_DIRECTORY ${DOCS_APPPATH})
message(FATAL_ERROR "DOCS_APPPATH (${DOCS_APPPATH}) does not exist")
endif(NOT IS_DIRECTORY ${DOCS_APPPATH})

set(DOCS_JLINKPATH /Applications/Mathematica.app/Contents/SystemFiles/Links/JLink/ CACHE PATH "Path of JLink")

message(STATUS "DOCS_JLINKPATH: ${DOCS_JLINKPATH}")

if (NOT IS_DIRECTORY ${DOCS_JLINKPATH})
message(FATAL_ERROR "DOCS_JLINKPATH (${DOCS_JLINKPATH}) does not exist")
endif(NOT IS_DIRECTORY ${DOCS_JLINKPATH})


#
# build the docs
#
add_custom_command(
  OUTPUT
    ${BUILT_DOCUMENTATION}
  DEPENDS
    ${DOCUMENTATION_SOURCE}
  COMMAND
    ant -DmathExe=${WOLFRAMKERNEL} -DappPath=${DOCS_APPPATH} -Djlinkpath=${DOCS_JLINKPATH} -DinputDir=${PROJECT_SOURCE_DIR}/${PACLET}/Documentation/ -DoutputDir=${PROJECT_BINARY_DIR}/paclet/${PACLET}/Documentation/ -file ${DOCS_APPPATH}/DocumentationBuild/SystemFiles/ant/Build/notebook.xml
  WORKING_DIRECTORY
    ${PROJECT_SOURCE_DIR}
)

endif(BUILD_DOCS)






#
# paclet target
#
add_custom_target(paclet
  DEPENDS ${PROJECT_BINARY_DIR}/paclet/${PACLET}-${PACLET_VERSION}.paclet
)

#
# Create the paclet archive
#
add_custom_command(
  OUTPUT
    ${PROJECT_BINARY_DIR}/paclet/${PACLET}-${PACLET_VERSION}.paclet
  DEPENDS
    ${PACLET_SOURCES}
    ${PROJECT_SOURCE_DIR}/${PACLET}/Generate/CreatePacletArchive.wl
    ${PROJECT_SOURCE_DIR}/cmake/WolframScript.cmake
  COMMAND
    ${CMAKE_COMMAND} -DSCRIPT=${PROJECT_SOURCE_DIR}/${PACLET}/Generate/CreatePacletArchive.wl -DSRCDIR=${PROJECT_SOURCE_DIR} -DBUILDDIR=${PROJECT_BINARY_DIR} -DPACLET=${PACLET} -DWOLFRAMKERNEL=${WOLFRAMKERNEL} -P ${PROJECT_SOURCE_DIR}/cmake/WolframScript.cmake
  VERBATIM
  WORKING_DIRECTORY
    ${PROJECT_SOURCE_DIR}
)
