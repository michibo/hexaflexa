#!/usr/bin/env python

from math import *
import cairo

import argparse, itertools

def drawHexaflexaOutline(ctx, a):

    curpt = ctx.get_current_point()

    for k in range(0, 19):
        drawHexaFlexaTriangle( ctx, a, k, "dur" )

        ctx.set_source_rgb (0.0, 0.0, 0.0)
        ctx.set_line_width (1)
        ctx.stroke ()

        ctx.move_to(*curpt)

        drawHexaFlexaTriangle( ctx, a, k, "moll" )

        ctx.set_source_rgb (0.0, 0.0, 0.0)
        ctx.set_line_width (1)
        ctx.stroke ()

        ctx.move_to(*curpt)

def drawHexaFlexaPicture(ctx, a, face, ori, img):
    curpt = ctx.get_current_point()

    b = a/2
    h = sqrt(3)/2 * a

    if face < 3:
        tune = "dur"
    else:
        tune = "moll"

    scale1 = 2/5*1/2
    scale2 = 1/2

    width, height = img.get_width(), img.get_height()
    grad = cairo.RadialGradient(width//2, height//2, 
                            scale1*(width+height)//2, 
                            width//2, height//2, 
                            scale2*(width+height)//2)

    red   = 1.0 if face     % 3 == 0 else 0.0
    green = 1.0 if (face+1) % 3 == 0 else 0.0
    blue  = 1.0 if (face+2) % 3 == 0 else 0.0

    grad.add_color_stop_rgba( 0.2, red, green, blue, 0.3 )
    grad.add_color_stop_rgba( 0.7, red, green, blue, 0.3 )
    grad.add_color_stop_rgba( 1.0, red, green, blue, 0.3 )

    for m in range(0,6):
        if tune == "dur":
            k = 1 + 3*m + face
        else:
            k = m%2 + 2*(face-3+3*(m//2))

        trans = k%2

        drawHexaFlexaTriangle(ctx, a, k, tune)

        x,y = ctx.get_current_point()

        ctx.save()
        # tune X ori X major
        matrix_translation = \
            [ 
                [ [ (0, 0), (-h, b) ], [ (0, -a), (-h, -b) ], [ (-h, -b), (0, 0) ] ],
                [ [ (0, 0), (0, 0) ], [ (h, -b), (h, -b) ] ] 
            ]
        matrix_rot = \
            [ 
                [ [ -2*pi/12, 2*pi/12 ], [ -2*pi*5/12, 2*pi*5/12 ], [ 2*pi/4, -2*pi/4 ] ],
                [ [ 2*pi/4, 2*pi/12 ], [ -2*pi/4, -2*pi*5/12 ] ]
            ]

        tunes = { "dur" : 0, "moll" : 1 }
        oris = { "fire" : 0, "water" : 1, "earth" : 2 }
        dx, dy = matrix_translation[tunes[tune]][oris[ori]][trans]
        rot    = matrix_rot[tunes[tune]][oris[ori]][trans] + 2*pi/6*m + \
                ( 2*pi/12 if tune == "dur" else -2*pi/12 ) + \
                (-2*pi*2/3 if ori == "earth" else 0)

        ctx.translate(x+dx, y+dy)

        if tune == "dur" and ori == "earth":
            ref_size = sqrt(width*height)*2*.7
        else:
            ref_size = min(width,height)
        ctx.scale(2*a/ref_size, 2*a/ref_size)
        ctx.rotate(rot)

        ctx.translate(-.5*width, -.5*height)

        ctx.clip()
        ctx.set_source_surface(img)

        if tune == "dur" and ori == "earth":
            ctx.mask(grad)
        elif tune == "dur" and ori == "water":
            ctx.paint()
        elif tune == "moll":
            ctx.paint()

        ctx.restore()

        ctx.move_to(*curpt)


def drawHexaFlexaTriangle(ctx, a, k, tune):
    b = a/2
    h = sqrt(3)/2 * a
    num = 10

    trans = k % 2 == 0

    ctx.rel_move_to(h, a * (k//2+1))

    if tune == "moll":
        h = -h

    if trans:
        ctx.rel_line_to(-h, -b)
        ctx.rel_line_to(h, -b)
        ctx.rel_line_to(0, a)
    else:
        ctx.rel_line_to(-h, b)
        ctx.rel_line_to(0, -a)
        ctx.rel_line_to(h, b)

    ctx.close_path()

def main():
    WIDTH, HEIGHT = 595, 842
 
    parser = argparse.ArgumentParser(description='Make a hexaflexagon with pictures hidden in it.')
    parser.add_argument('pics', type=str, nargs='+',
                        help='Filenames to pictures (only png).')
    parser.add_argument('--output', type=str,
                        help='Output filename (pdf).', default="out.pdf")

    args = parser.parse_args()
    
    surface = cairo.PDFSurface (args.output, WIDTH, HEIGHT)
    ctx = cairo.Context (surface)

    border = 1 * 72.0 / 2.54
    size = (HEIGHT - 2*border)/10
    

    for i in range(3):
        ctx.move_to( border + i*(2*size), border )

        commonfaces = itertools.product(range(0,3), ["water", "earth"])
        hiddenfaces = itertools.product(range(3,6), ["water"])

        #for pic_fn, (face, ori) in zip(args.pics, itertools.chain(commonfaces, hiddenfaces)):
            #img = cairo.ImageSurface.create_from_png(pic_fn)
            #drawHexaFlexaPicture(ctx, size, face, ori, img)

        drawHexaflexaOutline(ctx, size)

    surface.show_page()

if __name__ == "__main__":
    main()

