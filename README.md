# pyOPC - A Python OPC browser

This packaged is made for simplifying working with OPC data from the
Python CLI. It enables easy scan of a nested structure, searching
through all branches, reading value and properties, writing value,
comparing the live values to the saved ones.

The program copies the OPC structure of the server so that the user
can use the OPC dot-notation in the CLI to traverse to the object
the user wants to work on.

## Initialization
> import opc_fetch\
> nested_levels_to_search = 3\
> root = opc_fetch.connect_and_build(nested_levels_to_search)

This will prompt you to input which server to connect to
if you haven't specified it in settings.OPC_SERVER .
After connecting will it start searching through the structure, as many
levels as given to __connect_and_build__.

When initialized can you traverse the OPC-tree with the dot-notation, and
run functions on the specified node. While traversing the tree structure can
__Tab__ be used to auto-complete and __Tab__ __Tab__ for showing available children.

### Load more children
If you want to load more children to a part of the tree, use
__.load_children(levels)__.
>root.Applications.Application_1.load()

### First read of properties
After loading a tree you can read the properties of all leafs (opc variables) by
writing 

>root.Applications.Application_1.first_read()

on the level of your choosing. Reading the properties of the variables is required
before writing values to them. Reading all item properties in you system might take
quite some time, depending on the number of tags in your system. You can press
ctrl+C to abort the action, you might want to limit your scope before reading.

The read will be performed in chunks of 40 variables at the time, which might be 
take longer time than necessary, if you have a fast server you can specify a higher
number like this:

>root.Applications.Application_1.first_read(max_chunk=1000)
 
which reads 1000 properties on each call.

## Saving and restoring
After reading all properties you probably want to save your updated root. Do that
by writing

>root.save('<optional name>')

the object is now saved as '<optional name>.pickle'. If you don't specify a
name will it be saved as the name specified in settings.OPC_OBJ_PICKLE
(standard: 'opc_obj.pickle'). 
The object can now be restored with either

>restored_root = opc_fetch.restore('<file name if specified when saved>')

or

>root_to_restore = root_to_restore.restore('<file name if specified when saved>')

## Filter out specific parts by name or properties


## Reading and writing values
After the initial read that included the item properties will it go much faster
to just relaod the values of the leaves, which can be done with

>root.branch_to_read_from.read()
