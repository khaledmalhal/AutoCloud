from car_FreeNove import *


class IESCar(CarPhy):

    def run(self):

        passW2 = 0
        passN4 = 0
        passE1 = 0

        self.start()
        while True:
            try:
                # --> Codi a omplir...
                tag_id = self.get_tag()

                if tag_id == RFIDTAG.ABOCADOR:
                    self.stop()
                elif tag_id == RFIDTAG.W1:
                    print("tag:", tag_id)
                    color = self.get_trafficlight_color('TW1')
                    print(color)
                    if is_red(color) or is_yellow(color):
                        if self.get_tag() == RFIDTAG.W1:
                            self.stop()
                    elif is_green(color):
                        if self.is_stopped():
                            self.start()
                    if passW2 == 0:
                        self.go_straight_on()
                    else:
                        self.turn_left()

                elif tag_id == RFIDTAG.S3:
                    print("tag:", tag_id)
                    color = self.get_trafficlight_color('TS1')
                    print(color)

                    if is_red(color) or is_yellow(color):
                        if self.get_tag() == RFIDTAG.S3:
                            self.stop()
                    elif is_green(color):
                        if self.is_stopped():
                            self.start()
                    self.turn_left()

                elif tag_id == RFIDTAG.C1:
                    print("tag:", tag_id)
                    if passN4 == 0:
                        self.turn_right()
                    else:
                        self.turn_left()
                elif tag_id == RFIDTAG.S6:
                    print("tag:", tag_id)
                    passW2 = 1
                    passN4 = 1
                    passE1 = 1
                elif tag_id == RFIDTAG.S5:
                    print("tag:", tag_id)
                    color = self.get_trafficlight_color('TS2')
                    print(color)

                    if is_red(color) or is_yellow(color):
                        if self.get_tag() == RFIDTAG.S5:
                            self.stop()
                    elif is_green(color):
                        if self.is_stopped():
                            self.start()
                    self.turn_right()

                elif tag_id == RFIDTAG.E2:
                    print("tag:", tag_id)
                    self.go_straight_on()

                elif tag_id == RFIDTAG.B7:
                    print("tag:", tag_id)
                    self.turn_left()

                elif tag_id == RFIDTAG.E1:
                    print("tag:", tag_id)
                    if passE1 == 0:
                        self.go_straight_on()  # TODO: no caldria
                    else:
                        self.stop()

                # <---
            except Exception as e:
                print("ERROR:{}".format(e))
            time.sleep(0.05)  # TODO: add this line


if __name__ == '__main__':
    try:
        cotxe = IESCar()
    except Exception as e:
        print(e)
        print_bye_message()