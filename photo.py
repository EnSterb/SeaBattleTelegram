from PIL import Image, ImageDraw, ImageFont

matrix_size = 11
grid_size = 100  # Размер ячейки сетки

image_width = matrix_size * grid_size
image_height = matrix_size * grid_size

whale = (Image.open('whale.png')).resize((grid_size - 2, grid_size - 2))
ship = (Image.open('ship_cell.png')).resize((grid_size - 2, grid_size - 2))
damaged = (Image.open('damaged_cell.png')).resize((grid_size - 2, grid_size - 2))
destroyed = (Image.open('destroyed_cell.png')).resize((grid_size - 2, grid_size - 2))
miss = (Image.open('miss.png')).resize((grid_size - 2, grid_size - 2))
one = (Image.open('one.png')).resize((grid_size - 2, grid_size - 2))
two = (Image.open('two.png')).resize((grid_size - 2, grid_size - 2))
three = (Image.open('three.png')).resize((grid_size - 2, grid_size - 2))
four = (Image.open('four.png')).resize((grid_size - 2, grid_size - 2))
five = (Image.open('five.png')).resize((grid_size - 2, grid_size - 2))
six = (Image.open('six.png')).resize((grid_size - 2, grid_size - 2))
seven = (Image.open('seven.png')).resize((grid_size - 2, grid_size - 2))
eight = (Image.open('eight.png')).resize((grid_size - 2, grid_size - 2))
nine = (Image.open('nine.png')).resize((grid_size - 2, grid_size - 2))
ten = (Image.open('ten.png')).resize((grid_size - 2, grid_size - 2))
A = (Image.open('A.png')).resize((grid_size - 2, grid_size - 2))
B = (Image.open('B.png')).resize((grid_size - 2, grid_size - 2))
C = (Image.open('C.png')).resize((grid_size - 2, grid_size - 2))
D = (Image.open('D.png')).resize((grid_size - 2, grid_size - 2))
E = (Image.open('E.png')).resize((grid_size - 2, grid_size - 2))
F = (Image.open('F.png')).resize((grid_size - 2, grid_size - 2))
G = (Image.open('G.png')).resize((grid_size - 2, grid_size - 2))
H = (Image.open('H.png')).resize((grid_size - 2, grid_size - 2))
ii = (Image.open('I.png')).resize((grid_size - 2, grid_size - 2))
J = (Image.open('J.png')).resize((grid_size - 2, grid_size - 2))
white = (Image.open('white.jpg')).resize((grid_size - 2, grid_size - 2))

width, height = ship.size
font = ImageFont.truetype('arial.ttf', 20)


def draw_image(data, flag):
    image = Image.new('RGB', (image_width, image_height), 'white')
    draw = ImageDraw.Draw(image)
    for i in range(matrix_size):
        for j in range(matrix_size):
            x = j * grid_size
            y = i * grid_size
            draw.rectangle(((x, y), (x + grid_size, y + grid_size)), outline='black', fill=None)
    image.paste(whale, (0 * grid_size + 2, 0 * grid_size + 2))
    for x in range(matrix_size):
        for y in range(matrix_size):
            if data[x][y] == 1:
                image.paste(one, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 2:
                image.paste(two, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 3:
                image.paste(three, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 4:
                image.paste(four, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 5:
                image.paste(five, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 6:
                image.paste(six, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 7:
                image.paste(seven, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 8:
                image.paste(eight, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 9:
                image.paste(nine, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 10:
                image.paste(ten, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 'A':
                image.paste(A, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 'B':
                image.paste(B, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == "C":
                image.paste(C, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 'D':
                image.paste(D, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 'E':
                image.paste(E, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 'F':
                image.paste(F, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 'G':
                image.paste(G, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 'H':
                image.paste(H, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 'I':
                image.paste(ii, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 'J':
                image.paste(J, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 'm':
                image.paste(miss, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 'd':
                image.paste(destroyed, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 'dam':
                image.paste(damaged, (y * grid_size + 2, x * grid_size + 2))
            elif data[x][y] == 's':
                if flag == 2:
                    image.paste(white, (y * grid_size + 2, x * grid_size + 2))
                else:
                    image.paste(ship, (y * grid_size + 2, x * grid_size + 2))

    # Сохраняем изображение
    image.save('matrix_grid.png')


def draw_result(nomer, bot_name, cur_name):
    if nomer == 1:
        image = Image.new('RGB', (2600, 1550), color=(218, 189, 171))
        image.save('result.png')
    photo_send = Image.open('matrix_grid.png')
    res = Image.open('result.png')
    if nomer == 1:
        font = ImageFont.truetype('cd2f1-36d91_sunday.ttf', size=50)
        draw_text = ImageDraw.Draw(res)
        draw_text.text((500, 100), f'поле {cur_name}',
                       font=font, fill='#1C0606')
        res.paste(photo_send, (100, 250))
    if nomer == 2:
        font = ImageFont.truetype('cd2f1-36d91_sunday.ttf', size=50)
        draw_text = ImageDraw.Draw(res)
        draw_text.text((1800, 100), f'Поле {bot_name}',
                       font=font, fill='#1C0606')
        res.paste(photo_send, (1400, 250))
    res.save('result.png')
