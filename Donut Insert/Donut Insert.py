#! /usr/bin/env python3
import sys

from solid import scad_render_to_file
from solid.objects import cube, cylinder, difference, translate, union, hull, rotate
from solid.utils import right,left,up,down,minkowski,rotate_extrude,distribute_in_grid
from math import sin,cos,pi

SEGMENTS = 48
wall = 3

def create_donut(diameter, outer_wall, height, solid_bottom):
    inner_diameter = diameter - (outer_wall * 2)
    donut = (cylinder(d=diameter,h=height))

    if(solid_bottom):
            z_offset = wall
    else:
            z_offset = -wall

    inner_hole = translate([0, 0, z_offset])(cylinder(d=inner_diameter, h=height + wall * 2))
    donut -= inner_hole
    return donut

def donut_insert():
    insert_diameter = 20
    height = 20
    number_of_stacks = 5
    solid_bottom = False
    """ Calculated Variables """
    # Determine the diameter of the circle
    #  - Calc circumference, number of stack with extra space
    #  - Calc diameter, circumference / pi
    outer_diameter = insert_diameter * number_of_stacks * 2 / pi
    # Make the out wall thickness slightly less than the insert
    outer_wall_thickness = insert_diameter - 1.5

    donut = create_donut(outer_diameter, outer_wall_thickness, height, solid_bottom)
    rotate_step = 360 / number_of_stacks
    stack = (cylinder(d=insert_diameter, h=height))
    stack = translate([outer_diameter / 2 - outer_wall_thickness / 2, 0, wall])(stack)
    for i in range(number_of_stacks):
        donut -= rotate([0,0,i * rotate_step])(stack)

    lid = (cylinder(d=outer_diameter + wall, h = wall * 2))
    lid -= (translate([0,0,wall]))(cylinder(d=outer_diameter, h = wall+1))
    lid = (translate([75,0,0]))(lid)
    all_objects = [donut, lid]
    return distribute_in_grid(all_objects,max_bounding_box=[5,5],rows_and_cols=[len(all_objects),1],)

if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else None

    a = donut_insert()

    file_out = scad_render_to_file(a,out_dir, file_header=f'$fn = {SEGMENTS};')
    print(f"{__file__}: SCAD file written to: \n{file_out}")