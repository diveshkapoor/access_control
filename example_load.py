#!/usr/bin/env python

import access_control.load


# create access control list
load = access_control.load.Registry()

# add roles
load.add_role("member")
load.add_role("student", ["member"])
load.add_role("teacher", ["member"])
load.add_role("junior-student", ["student"])

# add resources
load.add_resource("course")
load.add_resource("senior-course", ["course"])

# set rules
load.allow("member", "view", "course")
load.allow("student", "learn", "course")
load.allow("teacher", "teach", "course")
load.deny("junior-student", "learn", "senior-course")

# use load to check permission
if load.is_allowed("student", "view", "course"):
    print("Students can view courses.")
else:
    print("Students can not view courses.")

# use load to check permission again
if load.is_allowed("junior-student", "learn", "senior-course"):
    print("Junior students can learn senior courses.")
else:
    print("Junior students can not learn senior courses.")
