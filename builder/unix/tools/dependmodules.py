#!/usr/bin/python
################################################################
#
#        Copyright 2013, Big Switch Networks, Inc.
#
# Licensed under the Eclipse Public License, Version 1.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#        http://www.eclipse.org/legal/epl-v10.html
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the
# License.
#
################################################################

###############################################################################
#
# Generates dependmodules.x
#
###############################################################################
import os
import sys

if len(sys.argv) == 1:
    print("usage: %s MACRO:MODULE [MACRO:MODULE] [MACRO:MODULE] ...")
    sys.exit(1);


macros = {}

#
# Parse all macro:module parameters into the macros dict
#
for arg in sys.argv[1:]:
    entry = arg.split(":")
    if(len(entry) != 2):
        raise Exception("bad arguments.")
    if not entry[0] in macros:
        macros[entry[0]] = []
    macros[entry[0]].append(entry[1])


# Print entries.
print("/* Autogenerated Module Dependencies. */\n")

for (macro, entries) in macros.items():
    m = "DEPENDMODULE_%s" % macro.upper()
    print("#ifdef %s" % m)
    for mod in entries:
        print("%s(%s)" % (m, mod))
    print("#undef %s" % m)
    print("#endif /* %s */\n" %m)

# The special 'build' class also gets native compilation defines
print("/* Preprocessor definitions for all modules included in this build. */")
for mod in macros['build']:
    print("""
#ifndef DEPENDMODULE_INCLUDE_%(MODULE)s
#define DEPENDMODULE_INCLUDE_%(MODULE)s
#endif
""" % dict(MODULE=mod.upper()))








