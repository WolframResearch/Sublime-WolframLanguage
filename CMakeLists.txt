
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

message(STATUS "CMAKE_VERSION: ${CMAKE_VERSION}")

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
	${PROJECT_SOURCE_DIR}/sublime/WolframLanguage.sublime-completions
	${PROJECT_SOURCE_DIR}/sublime/WolframLanguage\ \(Linux\).sublime-settings
	${PROJECT_SOURCE_DIR}/sublime/WolframLanguage\ \(OSX\).sublime-settings
	${PROJECT_SOURCE_DIR}/sublime/WolframLanguage\ \(Windows\).sublime-settings
	${PROJECT_SOURCE_DIR}/sublime/WolframLanguage.sublime-settings
	${PROJECT_SOURCE_DIR}/sublime/WolframLanguage.sublime-syntax
)



file(MAKE_DIRECTORY
	${PROJECT_BINARY_DIR}/package/WolframLanguage
)



#
# Copy source files
#

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



#
# package target
#

set(PACKAGE_SOURCES
	${COPIED_PACKAGE_SOURCES}
)

add_custom_target(package
	DEPENDS
		${PACKAGE_SOURCES}
)



