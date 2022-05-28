# Cleaning

This repository contains five notebooks, each of which is used to clean the masterlists of the top five economic journals and merge it with pivot lists. The output is an excel file of a modified masterlist with each article labelled by content_type eg: Article, Review, Miscellaneous etc. Note that the cleaning is not completely accurate - it is more likely to classify non-articles as articles. The goal of these notebooks is to identify and remove the non-articles such as forewords, front matters and back matters which would have had no meaningful data. This can reduce the processing load when extracting references, affiliations, tables and figures.

## Table of contents
- [Setup instructions](#setup-instructions)
- [General cleaning procedure](#general-cleaning-procedure)
- [Abbreviations](#abbreviations)
- [Next steps](#next-steps)

## Setup instructions
Assumptions:

- Python has been installed
- Jupyter notebook is installed or extensions in VS code are enabled to read .ipynb files.

__Note: Follow [this article](https://betterprogramming.pub/install-jupyter-notebooks-without-anaconda-5a19ac20bae2) to install jupyter notebook without anaconda.__

To generate a cleaned masterlist:

- Go to a prompt (CMD in Windows) and type jupyter notebook and navigate to the .ipynb file
- In the first two code blocks change the file path to a local path such that it points to the correct excel files needed for processing
- Follow the instructions in the first two blocks - change the file paths to your own local path (see image below).
- Ensure that the file paths are pointing to the right files.
- Download [masterlists](https://drive.google.com/drive/folders/1bqs01QcpYeS-wi1jYrrnXkE0GsINqYLs), [pivot lists](https://drive.google.com/drive/folders/1nmxCa9po1drhWBoMOxi1660XI3FzElEf) and [scopus data](https://drive.google.com/drive/folders/1qh9XNus41zYXlSVwMzqNoERtXG16EKp3) of each journal by following their respective hyperlinks.**

![image](https://user-images.githubusercontent.com/80747408/170805388-00cce929-12e8-46ee-ac13-930c6148ecf9.png)


** ignore datadumpts for now

## General cleaning procedure
This is an overview of how the each article was categorized. The assumption is that all data without author names must be miscellaneous documents like reports by the committee, forewords, front matters etc.. The goal of this notebook is to check for certain that all the documents without author names are actually miscellaneous documents and then classify them as miscellaneous (MISC). Hence, first we group everything the data by title to see the repetitive general content that can likely be removed.

![image](https://user-images.githubusercontent.com/80747408/170804726-2cc3ec48-d4cb-4d5f-99ef-ac71696c4702.png)

The duplicates above a certain count are classified as miscellaneous and then regex pattern matching is used for less consistent repetitions eg: titles of AGM documents with changing years. Some individual errors such as missing author names are corrected if found during this phase.

The next step is to classify other content such as reviews, discussions, comments, replies and rejoinders which may have a different format than common articles.

The pivot lists which is simply a list of every issue in a journal including the year and title is sorted for special (S) and normal (N) issues articles in supplementary issues are sometimes formatted differently to articles in other issues. The pivot list and masterlist are merged so that each article has additional fields of year, issue number, volume number and indicator on being part of a special or normal issue.

Lastly, there is a summary section of counts for all content types.

## Next steps
- Add number of pages per article for masterlists
- Merge scopus data and masterlists
- Merge datadumps and masterlists

## Abbreviations
- AER: American economic review
- ECTA: Econometrica
- JPE: Journal of political economy
- QJE: Quarterly Journal of economics
- RES: Review of economic studies
