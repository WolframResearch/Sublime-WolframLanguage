
#
# Require CMake 3.11 to allow "package" target
#
# Related policies: https://cmake.org/cmake/help/v3.11/policy/CMP0037.html
#
cmake_minimum_required(VERSION 3.11)

project(sublime-wolframlanguage
	LANGUAGES
		NONE
)

set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})
include(WolframKernel)
include(PacletInfo)

#
# Used for quickly reporting syntax errors in WL source files
#
find_program(CODEPARSER_EXE
	NAMES
		codeparser codeparser.exe
	HINTS
		${CODEPARSER_EXE_DIR}
)

set(PACLET "SublimeWolframLanguage")
set(WOLFRAMKERNEL ${WOLFRAMKERNEL_DEFAULT} CACHE FILEPATH "Path to WolframKernel")
set(LOCAL_BUILD OFF CACHE BOOL "Local build")
# Work-around for bug 349779 is to pause ~1 second
set(BUG349779_PAUSE 1 CACHE STRING "Bug 349779 pause")
#
# Evidence suggests that when bug 349779 strikes, the kernel does exit after 30 minutes
# So double that and cross fingers.
#
# Related bugs: 349779
# Related issues: RE-514227
#
set(BUG349779_TIMEOUT 3600 CACHE STRING "Bug 349779 timeout")

message(STATUS "CMAKE_VERSION: ${CMAKE_VERSION}")
message(STATUS "PACLET: ${PACLET}")
message(STATUS "WOLFRAMKERNEL: ${WOLFRAMKERNEL}")
message(STATUS "LOCAL_BUILD: ${LOCAL_BUILD}")
message(STATUS "CMAKE_SIZEOF_VOID_P: ${CMAKE_SIZEOF_VOID_P}")
message(STATUS "BUG349779_PAUSE: ${BUG349779_PAUSE}")
message(STATUS "BUG349779_TIMEOUT: ${BUG349779_TIMEOUT}")
message(STATUS "CODEPARSER_EXE: ${CODEPARSER_EXE}")

set(STATIC_PACKAGE_SOURCES
	#
	# why still use the older-style .tmPreferences?
	# https://forum.sublimetext.com/t/toggle-comment-with-a-custom-sublime-syntax/18789
	#
	${PROJECT_SOURCE_DIR}/sublime/Comments.tmPreferences
	${PROJECT_SOURCE_DIR}/sublime/Context.sublime-menu
	${PROJECT_SOURCE_DIR}/sublime/Default.sublime-commands
	${PROJECT_SOURCE_DIR}/sublime/Main.sublime-menu
	${PROJECT_SOURCE_DIR}/sublime/plugin.py
	${PROJECT_SOURCE_DIR}/sublime/SymbolListConstants.tmPreferences
	${PROJECT_SOURCE_DIR}/sublime/syntax_test_wolfram_language.wl
	${PROJECT_SOURCE_DIR}/sublime/WolframLanguage.sublime-color-scheme
	${PROJECT_SOURCE_DIR}/sublime/WolframLanguage\ \(Linux\).sublime-settings
	${PROJECT_SOURCE_DIR}/sublime/WolframLanguage\ \(OSX\).sublime-settings
	${PROJECT_SOURCE_DIR}/sublime/WolframLanguage\ \(Windows\).sublime-settings
	${PROJECT_SOURCE_DIR}/sublime/WolframLanguage.sublime-settings
)

set(PROCESSED_SYMBOLS_DUMP ${PROJECT_BINARY_DIR}/processedSymbols.mx)

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

set(COPIED_PACLETINFO ${PROJECT_BINARY_DIR}/paclet/${PACLET}/PacletInfo.m)

set(COPIED_SYNTAX_TEMPLATE ${PROJECT_BINARY_DIR}/WolframLanguage.sublime-syntax.template)
set(APPLIED_SYNTAX_TEMPLATE ${PROJECT_BINARY_DIR}/package/WolframLanguage/WolframLanguage.sublime-syntax)

set(COPIED_COMPLETIONS_TEMPLATE ${PROJECT_BINARY_DIR}/WolframLanguage.sublime-completions.template)
set(APPLIED_COMPLETIONS_TEMPLATE ${PROJECT_BINARY_DIR}/package/WolframLanguage/WolframLanguage.sublime-completions)

add_custom_command(
	OUTPUT
		${COPIED_PACLETINFO}
	COMMAND
		${CMAKE_COMMAND} -DSRC=${PACLETINFO_SOURCE} -DCODEPARSER_EXE=${CODEPARSER_EXE} -DWOLFRAMKERNEL=${WOLFRAMKERNEL} -DBUG349779_TIMEOUT=${BUG349779_TIMEOUT} -P ${PROJECT_SOURCE_DIR}/cmake/InspectFile.cmake
	COMMAND
		${CMAKE_COMMAND} -E copy ${PACLETINFO_SOURCE} ${COPIED_PACLETINFO}
	COMMAND
		${CMAKE_COMMAND} -DLOCAL_BUILD=${LOCAL_BUILD} -DLOCAL_BUILD_VERSION=${LOCAL_BUILD_VERSION} -DCOPIED_PACLETINFO=${COPIED_PACLETINFO} -P ${PROJECT_SOURCE_DIR}/cmake/ReplacePacletInfo.cmake
	DEPENDS
		${PACLETINFO_SOURCE}
		${PROJECT_SOURCE_DIR}/cmake/InspectFile.cmake
		${PROJECT_SOURCE_DIR}/cmake/ReplacePacletInfo.cmake
)
list(APPEND COPIED_WL_PACLET_SOURCES ${COPIED_PACLETINFO})

foreach(SRC ${STATIC_PACKAGE_SOURCES})
	get_filename_component(BARE_SRC ${SRC} NAME)
	add_custom_command(
		OUTPUT
			${PROJECT_BINARY_DIR}/package/WolframLanguage/${BARE_SRC}
		COMMAND
			${CMAKE_COMMAND} -E copy ${SRC} ${PROJECT_BINARY_DIR}/package/WolframLanguage/${BARE_SRC}
		DEPENDS
			${SRC}
		VERBATIM
	)
	list(APPEND COPIED_PACKAGE_SOURCES ${PROJECT_BINARY_DIR}/package/WolframLanguage/${BARE_SRC})
endforeach()


add_custom_command(
	OUTPUT
		${PROCESSED_SYMBOLS_DUMP}
	COMMAND
		${CMAKE_COMMAND} -DSCRIPT=${PROJECT_SOURCE_DIR}/SublimeWolframLanguage/Generate/ProcessSymbols.wl -DSRCDIR=${PROJECT_SOURCE_DIR} -DBUILDDIR=${PROJECT_BINARY_DIR} -DWOLFRAMKERNEL=${WOLFRAMKERNEL} -DBUG349779_TIMEOUT=${BUG349779_TIMEOUT} -P ${PROJECT_SOURCE_DIR}/cmake/WolframScript.cmake
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
		${CMAKE_COMMAND} -DSCRIPT=${PROJECT_SOURCE_DIR}/SublimeWolframLanguage/Generate/ApplyTemplates.wl -DSRCDIR=${PROJECT_SOURCE_DIR} -DBUILDDIR=${PROJECT_BINARY_DIR} -DWOLFRAMKERNEL=${WOLFRAMKERNEL} -DBUG349779_TIMEOUT=${BUG349779_TIMEOUT} -P ${PROJECT_SOURCE_DIR}/cmake/WolframScript.cmake
	DEPENDS
		${SYNTAX_TEMPLATE_SOURCE}
		${COMPLETIONS_TEMPLATE_SOURCE}
		${PROJECT_SOURCE_DIR}/SublimeWolframLanguage/Generate/ApplyTemplates.wl
		${PROJECT_SOURCE_DIR}/cmake/WolframScript.cmake
		${PROCESSED_SYMBOLS_DUMP}
)







set(PACLET_SOURCES
	${COPIED_WL_PACLET_SOURCES}
	${WL_GENERATE_CREATEPACLETARCHIVE_SOURCES}
)

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
# paclet target
#

if(LOCAL_BUILD)
set(PACLET_OUTPUT ${PROJECT_BINARY_DIR}/paclet/${PACLET}-${LOCAL_BUILD_VERSION}.paclet)
else(LOCAL_BUILD)
set(PACLET_OUTPUT ${PROJECT_BINARY_DIR}/paclet/${PACLET}-${PACLET_VERSION}.paclet)
endif(LOCAL_BUILD)

add_custom_target(paclet
	DEPENDS
		${PACLET_OUTPUT}
)

#
# Create the paclet archive
#
add_custom_command(
	OUTPUT
		${PACLET_OUTPUT}
	DEPENDS
		${PACLET_SOURCES}
		${PROJECT_SOURCE_DIR}/${PACLET}/Generate/CreatePacletArchive.wl
		${PROJECT_SOURCE_DIR}/cmake/WolframScript.cmake
	COMMAND
		${CMAKE_COMMAND} -DSCRIPT=${PROJECT_SOURCE_DIR}/${PACLET}/Generate/CreatePacletArchive.wl -DSRCDIR=${PROJECT_SOURCE_DIR} -DBUILDDIR=${PROJECT_BINARY_DIR} -DPACLET=${PACLET} -DWOLFRAMKERNEL=${WOLFRAMKERNEL} -DBUG349779_TIMEOUT=${BUG349779_TIMEOUT} -P ${PROJECT_SOURCE_DIR}/cmake/WolframScript.cmake
	VERBATIM
	WORKING_DIRECTORY
		${PROJECT_SOURCE_DIR}
)
