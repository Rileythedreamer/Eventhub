# EventHub
On Eventhub you can explore and buy tickets for events or organize your own.

#### [Video Demo](linkhere)



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
Eventhub is an online platform for organizing and attending real world activities.
### For Attendees
Upon signing up, attendees gain access to an event catalog. They can utilize powerful search and filtering tools by category, location, date, and time to discover activities that match their interests.
The platform allows users to purchase any number of available tickets for an event. The purchasing option is active only for events that have not been completed, cancelled, or sold out.
After they purchase tickets they'll be presented with a confirmation page displaying all details related to their transaction.   
The search and filter features are implemented to enhance user experience by making it faster and easier to discover relevant events.
### For Organizers
Users can create and manage their own events by providing the required details such as event title, description, date and time, location, ticket quantity, and pricing. When a user organizes their first event, they automatically gain access to the Organizer Dashboard. This dashboard allows organizers to view, edit, or cancel their events. It also provides comprehensive ticket sales data, including how many tickets have been sold, how many remain, and overall revenue generated. The dashboard supports filtering, enabling organizers to track and manage all of their events in one place. Access to the dashboard and related management features is restricted to users with organizer status through role-based access control.
---

## Distinctiveness and Complexity

My Eventhub project is distinct from an E-commerce website because while it does include ticketing (a transaction), it's only one feature amongst many.
It's specifically distinct from Auctions because I had to manage event status and also ticket quantities when sales were made.
A large part of my app is the event management tools for organizers.

### 1. Asynchronous Task Scheduling
  The core functionality of this project is based on people being able to book tickets for events they wanna attend. which means Events need to have a status , Organizers set a date and time for the event when they're first creating it (for when the event is going to happen), If that date has passed, people shouldn't be able to buy tickets for those events.
  That's where celery comes in. It allows us to run code asynchronously.
  One of the use cases for celery is running scheduled tasks in the background.
  The way celery works is after you define the task that you wanna run in the background celery beat is like a heartbeat that beats every minute and every minute it checks if there are any tasks who's date and time has passed if so it updates those tasks status.
  This process involves 3 main parts
  1. Client : the Django App  where I define and run background tasks.
  2. Message Broker: A service that holds tasks in queue untill  the worker picks them up
  3. Worker : watches the queu for new tasks and executes them when tasks are ready for execution
  - Celery Beat : like a timer that keeps track of when tasks enter the queu
  
### 2. Organizer Dashboard
  The organizer Dashboard is only accessible for event organizers.
  Organizer can manage events they've organized and cancel or delete those events, they can also access ticket sale data.

### 3. Role Based Access
  I've defined roles for all the users who've logged in and by default everyone are attenders whenever a user create their first event ever, they automatically become an organizer which allows them access to other parts of the website.
  Only Organizers can access certain parts of the website to achieve this I had to define a new decorator very similar to login_required but the difference is it checks if the user who's trying to access a certain view function is an Organizer if not it prevents access.

## Features

- Role Based Access 
- Create Events
- Buy tickets for events
- keeping track of tickets sold & the tickets left quantity for each event.
- people can only purchase tickets for "Active" events.
- keeping track of the status of events (Active, Canceled, Compeleted, Sold Out)
- Search & Filter events without page reload using JS and calls to the API
- Organizer Dashboard
  - View eveything about all the events they have ever organized on the website
  - filter and search amongst all the events they've ever organized without page reload using JS.
  - View Sale Data
  - View Tickets Sold
  - how many tcikets have been sold for each event and how many are remaining.
  - Manage and Edit Events
- Events Status Update using Celery 

---

## Project Structure & File Breakdown
```

Eventhub/
├── manage.py            used to run commands on the django app
├── README.md            project docs
├── requirements.txt     list of all dependencies. TODO 
├── sqlite3.db           project's database file
└── Eventhub             contains the main project files 
     ├── settings.py     contains all configuration settings for the project
     ├── urls.py         contains all the url patterns for the entire project
     ├──         
     ├── 
     └── 

└── events              contains the files for the only app for the project
     ├── urls.py        contains all the url patterns for the events app.
     ├── views.py       contains all the view functions for event's app (how requests that are made to the app are handled)
     ├── models.py      contains all the defintions for my app's django models (the structure of the database tables)
     ├── forms.py       the form defintion for Event creation based of the Event Model
     └──    
````


---
### Files  Breakdown TODO: maybe write an explanation for the files that i created not the ones that are already there by default


## Installation and Usage

```bash

# install required packages
pip install -r requirements.txt
python3 manage.py runserver
TODO: maybe i need to activate celery whenever i wanna run the server?
````

---





## Design Decisions


---



## Dependencies

- **Python**: 3.8+ (async/await support required)

- **Packages**:
  - `django` – for text-to-speech conversion
  - `celery` – for progress bars
  - `` - Only required for testing, not running the program.

- **Standard Library (no installation needed)**:
  - ``
  - ``
  - ``
  - ``

---


## Future Improvements

* ### Improve the Organizer Dashboard
  - More detailed Analytics
  - Graphs for statics and anlyziong sale data
  
* Better more complex Search functionality for browsing amongst events :
  maybe people don't provide the exact title for the evnt when they are searching for it and they might have typos the search results could look past the typos, maybe that would be a better user experience.
  (Maybe using haystack whoosh or maybe using regex)
* adding a Reccomender AI : 
people who have bought tickets on the website before get offered events they might be interested in that is similar to what they have enjoyed before.
* people fill a quiz at sign up which asks them about their interests and suggests events related to those interests.
* An E-mail is sent automatically to people who purchase tcikets with their ticket information so that they can use that e-mail on entry to the venue where the event is held.

* 

---



## Author : **Negin Jahedi**

