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

    return (cube([1,1,1]))

if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else None

    a = tokens_and_insert()

    file_out = scad_render_to_file(a,out_dir, file_header=f'$fn = {SEGMENTS};')
    print(f"{__file__}: SCAD file written to: \n{file_out}")