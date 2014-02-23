pycho
=====

A game engine with inbuilt AI support written for Python 2 and 3.

Comes with batteries built in, but also designed in such a way that nearly everything is modular, and if it's not then it will be in a future release. The source is designed to be clean and simple, so that anyone who needs to extend it in any way can easily see what and where they should change things.

Current support for graphics toolkits
-------------------------------------

Currently uses PyQt5 for GUI stuff. Adding PyQt4 support is trivial and will be included in later versions, but PyQt5 is the main target. 

Builtin objects
----------------

There are several objects provided by the game engine. These may be moved out in future releases. 

- Bombs increase in size over time, until they reach a certain size and explode. The fragments cause damage on contact and are destoryed on first contact.

- The player and old grumpers are basic examples of objects which support collision detection and ticks

- Walls are the primative which allows you to section off areas and can have gaps, which may function as portals to other levels.

- Words are text, converted into block-based represetations which can be drawn and collide in the world.


Creating custom objects
-----------------------

Objects in pycho are both drawn and collided in the same way. populated_at is called when needed, and should return a list of (Color, x, y) tuples. These tuples are used to calculate collisions, by figuring out during movement if there is anything in the up coming square or not. Color is used for the drawing of the objects.

Groups of same-colored squares will be grouped together to improve drawing performance. 

[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/eeue56/pycho/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

