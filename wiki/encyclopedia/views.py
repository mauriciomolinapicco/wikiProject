from django.shortcuts import render
from django.utils.safestring import mark_safe
import markdown
from . import util
from django import forms
import random


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    body = forms.CharField(label="Body")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    
    if util.get_entry(entry) is None:
        return render(request, "encyclopedia/error.html")
    else:
        contentMarkdown = util.get_entry(entry)
        contentHtml = mark_safe(markdown.markdown(contentMarkdown))
        return render(request, "encyclopedia/entry.html", {
        "content": contentHtml,
        "title": entry
    })


def search(request):
    if request.method == 'POST':
        entry_search = request.POST['q'] #q es el tag name en html
        entries = util.list_entries()

        if entry_search in entries:
            contentMarkdown = util.get_entry(entry_search)
            contentHtml = mark_safe(markdown.markdown(contentMarkdown))
            return render(request, "encyclopedia/entry.html", {
                "content": contentHtml,
                "title": entry_search.upper()
            })

        recommendation = []
        for entry in entries:
            if entry_search.lower() in entry.lower():
                recommendation.append(entry)
        return render(request, "encyclopedia/search.html", {
            "recommendations": recommendation
        })


def newpage(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST["content"]
        
        titleExists = util.get_entry(title)
        if titleExists is not None:
            return render(request, "encyclopedia/error.html",{
                "message": "Entry page already exists"
            })

        else:
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html",{
                "content": mark_safe(markdown.markdown(content)),
                "title": title
            })

    else:
        return render(request, "encyclopedia/newpage.html",{
            "form": NewPageForm()
        })


def randompage(request):
    random_entry = random.choice(util.list_entries())

    contentMarkdown = util.get_entry(random_entry)
    contentHtml = mark_safe(markdown.markdown(contentMarkdown))
    return render(request, "encyclopedia/entry.html", {
        "content": contentHtml,
        "title": random_entry
    })


def editpage(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/editpage.html",{
            "title": title,
            "content": content
        })


def save_edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        util.save_entry(title, content)

        contentMarkdown = util.get_entry(title)
        contentHtml = mark_safe(markdown.markdown(contentMarkdown))
        return render(request, "encyclopedia/entry.html", {
            "content": contentHtml,
            "title": title
        })