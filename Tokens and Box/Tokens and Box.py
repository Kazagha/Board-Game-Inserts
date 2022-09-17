#! /usr/bin/env python3
import sys

from solid import scad_render_to_file,color
from solid.objects import cube, cylinder, difference, translate, union, hull, rotate,circle
from solid.utils import right,left,up,down,minkowski,rotate_extrude,distribute_in_grid
from Templates.Box_Template import Create_Box,Create_Round_Box
from math import sin,cos,pi

SEGMENTS = 48
wall = 2

def tokens_and_insert():
    height = 44 + wall
    token_diameter = 20
    number_of_tokens = 1
    # Smallest
    tolerence = 0.2
    edge_radius = 2

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
    token_box = (Create_Round_Box([width, token_box_length, height],radius=edge_radius))
    # Create a flat back where the two sections join together
    token_box = token_box + translate([0, token_box_length / 2, 0])(cube([width, token_box_length / 2, height]))
    token_box -= translate([(token_diameter / 2) + wall, (token_diameter / 2) - wall, wall])(all_tokens)

    # Create the main box with an insert
    main_box = Create_Round_Box([width, main_box_length, height], radius=2)
    insert = translate([wall, wall, wall])\
        (Create_Round_Box([width - wall * 2, width / 2 - wall * 2, height],radius=2,shape='sphere'))
    main_box -= insert

    # Add the main box and token section together
    # Overlapping 1 wall thickness
    main_box = translate([0,token_diameter - wall,0])(main_box) + token_box

    # Create a lip around the box for the lid to sit in
    # Dimensions of the whole box
    box_size = [width + wall, main_box_length + token_box_length - wall + wall, wall * 2]
    # Dimensions of the cut-out
    inner_wall = [box_size[0] - wall * 2, box_size[1] - wall * 2, box_size[2] + wall * 3]
    box_lip = Create_Round_Box(box_size,radius=edge_radius)
    box_lip_insert = translate([wall, wall, -wall])(Create_Round_Box(inner_wall,radius=2))
    box_lip -= box_lip_insert

    # Remove the lip from the main box
    box_lip = translate([-wall / 2, -wall / 2,height - wall])(box_lip)
    main_box -= box_lip

    # Create the lid with small inner lip
    # Create main lid based on inner wall, so it sits flush with the edge
    lid_size = [inner_wall[0] + wall, inner_wall[1] + wall, box_size[2]]
    lid = Create_Round_Box(lid_size, radius=2)
    # Create the lid insert
    insert_size = [lid_size[0] - wall * 1 + tolerence, lid_size[1] - wall * 1 + tolerence, lid_size[2]]
    lid_insert = Create_Round_Box(insert_size, radius=edge_radius)
    lid_insert = translate([wall / 2 - tolerence / 2, wall / 2 - tolerence / 2, wall])(lid_insert)
    lid -= lid_insert

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