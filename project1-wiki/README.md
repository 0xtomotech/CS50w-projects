# Project Wiki: A Django Encyclopedia Web Application

This Django web application was created as part of Harvard
's CS50W course and it is a simple encyclopedia, where users can search for, view, edit, and create new content. The content is rendered in Markdown, allowing users to leverage the rich formatting features of Markdown.

[App Demo on Youtube](https://youtu.be/bAQbfF_eGuA)

[Project Instructions](https://cs50.harvard.edu/web/2020/projects/1/wiki/)


## Features

1. **Search Functionality**: Users can search for existing encyclopedia entries.
2. **Create New Pages**: Users can add new pages to the encyclopedia.
3. **Edit Existing Pages**: Existing pages can be edited and updated.
4. **Markdown Support**: All entries are written and rendered in Markdown format.
5. **Random Page**: Users can view a random encyclopedia page.

## Core Components

### Forms

1. `SearchForm`: For searching encyclopedia entries.
2. `TitleForm`: To input the title of a page when creating or editing.
3. `EntryForm`: To input the content of a page in Markdown format when creating or editing.

### Views

1. `index`: Display a list of all encyclopedia entries and provides a search function.
2. `new`: Allows users to create new encyclopedia pages.
3. `edit`: Provides an interface to edit existing encyclopedia pages.
4. `wiki_title`: Displays the content of an encyclopedia page.
5. `random_page`: Directs users to a random encyclopedia page.

## How to Run

Ensure you have Django installed:

```
pip install django
```
Navigate to the root directory of the project and run:
```
python manage.py runserver
```
Open a browser and go to http://127.0.0.1:8000/ to access the web application.

## Future Enhancements

1. Add user authentication and authorization.
2. Incorporate category tags for better content organization.
3. Implement a revision history feature to track changes made to each page.

## Contributions

Feel free to fork this repository and submit pull requests. All contributions are welcome!