from PIL import Image
import glob
import itertools
import random

_id = 0
for tilename in glob.glob('tiles/*.png'):
    tile = Image.open(tilename).convert("RGBA")
    for piecename in glob.glob('pieces/*.png'):
        piece = Image.open(piecename).convert("RGBA")
        new_tile = tile.copy()
        new_tile.paste(piece, (0, 0), mask = piece)
        name = int(piecename.replace('pieces/','').replace('.png',''))
        piece_id = name % 6
        color_id = 1 if (name % 12) > 5 else 0
        new_tile.save(f'dataset/{str(_id).zfill(5)}_{color_id}_{piece_id}_.png', "PNG")#
        _id += 1

tile_names = []
for tilename in glob.glob('tiles/*.png'):
    tile_names.append(tilename)

iterator_tiles = iter(itertools.cycle(tile_names))
for i in range(1300):
    tilename = next(iterator_tiles)
    tile = Image.open(tilename).convert("RGBA")
    tile = tile.copy()
    choice = random.choice([0, 1])
    tile.save(f'dataset/{str(_id).zfill(5)}_{choice}_{6}_.png', "PNG")#
    _id += 1
