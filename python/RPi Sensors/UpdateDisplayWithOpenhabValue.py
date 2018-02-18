#!/usr/bin/python
# -*- coding: utf-8 -*-

import openhab
import display

# Create display
display = display.Display()

value = openhab.get_item("Present")

display.set_line_1("# Status #",1,True)
display.set_line_2("Present:"+str(value.text),2,False)

