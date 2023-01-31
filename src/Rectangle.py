import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class Rect:
    def __init__(self, bottom_left, width, height):
        self.bottom_left = bottom_left
        self.width = width
        self.height = height


def is_intersect(rect_1, rect_2):
    """Сначала проверяем случай, когда левая нижняя точка одного прямоугольника находится
    "внутри" другого. Затем ("Или") проверяем случай, когда левая нижняя точка находится "снаружи"."""
    if (rect_2.bottom_left[0] >= rect_1.bottom_left[0]) and \
            (rect_2.bottom_left[1] >= rect_1.bottom_left[1]) and \
            (rect_2.bottom_left[0] <= rect_1.bottom_left[0] + rect_1.width or
             rect_2.bottom_left[1] <= rect_1.bottom_left[1] + rect_1.height) or \
            (rect_2.bottom_left[0] + rect_2.width >= rect_1.bottom_left[0] and
             rect_2.bottom_left[1] + rect_2.height >= rect_1.bottom_left[1]):
        return True
    return False


def plot_rect(rects):
    _, ax = plt.subplots()
    ax.plot()

    for rect in rects:
        ax.add_patch(Rectangle(rect.bottom_left, rect.width, rect.height, fill=False))
    plt.show()


class Rect:
    def __init__(self, bottom_left, width, height):
        self.bottom_left = bottom_left
        self.width = width
        self.height = height


rect_1 = Rect([5, 5], 15, 10)
rect_2 = Rect([9, 1], 3, 3)
rect_3 = Rect([4, 4], 4, 5)
plot_rect([rect_1, rect_3])
print(is_intersect(rect_1, rect_3))
