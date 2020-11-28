# tef - The Enumeration Framework
tef is an enumeration framework written in Python3, designed to ease the process of creating python scripts that parse networked resources. This project was heavily inspired by HD Moore's metasploit framework, so users of the metasploit framework should be familiar with much of the syntax. This project was started as a way to learn Python, and is very much a forever work in progress. Bug reports and contributions are much appreciated.


# Project Features

Features of this project include:
* Easily enumerate targets using various modules
* Database to save module output
* Multiple workspace support
* Built-in multithreading
* Easily create custom modules using template


# How to use tef
## tef.py
tef.py is the main script to run, which is located in the root of the repository. This script will function from any directory, so it will work regardless of which directory it is installed in, or what the current directory is when the script is run. Because many data structures in tef use python dictionaries, it will be common to use the terminology 'key' and 'value' to describe items or fields and their values.

The general workflow of tef is to locate a helpful module using the 'search' command, active the module with the 'use' command, set the options (i.e. variables) of the module using the 'set' command, and finally running the module with the 'run' command. Below is a more detailed usage of the most common tef commands, for a more brief description, use the 'help' command in the tef console.

**search** - The search command can be used for finding modules based on keywords. Running the 'search' command by itself will list basic syntax of the command as well as every module available. Running 'search' followed by any number of terms will search all values in the module's info dictionary for any of the terms. Specific keys can be searched for using key:term. For example, to find all modules with the text ftp in the module description, use the command 'search description:ftp'.

**use** - The use command can be used to set a module as the current module. Use can either be to select a module by name, such as 'use scanner.ftp_anon', or using the index value of the previously used search, such as 'use 1'.

**options** - Once a module has been selected, the 'options' command can be used to display a list of options available for the module. Common options for modules include host and port, which let the user target which remote IP address and port to run the module against. Module authors can include a short description for each option.

**set** - In order to assign a value to an option, the 'set' command must be used. The syntax for the set command is 'set option value' where option is the option name, and value is the user-defined value for the option. Note that even if modules have a similar option between them, such as host, the option will need to be set again if the module is changed with the use command. To keep the option value persistent, use the 'setg' command.

**unset** - Unset can be used to set the value of the option to the module default value. The syntax for the unset command is 'unset option'.

**setg** - Similar in functionality and syntax to the 'set' command, the only difference is that the option value will persist when changing modules. 

**unsetg** - Similar in functionality and syntax to the 'unset' command, except that it unsets the value of a global option value.

## Creating Modules
Modules are located within the modules directory of the repository. tef will recursively locate and load all .py files within the modules directory. A template module located in the root of modules can be used as a guide when creating a tef module. tef modules require three functions, info(), options(), and run().

**info()** - General module information that will be used for info and search commands, the information dictionary key and value must be a string. Arbitrary keys can be created to be used as tags when searching.

**options()** - Variables you want to use in your module, the options dictionary value must be a list containing [default value, option description]. The only required option is host. At this time only the host, port, timeout, and theads values are validated in tef.py, all other options must be validated in the run() function.

**run()** - The main code block that will be executed when the run command is used.

tef itself can optionally be imported into the module to utilitze some helper functions such as minus(), plus(), write_creds(), and write_database(). Some examples can be found in template.py

## Workspaces
tef allows modules the ability to save data such as hosts, ports, module output, and discovered credentials to a database. These database files are called workspaces in tef, and multiple workspaces can be created to keep module results seperate. Workspace files are saved in the .tef directory in the user's home directory.

There are currently two tables in the workspace database, creds and module_data. The creds table will be populated with any modules that save credential data to the database using the write_creds() function. Likewise, the module_data table will be populated with any modules that save credential data to the database using the write_database() function. Information in the two tables can be queried using the 'creds' and 'db' commands respectively. See 'help creds' and 'help db' for more syntax options.


## Prerequisites
Ensure you have the following installed:

* Python3
* pip3


## Installation

How to install tef:

```shell
$ git clone https://github.com/morepoints/tef && cd tef
$ chmod +x install.sh
$ ./install.sh
```

These commands will simply clone the tef repository and run the install.sh script, which installs the necessary python library dependancies.

### Contributing
As I am currently learning git as well as python, any fixes/changes/suggestions or new modules are always welcome.

For a guide on how to contribute to the project see https://www.dataschool.io/how-to-contribute-on-github/. 


### Licensing
This project is licensed under the GNU GPLv3 license. See LICENSE for full licensing details.