import secrets
from django.urls import reverse
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from markdown import Markdown

from . import util



class NewEntryForm(forms.Form):
    title = forms.CharField(label="new title", widget=forms.TextInput(attrs={'class': 'form-control col-7 md-col-lg-7'}))
    content = forms.CharField(label="new content", widget=forms.Textarea(attrs={'class': 'form-control col-7 md-7 col-lg-7'}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

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
    markdownn = Markdown()
    entryPage = util.get_entry(entry)

    if entryPage is None:
        return render(request, "encylopedia/notMatchEntry.html", {
            "entryTitle" : entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry" : markdownn.convert(entryPage),
            "entryTitle": entry 
    })

def search(request):
    value = request.GET.get('q')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': value}))
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

def edit(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/notMatchEntry.html", {
            "entryTitle": entry 
        })
    else:
        form = NewEntryForm()
        form.fields["title"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/createPage.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "entryTitle": form.fields["title"].initial
        })

def random(request):
    entries = util.list_entries()
    randomEntry = secrets.choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={"entry": randomEntry}))