from django.http import HttpResponse
from django.shortcuts import render
import csv
import random

RESOURCES_EMAIL_TXT = "resources/email.txt"
EMAIL_TEMPLATE_TXT = "resources/email_template.txt"
SELECTED_NAMES_CSV = "resources/selected_names.csv"
NAMES_CSV = "resources/names.csv"


def index(request):
    names_list = get_list_of_names(NAMES_CSV)
    selected_names_list = get_list_of_names(SELECTED_NAMES_CSV)

    names_list.sort()
    selected_names_list.sort()

    context = {
        'names_list': names_list,
        'selected_names_list': selected_names_list,
    }
    return render(request, 'generator/index.html', context)


def generate_names(request):

    names_list = get_list_of_names(NAMES_CSV)
    pre_selected_names = get_list_of_names(SELECTED_NAMES_CSV)
    add_extra_names(names_list, pre_selected_names)
    selected_names = generate_list_of_selected_names(names_list, pre_selected_names)
    email = generate_email(selected_names)

    if len(names_list) == 0:
        open(SELECTED_NAMES_CSV, 'w').close()
        write_list_to_file(list(dict.fromkeys(pre_selected_names)), NAMES_CSV)
    else:
        write_list_to_file(pre_selected_names, SELECTED_NAMES_CSV)
        write_list_to_file(names_list, NAMES_CSV)

    return HttpResponse(email)


def add_extra_names(names_list, pre_selected_names):
    while len(names_list) < 4:
        names_list.append(random.choice(pre_selected_names))


def generate_list_of_selected_names(names_list, pre_selected_names):
    selected_names = []
    i = 0
    while i < 4:
        i += 1
        name = random.choice(names_list)
        selected_names.append(name)
        names_list.remove(name)
        pre_selected_names.append(name)

    return selected_names


def get_list_of_names(resource):
    names_list = []
    csv_reader = csv.reader(open(resource))
    for row in csv_reader:
        names_list.append(row[0])
    return names_list


def generate_email(selected_names):
    email = open(EMAIL_TEMPLATE_TXT, "r").read().format(selected_names[0], selected_names[1], selected_names[2], selected_names[3])
    email_file = open(RESOURCES_EMAIL_TXT, "w+")
    email_file.write(email)
    email_file.close()
    return email


def write_list_to_file(pre_selected_names, resource):
    open(resource, 'w').close()
    for x in pre_selected_names:
        open(resource, "a+").write(x + "\n")
