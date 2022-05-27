#! /usr/bin/env python3
import sys

from solid import scad_render_to_file
from solid.objects import cube, cylinder, difference, translate, union, hull, rotate
from solid.utils import right,left,up,down,minkowski
from math import sin,cos

SEGMENTS = 48

def donut_insert():
    outer_diameter = 100
    insert_diameter = 20
    wall = 3
    height = 20
    solid_bottom = True

    inner_diameter = outer_diameter - insert_diameter - (wall * 2)
    donut = (cylinder(d=outer_diameter,h=height))
    inner_hole = (cylinder(d=inner_diameter, h=height + wall * 2))

    if(solid_bottom):
            z_offset = wall
    else:
            z_offset = -wall

    inner_hole = translate([0, 0, z_offset])(cylinder(d=inner_diameter, h=height + wall * 2))
    donut -= inner_hole

    return donut

if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else None

    a = donut_insert()

    file_out = scad_render_to_file(a,out_dir, file_header=f'$fn = {SEGMENTS};')
    print(f"{__file__}: SCAD file written to: \n{file_out}")