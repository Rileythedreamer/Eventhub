# EventHub
#### [Video Demo](linkhere)
#### Short Description:
On Eventhub you can explore and buy tickets for events or organize your own.

---

## Table of Contents
- [Overview](#overview)
- [Distinctiveness and Complexity](#distinctiveness-and-complexity)
- [Features](#features)
- [Project Structure & File Breakdown](#project-structure)
- [How to Run Eventhub](#installation-and-usage)
- [Design Decisions](#design-decisions)
- [Dependencies](#dependencies)
- [Future Improvements](#future-improvements)

---

## Overview
Eventhub is an online platform for finding events near you.
peaple can sign up and after they do they can browse all the events that are on the website; they can filter (by category, location, date and time) and search  the events and find what they are looking for. 
after they find what interests them they can purchase tickets for the event if it is not past / canceled or sold out.
After they purchase tickets they'll be presented with a confirmation page.   
People can also organize events, when a user organizes their first event, the Organizer dashboard which is used for managing their organized events and accessing sale data automatically  becomes available for them.
---

## Distinctiveness and Complexity

### 1. Celery

### 2. Organizer Dashboard

### 3. Role Based Access

## Features
- 
- 
---

## Project Structure
```

project/
├── project.py            main Audiofy file containing all core and helper functions.
├── test_project.py       test file for testing that project.py works as expected.
├── README.md             Documentation.
├── requirements.txt       list of all dependencies.
└── test_cases            contains 5 books for testing the functionality of the project.
     ├── book1.txt        empty book.
     ├── book2.txt        contains a book with simple chapter structure.
     ├── book3.txt        contains a book with intro , toc and simple chapter structure.
     ├── book4.txt        contains a book with no structure.
     └── World.txt        the text format of around the world in 80 days.
````

Output :
running ```project.py test_cases/World.txt``` will result in a directory being created inside test_cases.
the folder structure displayed above stays the same except :
````
└── test_cases
     ├── book2.txt
     ├── book3.txt
     ├── book4.txt
     ├── World
     |     ├── CHAPTER I.mp3
     |     ├── CHAPTER II.mp3
     |     ├── ...
     |     └── CHAPTER XXXVII.mp3
     └── World.txt
````
---
### Files  Breakdown


## Installation and Usage

```bash

# install required packages
pip install -r requirements.txt
````

---





## Design Decisions


---



## Dependencies

- **Python**: 3.8+ (async/await support required)

- **Packages**:
  - `edge-tts` – for text-to-speech conversion
  - `tqdm` – for progress bars
  - `pytest` - Only required for testing, not running the program.

- **Standard Library (no installation needed)**:
  - `asyncio`
  - `sys`
  - `re`
  - `os`

---


## Future Improvements

* Command Line programs are only used by developers and the target audience for my program isn't just developers I better design a different Interface for it. a website would be great.
* Instead of the user having to type the voice name they could choose from a dropdown selector.
* Instead of the user having to provide the ebook they could also have the option of going through ebooks that are already available and convert those if they want.
the ebooks could be listed using an API to an open source library like [Project Gutenberg](https://www.gutenberg.org/)
* the audiobooks that have been converted before by other users can be stored so that new users can save time if they want the already existing audiobooks
* I think I could look for better text to speech libraries especially if there is one powered by AI  it would sound better.

#### Testing Improvements
I think the biggest flaw my program has are the tests they are not exactly reliable and I don't think that's how tests in the real world are written.
I would like to learn more about mocks and fixtures in pytest because I think that my tests have a big potential fo improvement.
I also need to learn how to test asynchronous functions/ processes.

---



## Author : **Negin Jahedi**
# Eventhub
