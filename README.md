# Dolores

- [Dolores](#dolores)
  - [Abstract](#abstract)
  - [Requirements](#requirements)
  - [How to use it](#how-to-use-it)
  - [What's left to improve it](#whats-left-to-improve-it)

Project for the Algorithmic Music and Sound Computing course at the University of Salerno.
A very simple python tool for converting sheet music into musicXML format.

## Abstract

This projects build a MXML parser, using a neural network previously trained by University of Salerno students.
More details on the subject can be found in the reference folder, with the [referenced thesis](./docs/PentaKey_Tesi.pdf).

The neural network exploits YoloV3 which is a real time object detection algorithm employed by open source tools like Darknet, which was used in order to train the model to recognize various musical notation elements in order to reconstruct, based on a clear musical sheet image, a musicXML equivalent of the composition, that can then be used by other tools, like MuseScore, to aid in various tasks related to composition and execution of musical scores.

This project is meant to be a prototype, defining a simple way to approach the recognition and the parsing of the score elements, which could be used as a reference for a more fleshed out implementation.

## Requirements

The project is mainly written in Python, and uses a library, [pymusicxml](https://github.com/MarcTheSpark/pymusicxml) that makes it easier to build a mxml file.

It also features a [jupyter notebook](./notebooks/pentakey_dolores.ipynb) which can be imported in colab in order to use the model.
If you don't want to bother going all the way and training the model from scratch, you can use pre-trained weights and skip the relevant points.
The notebook explains how to train the neural net based on the instructions left by the thesis' authors, and how to fetch the results, by using [Darknet](https://pjreddie.com/darknet/).

Once the results are available, using the code in this repository we can execute a series of scripts which will:

- Interpret the results of the model, rearranging them and sorting them
- Normalize them, by deducing all the notes durations, beam grouping, and modifiers in order to create an intermediate, "cleaned" result
- Collapsing every element into a simple object model, which is used to parse the results into MXML tag elements.
- Making some additional transofmrations, like pitching everynote to uppercase in order to make the resulting file compatible with applications like MuseScore which demands this sort of notation.

## How to use it

Assuming you've placed the model's result, after choosing a score example, in the input folder, and installed the required dependencies you can simply:

```bash
python3 ./src/run.py
```

And you'll find the result in the output folder.

## What's left to improve it

Currently this is still an experimental prototype, which focuses on finding a clear and simple way to parse the score and validate the model's result.

Clearly the model itself could benefit from additional training and a definition of a more fleshed out and complete set of classes.

The code itself also tries to solve some problems in the class hierarchy by reasoning strictly in geometrical terms on the placement of objects, but a more fleshed out class system could also lower the amount of effort required in normalizing the output, possibly yielding better results.

Also, it's still somewhat cumbersome to use, and could benefit from a simpler way of tying everything together by having a complete application which could call the model, available for example as an API, parse the results and directly printing them instead of going all the way through the notebook and then going back to the code.
