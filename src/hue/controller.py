import os
from phue import Bridge, Light

from dotenv import load_dotenv
load_dotenv()

IP = os.getenv('IP')


class PhillipsHue:
    MAX_HUE = 65535
    MAX_SAT = 254
    MIN_HUE = 0
    MIN_SAT = 0
    b = None
    light_name_list = None

    def __init__(self):
        self.b = Bridge(IP)
        self.b.connect()
        self.light_name_list = self.b.get_light_objects('name')

    def increase_hue(self):
        for light in self.light_name_list:
            if self.light_name_list[light].hue + 1000 > self.MAX_HUE:
                self.light_name_list[light].hue = self.MAX_HUE
            else:
                self.light_name_list[light].hue += 1000

    def increase_sat(self):
        for light in self.light_name_list:

            if self.light_name_list[light].saturation + 200 > self.MAX_SAT:
                self.light_name_list[light].saturation = self.MAX_SAT
            else:
                self.light_name_list[light].saturation += 10

    def decrease_hue(self):
        for light in self.light_name_list:
            if self.light_name_list[light].hue - 1000 < self.MIN_HUE:
                self.light_name_list[light].hue = self.MIN_HUE
            else:
                self.light_name_list[light].hue -= 1000

    def decrease_sat(self):
        for light in self.light_name_list:
            if self.light_name_list[light].saturation - 115 < self.MIN_SAT:
                self.light_name_list[light].saturation = self.MIN_SAT
            else:
                self.light_name_list[light].saturation -= 50

    def reset_vals(self):
        for light in self.light_name_list:
            self.light_name_list[light].hue = 10
            self.light_name_list[light].saturation = 120

    def make_colour(self, hue, sat):
        for light in self.light_name_list:
            self.light_name_list[light].hue = hue
            self.light_name_list[light].saturation = sat

    def turn_lamps_on(self):
        light: Light
        for light in self.b.lights:
            print(light)
            light.on = True

    def change_scene(self, scene_str: str):
        scenes = self.b.scenes
        print(self.b.get_group(1))
        for scene in scenes:
            if scene_str in scene.name.lower():
                self.b.run_scene("Habitación", scene.name)

    def turn_lamps_off(self):
        light: Light
        for light in self.b.lights:
            light.on = False
