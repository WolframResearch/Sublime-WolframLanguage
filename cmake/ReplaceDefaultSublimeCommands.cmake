
file(READ ${SOURCE_SUBLIMECOMMANDS} filedata)

if(DEBUG_COMMANDS)

string(REGEX REPLACE "BEGIN_DEBUG" "" filedata ${filedata})
string(REGEX REPLACE "END_DEBUG" "" filedata ${filedata})

else()

string(REGEX REPLACE "BEGIN_DEBUG.*END_DEBUG" "" filedata ${filedata})

endif()

file(WRITE ${GENERATED_SUBLIMECOMMANDS} "${filedata}")
