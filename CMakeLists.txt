
#
# Require CMake 3.11 to allow "package" target
#
# Related policies: https://cmake.org/cmake/help/v3.11/policy/CMP0037.html
#
#
# https://cmake.org/cmake/help/latest/release/3.15.html
# The cmake(1) command gained a new --install option. This may be used after building a project to run installation without using the generated build system or the native build tool.
#
cmake_minimum_required(VERSION 3.15)

project(sublime-wolframlanguage
	LANGUAGES
		NONE
)

message(STATUS "CMAKE_VERSION: ${CMAKE_VERSION}")
message(STATUS "PACKAGE_INSTALL_DIR: ${PACKAGE_INSTALL_DIR}")

if(DEFINED PACKAGE_INSTALL_DIR)
if(NOT EXISTS ${PACKAGE_INSTALL_DIR})
message(FATAL_ERROR "PACKAGE_INSTALL_DIR is defined but does not exist: ${PACKAGE_INSTALL_DIR}")
endif()
endif()

set(STATIC_PACKAGE_SOURCES
	#
	# why still use the older-style .tmPreferences?
	# https://forum.sublimetext.com/t/toggle-comment-with-a-custom-sublime-syntax/18789
	#
	${PROJECT_SOURCE_DIR}/sublime/messages/install.txt
	${PROJECT_SOURCE_DIR}/sublime/Comments.tmPreferences
	${PROJECT_SOURCE_DIR}/sublime/Context.sublime-menu
	${PROJECT_SOURCE_DIR}/sublime/Default.sublime-commands
	${PROJECT_SOURCE_DIR}/sublime/Main.sublime-menu
	${PROJECT_SOURCE_DIR}/sublime/messages.json
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

#
# static package sources
#
foreach(SRC ${STATIC_PACKAGE_SOURCES})
	file(RELATIVE_PATH REL ${PROJECT_SOURCE_DIR}/sublime/ ${SRC})
	add_custom_command(
		OUTPUT
			${PROJECT_BINARY_DIR}/package/WolframLanguage/${REL}
		COMMAND
			${CMAKE_COMMAND} -E copy ${SRC} ${PROJECT_BINARY_DIR}/package/WolframLanguage/${REL}
		DEPENDS
			${SRC}
		VERBATIM
	)
	list(APPEND COPIED_PACKAGE_SOURCES ${PROJECT_BINARY_DIR}/package/WolframLanguage/${REL})
endforeach()



set(PACKAGE_SOURCES
	${COPIED_PACKAGE_SOURCES}
)

set(PACKAGE_OUTPUT ${PROJECT_BINARY_DIR}/package/WolframLanguage.sublime-package)


#
# package target
#

add_custom_target(package
	DEPENDS
		${PACKAGE_OUTPUT}
)

foreach(SRC ${PACKAGE_SOURCES})
	file(RELATIVE_PATH REL ${PROJECT_BINARY_DIR}/package/WolframLanguage ${SRC})
	list(APPEND PACKAGE_REL_SOURCES ${REL})
endforeach()

add_custom_command(
	OUTPUT
		${PACKAGE_OUTPUT}
	COMMAND
		#
		# .sublime-package files are just .zip files
		#
		# approximately around here:
		# https://github.com/wbond/package_control/blob/master/package_control/package_manager.py#L927
		#
		# is where the zipping happens
		#
		${CMAKE_COMMAND} -E tar cf ${PACKAGE_OUTPUT} --format=zip ${PACKAGE_REL_SOURCES}
	DEPENDS
		${PACKAGE_SOURCES}
	VERBATIM
	WORKING_DIRECTORY
		${PROJECT_BINARY_DIR}/package/WolframLanguage
)

if(DEFINED PACKAGE_INSTALL_DIR)
install(
	FILES
		${PACKAGE_OUTPUT}
	DESTINATION
		${PACKAGE_INSTALL_DIR}
)
endif()
