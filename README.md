# Dolores

- [Dolores](#dolores)
  - [Abstract](#abstract)
  - [Requirements](#requirements)
  - [How to use it](#how-to-use-it)
  - [How it works](#how-it-works)
    - [pentakey\_adapter.py](#pentakey_adapterpy)
    - [scoreParser.py](#scoreparserpy)
  - [What's left to improve it](#whats-left-to-improve-it)

Project for the Algorithmic Music and Sound Computing course at the University of Salerno.
A very simple python tool for converting sheet music into musicXML format.

## Abstract

This projects build a MXML parser, using a neural network previously trained by University of Salerno students.
More details on the subject can be found in the reference folder, with the [referenced thesis](./docs/PentaKey_Tesi.pdf).

The neural network exploits YoloV3 which is a real time object detection algorithm employed by open source tools like Darknet, which was used in order to train the model to recognize various musical notation elements in order to reconstruct, based on a clear musical sheet image, a musicXML equivalent of the composition, that can then be used by other tools, like MuseScore, to aid in various tasks related to composition and execution of musical scores.

This project is meant to be a prototype, defining a simple way to approach the recognition and the parsing of the score elements, which could be used as a reference for a more fleshed out implementation.

## Requirements

The project is mainly written in Python, and uses the [pymusicxml](https://github.com/MarcTheSpark/pymusicxml) library that makes it easier to build a mxml file.

It also features a [jupyter notebook](./notebooks/pentakey_dolores.ipynb) which can be imported in colab in order to use the model.
If you don't want to bother going all the way and training the model from scratch, you can use pre-trained weights and skip the relevant points.
The notebook explains how to train the neural net based on the instructions left by the thesis' authors, and how to fetch the results, by using [Darknet](https://pjreddie.com/darknet/).

Once the results are available, using the code in this repository we can execute a series of scripts which will:

- Interpret the results of the model, rearranging them and sorting them
- Normalize them, by deducing all the notes durations, beam grouping, and modifiers in order to create an intermediate, "cleaned" result
- Collapsing every element into a simple object model, which is used to parse the results into MXML tag elements.
- Making some additional transformations, like pitching everynote to uppercase in order to make the resulting file compatible with applications like MuseScore which demands this sort of notation.

## How to use it

Assuming you've placed the model's result, after choosing a score example, in the input folder, and installed the required dependencies you can simply:

```bash
python3 ./src/run.py
```

And you'll find the result in the output folder.

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

Then, for every score, we iterate through the model's output and we add, for each score's sublists, all of the elements which fall within the score's bounding boxes.
This is done wih simple math, by checking if the y coordinate of the object falls within the score's bboxes.
Then, after every object has been put in the right "bucket", we proceed in sorting them by x coordinate, declaring who comes first and who comes second for each row.

At the end, we append every sublist to the arranged output list of lists, which reeturns an arranged, "normalized" list of lists containing a list for each score, each of them containing musical notation elements.

This is not the only thing we must do. In particular, for the currently used neural net, we need to normalize durations.

In short, sometimes the model will insert durations after the note. Sometimes it will insert them before the notes. And sometimes the duration will not be explicitly stated, but needs to be deduced from the position of the note inside a beam.

The rule is pretty simple: for every beam the note is contained in, the standard duration (1/4) gets halved.

We could also approach the problem in the opposite way, by deducing the duration further down the pipeline, in the parser, and keeping the beams tangled. To avoid complicating the parser logic, since this is meant to be a first approach and part of the parser was already written, we decided to untangle the beams right now. But it must be noted that this is also a valid approach, that could avoid us losing beam information.

Modifying the logic in case something needs to be added should be pretty simple: avoid removing the beam information in the normalize_durations function and discover a new way to implement it in the parser.

Anyway, after the durations for every node are inserted and the beams are removed from the equation, we only need to tag the time signature.
The model doesn't immediately recognize which is the numerator and which is the denominator, so by simply viewing whose center y is higher we tag each timesign element with its correct position in the fraction, so the parser simply needs to read this information.

Then, the output gets saved in a json file, ready to be interpreted by the parser.

### scoreParser.py

This script defines classes and functions to map simple strings - found in the model's prediction output - to MusicXML elements (specifically using the pymusicxml library) and build a musical score in the form a .musicxml file.

The code defines lists of musical elements, specifically time signatures, notes, modifiers, clefs, rests, durations, metas and others. They contain all the possible strings in a generic model's output file and are eventually used in scoreParser.py to recognize the type of object it's dealing with as the model's output is parsed line by line.

The script also defines a ScoreElement class that represents different types of musical elements. ScoreElement instances are the intermediate step between simple strings and MusicXMLComponent objects. The latter is an abstract pymusicxml base class representing all musical objects, providing functionality for rendering and exporting to a file.

The ScoreElement class has methods to initialize and map a string representation of an element to its corresponding type. Subclasses of ScoreElement are defined for specific types (as per the lists definition).

There is a function scoreElementToDurationalObject that maps a ScoreElement to a DurationalObject. It is again a base pymusicxml object representing all objects that have duration within a measure, extending the former MusicXMLComponent and extended by other subclasses representing the specific type of object. Possible DurationalObject instances are Note, Clef, Rest and Duration instances. Other entities (such as barlines, pitch modifiers, augmentation dots, etc.) are not automatically mapped to pymusicxml but managed case by case instead.

The main logic is in the if __name__ == "__main__": block. It reads a JSON file containing musical elements, processes them, creates a musical score, and exports it to a MusicXML file.

## What's left to improve it

Currently this is still an experimental prototype, which focuses on finding a clear and simple way to parse the score and validate the model's result.

Clearly the model itself could benefit from additional training and a definition of a more fleshed out and complete set of classes.

The code itself also tries to solve some problems in the class hierarchy by reasoning strictly in geometrical terms on the placement of objects, but a more fleshed out class system could also lower the amount of effort required in normalizing the output, possibly yielding better results.

Also, it's still somewhat cumbersome to use, and could benefit from a simpler way of tying everything together by having a complete application which could call the model, available for example as an API, parse the results and directly printing them instead of going all the way through the notebook and then going back to the code.

Currently we are developing a simple service integration using Django, which could make it possible to install all the required dependencies on a machine and then simply using exposed API methods, to simplify user interaction.
