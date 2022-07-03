from django.urls import reverse
import re
from django import forms
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from markdown import Markdown

from . import util


# class NewTasksForm(forms.Form):
    # task = forms.CharField(label="New Task")

class NewEntryForm(forms.Form):
    title = forms.charField(label="new title", widget=forms.TextInput(attrs={'class': 'form-control col-md-col-lg-8'}))
    content = forms.CharField(label="new content", widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8'}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput, required=False)

def createPage(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if (util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            else:
                return render(request, "encyclopedia/createPage.html", {
                    "form": form,
                    "found": True,
                    "entry": title
                })
        else:
            return render(request, "encyclopedia/createPage.html", {
                "form": form,
                "found": False
            })
    else:
        return render(request, "encyclopedia/createPage.html", {
            "form": NewEntryForm(),
            "found": False
        })


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    markdown = Markdown()
    entryPage = util.get_entry(entry)

    if entryPage is None:
        return render(request, "encylopedia/notMatchEntry.html")

    else:
        return render(request, "encyclopedia/entry.html", {
            "entry" : markdown.covert(entryPage),
            "entryTitle": entry

    })

def search(request):
    value = request.GET.get('q','')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", Kwargs={'entry': value }))
    
    else:
        Entries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                Entries.append(entry)

        return render(request, "encyclopedia/index.html", {
            "entries": Entries,
            "search": True,
            "value": value
        })
 
def creatPage(request):
    return render(request, "encyclopedia/creatPage.html")