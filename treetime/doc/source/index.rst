.. TreeTime documentation master file, created by
   sphinx-quickstart on Mon Jul 31 11:44:07 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TreeTime documentation
====================================

TreeTime is organized as a hierarchy of classes. The GTR class implements sequence evolution models, TreeAnc does ancestral sequence reconstruction, ClockTree implements time tree inference for a fixed tree topology, while TreeTime provides convenient wrapper functions and additional functionality to manipulate the tree (e.g. rerooting and polytomy resolution).

.. toctree::
   :maxdepth: 2
   :hidden:

   gtr
   treeanc
   clock_tree
   treetime


.. automodule:: treetime


:doc:`GTR class<gtr>`
---------------------

:doc:`TreeAnc class<treeanc>`
------------------------------

:doc:`ClockTree class<clock_tree>`
----------------------------------

:doc:`TreeTime class<treetime>`
-------------------------------


Command-line functions
=====================
TreeTime is designed to be part of python workflows, but for a number of standard
tasks we have implemented scripts that can be called from the command line like
regular linux programs.

homoplasy_scanner
-----------------

ancestral_reconstruction
------------------------

temporal_signal
---------------

timetree_inference
------------------

mugration
---------



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

