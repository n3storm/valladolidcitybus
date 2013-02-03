valladolidcitybus
=================

Web mobile application to query Valladolid City Bus arrivals

Written in Python (works under 2.6 and 2.7)

Requirements
============

Flask web microframework

BeautifulSoup4

Scypi for bus lines color extraction

More libs
=========
Web interface and interaction is brought by jQuery and jQuery Mobile

Usage
=====

You can run it as any Flask application, check their great documentation.
Point your browser to server url and you will see a list of bus lines at city of Valladolid (Spain), you can filter this list or
choose one.
After choosing one you will get a list of bus stops with a question mark on the right (?) Click on the stop you are 
interested in and ? mark will try to be updated with how many minutes are left for the bus in selected line to arrive to selected stop. That's all.

Some times a demo at http://vcb.getcloud.info may be available.

More information
================

At libs/valladolidcitybus.py lives Objects and methods related to Bus structure:

City > Line > Route > Stop

This objects, are filled up by BeautifulSoup extracted information from spaghetti HTML at http://www.auvasa.es

LICENSE
=======

Each library and component have their own license. The other code (supposedly mine, though I may have transformed it from places like ActiveState or StackXchange) 
is under the BSD License.

See valladolidcitybus/templates/about.html for further information.

