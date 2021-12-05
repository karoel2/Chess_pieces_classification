from PIL import Image, ImageOps
import glob
import random
import itertools

GREYSCALE = True
FULL_IMG = False
# PADDING = True

_MODE = 'L' if GREYSCALE == True else 'RGBA'
_COLOR = (0) if _MODE == 'L' else (0,0,0,0)

pieces_names = []
for filename in glob.glob('pieces/*.png'):
    pieces_names.append(filename)
size = 96 #image_list[0].size
webpages_names = []
for filename in glob.glob('webimg/*.jpg'):
    webpages_names.append(filename)# 1440 x 900


def create_new_boards():
    tile_list = []
    for filename in sorted(glob.glob('tiles/*.png'), key = lambda i: (len(i), i)):
        im = Image.open(filename).convert(_MODE)
        tile_list.append(im)

    def pairwise(iterable):
        "s -> (s0, s1), (s2, s3), (s4, s5), ..."
        a = iter(iterable)
        return zip(a, a)

    boards = []
    for white, black in pairwise(tile_list):
        line = Image.new(_MODE, (8*96, 96), _COLOR)
        for i in range(4):
            line.paste(white, (i*96*2, 0), mask = white)
            line.paste(black, ((i*96*2)+96, 0), mask = black)
        fliped = line.copy()
        fliped = fliped.transpose(method=Image.FLIP_LEFT_RIGHT)
        board = Image.new(_MODE, (8*96, 8*96), _COLOR)
        for i in range(4):
            board.paste(line, (0, i*96*2), mask = line)
            board.paste(fliped, (0, (i*96*2)+96), mask = fliped)
        boards.append(board)
    return boards

def set_board(pieces_names, board):
    board = board.copy()
    choices = [0.1, 0.2, 0.3, 0.4, 0.5]
    choice_threshold = random.choice(choices)
    y = 0
    for i in range(8):
        x = 0
        for j in range(8):
            choice_value = random.uniform(0, 1)
            if choice_value < choice_threshold:
                piece = random.choice(pieces_names)
                piece_img = Image.open(piece).convert(_MODE)
                board.paste(piece_img, (x, y), mask = piece_img)
            x += size
        y += size
    return board

_part = 0
_id = -1

def generate_board(number):
    boards = create_new_boards()
    iterator_board = iter(itertools.cycle(boards))
    iterator_webpage = iter(itertools.cycle(webpages_names))
    for i in range(number):
        empty_board = next(iterator_board)
        webpage = next(iterator_webpage)
        generated_board = set_board(pieces_names, empty_board)
        rand_size_board2(generated_board, webpage)

def rand_size_board2(generated_board, webpage_name):
    global _part, _id
    size = random.randrange(320, 800, 8)
    half_size = size/2
    generated_board = generated_board.resize((size,size))
    webimage = Image.open(webpage_name).convert(_MODE)
    webimage = webimage.copy()

    if FULL_IMG:
        webimage_w, webimage_h = webimage.size
    else:
        webimage_h = random.randint(size, 900)
        webimage_w = random.randint(size, 1440)
        webimage = webimage.crop((0, 0, webimage_w, webimage_h))

    new_h = random.randint(0, webimage_h - size)
    new_w = random.randint(0, webimage_w - size)

    webimage.paste(generated_board, (new_w, new_h))

    if FULL_IMG:
        webimage = webimage.resize((512,320))
    else:
        if webimage_w >= webimage_h:
            webimage = webimage.resize((512, webimage_h*512//webimage_w))
        else:
            webimage = webimage.resize((webimage_w*512//webimage_h, 512))

    # size_w, size_h = webimage.size
    #
    # h, w, hh, ww = 1, 1, 0, 0
    # if PADDING:
    #     padded = Image.new(_MODE, (512, 512), _COLOR)
    #     if size_w < size_h:
    #         padded.paste(webimage, ((512-size_w)//2, 0))
    #         webimage = padded
    #         w = 512/size_w
    #         ww = (size_w - 512) / 2
    #     elif size_w > size_h:
    #         padded.paste(webimage, (0, (512-size_h)//2))
    #         webimage = padded
    #         h = 512/size_w
    #         hh = (size_h - 512) / 2
    # # print(webimage.size)

    if _id % 5000 == 0:
        _part += 1
    _id += 1

    with open(f'dataset_{_part}/{_id}.txt', "w") as f:
        f.write(f'0 {(new_w + half_size)/webimage_w} {(new_h + half_size)/webimage_h} {size/webimage_w} {size/webimage_h}')
    webimage.save(f'dataset_{_part}/{_id}.png', "PNG")

if __name__ == "__main__":
    import time
    start = time.time()

    generate_board(20000)

    end = time.time()
    print(end - start)
