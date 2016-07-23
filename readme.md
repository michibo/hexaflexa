
HEXAFLEXA
=========

Hexaflexa is a python program which makes hexaflexagon printouts, such that each face of the hexaflexagon shows a different picture. 

If you don't know what a hexaflexagon is, I recommend this great youtube video [LINK] or this website [LINK] or this book [LINK]. 

How to use the program
======================

To run hexaflexa you need *pycairo* [LINK].

Run 

    python hexaflexa.py --output myhexaflexagon.pdf pic1.png pic2.png ...

You have to put in *six* different pictures or it is boring. You can put in up to *nine* different pictures. The last three pictures should be watermark-images with given transparency values. 

-   The first three pictures will be printed on the *common* faces of the hexaflexagon, 
-   the next three pictures will be printed on the *hidden* faces, 
-   the last three pictures will be additionally printed *over* the first three faces, but *twisted* and with a watermark/transparency effect. These *twisted* faces always appear after a hidden face. 


How to make a hexaflexagon ( i.e. how to fold that thing to see the nice pictures )
===================================================================================


