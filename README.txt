Overview
========

This project aims to bring the fun and ease of the Pyramid development style
into Plone.

Status
------

The work is at a very early alpha stage. There's no promises of API stability
or functionality yet.

Development
-----------

The code and issue tracker can be found at
https://github.com/hannosch/plutonian

Assumptions
-----------

This project assumes you are writing a specific application based on top of
Plone. Your project will consist of configuration, specific deployment
settings, policy code and knowledge about the content structure.

We further assume that non-persistent configuration is generally preferable
over persistent configuration, as it is easier to manage and version.

This approach is very different from the typical Plone development model, in
which you write add-ons for the Plone CMS application.
