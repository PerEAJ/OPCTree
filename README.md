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

If you want to load more children to a part of the tree, use
__.load_children(levels)__.
>root.Applications.Application_1.load()

