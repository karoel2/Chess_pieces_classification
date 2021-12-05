from PIL import Image
import glob
import random
import itertools

LABEL_COUNT = [0 for _ in range(13)]
IDX = 0
threshold = 1
size = 96 # don't touch

def generate_board(threshold):
    pieces_names = []
    for filename in glob.glob('../create dataset/pieces/*.png'):
        pieces_names.append(filename)
    boards = create_new_boards()
    iterator_board = iter(itertools.cycle(boards))
    while sum(LABEL_COUNT) < 13 * threshold:
        empty_board = next(iterator_board)
        generated_board, labels = set_board(pieces_names, empty_board)
        board, w, h = img_cut(generated_board)
        img_list = img_split(board, w, h, (20,20))
        labeled(img_list, transpose_cut(labels), threshold)

def labeled(img_list, labels, threshold):
    global LABEL_COUNT, IDX
    for img, label in zip(img_list, labels):
        if LABEL_COUNT[label] < threshold:
            img.save(f'dataset/{IDX}_{label}.png')
            LABEL_COUNT[label] += 1
            IDX += 1

def transpose_cut(a):
    board = []
    for i in range(1,9):
        tab = [a[10+i], a[20+i], a[30+i], a[40+i], a[50+i], a[60+i], a[70+i], a[80+i]]
        board.extend(tab)
    return board

def create_new_boards():
    tile_list = []
    for filename in sorted(glob.glob('../create dataset/tiles/*.png')):#, key = lambda i: (len(i), i)):
        im = Image.open(filename).convert("RGBA")
        tile_list.append(im)

    def pairwise(iterable):
        "s -> (s0, s1), (s2, s3), (s4, s5), ..."
        a = iter(iterable)
        return zip(a, a)

    boards = []
    for white, black in pairwise(tile_list):
        line = Image.new('RGBA', (10*96, 96), color=(0,0,0,0))
        for i in range(5):
            line.paste(white, (i*96*2, 0), mask = white)
            line.paste(black, ((i*96*2)+96, 0), mask = black)
        fliped = line.copy()
        fliped = fliped.transpose(method=Image.FLIP_LEFT_RIGHT)
        board = Image.new('RGBA', (10*96, 10*96), color=(0,0,0,0))
        for i in range(5):
            board.paste(line, (0, i*96*2), mask = line)
            board.paste(fliped, (0, (i*96*2)+96), mask = fliped)
        boards.append(board)
    return boards

def set_board(pieces_names, board):
    board = board.copy()
    choice_threshold = 0.7
    board_labels = []
    labels_line = []
    y = 0
    for i in range(10):
        x = 0
        for j in range(10):
            choice_value = random.uniform(0, 1)
            if choice_value < choice_threshold:
                piece = random.choice(pieces_names)
                piece_name = piece.replace('../create dataset/pieces/','').replace('.png','')
                labels_line.append(int(piece_name)%12)
                piece_img = Image.open(piece).convert("RGBA")
                board.paste(piece_img, (x, y), mask = piece_img)
            else:
                labels_line.append(12)
            x += size
        y += size
    return board, labels_line

def img_cut(image):
    offset = [random.randrange(-30, 30) for _ in range(4)]
    # offset = [15, 15, 15, 15]
    coords = (
        size - offset[0],
        size - offset[1],
        (9 * size) + offset[2],
        (9 * size) + offset[3],
        )
    w = (9 * size) + offset[2] - (size - offset[0])
    h = (9 * size) + offset[3] - (size - offset[1])
    # print(offset)
    region = image.crop(coords)
    return region, w, h

def img_split(img, w, h, size):
    board = []
    right = w / 8
    bottom = h / 8
    for i in range(8):
        for j in range(8):
            image = img.crop((i*right, j*bottom, (i+1)*right, (j+1)*bottom))
            board.append(image.resize(size))
    return board

if __name__ == "__main__":
    import time
    start = time.time()
    generate_board(1)
    end = time.time()
    print(end - start)
