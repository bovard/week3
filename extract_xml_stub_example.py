#! /usr/local/bin/python
#reference website http://docs.python.org/2.7/library/xml.etree.elementtree.html
"""
Write a python program to process "enwiki-latest-stub-articles1.xml" file for the following tasks:
1. collect all page ids and title names for pages whose title starts with either "Afghanistan" or "America". Write this info into the file named pages.txt in the following format:

<page id>, <page title>

2. for each of those in (1) above, find contributor username and their id. Write this info into file named "users.txt" in the following format:

<conributor id>, <conributor name>


3. From (1) and (2) above, get page id and  conributor id and write into the file named page_users.txt in the following format:

<page id>, <conributor name>


4. What is the number of pages which start with either "Afghanistan" or "America" (case-sensitive)


Note: there are some pages which do not have usernames for contributors, ignore task (2) and (3) for such cases
eg:  <title>Afghanistan (1911 Encyclopedia)</title> has contibutor <ip>96.251.199.116</ip>
i.e, it does not have username and userid

Also Note: Unicode UTF-8 encoding is used in the XML data. This is not an issue
for reading or writing to files (which is done on a byte-by-byte basis) but
may cause error when printing to the terminal. This is a messy issue concerned
with locales, the codecs used for IO to stdout, etc. But if you get an 
error like "UnicodeEncodeError: 'ascii' codec can't encode character u'\xf3' in position 8: ordinal not in range(128)" it means that you need to set a
PYTHONIOENCODING environment variable to UTF-8. In csh or tcsh this
can be done with "setenv PYTHONIOENCODING UTF-8" before starting python. For
bash you can use "export PYTHONIOENCODING=UTF-8"


"""
import os
from xml.etree import ElementTree


# Load and parse an XML file
def parseXmlFile(fname):
    try:
        tree = ElementTree.parse(fname)
    except Exception as inst:
        print ("error opening file: %s", inst)
        return
    return tree



def main():
    # open up the output files
    ftitle = open("pages.txt", 'w')
    fuser = open("users.txt", 'w')
    ftile_user = open("page_users.txt", 'w')
    # read and parse the xml data into an element tree
    tree = parseXmlFile("./enwiki-latest-stub-articles1.xml")
    if tree is None:
        raise Exception('no XML!')
    root = tree.getroot()
    print "Root of the XML is %s", root.tag

    #to get the list of titles in all the docs
    count = 0
    for child in root.iter('page'):
        # this iterates over every page in the data
        # use the elementree 'find' method
        # e.g. if child.find('tag name to find').text...
        # to find the direct children of the page element
        # see https://docs.python.org/2/library/xml.etree.elementtree.html
        # for a tutorial on the elementtree library
        page_title = child.find('title').text
        page_id = child.find('id').text
        if page_title.startswith(('America', 'Afghanistan')):
            count += 1
            ftitle.write('{}, {}\n'.format(page_id, page_title))

            contributor = child.find('contributor')
            if contributor:
                username = contributor.find('username').text
                user_id = contributor.find('id').text

                fuser.write('{}, {}\n'.format(user_id, username))
                ftile_user.write('{}, {}\n'.format(page_id, user_id))

    print 'Found {} pages that start with America or Afghanistan'.format(count)

    ftitle.close()
    fuser.close()
    ftile_user.close()

if __name__ == '__main__':
    main()





