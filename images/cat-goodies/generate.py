"""Build small transparent pixel sprites to match the contact-page cat."""

from pathlib import Path
import struct
import zlib


HERE = Path(__file__).parent
PIXEL = 6
SIZE = 24
COLORS = {
    ".": (0, 0, 0, 0),
    "O": (251, 238, 230, 255),  # cat's cream outline
    "K": (17, 17, 17, 255),
    "P": (247, 168, 196, 255),  # cat pink
    "D": (226, 122, 158, 255),  # cat shadow pink
    "A": (226, 84, 43, 255),    # site coral
    "W": (255, 250, 245, 255),
    "M": (217, 217, 223, 255),  # cat laptop gray
    "N": (154, 154, 163, 255),
    "B": (55, 72, 64, 255),    # nori
    "G": (111, 174, 78, 255),  # signpost grass
    "Y": (252, 207, 143, 255),
    "T": (200, 139, 91, 255),
}


def canvas():
    return [["." for _ in range(SIZE)] for _ in range(SIZE)]


def put(grid, x, y, color):
    if 0 <= x < SIZE and 0 <= y < SIZE:
        grid[y][x] = color


def circle(grid, cx, cy, radius, color):
    for y in range(SIZE):
        for x in range(SIZE):
            if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                put(grid, x, y, color)


def sushi():
    g = canvas()
    circle(g, 11, 11, 9.8, "O")
    circle(g, 11, 11, 8.5, "B")
    circle(g, 11, 11, 6.6, "W")
    circle(g, 11, 11, 3.7, "P")
    for x, y in [(10, 9), (11, 9), (12, 9), (9, 10), (10, 10), (11, 10),
                 (9, 11), (10, 11), (11, 11), (10, 12)]:
        put(g, x, y, "A")
    for x, y in [(12, 11), (13, 11), (12, 12), (13, 12), (12, 13), (13, 13)]:
        put(g, x, y, "G")
    for x, y in [(8, 8), (14, 7), (7, 12), (15, 14), (10, 16)]:
        put(g, x, y, "O")
    return g


def cake():
    g = canvas()
    # A strawberry on a frosted, layered wedge.
    right_edge = [15, 17, 18, 19, 20, 21, 21, 21, 20, 20, 19, 19, 18]
    for y in range(7, 20):
        right = right_edge[y - 7]
        for x in range(3, right + 1):
            if x in (3, right) or y == 19:
                color = "O"
            elif y in (7, 8):
                color = "W"
            elif y in (10, 15):
                color = "P"
            elif y in (11, 16):
                color = "D"
            elif y == 18:
                color = "T"
            else:
                color = "Y"
            put(g, x, y, color)
    for x in range(5, 17):
        put(g, x, 6, "O" if x in (5, 16) else "W")
    for x in range(7, 16):
        put(g, x, 5, "O" if x in (7, 15) else "W")
    # Strawberry with two green leaves and a tiny cream shine.
    for y, left, right in [(2, 10, 12), (3, 9, 13), (4, 9, 13), (5, 10, 12)]:
        for x in range(left, right + 1):
            put(g, x, y, "O" if x in (left, right) else "A")
    for x, y in [(10, 1), (12, 1), (11, 2), (12, 3)]:
        put(g, x, y, "G" if y < 3 else "W")
    return g


def golf_ball():
    g = canvas()
    circle(g, 11, 11, 9.8, "O")
    circle(g, 11, 11, 8.5, "W")
    for cx, cy in [(8, 7), (13, 6), (16, 10), (7, 12), (12, 11), (10, 16), (15, 15)]:
        for x, y in [(cx, cy), (cx + 1, cy), (cx, cy + 1)]:
            put(g, x, y, "M")
    for x, y in [(6, 8), (7, 6), (8, 5), (13, 4)]:
        put(g, x, y, "O")
    return g


def write_png(path, grid):
    width = height = SIZE * PIXEL
    rows = bytearray()
    for y in range(height):
        rows.append(0)
        for x in range(width):
            rows.extend(COLORS[grid[y // PIXEL][x // PIXEL]])

    def chunk(kind, data):
        return (struct.pack(">I", len(data)) + kind + data +
                struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff))

    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(bytes(rows), 9))
        + chunk(b"IEND", b"")
    )


def write_svg(path, grid):
    rects = []
    for y, row in enumerate(grid):
        for x, key in enumerate(row):
            if key == ".":
                continue
            rgb = COLORS[key][:3]
            rects.append(
                f'<rect x="{x}" y="{y}" width="1" height="1" '
                f'fill="#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"/>'
            )
    path.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
        'shape-rendering="crispEdges">\n' + "\n".join(rects) + "\n</svg>\n"
    )


for name, builder in [("sushi-roll", sushi), ("cake-slice", cake), ("golf-ball", golf_ball)]:
    pixels = builder()
    write_png(HERE / f"{name}.png", pixels)
    write_svg(HERE / f"{name}.svg", pixels)
