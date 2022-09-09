#! /usr/bin/env python3
import sys

from solid import scad_render_to_file,color
from solid.objects import cube, cylinder, difference, translate, union, hull, rotate,circle,sphere
from solid.utils import right,left,up,down,minkowski,rotate_extrude,distribute_in_grid,linear_extrude
from math import sin,cos,pi

SEGMENTS = 48
wall = 3

#def Create_Box(dimensions, minkowski=False, inserts=[1], minkowski_insert=False):
def Create_Box(dimensions, minkowski=False):

    box = (cube([0,0,0]))

    if(minkowski):
        box = (Create_Round_Box(dimensions,wall))
    else:
        box = (cube([dimensions]))

    return box

def Create_Inserts(dimensions, radius, insert_rows=1, insert_columns=1,
                   row_gap=4, column_gap=4, height_gap=4, shape='cylinder'):

    valid_shapes = {'cylinder','sphere'}
    if shape not in valid_shapes:
        raise ValueError("Invalid sim type. Expected one of: %s" % valid_shapes)

    x,y,z = dimensions

    insert_x = (x - ((insert_rows + 1) * row_gap)) / insert_rows
    insert_y = (y - (insert_columns + 1) * column_gap) / insert_columns
    insert_z = z
    insert_dimensions = [insert_x, insert_y, insert_z]

    _template = Create_Round_Box(insert_dimensions, radius)
    inserts = (cube([0,0,0]))
    for row in range(insert_rows):
        for column in range(insert_columns):
            offset = [row * (row_gap + insert_x), column * (column_gap + insert_y), 0]
            inserts += translate(offset)(_template)

    inserts = translate([row_gap, column_gap, height_gap])(inserts)
    return inserts;

def Create_Round_Box(dimensions, radius, shape='cylinder'):
    """"box with rounded edges."""

    valid_shapes = {'cylinder','sphere'}
    if shape not in valid_shapes:
        raise ValueError("Invalid sim type. Expected one of: %s" % valid_shapes)

    x,y,z = dimensions
    x = x - radius * 2
    y = y - radius * 2
    z = z - 1 if shape == 'cylinder' else z - radius * 2

    round_box = (cube([x, y, z]))

    if shape == 'cylinder':
        round_box = minkowski()(round_box)(cylinder(r=radius))
    if shape == 'sphere':
        round_box = minkowski()(round_box)(sphere(r=radius))
        # Move the box up as the Miknowski adds 1 radius to the bottom
        round_box = translate([0,0,radius])(round_box)

    # Translate the box back into the centre
    round_box = translate([radius,radius,0])(round_box)

    return round_box