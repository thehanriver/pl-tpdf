pl-tpdf
================================

.. image:: https://img.shields.io/docker/v/fnndsc/pl-tpdf?sort=semver
    :target: https://hub.docker.com/r/fnndsc/pl-tpdf

.. image:: https://img.shields.io/github/license/fnndsc/pl-tpdf
    :target: https://github.com/FNNDSC/pl-tpdf/blob/master/LICENSE

.. image:: https://github.com/FNNDSC/pl-tpdf/workflows/ci/badge.svg
    :target: https://github.com/FNNDSC/pl-tpdf/actions


.. contents:: Table of Contents


Abstract
--------

An app to generate PDFs based in the topological covidnet workflow


Description
-----------

``tpdf`` is a ChRIS-based application that takes in subdirectories from TS plugin and generates PDFs


Usage
-----

.. code::

    python tpdf.py
        [-h|--help]
        [--json] [--man] [--meta]
        [--savejson <DIR>]
        [-v|--verbosity <level>]
        [--version]
        [--dir]
        <inputDir> <outputDir>


Arguments
~~~~~~~~~

.. code::

    [-h] [--help]
    If specified, show help message and exit.
    
    [--json]
    If specified, show json representation of app and exit.
    
    [--man]
    If specified, print (this) man page and exit.

    [--meta]
    If specified, print plugin meta data and exit.
    
    [--savejson <DIR>] 
    If specified, save json representation file to DIR and exit. 
    
    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.
    
    [--version]
    If specified, print version number and exit.
    
    [--dir]
    Name of sub directory in the previous plugin

Getting inline help is:

.. code:: bash

    docker run --rm jonocameron/pl-tpdf tpdf --man

Run
~~~

You need to specify input and output directories using the `-v` flag to `docker run`.


.. code:: bash

    docker run --rm -u $(id -u)                             \
        -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
        jonocameron/pl-tpdf tpdf --dir "41"                      \
        --imagefile "ex-covid.jpeg" --patientId 12345678 /incoming /outgoing

.. code:: bash

    docker run --rm -u $(id -u)                             \
        -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
        jonocameron/pl-tpdf tpdf                      \
        --imagefile ex-covid.jpeg /incoming /outgoing
        
.. code:: bash

    docker run --rm -u -u $(id -u):$(id -g) \
        -v $PWD/covidnet-in:/incoming:ro -v $PWD/covidnet-out:/outgoing:rw \
        fnndsc/pl-covidnet:0.2.0 covidnet \
        --imagefile chest-scan.jpg /incoming /outgoing

.. code:: bash

    docker run --rm -u -u $(id -u):$(id -g) \
        -v $PWD/covidnet-out:/incoming:ro -v $PWD/pdfgeneration-out:/outgoing:rw \
        fnndsc/pl-covidnet-pdfgeneration:0.2.0 pdfgeneration \
        --imagefile chest-scan.jpg --patientId 12345678 /incoming /outgoing

.. code:: bash

    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing \
        jonocameron/pl-tpdf tpdf --imagefile "ex-covid.jpeg" --patientId "77812345" \
        /incoming /outgoing

Development
-----------

Build the Docker container:

.. code:: bash

    docker build -t local/pl-tpdf .

Run unit tests:

.. code:: bash

    docker run --rm local/pl-tpdf nosetests

Examples
--------

Put some examples here!


.. image:: https://raw.githubusercontent.com/FNNDSC/cookiecutter-chrisapp/master/doc/assets/badge/light.png
    :target: https://chrisstore.co
