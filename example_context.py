#!/usr/bin/env python

from access_control.load import Registry
from access_control.context import IdentityContext, PermissionDenied


# -----------------------------------------------
# build the access control list and add the rules
# -----------------------------------------------

load = Registry()
context = IdentityContext(load)

load.add_role("staff")
load.add_role("editor", parents=["staff"])
load.add_role("unauthorized ", parents=["staff"])
load.add_resource("main")

load.allow("staff", "view", "main")
load.allow("editor", "edit", "main")
load.deny("unauthorized ", None, "main")


# -------------
# to be a staff
# -------------

@context.set_roles_loader
def first_load_roles():
    yield "staff"


print("* Now you are %s." % ", ".join(context.load_roles()))


@context.check_permission("view", "main", message="can not view")
def main_page():
    return "<view>"


# use it as `decorator`
@context.check_permission("edit", "main", message="can not edit")
def edit_main_page():
    return "<edit>"


if main_page() == "<view>":
    print("You can view the main page.")

try:
    edit_main_page()
except PermissionDenied as exception:
    print("You can not edit the main page, ")
    print("the exception said: '%s'." % exception.kwargs['message'])

try:
    # use it as `with statement`
    with context.check_permission("edit", "main"):
        pass
except PermissionDenied:
    print("Maybe it's because you are not a editor.")


# --------------
# to be a editor
# --------------

@context.set_roles_loader
def second_load_roles():
    yield "editor"


print("* Now you are %s." % ", ".join(context.load_roles()))

if edit_main_page() == "<edit>":
    print("You can edit the main page.")


# ---------------
# to be a unauthorized person
# ---------------

@context.set_roles_loader
def third_load_roles():
    yield "unauthorized "


print("* Now you are %s." % ", ".join(context.load_roles()))

try:
    main_page()
except PermissionDenied as exception:
    print("You can not view the main page,")
    print("the exception said: '%s'." % exception.kwargs['message'])

# use it as `nonzero`
if not context.check_permission("view", "main"):
    print("Oh! A unauthorized  can not view the main page.")

# use it as `check function`
try:
    context.check_permission("edit", "main").check()
except PermissionDenied as exception:
    print("Yes, of course, a unauthorized  can not edit the main page too.")
