## circular motion (bicycle model) update
##
## state is modelled as x, y coordinates plus polar orientation
##
## movement updates are calculated by steering_angles. the appropriate
## trigonometry is built in to this implementation.

from math import pi, sin, cos, tan


class Bicycle:

    def __init__(self, x, y, orientation, length=1):
        self.x = x
        self.y = y
        self.orientation = orientation  # radians
        self.length = length  # the distance between the front and rear axles

    def __str__(self):
        return str((self.x, self.y, self.orientation))

    def move(self, steering_angle, distance):
        turning_angle = (distance / self.length) * tan(steering_angle)

        # special case approximately straight motion
        if turning_angle < 0.001:
            self.x = self.x + distance * cos(self.orientation)
            self.y = self.y + distance * sin(self.orientation)
            self.orientation = (self.orientation + turning_angle) % (2 * pi)
        else:
            radius = distance / turning_angle
            cx = self.x - sin(self.orientation) * radius
            cy = self.y + cos(self.orientation) * radius
            self.x = cx + sin(self.orientation + turning_angle) * radius
            self.y = cy - cos(self.orientation + turning_angle) * radius
            self.orientation = (self.orientation + turning_angle) % (2 * pi)


if __name__ == "__main__":
    bike = Bicycle(0, 0, 0)
    print bike
    bike.move(0, 10)
    print bike
    bike.move(pi / 6, 10)
    print bike
