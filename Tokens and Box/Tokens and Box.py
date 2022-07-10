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
    tolerence = 0.25

    # Calculated Variables
    width = (token_diameter + wall) * number_of_tokens + (wall)
    main_box_length = width / 2
    token_box_length = token_diameter

    # Create the token inserts
    token = (cylinder(d=token_diameter, h=height))
    all_tokens = (cube([0,0,0]))
    for i in range(number_of_tokens):
        all_tokens += translate([((token_diameter + wall) * i  ),0,0])(token)

    # Create the token section of the box
    token_box = (cube([width,token_box_length, height]))
    token_box -= translate([(token_diameter / 2) + wall, (token_diameter / 2) - wall, wall])(all_tokens)

    # Create the main box with an insert
    main_box = (cube([width, main_box_length, height]))
    insert = translate([wall,wall,wall])(cube([width - wall * 2, width / 2 - wall * 2, height]))
    main_box -= insert

    # Add the main box and token section together
    # Overlapping 1 wall thickness
    main_box = translate([0,token_diameter - wall,0])(main_box) + token_box

    # Create the lid with small inner lip
    lid_thickness = 2
    lip_width = width - (wall * 2) - (tolerence * 2)
    lip_length = main_box_length - (wall * 2) - (tolerence * 2)
    # Create main lid
    lid = (cube([width, main_box_length + token_box_length - wall, lid_thickness]))
    # Create the lip
    lid_lip = (cube([lip_width, lip_length, lid_thickness]))
    # Remove the insert
    lid_lip -= translate([wall,wall,-1])(cube([lip_width - wall * 2, lip_length - wall * 2, lid_thickness + 2]))
    # Position the lip
    lid_lip = translate([wall + tolerence, token_box_length + tolerence, lid_thickness])(lid_lip)
    # Add the lip to the lid
    lid += lid_lip

    # Combine all objects for output
    all_objects = [main_box, lid]
    all_objects = distribute_in_grid(all_objects
                                     ,max_bounding_box=[width + 25,main_box_length + 25]
                                     ,rows_and_cols=[len(all_objects),1],)

    return all_objects

if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else None

    a = tokens_and_insert()

    file_out = scad_render_to_file(a,out_dir, file_header=f'$fn = {SEGMENTS};')
    print(f"{__file__}: SCAD file written to: \n{file_out}")