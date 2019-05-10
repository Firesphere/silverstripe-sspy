# SSPY - Python Stand-alone SSPAK solution

## Usage:

`sspy [create|load] (db|assets) --file=mysspak.sspak (--db=path/to/my/db.sql.gz --assets=path/to/my/assets.tar.gz`

## Options

|Option|Description           |
|------|----------------------|
|create|Create a new sspak    |
|load  |Load an existing sspak|

### Optional options

|Sub option|Description  |
|----------|-------------|
|db        |Database only|
|assets    |Assets only  |

### Arguments

|Argument|Description                     |
|--------|--------------------------------|
|--file  |The file to read or write       |
|--db    |Path to the database sql.gz file|
|--assets|Path to the assets tar.gz file  |


Shorthands are available, instead of `--file` you can use `-f`, instead of `--db` you can use `-d` and instead of `--assets` you can use `-a`

The db and assets arguments are optional. If omitted, the actual database and assets folder will be used.

The filename can be anything, but will be appended with `.sspak` if the file name does not have the correct extension.

If no filename is provided, the default filename `package.sspak` will be used.

**CAUTION**
Not providing a file name, might cause a single sspak to be loaded with the same files over and over, appending data to them instead of replacing!

# Attributions

João Magalhães - The original MySQL Dump library which has been altered to fit our needs and have a bit more flexibility
The pymysql project
The DotEnv project


# License

This module is published under BSD 3-clause license

http://www.opensource.org/licenses/BSD-3-Clause

Copyright (c) 2019-NOW(), Simon "Firesphere" Erkelens

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


# Did you read this entire readme? You rock!

Pictured below is a cow, just for you.
```

               /( ,,,,, )\
              _\,;;;;;;;,/_
           .-"; ;;;;;;;;; ;"-.
           '.__/`_ / \ _`\__.'
              | (')| |(') |
              | .--' '--. |
              |/ o     o \|
              |           |
             / \ _..=.._ / \
            /:. '._____.'   \
           ;::'    / \      .;
           |     _|_ _|_   ::|
         .-|     '==o=='    '|-.
        /  |  . /       \    |  \
        |  | ::|         |   | .|
        |  (  ')         (.  )::|
        |: |   |;  U U  ;|:: | `|
        |' |   | \ U U / |'  |  |
        ##V|   |_/`"""`\_|   |V##
           ##V##         ##V##
```

# And a monkey!
```
_______AAAA_______________AAAA________
       VVVV               VVVV        
       (__)               (__)
        \ \               / /
         \ \   \\|||//   / /
          > \   _   _   / <
           > \ / \ / \ / <
            > \\_o_o_// <
             > ( (_) ) <
              >|     |<
             / |\___/| \
             / (_____) \
             /         \
              /   o   \
               ) ___ (   
              / /   \ \  
             ( /     \ )
             ><       ><
            ///\     /\\\
            '''       '''
```