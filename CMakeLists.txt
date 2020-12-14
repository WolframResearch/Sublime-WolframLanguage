
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
	DEPENDS
		${PACKAGE_SOURCES}
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
	VERBATIM
	WORKING_DIRECTORY
		${PROJECT_BINARY_DIR}/package/WolframLanguage
)

if(EXISTS ${PACKAGE_INSTALL_DIR})
install(
	FILES
		${PACKAGE_OUTPUT}
	DESTINATION
		${PACKAGE_INSTALL_DIR}
)
else()
message(STATUS "PACKAGE_INSTALL_DIR does not exist; skipping install: ${PACKAGE_INSTALL_DIR}")
endif()
