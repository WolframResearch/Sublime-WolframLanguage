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

Specify `MATHEMATICA_INSTALL_DIR` if you have Mathematica installed in a non-default location:

```
cmake -DMATHEMATICA_INSTALL_DIR=/Applications/Mathematica122.app/Contents/ ..
cmake --build .
```

On Windows:

```
cmake -DMATHEMATICA_INSTALL_DIR="C:/Program Files/Wolfram Research/Mathematica/12.2" ..
cmake --build .
```

## Installing

You can install the package from CMake:
```
cmake --install .
```
