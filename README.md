# OPCTree - A tool for efficient CLI handling of OPC DA structures

This packaged is made for simplifying working with OPC data from the
Python CLI. It enables easy scan of a nested structure, searching
through all branches, reading value and properties, writing value,
comparing the live values to the saved ones.

The program copies the OPC structure of the server so that the user
can use the OPC dot-notation in the CLI to traverse to the object
the user wants to work on.

## Problems with installation
When this is written, is the latest version of OpenOPC, which is required, not
published on pypi.org, and can't be installed by ``pip install OpenOPC-DA``,
instead you need to download it/build it yourself from
https://github.com/j3mg/openopc or get hold of the wheel elsewhere. The version
number isn't published jet, but it should be higher than the current >1.5.0.
If your OPC-server where you want to install it don't have access to internet
you need to download/build wheels on another machine and transfer it.

## Notation
A OPC "tree" is built upon branches, i.e. data structs and "leaves", i.e.
OPC variables. The branches can have other branches as well as leaves on
them. The branches and the leaves within a struct are called children to the
parent node, i.e. the data struct. Children can be transferred to another temporary
parent node, that parent node is then referred to as the "plastic parent" of
the children.

## Initialization
````
>>> import OPCTree
>>> nested_levels_to_search = 3
>>> root = OPCTree.connect_and_build(nested_levels_to_search)
````
This will prompt you to input which server to connect to
if you haven't specified it in ```OPCTree.settings.OPC_SERVER``` .
After connecting will it start searching through the structure, as many
levels as given to ```connect_and_build```.

When initialized can you traverse the OPC-tree with the dot-notation, and
run functions on the specified node. While traversing the tree structure can
__Tab__ be used to auto-complete and __Tab__ __Tab__ for showing available children.

In the list will also the methods defined on the item show, if you want to
distinguish which is the actual OPC children, then you can look in
````
>>>root.opc_children
````
That is a list caring the name of all opc children on the parent. Observe that
the names differ slightly from their opc-path if their name wasn't possible to
use as name, for example if the opc-path included ```opc_children``` as item then that
can't be used as name of a child since that already is used for the list of
children.

### Load more children
If you want to load more children to a part of the tree, use
```.load_children(levels)```.
````
>>>root.Applications.Application_1.load()
````
>[!CAUTION]
>Observe that loading children removes all current children before loading the new. 
> So the items loaded to the node before are all lost.

If you want to reload items to a structure that already is loaded then you can use
````reload_children()````. This will keep the already loaded items, but delete the
items that no longer is in the OPC-server. If you are on the level that has changed
items, and you don't want to search through the hole subtree for changes, then can you
use ````reload_children(ignore_existing=True)````, that will only load the subtrees
that isn't in the current object and remove the ones that no longer is in the OPC-server.

### First read of properties
After loading a tree you can read the properties of all leafs (opc variables) by
writing 
````
>>>root.Applications.Application_1.first_read()
````
on the level of your choosing. Reading the properties of the variables is required
before writing values to them. Reading all item properties in you system might take
quite some time, depending on the number of tags in your system. You can press
ctrl+C to abort the action, you might want to limit your scope before reading.

The read will be performed in chunks of 40 variables at the time, which might be 
take longer time than necessary, if you have a fast server you can specify a higher
number like this:
````
>>>root.Applications.Application_1.first_read(max_chunk=1000)
````
which reads 1000 properties on each call.

## Saving and restoring
After reading all properties you probably want to save your updated root. Do that
by writing
````
>>>root.save(\<optional string with name\>)
````
the object is now saved as '<optional name>.pickle'. If you don't specify a
name will it be saved as the name specified in ```settings.OPC_OBJ_PICKLE```
(standard: 'opc_obj.pickle'). 
The object can now be restored with either
````
>>>restored_root = opc_fetch.restore('<file name if specified when saved>')
````
or
````
>>>root_to_restore = root_to_restore.restore('<file name if specified when saved>')
````
## Filter out specific parts by name or properties
You can now filter out the parts of the tree that you are interested in by using
the ```.all('<your regular expression filter>')``` notation to get a new root with all
children as leaves on the first level. If you for example want to filter out all 
items that has an opc-path that ends with '.Forced' then you can write like this:
````
>>>temp_parent = root.all(r'\.Forced$')
````
Maybe you have a unit called 'H20' in App1.Diagram2 from which you
want to filter out all controller values called 'Direct', 'Gain', 'Ti' and 'Td' from
because you will do a re tuning of all controllers in this part of the program and want
to save their old values as backup. 
You know that your controllers contain the string 'LIC', 'TIC' or 'PIC', then you could 
use:
````
>>>temp_parent = root.Applications.App1.Diagram2.all(r'H20*\.*(LIC|TIC|PIC).*(Direct|Gain|Ti|Td)$')
````
or if you want to filter out the objects GP001 to GP005
````
>>>temp_parent = root.all(r'App1\.Diagram2\.H20\.GP00[1-5]')
````

An easy way of testing if your regular expression matched the paths that you
wanted is to print some of the matches with ``.print_paths(<count to print>)`` like this:
````
>>>root.all(r'App1\.Diagram2\.H20\.GP00[1-5]').print_paths(10)
Printing 10 of 2552 paths
Applications.App1.Diagram2.H20.GP001
Applications.App1.Diagram2.H20.GP001.AEAmpsDesc
Applications.App1.Diagram2.H20.GP001.AEAmpsDescInter
Applications.App1.Diagram2.H20.GP001.AEClass
Applications.App1.Diagram2.H20.GP001.AECondNameH
Applications.App1.Diagram2.H20.GP001.AECondNameHH
Applications.App1.Diagram2.H20.GP001.AECondNameL
Applications.App1.Diagram2.H20.GP001.AECondNameLL
Applications.App1.Diagram2.H20.GP001.AEConfAmps
Applications.App1.Diagram2.H20.GP001.AEConfHH
````


Maybe you want to filter out values based on the opc properties of
the items. You might first want to find which properties the item has by
looking into
````
>>>temp_parent.<\child_path\>.name_prop
````
or if you rather access the properties by OPC index
````
>>>temp_parent.<child_path>.idx_prop
````
If you are connected to an ABB 800M OPC-server then will you on index
'5002' have information on if the value is 'ColdRetain' or 'Retain',
if you want to use that to filter out all 'ColdRetain' values, then
can you define a custom filter like this:
````
>>>isColdRetain = lambda child: child.idx_prop[5002] == 'ColdRetain' if hasattr(child,'idx_prop') else False
````
and select with
````
>>>temp_parent = root.all(re_path='<optional_path>',filter_func=isColdRetain)
````
Some examples of filters, including the one above, is in
the example_filters.py file.


## Reading, writing and printing values
After the initial read that included the item properties will it go much faster
to just reload the values of the leaves, which can be done with

>\>>>root.branch_to_read_from.read()

if you also want to print the vales that you have written, then can you
use
````
>>>root.branch_to_read_from.print_values()
````
or directly on the returned branch from the read() result:
````
>>>root.branch_to_rad_from.read().print_values()
````
This can be combined with the all filter like this:

````
>>>root.Applications.App1.Diagram2.all(r'H20*\.*(LIC|TIC|PIC).*(Gain|Ti|Td)$').read().print_values()
Read      537 of 537      items
0.0            Applications.App1.Diagram2.H20.LIC1.Aux.Backward.Gain
0.0            Applications.App1.Diagram2.H20.LIC1.Aux.Backward.Td
0.0            Applications.App1.Diagram2.H20.LIC1.Aux.Backward.Ti
0.0            Applications.App1.Diagram2.H20.LIC1.FFGain
0.0            Applications.App1.Diagram2.H20.LIC1.InitFfGain
1.0            Applications.App1.Diagram2.H20.LIC1.InitGain
0.0            Applications.App1.Diagram2.H20.LIC1.InitTd
20.0           Applications.App1.Diagram2.H20.LIC1.InitTi
0.0            Applications.App1.Diagram2.H20.LIC1.InteractionParPIDCC_MainOld.FfGain
1.0            Applications.App1.Diagram2.H20.LIC1.InteractionParPIDCC_MainOld.Gain
0.0            Applications.App1.Diagram2.H20.LIC1.InteractionParPIDCC_MainOld.Td
20.0           Applications.App1.Diagram2.H20.LIC1.InteractionParPIDCC_MainOld.Ti
0.0            Applications.App1.Diagram2.H20.LIC1.InteractionParPIDCC.Main.FfGain
...
````

Doing a read() will save the live value to the opc_variable items ```.value```

If you want to compare the vales already fetched with the live values then
can you use ```.changed()``` which will filter out all values that has changed
and print them out:
````
>>> root.Applications.App1.Diagram2.all(r'H20*\.*(LIC|TIC|PIC).*(Direct|Gain|Ti|Td)$').changed()
Live value                    Saved value                   Tag
0.0                           0.6                           Applications.App1.Diagram2.H20.LIC1.InteractionParPIDCC.Main.FfGain
20.0                          40                            Applications.App1.Diagram2.H20.LIC1.InteractionParPIDCC.Main.Ti
````
if you want to write the values in the Python object that differ from the live system to the live system you can use:
````
>>>root.Applications.App1.Diagram2.all(r'H20*\.*(LIC|TIC|PIC).*(Direct|Gain|Ti|Td)$').changed().write()
````
## Renaming
It is possible to change the name of a child so that all the opc-paths
is changed in the hole subtree. This can especially be useful if the 
live object has changed or is about to change so that all children don't 
have to be reloaded. It can also be used as a backup of all values in the
live system. Renaming in the live system might result in loss of
configured values, and then can this renaming be done so that the values
in the Python object can be written to the live system.

You have to do the renaming from the parent node like this:
````
>>>branch_with_child_to_rename.rename_child(name_now='child_old_name', new_name='new_name')
````
or simply
````
>>>branch_with_child_to_rename.rename_child('child_old_name', 'new_name')
````

## Custom coding and upgrading
If you want a function that is missing, don't hesitate to add it, after
adding or modification of opc_obj.py, opc_vars.py or custom
opc_class-libraries can the Python branch be upgraded to the latest version
by running
````
>>>root = root.upgrade()
````
this will reload the libraries and upgrade the branch/root and all
of its children.

If you fixed a bug or added some nice fetcher, request a pull on your
branch of the code so that it can be added to the main branch for others
to enjoy.

## Visualization in browser
If you want to see the structure in a web-browser you can use ``.visualize()``
on a node. This will generate a json-file, start a webserver providing the 
json-fil together with the vis_template.html page with which you can see
the structure. The node is collapsed by default and are expanded when clicked.

## Restore ABB 800M StartValueAnalyzer Data
The module allows building a root based on StartValueAnalyzer files from an ABB
800M PLC. If you want to use that you need to create a folder "Input" in your
working directory, and in that folder put the files from the StartValueAnalyzer
tool (found on 800xA installation media). So that you have paths like this:
'\Input\StartValuesData_YYYY-MM-DD HH.MM.SS.mils'

Project/\
├── .venv          ← Your virtual environment\
├── Input/         ← Folder to put the StartValuesData in\
└── WorkingDir/    ← Optional folder for saving/restoring root\

You can then run ``new_root = OPCTree.create_from_StartValuesData()`` which will
create a new root built on your extracted values. All leaves will be given an
attribute ``.init_value`` holding the initial value, and the ``.value`` will hold
the retrieved retained value, which could be written back to the live application
with ``.write``, if you are connected to the OPC server. If you aren't
you need to initialize it first, which could be done with ``OPCTree.initialize_opc_client()``.
