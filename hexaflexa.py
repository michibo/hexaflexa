
#
#   This program makes hexaflexagon printouts.
#   
#   Author: Michael Borinsky
#   License: GPL
#   
#   programmed with love in 2016
#   

from math import *
import cairo

import argparse

def drawTriangle(ctx, a, b, h, k, tune):
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

def drawOutline(ctx, a, b, h):
    curpt = ctx.get_current_point()

    for k in range(0, 19):
        for tune in ["dur", "moll"]:
            drawTriangle( ctx, a, b, h, k, tune )

            ctx.set_source_rgb (0.0, 0.0, 0.0)
            ctx.set_line_width (1)
            ctx.stroke ()

            ctx.move_to(*curpt)

def transformToTextureSpace(ctx, a, b, h, tune, ori, trans, img_width, img_height, m):
    translation = { "dur" : {   
                                "stone"   : [ (0, 0), (-h, b) ], 
                                "scissor" : [ (0, -a), (-h, -b) ], 
                                "paper"   : [ (-h, -b), (0, 0) ] 
                            },
                    "moll" : {  
                                "stone"   : [ (0, 0), (0, 0) ], 
                                "scissor" : [ (h, -b), (h, -b) ] 
                             }
                  }

    rotation    = { "dur" :  {  
                                "stone"   : [ 0, 2 ],
                                "scissor" : [ -4, 6 ],
                                "paper"   : [ -4, 2 ],
                             },
                    "moll" : {  
                                "stone"   : [ 2, 0 ], 
                                "scissor" : [ -4, -6 ] 
                             }
                  }

    dx, dy = translation[tune][ori][trans]
    rot    = 2*pi/12 * ( rotation[tune][ori][trans] + 2*m )

    ref_size = min(img_width, img_height)
    scale = 2*a/ref_size

    x,y = ctx.get_current_point()

    ctx.translate(x+dx, y+dy)
    ctx.scale(scale, scale)
    ctx.rotate(rot)

    ctx.translate(-.5*img_width, -.5*img_height)

def drawPicture(ctx, a, b, h, face, ori, img):
    curpt = ctx.get_current_point()

    if face < 3:
        tune = "dur"
    else:
        tune = "moll"

    alpha = 0.4
    img_width, img_height = img.get_width(), img.get_height()
    pat = cairo.SolidPattern(0.0, 0.0, 0.0, alpha) 

    for m in range(0,6):
        if tune == "dur":
            k = 1 + 3*m + face
        elif tune == "moll":
            k = m%2 + 2*(face-3+3*(m//2))

        trans = k%2

        drawTriangle(ctx, a, b, h, k, tune)

        ctx.save()
        
        transformToTextureSpace(ctx, a, b, h, tune, ori, trans, img_width, img_height, m)

        ctx.clip()
        ctx.set_source_surface(img)

        if tune == "dur" and ori == "paper":
            ctx.mask(pat)
        else:
            ctx.paint()

        ctx.restore()

        ctx.move_to(*curpt)


def main():
    parser = argparse.ArgumentParser(description='Make a hexaflexagon with a picture printed on each of the six faces.')
    parser.add_argument('pics', type=str, nargs='+',
                        help='Filenames to pictures (only png).')
    parser.add_argument('--output', type=str,
                        help='Output filename (pdf).', default="out.pdf")
    parser.add_argument('--paper', type=str,
                        help='Paper size', default="A4");

    args = parser.parse_args()

    # The units for pdf size is a point=1/72inch
    if (args.paper.upper() == 'A4'):
        WIDTH, HEIGHT = 595, 842
    elif (args.paper.upper() == 'LETTER'):
        WIDTH, HEIGHT = 612, 792
    elif (args.paper.upper() == 'LEGAL'):
        WIDTH, HEIGHT = 612, 1008
    elif (args.paper.upper() == 'TABLOID'):
        WIDTH, HEIGHT = 792, 1224
    else:
        print("Paper type not understood: '"+args.paper+"'")
        sys.exit(1)

    surface = cairo.PDFSurface(args.output, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)

    border = .75 * 72.0 / 2.54   # border = 3/4cm
    a = (HEIGHT - 2*border)/10   # eq. triangle side, we need 10 down the spine
    b = a/2                      # half-side of eq. triangles
    h = sqrt(3)/2 * a            # height of eq.triangles
    n = int(WIDTH / (h*2));      # this is how many will fit in the paper's width

    for i in range(n):
        ctx.move_to( border + i*(2*h), border )

        commonfaces         = list(zip(range(0,3), ["scissor"] * 3))
        hiddenfaces         = list(zip(range(3,6), ["scissor"] * 3))
        transparentfaces    = list(zip(range(0,3), ["paper"]   * 3))

        for pic_fn, (face, ori) in zip(args.pics, commonfaces + hiddenfaces + transparentfaces):
            img = cairo.ImageSurface.create_from_png(pic_fn)

            drawPicture(ctx, a, b, h, face, ori, img)

        drawOutline(ctx, a, b, h)

    surface.show_page()

if __name__ == "__main__":
    main()

