#!/usr/bin/env python
#######################################
#
# Script to push a file to the database.
#
# Author: Matt Mottram
#         <m.mottram@sussex.ac.uk> 
#
#######################################

from orca_side import tellie_database, tellie_document
import argparse
import os
import json
import sys
import glob

db = None

def push_directory(directory, override):
    """Push all JSON files in a directory to the database.

    Assumes only .js suffixes are desired.
    """
    for fname in glob.glob(os.path.join(directory, "*.js")):
        push_file(fname, override)


def push_file(filename, override):
    """Push a file (.js format) to the database.
    """
    doc = tellie_document.assign_document(json.load(open(filename, 'r')))
    (view_name, view_key) = doc.unique_view()
    rows = db.db.view(view_name, key=view_key)
    if len(rows)!=0:
        if override is False:
            sys.stderr.write("Cannot save %s; matching document exists\n" % (filename))
        else:
            if len(rows)!=1:
                sys.stderr.write("Too many rows!")
            else:
                sys.stderr.write("Replacing document with %s; you'd better be careful!\n" % (filename))
                for row in rows:
                    old_doc = db.db[row.id]
                    doc["_id"] = old_doc.id
                    doc["_rev"] = old_doc.rev
                    db.db.save(doc)
    else:
        print "Pushing", filename
        db.db.save(doc)
    
def update_db():
    rows = db.db.view("_design/channels/_view/channel_by_number")
    for row in rows:
	    old_doc = db.db[row.id]
            if old_doc["run_range"][0] == 9436 and old_doc["run_range"][1] ==0:
	    	old_doc["run_range"] = [old_doc["run_range"][0],10417]
	    	print old_doc
    		#db.db.save(old_doc)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", dest="server", help="Database server [http://couch.snopl.us]",
                        default="http://couch.snopl.us")
    parser.add_argument("-n", dest="name", help="Database name [telliedb]", 
                        default="telliedb")
    parser.add_argument("--override", dest="override", help="Override existing docs (i.e. replace, retain document ID)\n\
***This option is for testing purposes only!***",
                        action="store_true")
    args = parser.parse_args()
    
    db = tellie_database.TellieDatabase.get_instance()
    db.login(args.server, args.name)

    update_db()

