# Dolores

- [Dolores](#dolores)
  - [Abstract](#abstract)
  - [Requirements](#requirements)
    - [Local Installation](#local-installation)
  - [How to use it](#how-to-use-it)
  - [How it works](#how-it-works)
    - [pentakey\_adapter.py](#pentakey_adapterpy)
    - [scoreParser.py](#scoreparserpy)
    - [pentakey/spartito/views.py](#pentakeyspartitoviewspy)
    - [Things of note](#things-of-note)
  - [What's left to improve it](#whats-left-to-improve-it)

Project for the Algorithmic Music and Sound Computing course at the University of Salerno.

## Abstract

The goal of this project is to build an endpoint to a service that makes the user able to upload an image, representing a score sheet, and convert it to a musicXML file that can be opened and edited with tools like MuseScore.

The neural network exploits [YoloV3](https://pjreddie.com/darknet/yolo/) which is a real time object detection algorithm employed by open source tools like Darknet, which was used in order to train the model to recognize various musical notation elements in order to reconstruct, based on a clear musical sheet image, a musicXML equivalent of the composition, that can then be used by other tools, like MuseScore, to aid in various tasks related to composition and execution of musical scores.

This project is meant to be a prototype, defining a simple way to approach the recognition and the parsing of the score elements, which could be used as a reference for a more fleshed out implementation.
This prototype uses Django in order to create a simple web application where the user can interact with the system.

## Requirements

The project is mainly written in Python, and uses the [pymusicxml](https://github.com/MarcTheSpark/pymusicxml) library that makes it easier to build a mxml file.

It also uses [Django](https://www.djangoproject.com) to developed a fully fleshed-out web application that interacts with the underlying [Darknet](https://pjreddie.com/darknet/) implementation to return the MXML file.

It also features a [jupyter notebook](./notebooks/pentakey_dolores.ipynb) which can be imported in Colab in order to use the model without the web application itself.

If you don't want to bother going all the way and training the model from scratch, you can use pre-trained weights and skip the relevant points.
In any case, the notebook explains how to train the neural net based on the instructions left by the thesis' authors.
On a side note, all of the code was tested on macOS and Ubuntu since none of the project members uses a Windows release.

### Local Installation

In order to use it, you need to have all of the required dependencies.
To make it easier, simply past this code in your console:
Simply clone the repository with

```bash
git clone https://github.com/blazQ/pentakey-dolores.git
```

Then clone darknet inside the darknet folder with

```bash
git clone https://github.com/AlexeyAB/darknet
```

Then, follow the instructions contained in the [notebook](./notebooks/pentakey_dolores.ipynb) starting from point 1 to correctly configure darknet and import the weight.
After testing that your darknet installation is fully functional and the model has been trained, you can install the required dependencies for the Django application.

```bash
pip install pymusicxml
pip install django
pip install django-cors-headers
```

## How to use it

Assuming you've followed the other steps correctly, you can simply run:

```bash
# from main directory
cd pentakey
python3 manage.py runserver #you can specify a specific port if you'd like
```

You'll then be able to reach the service endpoint at [localhost:8000/spartito/upload/](http://127.0.0.1:8000/spartito/upload/)

## How it works

### pentakey_adapter.py

This script defines a series of steps required in order to rearrange and make sense of the neural net's json output.

It basically reads a json file, currently from the input folder, with the get_arranged_output function.
This function opens the file, and iterates on the entries in the resulting python dictionary.

The first thing it does, it gets all of the SCORE elements described in the model.

The reason we do this is that all of the notes are contained in this element, and there's one for each row of the musical score image.

By getting the scores, we basically know how big each section of the musical sheet paper is.

We then proceed in reordering every score depending on the y axis. (Obviously the scores which are higher on paper have a smaller center y coordinate)
This is done in order to establish a precedence which is used to rearrange all of the elements in the following sections.

Then, for every score, we iterate through the model's output and we add, for each score's sub-lists, all of the elements which fall within the score's bounding boxes.
This is done wih simple math, by checking if the y coordinate of the object falls within the score's bounding boxes.
Then, after every object has been put in the right "bucket", we proceed in sorting them by x coordinate, declaring who comes first and who comes second for each row.

At the end, we append every sub-list to the arranged output list of lists, which returns an arranged, "normalized" list of lists containing a list for each score, each of them containing musical notation elements.

This is not the only thing we must do. In particular, for the currently used neural net, we need to normalize durations.

In short, sometimes the model will insert durations after the note. Sometimes it will insert them before the notes. And sometimes the duration will not be explicitly stated, but needs to be deduced from the position of the note inside a beam.

The rule is pretty simple: for every beam the note is contained in, the standard duration (1/4) gets halved.

We could also approach the problem in the opposite way, by deducing the duration further down the pipeline, in the parser, and keeping the beams tangled. To avoid complicating the parser logic, since this is meant to be a first approach and part of the parser was already written, we decided to untangle the beams right now. But it must be noted that this is also a valid approach, that could avoid us losing beam information.

Modifying the logic in case something needs to be added should be pretty simple: avoid removing the beam information in the normalize_durations function and discover a new way to implement it in the parser.

Anyway, after the durations for every node are inserted and the beams are removed from the equation, we only need to tag the time signature.
The model doesn't immediately recognize which is the numerator and which is the denominator, so by simply viewing whose center y is higher we tag each time signature element with its correct position in the fraction, so the parser simply needs to read this information.

Then, the output gets saved in a json file, ready to be interpreted by the parser.

### scoreParser.py

This script defines classes and functions to map simple strings - found in the model's prediction output - to MusicXML elements (specifically using the pymusicxml library) and build a musical score in the form a .musicxml file.

The code defines lists of musical elements, specifically time signatures, notes, modifiers, clefs, rests, durations, metas and others. They contain all the possible strings in a generic model's output file and are eventually used in scoreParser.py to recognize the type of object it's dealing with as the model's output is parsed line by line.

The script also defines a ScoreElement class that represents different types of musical elements. ScoreElement instances are the intermediate step between simple strings and MusicXMLComponent objects. The latter is an abstract pymusicxml base class representing all musical objects, providing functionality for rendering and exporting to a file.

The ScoreElement class has methods to initialize and map a string representation of an element to its corresponding type. Subclasses of ScoreElement are defined for specific types (as per the lists definition).

There is a function scoreElementToDurationalObject that maps a ScoreElement to a DurationalObject. It is again a base pymusicxml object representing all objects that have duration within a measure, extending the former MusicXMLComponent and extended by other subclasses representing the specific type of object. Possible DurationalObject instances are Note, Clef, Rest and Duration instances. Other entities (such as barlines, pitch modifiers, augmentation dots, etc.) are not automatically mapped to pymusicxml but managed case by case instead.

The main logic is in the if __name__ == "__main__": block. It reads a JSON file containing musical elements, processes them, creates a musical score, and exports it to a MusicXML file.

### pentakey/spartito/views.py

It handles most of the logic of the web application.
Here we redirect our requests, after saving the image locally, to darknet, in order to retrieve the model's output.
Then, we refer to the other scripts that we just mentioned in order to process the json file and parse the XML file.

### Things of note

In order to accept requests from another app that's deployed locally, we've disabled CORS-headers with django-cors-headers. This might be useful if you want to test this app and integrate it with another, locally.
Be mindful of the fact that if you plan on improving the project and release it, another way of handling the matter has to be found.

## What's left to improve it

- The first problem with the current implementation is that it's deeply tied to a side darknet installation that must be correctly configured and could have some versioning issues in the future, if something were to change.
  - In order to make it resilient and not just functional, the model needs to be ported in a different format and possibly retrained. This could also lead to a simpler implementation, and possibly dockerization, to make it a scalable platform.
- The second problem is that the model is currently limited in its form, and could obviously be improved to recognize more complex scores than the one we used to train it, with a more fleshed out class system.
- It could benefit from using a more lightweight framework like Flask.
