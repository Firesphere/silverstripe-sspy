# SSPY - Python Stand-alone SSPAK solution
##### &copy; Simon `Firesphere` Erkelens; Moss `Mossman` Cantwell

## Usage:

      sspy [create|load|extract] (db|assets) --file=my.sspak --db=mydb.tar.gz --assets=myassets.tar.gz --webroot=relative/path/to/webroot
          
the db and assets commands are optional.

This script should preferably be run from the webroot of the site

### Arguments:

    create
           db     Only create a database snapshot
           assets Only create an assets snapshot
           none   Create a full snapshot
    load
           No arguments required, it detects if there is a database or assets
           Warning: No backup of database or assets will be created!
    extract
           No arguments required. The SSPAK file will be extracted in to database.sql.gz and assets.tar.gz
### Parameters

    --file=|-f 
                 Required, path to the sspak. E.g. --file=my.sspak or -f my.sspak
                 (note, no = sign for the shorthand!
    --db=|-d 
                 Optional, path to existing database file, e.g. --db=mydatabase.sql.gz or -d mydatabase.sql.gz to create the sspak from existing sources
                 (note, no = sign for the shorthand!
    --assets=|-a 
                 Optional, path to existing assets file, e.g. --assets=myassets.tar.gz or -a myassets.tar.gz to create the sspak from existing sources
                 (note, no = sign for the shorthand!

----------
    --webroot=|-w 
                  Optional, relative path from the current location to the webroot

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

|Argument |Description                                             |Default|Required|
|---------|--------------------------------------------------------|-------|--------|
|--file   |The file to read or write                               |None   |Yes     |
|--db     |Path to the database sql.gz file to create from existing|None   |No      |
|--assets |Path to the assets tar.gz file to create from existing  |None   |No      |
|--webroot|Relative path to the webroot from the current location  |.      |No      |



Shorthands are available, instead of `--file` you can use `-f`, instead of `--db` you can use `-d` and instead of `--assets` you can use `-a` and instead of `--webroot` you can use `-w`

Note that using shorthand commands, it should be `-f myfile.sspak` instead of `--file=myfile.sspak`

The db and assets arguments are optional. If omitted, the actual database and assets folder will be used.

The file name can be anything, but will be appended with `.sspak` if the file name does not have the correct extension.

**CAUTION**
Not providing a unique file name, might cause a single sspak to be loaded with the same files over and over, appending data to them instead of replacing!

# Attributions

- João Magalhães - The original MySQL Dump library which has been altered to fit our needs and have a bit more flexibility overall
- The pymysql project
- The DotEnv project

# License

This module is published under BSD 3-clause license

http://www.opensource.org/licenses/BSD-3-Clause

Copyright &copy 2019-NOW(), Simon `Firesphere` Erkelens; Moss `Mossman` Cantwell

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


## Did you read this entire readme? 

You rock!

# Pictured below is a cow, just for you.
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