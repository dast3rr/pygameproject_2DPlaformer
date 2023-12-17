from PIL import Image, ImageDraw
from random import choice, randint


def get_map(size, size_block, name):
    size = tuple([size_block * i for i in size])
    new_image = Image.new("RGB", size, (0, 0, 0))
    colors = [(65, 106, 137), (25, 75, 118), (81, 125, 164)]

    for i in range(size[0] // size_block):
        for j in range(size[1] // size_block):
            color = choice(colors)
            block_image = Image.new("RGB", (size_block, size_block), color)
            draw = ImageDraw.Draw(block_image)
            draw.line((size_block // 10, size_block // 10, size_block // 10, size_block - size_block // 10), fill=tuple([i + 5 for i in color]), width=((size_block // 50) * 3))
            draw.line((size_block // 10, size_block // 10, size_block - size_block // 10, size_block // 10),
                      fill=tuple([i + 5 for i in color]), width=((size_block // 50) * 3))

            draw.line((0, 0, 0, size_block), fill=tuple([i - 20 for i in color]), width=2)
            draw.line((0, 0, size_block, 0), fill=tuple([i - 20 for i in color]), width=2)
            draw.line((size_block, size_block, 0, size_block), fill=tuple([i - 20 for i in color]), width=2)
            draw.line((size_block, size_block, size_block, 0), fill=tuple([i - 20 for i in color]), width=2)

            for _ in range(20):
                x, y = randint(5, size_block - 5), randint(5, size_block - 5)
                draw.rectangle((x, y, x + size_block // 20, y + size_block // 20), fill=tuple([i + randint(-15, 15) for i in color]))
            new_image.paste(block_image, (i * size_block, j * size_block))
    new_image.save(f'{name}.png', "PNG")


size = tuple(map(int, input().split()))
size_block = int(input())
get_map(size, size_block, 'map')
