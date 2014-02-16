pycho
=====

A game engine with inbuilt AI support written for Python 2 and 3.


Creating custom objects
-----------------------

Objects in pycho are both drawn and collided in the same way. populated_at is called when needed, and should return a list of (Color, x, y) tuples. These tuples are used to calculate collisions, by figuring out during movement if there is anything in the up coming square or not. Color is used for the drawing of the objects.

Groups of same-colored squares will be grouped together to improve drawing performance. 