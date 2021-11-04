from PIL import Image
import glob
import random
import itertools

pieces_names = []
for filename in glob.glob('pieces/*.png'):
    pieces_names.append(filename)
print(len(pieces_names))
size = 96 #image_list[0].size
webpages_names = []
for filename in glob.glob('webimg/*.jpg'):
    webpages_names.append(filename)# 1440 x 900
print(len(webpages_names))

# board = Image.open("board.png").convert("RGBA").resize((1600,1600))
#replace with function to make whole board

def create_new_boards():
    tile_list = []
    for filename in sorted(glob.glob('tiles/*.png'), key = lambda i: (len(i), i)):
        im = Image.open(filename).convert("RGBA")
        tile_list.append(im)

    def pairwise(iterable):
        "s -> (s0, s1), (s2, s3), (s4, s5), ..."
        a = iter(iterable)
        return zip(a, a)

    boards = []
    for white, black in pairwise(tile_list):
        line = Image.new('RGBA', (8*96, 96), color=(0,0,0,0))
        for i in range(4):
            line.paste(white, (i*96*2, 0), mask = white)
            line.paste(black, ((i*96*2)+96, 0), mask = black)
        fliped = line.copy()
        fliped = fliped.transpose(method=Image.FLIP_LEFT_RIGHT)
        board = Image.new('RGBA', (8*96, 8*96), color=(0,0,0,0))
        for i in range(4):
            board.paste(line, (0, i*96*2), mask = line)
            board.paste(fliped, (0, (i*96*2)+96), mask = fliped)
        boards.append(board)
    return boards

def generate_board(number):
    boards = create_new_boards()
    iterator_board = iter(itertools.cycle(boards))
    iterator_webpage = iter(itertools.cycle(webpages_names))
    for i in range(number):
        empty_board = next(iterator_board)
        webpage = next(iterator_webpage)
        generated_board = set_board(pieces_names, empty_board)#.save(f'dataset/chess{i}.png', "PNG")
        rand_size_board(generated_board, webpage, i)

def set_board(pieces_names, board):
    choices = [0.1, 0.2, 0.3, 0.4, 0.5]
    choice_threshold = random.choice(choices)
    y = 0
    for i in range(8):
        x = 0
        for j in range(8):
            choice_value = random.uniform(0, 1)
            if choice_value < choice_threshold:
                piece = random.choice(pieces_names)
                piece_img = Image.open(piece).convert("RGBA")
                board.paste(piece_img, (x, y), mask = piece_img)
            x += size
        y += size
    return board

part = -1
def rand_size_board(generated_board, webpage_name, _id):
    global part
    size = random.randrange(320, 800, 8)
    generated_board = generated_board.resize((size,size))
    webimage = Image.open(webpage_name).convert("RGBA")

    new_h = random.randint(0, 1440 - size)
    new_w = random.randint(0, 900 - size)
    webimage.paste(generated_board, (new_h, new_w))
    webimage = webimage.resize((512,320))

    if _id % 3000 == 0:
        part += 1
    f = open(f'dataset_{part}/{_id}.txt', "w")
    f.write(f'0 {(new_h + size//2)/1440} {(new_w + size//2)/900} {size/1440} {size/900}')
    f.close()
    webimage.save(f'dataset_{part}/{_id}.png', "PNG")


if __name__ == "__main__":
    import time
    start = time.time()
    generate_board(30000)
    end = time.time()
    print(end - start)
