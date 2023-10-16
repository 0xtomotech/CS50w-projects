from django.shortcuts import render
from django import forms
from . import util
import markdown2
import random


class SearchForm(forms.Form):
    search = forms.CharField(label="",
                             widget=forms.TextInput(attrs={
                                 'placeholder': 'Search the Encyclopedia',
                                 'class': 'search-input',
                             }))


class TitleForm(forms.Form):
    title = forms.CharField(label="",
                            widget=forms.TextInput(attrs={
                                'placeholder': 'Enter a title',
                                'class': 'title-input',
                            }))


class EntryForm(forms.Form):
    entry = forms.CharField(label="",
                            widget=forms.Textarea(attrs={
                                'placeholder': 'Start writing here',
                                'class': 'entry-input',
                            }))


def index(request):
    if request.method == "POST":
        results = []
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            # Check each saved title
            for title in util.list_entries():
                # If search exact matches title: redirect to title page
                if title.lower() == search.lower():
                    return wiki_title(request, search)
                if search.lower() in title.lower():
                    results.append(title)
            # Loop check over, no exact match, let's return soft matches if any
            if results:
                return render(request, "encyclopedia/searchresults.html", {
                    "entries": results,
                    "form": SearchForm(),
                    "foundresults": True
                })
            # empty results, show all pages
            else:
                return render(request, "encyclopedia/searchresults.html", {
                    "entries": util.list_entries(),
                    "form": SearchForm(),
                    "foundresults": False
                })
    # Method Get
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": SearchForm()
        })


def new(request):
    if request.method == "POST":
        title_form = TitleForm(request.POST)
        entry_form = EntryForm(request.POST)

        if title_form.is_valid() and entry_form.is_valid():
            title = title_form.cleaned_data["title"]
            entry = entry_form.cleaned_data["entry"]

            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/error.html", {
                    "message": "Page already exists. Please edit the page instead.",
                    "form": SearchForm()
                })
            else:
                util.save_entry(title, '#' + title + '\n' + entry)
                return wiki_title(request, title)

    else:
        # Get Request
        return render(request, "encyclopedia/new.html", {
            "form": SearchForm(),
            "title_form": TitleForm(),
            "entry_form": EntryForm(),
        })


def edit(request, title):
    if request.method == "POST":
        title_form = TitleForm(request.POST)
        entry_form = EntryForm(request.POST)

        if title_form.is_valid() and entry_form.is_valid():
            title = title_form.cleaned_data["title"]
            entry = entry_form.cleaned_data["entry"]
            util.save_entry(title,entry)
            return wiki_title(request, title)
    # Request method get, render the edit page
    else:
        entry = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "form": SearchForm(),
            "title_form": TitleForm(initial={'title': title}),
            "entry_form": EntryForm(initial={'entry': entry}),
        })


# Get Wiki Entry via wiki/[title]
def wiki_title(request, title):
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/404.html", {
            "message": "Requested entry does not exist in the encyclopedia.",
            "form": SearchForm(),
        })
    else:
        return render(request, "encyclopedia/title.html", {
            "title": title.capitalize(),
            "entry": markdown2.markdown(util.get_entry(title)),
            "form": SearchForm(),
        })


def random_page(request):
    random_title = random.choice(util.list_entries())
    return wiki_title(request, random_title)
