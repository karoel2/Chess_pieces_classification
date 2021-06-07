from PIL import Image
import glob
import random

image_list = []
for filename in glob.glob('pices/*.png'):
    im = Image.open(filename).convert("RGBA")
    image_list.append(im)
    print(image_list[0].size)
size = image_list[0].size

board = Image.open("board.png").convert("RGBA").resize((1600,1600))

def create_board(number):
    for i in range(number):
        empty_board = board.copy()
        set_board(image_list, empty_board).save(f'dataset/chess{i}.png', "PNG")
        print(f'chess{i}.png')

def set_board(pices_list, board):
    choices = [0.1, 0.2, 0.3, 0.4, 0.5]
    choice_threshold = random.choice(choices)
    y = 0
    for i in range(8):
        x = 0
        for j in range(8):
            choice_value = random.uniform(0, 1)
            if choice_value < choice_threshold:
                pice = random.choice(pices_list)
                board.paste(pice, (x, y), mask = pice)
            x += size[0]
        y += size[0]
    return board

def rand_size_board(webimage, id_):
    print(id_)
    size = random.randrange(320, 800, 8)
    empty_board = board.copy()
    generated_board = set_board(image_list, empty_board).resize((size,size))

    new_h = random.randint(0, 1440 - size)
    new_w = random.randint(0, 900 - size)
    webimage.paste(generated_board, (new_h, new_w))
    webimage = webimage.resize((512,320))


    f = open(f'dataset/{id_}.txt', "w")
    f.write(f'0 {(new_h + size//2)/1440} {(new_w + size//2)/900} {size/1440} {size/900}')
    f.close()
    webimage.save(f'dataset/{id_}.png', "PNG")

count = 0
id_ = 0
for filename in glob.glob('webimg/*.jpg'):
    webpage = Image.open(filename)  #1440 x 900
    rand_size_board(webpage, id_)
    id_ += 1
    count +=1
    if count > 4000:
        break
