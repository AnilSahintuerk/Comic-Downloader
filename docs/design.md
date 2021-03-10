# Design

## Purpose of File

The purpose of this doc is to state my design choices and how the classes I in comic.py interact with each other

## Visual Workflow

*TODO: Add draw.io diagramm for the workflow of the classes*

## Structure

The comic.py has 3 classes that are responsible for creating the comic. For further information for the functions look into the [api doc](./api.md)

#### class Scraper(abc.ABC)

The main purpose of the Scraper is to get all images from a comic and save them in a folder named after the chapter.

#### class Converter(abc.ABC)

The main purpose of the converter is to replace a folder with images from a comic with a single pdf that contains all the images in order.

#### class Make(abc.ABC)

The main purpose is to wrap the functionality for the *class Scraper* and *class Converter*. So that when a method from the class Make gets called we get all images from a comic and convert it into a single pdf.

