from django.http import HttpResponse
from django.shortcuts import render
import csv
import random


def index(request):
    name_csv_reader = csv.reader(open("resources/names.csv"))
    selected_names_csv_reader = csv.reader(open("resources/selected_names.csv"))

    names_list = []
    selected_names_list = []

    for row in name_csv_reader:
        names_list.append(row[0])

    for row in selected_names_csv_reader:
        selected_names_list.append(row[0])

    names_list.sort()
    selected_names_list.sort()

    context = {
        'names_list': names_list,
        'selected_names_list': selected_names_list,
    }
    return render(request, 'generator/index.html', context)


def generate_names(request):
    csv_reader = csv.reader(open("resources/names.csv"))
    selected_csv_reader = csv.reader(open("resources/selected_names.csv"))

    names_list = []
    selected_names = []

    for row in csv_reader:
        names_list.append(row[0])

    pre_selected_names = []
    for row in selected_csv_reader:
        pre_selected_names.append(row[0])

    while len(names_list) < 4:
        names_list.append(random.choice(pre_selected_names))

    i = 0
    while i < 4:
        i += 1
        name = random.choice(names_list)
        selected_names.append(name)
        names_list.remove(name)
        pre_selected_names.append(name)

    email = open("resources/email_template.txt", "r").read().format(selected_names[0], selected_names[1], selected_names[2], selected_names[3])

    email_file = open("resources/email.txt", "w+")
    email_file.write(email)
    email_file.close()

    if len(names_list) == 0:
        open('resources/selected_names.csv', 'w').close()
        write_list_to_file(list(dict.fromkeys(pre_selected_names)), "resources/names.csv")
    else:
        write_list_to_file(pre_selected_names, "resources/selected_names.csv")
        write_list_to_file(names_list, "resources/names.csv")

    return HttpResponse()


def write_list_to_file(pre_selected_names, resource):
    open(resource, 'w').close()
    for x in pre_selected_names:
        open(resource, "a+").write(x + "\n")
