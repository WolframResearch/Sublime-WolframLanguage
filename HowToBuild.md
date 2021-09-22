# Building

Sublime-WolframLanguage uses CMake to generate build scripts and to build a `.sublime-package` file.

Here is an example transcript using the default make generator to build Sublime-WolframLanguage:
```
cd sublime-wolframlanguage
mkdir build
cd build
cmake ..
cmake --build .
```

The result is a directory named `package` that contains the WolframLanguage Sublime package.

## Installing

Specify the path to your `Installed Packages` directory:
```
cmake -DPACKAGE_INSTALL_DIR="/Users/brenton/Library/Application Support/Sublime Text/Installed Packages" ..
```

You only need to do this step once.

You can install the package from CMake:
```
cmake --install .
```

This copies the built `.sublime-package` file into your `Installed Packages` directory.
