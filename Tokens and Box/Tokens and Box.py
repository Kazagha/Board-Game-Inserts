#! /usr/bin/env python3
import sys

from solid import scad_render_to_file,color
from solid.objects import cube, cylinder, difference, translate, union, hull, rotate,circle
from solid.utils import right,left,up,down,minkowski,rotate_extrude,distribute_in_grid
from math import sin,cos,pi

SEGMENTS = 48
wall = 3

def tokens_and_insert():
    height = 22
    token_diameter = 20
    number_of_tokens = 5
    length = 100
    # Calculated Variables
    width = (token_diameter + wall) * number_of_tokens + (wall * 2)

    token = (cylinder(d=token_diameter, h=height + wall))
    all_tokens = (cube([0,0,0]))
    for i in range(number_of_tokens):
        all_tokens += translate([((token_diameter + wall) * i  ),0,0])(token)

    token_box = (cube([width,token_diameter, height + wall]))
    token_box -= translate([(token_diameter / 2) + wall, (token_diameter / 2) - wall, wall])(all_tokens)

    #distribute_in_grid(all_objects, max_bounding_box=[5, 5], rows_and_cols=[len(all_objects), 1], )

    return token_box

if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else None

    a = tokens_and_insert()

    file_out = scad_render_to_file(a,out_dir, file_header=f'$fn = {SEGMENTS};')
    print(f"{__file__}: SCAD file written to: \n{file_out}")