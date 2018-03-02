#!/usr/bin/env python

import sys
import getpass
from collections import namedtuple
from lxml import objectify
from project import Project
from importer import Importer


def read_xml_sourcefile(file_name):
  all_text = open(file_name).read()
  return objectify.fromstring(all_text)


try:
    from config import *

    Options = namedtuple("Options", "user passwd account repo")
    opts = Options(user=user, passwd=passwd, account=account, repo=repo)

except:
    print """
        A config.py file is required, defining these variables:

        jiraProj  # JIRA project name to use
        account   # GitHub account name
        repo      # GitHub project name
        user      # GitHub username
        passwd    # GitHub password
        file_name # Path to JIRA XML query file
    """
    sys.exit()

all_xml = read_xml_sourcefile(file_name)

project = Project(jiraProj)

for item in all_xml.channel.item:
  project.add_item(item)

project.merge_labels_and_components()
project.prettify()

'''
Steps:
  1. Create any milestones
  2. Create any labels
  3. Create each issue with comments, linking them to milestones and labels
  4: Post-process all comments to replace issue id placeholders with the real ones
'''
importer = Importer(opts, project)

importer.import_milestones()
importer.import_labels()
importer.import_issues()
importer.post_process_comments()
