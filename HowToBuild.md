# Building

Sublime-WolframLanguage uses a Wolfram Language kernel to build a `.sublime-package` file.

Sublime-WolframLanguage uses CMake to generate build scripts.

Here is an example transcript using the default make generator to build Sublime-WolframLanguage:
```
cd sublime-wolframlanguage
mkdir build
cd build
cmake ..
cmake --build .
```

The result is a directory named `package` that contains the WolframLanguage Sublime package.

Specify `MATHEMATICA_INSTALL_DIR` if you have Wolfram System installed in a non-default location:
```
cmake -DMATHEMATICA_INSTALL_DIR=/Applications/Mathematica123.app/Contents/ ..
cmake --build .
```

On Windows:
```
cmake -DMATHEMATICA_INSTALL_DIR="C:/Program Files/Wolfram Research/Mathematica/12.3" ..
cmake --build .
```

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
