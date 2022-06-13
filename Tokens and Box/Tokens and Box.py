#! /usr/bin/env python3
import sys

from solid import scad_render_to_file,color
from solid.objects import cube, cylinder, difference, translate, union, hull, rotate,circle
from solid.utils import right,left,up,down,minkowski,rotate_extrude,distribute_in_grid
from math import sin,cos,pi

SEGMENTS = 48
wall = 3

def tokens_and_insert():
    height = 44 + wall
    token_diameter = 20
    number_of_tokens = 5

    # Calculated Variables
    width = (token_diameter + wall) * number_of_tokens + (wall)
    main_box_length = width / 2

    # Create the token inserts
    token = (cylinder(d=token_diameter, h=height))
    all_tokens = (cube([0,0,0]))
    for i in range(number_of_tokens):
        all_tokens += translate([((token_diameter + wall) * i  ),0,0])(token)

    # Create the token section of the box
    token_box = (cube([width,token_diameter, height]))
    token_box -= translate([(token_diameter / 2) + wall, (token_diameter / 2) - wall, wall])(all_tokens)

    # Create the main box with an insert
    main_box = (cube([width, main_box_length, height]))
    insert = translate([wall,wall,wall])(cube([width - wall * 2, width / 2 - wall * 2, height]))
    main_box -= insert

    # Add the main box and token section together 
    main_box += translate([0,-token_diameter + wall,0])(token_box)

    return main_box

if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else None

    a = tokens_and_insert()

    file_out = scad_render_to_file(a,out_dir, file_header=f'$fn = {SEGMENTS};')
    print(f"{__file__}: SCAD file written to: \n{file_out}")