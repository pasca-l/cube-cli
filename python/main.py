from math import sin, cos
from time import sleep


class Cube:
    def __init__(self):
        self.height = 30
        self.width = 30
        self._init_memory()

        self.alpha = 0
        self.beta = 0
        self.gamma = 0

        self.size = 10
        self.sparsity = 1

    def _init_memory(self):
        # array storing foreground information with size (h, w, 2)
        # h: height of screen
        # w: width of screen
        # 2 channels contain following:
        #     ch: character to be placed
        #     d: depth of point (front most is kept and updated)
        self.foreground = [
            ([{"ch": ".", "d": 0}] * self.width) for _ in range(self.height)
        ]

    def _rotated_x(self, x, y, z):
        return x * cos(self.alpha) * cos(self.beta) \
                + y * cos(self.alpha) * sin(self.beta) * sin(self.gamma) \
                - y * sin(self.alpha) * cos(self.gamma) \
                + z * cos(self.alpha) * sin(self.beta) * cos(self.gamma) \
                + z * sin(self.alpha) * sin(self.gamma)

    def _rotated_y(self, x, y, z):
        return x * sin(self.alpha) * cos(self.beta) \
                + y * sin(self.alpha) * sin(self.beta) * sin(self.gamma) \
                + y * cos(self.alpha) * cos(self.gamma) \
                + z * sin(self.alpha) * sin(self.beta) * cos(self.gamma) \
                - z * cos(self.alpha) * sin(self.gamma)

    def _rotated_z(self, x, y, z):
        return - x * sin(self.beta) \
                + y * cos(self.beta) * sin(self.gamma) \
                + z * cos(self.beta) * cos(self.gamma)

    def _calculate_surface(self, x, y, z, ch):
        x = self._rotated_x(x, y, z)
        y = self._rotated_y(x, y, z)
        z = self._rotated_z(x, y, z) + 100

        z_bar = 1 / z

        w_idx = int(self.width / 2 + x)
        h_idx = int(self.height / 2 + y)

        # if rotated point is within the screen
        if 0 <= h_idx < self.height and 0 <= w_idx < self.width:
            # if the point is at the front most
            if z_bar > self.foreground[h_idx][w_idx]["d"]:
                self.foreground[h_idx][w_idx] = {"ch": ch, "d": z_bar}

    def draw_cube(self):
        for x in range(-self.size, self.size, self.sparsity):
            for y in range(-self.size, self.size, self.sparsity):
                self._calculate_surface(x, y, -self.size, '@')
                self._calculate_surface(self.size, y, x, '$')
                self._calculate_surface(-self.size, y, -x, '~')
                self._calculate_surface(-x, y, self.size, '#')
                self._calculate_surface(x, -self.size, -y, ';')
                self._calculate_surface(x, self.size, y, '+')

        for h in range(self.height):
            print(*[self.foreground[h][w]["ch"] for w in range(self.width)])

    def rotate_cube(self):
        # clear screen without moving cursor to the top
        print("\x1b[2J")

        while True:
            self._init_memory()

            self.draw_cube()

            # move cursor to the top
            print("\x1b[H")

            self.alpha += 0.05
            self.beta += 0.05
            self.gamma += 0.01

            sleep(0.1)


def main():
    cube = Cube()
    cube.rotate_cube()


if __name__ == "__main__":
    main()