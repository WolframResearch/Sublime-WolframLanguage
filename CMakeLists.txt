
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
if(DEFINED PACKAGE_INSTALL_DIR)
message(STATUS "PACKAGE_INSTALL_DIR: ${PACKAGE_INSTALL_DIR}")
else()
message(STATUS "PACKAGE_INSTALL_DIR: NOT DEFINED")
endif()

if(DEFINED PACKAGE_INSTALL_DIR)
if(NOT EXISTS ${PACKAGE_INSTALL_DIR})
message(FATAL_ERROR "PACKAGE_INSTALL_DIR is defined but does not exist: ${PACKAGE_INSTALL_DIR}")
endif()
endif()

set(STATIC_PACKAGE_SOURCES
	${PROJECT_SOURCE_DIR}/plugin/open.py
	#
	# why still use the older-style .tmPreferences?
	# https://forum.sublimetext.com/t/toggle-comment-with-a-custom-sublime-syntax/18789
	#
	${PROJECT_SOURCE_DIR}/Comments.tmPreferences
	${PROJECT_SOURCE_DIR}/Context.py
	${PROJECT_SOURCE_DIR}/Context.sublime-menu
	${PROJECT_SOURCE_DIR}/Default.sublime-commands
	${PROJECT_SOURCE_DIR}/Main.sublime-menu
	#
	# Do not include messages.json (or messages dir)
	#
	# ${PROJECT_SOURCE_DIR}/messages.json
	${PROJECT_SOURCE_DIR}/plugin.py
	${PROJECT_SOURCE_DIR}/SideBar.py
	${PROJECT_SOURCE_DIR}/Side\ Bar.sublime-menu
	${PROJECT_SOURCE_DIR}/SymbolListConstants.tmPreferences
	#
	# Do not include syntax tests
	#
	#${PROJECT_SOURCE_DIR}/syntax_test_wolfram_language.wl
	${PROJECT_SOURCE_DIR}/WolframLanguage.sublime-color-scheme
	${PROJECT_SOURCE_DIR}/WolframLanguage.sublime-completions
	${PROJECT_SOURCE_DIR}/WolframLanguage.sublime-settings
	${PROJECT_SOURCE_DIR}/WolframLanguage.sublime-syntax
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
	file(RELATIVE_PATH REL ${PROJECT_SOURCE_DIR}/ ${SRC})
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
	ALL
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
		# this line:
		# package_file = zipfile.ZipFile(package_path, "w", compression=zipfile.ZIP_DEFLATED)
		# approximately around here:
		# https://github.com/wbond/package_control/blob/master/package_control/package_manager.py#L929
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
	COMPONENT
		package
)
endif()
