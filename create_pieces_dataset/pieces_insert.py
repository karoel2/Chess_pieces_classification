from PIL import Image
import glob

_id = 0
pieces
for tilename in glob.glob('tiles/*.png'):
    tile = Image.open(tilename).convert("RGBA")
    for piecename in glob.glob('pieces/*.png'):
        piece = Image.open(piecename).convert("RGBA")
        new_tile = tile.copy()
        new_tile.paste(piece, (0, 0), mask = piece)
        tile_id = int(tilename.replace('tiles/','').replace('.png','')) % 2
        pice_id = int(piecename.replace('pieces/','').replace('.png','')) % 6
        new_tile.save(f'dataset/{str(_id).zfill(6)}_{tile_id}_{piece_id}_.png', "PNG")#
        _id += 1
