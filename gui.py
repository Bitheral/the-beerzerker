"""
    Author:  Nathan Dow / Bitheral
    Created: 23/10/2020
"""
import pygame
import re
import consts
import util
import os
import math
import webbrowser

from enums import Screens
from game import Game

pygame.font.init()


class Checkbox:
    def __init__(self, text_element, position=(0, 0)):
        self.text = text_element
        self.pos = position
        self.state = False
        self.area = (
            self.pos[0],
            self.pos[1],
            32,
            32
        )

        self.text.set_pos((
            (self.pos[0] + 40),
            (self.pos[1] + 18) - self.text.get_size()[1] / 2
        ))

        self.sprite = util.Spritesheet(consts.MANIFEST["TEXTURES"]["GUI"]["checkbox"])

    def render(self):
        #     Base sprite (No hover)                  Hover sprite
        off = (self.sprite.image_at((0, 0, 32, 32), -1), self.sprite.image_at((32, 0, 32, 32), -1))
        on = (self.sprite.image_at((0, 32, 32, 32), -1), self.sprite.image_at((32, 32, 32, 32), -1))

        sprite = off, on
        return sprite[int(self.state)][int(self.on_hover())]

    def get_pos(self):
        return self.pos

    def get_size(self):
        return 40 + self.text.get_size()[0], 32

    def set_state(self, state):
        self.state = state

    def set_pos(self, pos):
        self.pos = pos
        self.text.set_pos((
            (self.pos[0] + 40),
            (self.pos[1] + 18) - self.text.get_size()[1] / 2
        ))
        self.area = (
            self.pos[0],
            self.pos[1],
            32,
            32
        )

    def toggle(self):
        self.state = not self.state

    def on_hover(self):
        return self.area[0] < consts.MOUSE.get_pos()[0] < self.area[0] + self.area[2] and self.area[1] < \
               consts.MOUSE.get_pos()[1] < self.area[1] + self.area[3]


class Text:
    def __init__(self, _text, font_name, size, font_type=None, x=0, y=0):
        if os.path.isdir(consts.MANIFEST["FONTS"][font_name]):
            self.font = pygame.font.Font(consts.MANIFEST["FONTS"][font_name][font_type])
        else:
            self.font = pygame.font.Font(consts.MANIFEST["FONTS"][font_name], size)
        self.colour = (255, 255, 255)
        self.text = _text
        self.pos = (x, y)

        self.font_name = font_name
        self.font_size = size

    def render(self):
        return self.font.render(self.text, False, self.colour)

    def get_font(self):
        return self.font_name

    def get_font_size(self):
        return self.font_size

    def get_text(self):
        return self.text

    def get_size(self):
        return self.font.size(self.text)

    def get_pos(self):
        return self.pos

    def set_color(self, color):
        self.colour = color

    def set_text(self, text):
        self.text = text

    def set_pos(self, pos):
        self.pos = pos


class Link:
    def __init__(self, text, url):
        self.url = url
        self.text = text

    def on_hover(self):
        mouseover_x = self.text.get_pos()[0] < consts.MOUSE.get_pos()[0] < self.text.get_pos()[0] + \
                      self.text.get_size()[0]
        mouseover_y = self.text.get_pos()[1] < consts.MOUSE.get_pos()[1] < self.text.get_pos()[1] + \
                      self.text.get_size()[1]
        return mouseover_x and mouseover_y

    def click(self):
        webbrowser.open(self.url)

    def render(self):
        if self.on_hover():
            pygame.draw.rect(pygame.display.get_surface(), self.text.colour, (
                self.text.get_pos()[0], self.text.get_pos()[1] + self.text.get_size()[1] - 2, self.text.get_size()[0],
                2))
        return self.text.render()

    def get_font(self):
        return self.text.font_name

    def get_font_size(self):
        return self.text.font_size

    def get_text(self):
        return self.text.text

    def get_size(self):
        return self.text.font.size(self.text.text)

    def get_pos(self):
        return self.text.pos

    def set_color(self, color):
        self.text.colour = color

    def set_text(self, text):
        self.text.text = text

    def set_pos(self, pos):
        self.text.pos = pos


class Button:
    def __init__(self, text_element, size, position=(0, 0)):
        self.text = text_element
        self.pos = position
        self.size = size
        self.area = (
            self.pos[0],
            self.pos[1],
            self.size[0],
            self.size[1]
        )

        self.text.set_pos((
            (self.pos[0] + self.size[0] / 2) - self.text.get_size()[0] / 2,
            (self.pos[1] + self.size[1] / 2) - self.text.get_size()[1] / 2
        ))

        self.sprite = util.Spritesheet(consts.MANIFEST["TEXTURES"]["GUI"]["button"])

    def render(self):
        normal = self.sprite.image_at((0, 0, 128, 32), -1)
        hover = self.sprite.image_at((0, 32, 128, 32), -1)

        sprite = normal, hover

        return pygame.transform.scale(sprite[self.on_hover()], self.get_size())

    def get_pos(self):
        return self.pos

    def get_size(self):
        return self.size

    def set_pos(self, pos):
        self.pos = pos
        self.text.set_pos((
            (self.pos[0] + self.size[0] / 2) - self.text.get_size()[0] / 2,
            (self.pos[1] + self.size[1] / 2) - self.text.get_size()[1] / 2
        ))
        self.area = (
            self.pos[0],
            self.pos[1],
            self.size[0],
            self.size[1]
        )

    def set_action(self, action):
        self.action = action

    def on_hover(self):
        return self.area[0] < consts.MOUSE.get_pos()[0] < self.area[0] + self.area[2] and self.area[1] < \
               consts.MOUSE.get_pos()[1] < self.area[1] + self.area[3]


class Heart:
    def __init__(self, state, position=(0, 0)):
        self.pos = position
        self.state = state
        self.area = (
            self.pos[0],
            self.pos[1],
            32,
            32
        )

        self.sprite = util.Spritesheet(consts.MANIFEST["TEXTURES"]["SPRITESHEETS"]["steam_heart"])

    def render(self):
        full = self.sprite.image_at((0, 0, 32, 32), -1)
        half = self.sprite.image_at((32, 0, 32, 32), -1)
        low = self.sprite.image_at((64, 0, 32, 32), -1)
        none = self.sprite.image_at((96, 0, 32, 32), -1)

        sprite = {
            "NONE": none,
            "HALF": half,
            "LOW": low,
            "FULL": full
        }

        return sprite[self.state]

    def get_pos(self):
        return self.pos

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def set_pos(self, pos):
        self.pos = pos


class Beer:
    def __init__(self, state, position=(0, 0)):
        self.pos = position
        self.state = state
        self.area = (
            self.pos[0],
            self.pos[1],
            32,
            32
        )

        self.sprite = util.Spritesheet(consts.MANIFEST["TEXTURES"]["SPRITESHEETS"]["beer"])

    def render(self):
        full = self.sprite.image_at((0, 0, 32, 32), -1)
        half = self.sprite.image_at((32, 0, 32, 32), -1)
        none = self.sprite.image_at((64, 0, 32, 32), -1)

        sprite = {
            "NONE": none,
            "HALF": half,
            "FULL": full
        }

        return sprite[self.state]

    def get_pos(self):
        return self.pos

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def set_pos(self, pos):
        self.pos = pos


class GUIScreen(pygame.Surface):

    def __init__(self):
        super(GUIScreen, self).__init__(pygame.display.get_surface().get_size())
        self.components = {}

    def add_element(self, name, element):
        self.components[name] = element
        # self.components.append(element)

    def add_element_position(self, name, element, pos):
        self.components[name] = (element, pos)
        # self.components.append((element, pos))

    def handle_mouse_event(self):
        button_click = pygame.mixer.Sound(consts.MANIFEST["AUDIO"]["SOUNDS"]["GUI"]["button_click"])
        
        if pygame.event.get(pygame.MOUSEBUTTONDOWN):
            for component in self.components:
                if isinstance(self.components[component], Button):
                    button = self.components[component]
                    if button.on_hover():
                        button_click.play()
                        button.action()
                elif isinstance(self.components[component], Checkbox):
                    checkbox = self.components[component]
                    if checkbox.on_hover():
                        button_click.play()
                        checkbox.toggle()
                elif isinstance(self.components[component], Link):
                    link = self.components[component]
                    if link.on_hover():
                        button_click.play()
                        link.click()

    def handle_key_event(self):
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYUP:
        #         consts.LOGGER.debug("VALHALLA", f"{pygame.key.name(event.key).capitalize()} key pressed")
        pass


    def render(self):
        for component in self.components:
            element = self.components[component]

            if isinstance(element, pygame.Surface):
                pygame.display.get_surface().blit(element, (0, 0))

            elif isinstance(element, Button):
                # Button texture
                pygame.display.get_surface().blit(element.render(), element.get_pos())
                # Button text

                droptext = Text(
                    element.text.get_text(),
                    element.text.get_font(),
                    element.text.get_font_size(),
                    x=element.text.get_pos()[0] + 3,
                    y=element.text.get_pos()[1] + 3
                )
                droptext.set_color((20, 20, 20))

                pygame.display.get_surface().blit(droptext.render(), droptext.get_pos())
                pygame.display.get_surface().blit(element.text.render(), element.text.get_pos())
            elif isinstance(element, Checkbox):
                droptext = Text(
                    element.text.get_text(),
                    element.text.get_font(),
                    element.text.get_font_size(),
                    x=element.text.get_pos()[0] + 3,
                    y=element.text.get_pos()[1] + 3
                )
                droptext.set_color((20, 20, 20))

                pygame.display.get_surface().blit(element.render(), element.get_pos())  # Checkbox image
                pygame.display.get_surface().blit(droptext.render(), droptext.get_pos())
                pygame.display.get_surface().blit(element.text.render(), element.text.get_pos())  # Text
            elif isinstance(element, Text) or isinstance(element, Link):
                droptext = Text(
                    element.get_text(),
                    element.get_font(),
                    element.get_font_size(),
                    x=element.get_pos()[0] + 3,
                    y=element.get_pos()[1] + 3
                )
                droptext.set_color((20, 20, 20))

                pygame.display.get_surface().blit(droptext.render(), droptext.get_pos())
                pygame.display.get_surface().blit(element.render(), element.get_pos())
            elif isinstance(element, tuple):
                if isinstance(element[0], list):
                    for index, item in enumerate(element[0]):
                        if isinstance(item, Heart) or isinstance(item, Beer):
                            pygame.display.get_surface().blit(item.render(), element[1][index])
                else:
                    pygame.display.get_surface().blit(element[0], element[1])
            else:
                pygame.display.get_surface().blit(element.render(), element.get_pos())


class DebugOverlay(GUIScreen):

    def __init__(self):
        super().__init__()
        self.clock = pygame.time.Clock()

        window_width, window_height = pygame.display.get_surface().get_size()

        debug_mode_str = f"DEBUG OVERLAY - Press F12 to disable"
        debug_mode_text = Text(debug_mode_str, "Pixellari", 26, x=16, y=16)
        debug_mode_text.set_color((255, 0, 0))

        debug_mode_warning_str = f"WARNING - Opening this menu will slow down gameplay"
        debug_mode_warning_text = Text(debug_mode_warning_str, "Pixellari", 18, x=16, y=48)
        debug_mode_warning_text.set_color((255, 0, 0))

        mouse_str = f"Mouse position: {consts.MOUSE.get_pos()}"
        mouse_text = Text(mouse_str, "Pixellari", 26, x=16, y=72)

        screen_str = f"Current screen: {Screens(consts.current_screen).name}"
        screen_text = Text(screen_str, "Pixellari", 26, x=16, y=104)

        fps_str = f"FPS: {int(consts.clock.get_fps())}"
        fps_text = Text(fps_str, "Pixellari", 26, x=16, y=202)

        self.add_element("Debug text", debug_mode_text)
        self.add_element("Debug warning", debug_mode_warning_text)
        self.add_element("Mouse position", mouse_text)
        self.add_element("Current Screen", screen_text)
        self.add_element("FPS", fps_text)

    def render(self):
        super(DebugOverlay, self).render()
        self.components["Mouse position"].set_text(f"Mouse position: {consts.MOUSE.get_pos()}")
        self.components["Current Screen"].set_text(f"Current screen: {Screens(consts.current_screen).name}")
        self.components["FPS"].set_text(f"FPS: {int(consts.clock.get_fps())}")
        if consts.game is not None:
            player_str = f"Player position: {(round(consts.game.get_player().rect[0], 2), round(consts.game.get_player().rect[1], 2))}"
            player_text = Text(player_str, "Pixellari", 26, x=16, y=136)

            attack_str = f"Player attacking? : {consts.game.get_player().attacking}"
            attack_text = Text(attack_str, "Pixellari", 26, x=16, y=170)

            self.add_element("Player position", player_text)
            self.add_element("Player attack", attack_text)


class DisturbingSoundScreen(GUIScreen):

    def continue_action(self):
        consts.LOGGER.debug("VALHALLA", "Continue button pressed")
        consts.SETTINGS["HUMAN_SOUNDS"]["SKIP_WARNING"] = self.remember_warning_checkbox.state
        util.save_to_settings_file()
        consts.current_screen = Screens.GAME
        consts.LOGGER.info("VALHALLA", "Initializing new game")
        consts.game = Game()
        consts.start_time = pygame.time.get_ticks()

    def setting_action(self):
        consts.LOGGER.debug("VALHALLA", "Save button pressed")
        consts.last_screen = Screens.SOUND_WARNING
        consts.current_screen = Screens.SETTINGS

    def back_action(self):
        consts.LOGGER.debug("VALHALLA", "Back button pressed")
        consts.current_screen = Screens.MAIN_MENU

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()

        title_offset = (-42, 0)

        screen_title = Text("WARNING!", "Pixellari", 32)
        screen_title.set_color((255, 0, 0))
        screen_title.set_pos(
            ((window_width / 2) - (screen_title.get_size()[0] / 2), (window_width / 12) + title_offset[1]))

        note_11_text = Text("This game contains sounds to which some people",
                            "Pixellari", 26)
        note_11_text.set_pos(((window_width / 2) - (note_11_text.get_size()[0] / 2),
                              (screen_title.get_pos()[1] + note_11_text.get_size()[1] + 16)))

        note_12_text = Text("may find disturbing and/or disgusting.", "Pixellari", 26)
        note_12_text.set_pos(((window_width / 2) - (note_12_text.get_size()[0] / 2),
                              (note_11_text.get_pos()[1] + note_12_text.get_size()[1])))

        note_21_text = Text("If you are easily disturbed by the sounds of:", "Pixellari", 26)
        note_21_text.set_pos(((window_width / 2) - (note_21_text.get_size()[0] / 2),
                              (note_12_text.get_pos()[1] + note_21_text.get_size()[1] + 16)))

        note_221_text = Text("Belching", "Pixellari", 26)
        note_221_text.set_pos(
            (note_21_text.get_pos()[0] + 16, (note_21_text.get_pos()[1] + note_221_text.get_size()[1])))
        note_222_text = Text("Swallowing", "Pixellari", 26)
        note_222_text.set_pos(
            (note_21_text.get_pos()[0] + 16, (note_221_text.get_pos()[1] + note_222_text.get_size()[1])))

        self.note_23_text = Text("Please disable the setting 'Enable Human sounds'", "Pixellari", 26)
        self.note_23_text.set_pos(((window_width / 2) - (self.note_23_text.get_size()[0] / 2),
                                   (note_222_text.get_pos()[1] + self.note_23_text.get_size()[1] + 16)))

        remember_warning_checkbox_text = Text("Don't show this again", "Pixellari", 26)

        save_text = Text("Continue", "Pixellari", 26)
        save_button = Button(
            save_text,
            (128, 64)
        )
        save_button.set_pos(
            ((window_width / 2) - save_button.get_size()[0] - 64, window_height - save_button.get_size()[1] - 32))
        save_button.set_action(self.continue_action)

        settings_text = Text("Settings", "Pixellari", 26)
        settings_button = Button(
            settings_text,
            (128, 64)
        )
        settings_button.set_pos((save_button.get_pos()[0] + save_button.get_size()[0] + 16, save_button.get_pos()[1]))
        settings_button.set_action(self.setting_action)

        back_text = Text("Back", "Pixellari", 26)
        back_button = Button(
            back_text,
            (128, 64)
        )
        back_button.set_pos((settings_button.get_pos()[0] + settings_button.get_size()[0] + 16,
                             window_height - back_button.get_size()[1] - 32))
        back_button.set_action(self.back_action)

        self.remember_warning_checkbox = Checkbox(remember_warning_checkbox_text)
        self.remember_warning_checkbox.set_pos(
            (
                (window_width / 2) - (self.remember_warning_checkbox.get_size()[0] / 2) + 2,
                save_button.get_pos()[1] - self.remember_warning_checkbox.get_size()[1] - 16
            )
        )
        self.remember_warning_checkbox.state = consts.SETTINGS["HUMAN_SOUNDS"]["SKIP_WARNING"]

        self.add_element("Screen title", screen_title)
        self.add_element("Note 1.1 Text", note_11_text)
        self.add_element("Note 1.2 Text", note_12_text)
        self.add_element("Note 2.1 Text", note_21_text)
        self.add_element("Note 2.2.1 Text", note_221_text)
        self.add_element("Note 2.2.2 Text", note_222_text)
        self.add_element("Note 2.3 Text", self.note_23_text)
        # self.add_element("Note 22 Text", note_22_text)

        self.add_element("Back button", back_button)
        self.add_element("Settings button", settings_button)
        self.add_element("Save button", save_button)
        self.add_element("Skip warning checkbox", self.remember_warning_checkbox)

    def render(self):
        super(DisturbingSoundScreen, self).render()
        window_width = pygame.display.get_surface().get_size()[0]
        note_3_text = Text(
            f"You currently have the setting {'enabled' if consts.SETTINGS['HUMAN_SOUNDS']['VALUE'] else 'disabled'}",
            "Pixellari", 26)
        note_3_text.set_pos(((window_width / 2) - (note_3_text.get_size()[0] / 2),
                             (self.note_23_text.get_pos()[1] + note_3_text.get_size()[1] + 16)))
        self.add_element("Note 3 Text", note_3_text)


class GameOverlay(GUIScreen):

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()

        heart_offset = (16, 16)
        heart_pos = [
            (0 + heart_offset[0], 0 + heart_offset[1]),
            (32 + heart_offset[0], 0 + heart_offset[1]),
            (64 + heart_offset[0], 0 + heart_offset[1]),
            (96 + heart_offset[0], 0 + heart_offset[1]),
            (128 + heart_offset[0], 0 + heart_offset[1])
        ]

        beer_pos = [
            (0 + heart_offset[0], 32 + heart_offset[1]),
            (32 + heart_offset[0], 32 + heart_offset[1]),
            (64 + heart_offset[0], 32 + heart_offset[1]),
            (96 + heart_offset[0], 32 + heart_offset[1]),
            (128 + heart_offset[0], 32 + heart_offset[1])
        ]

        self.current_health = util.bind(consts.game.get_player().health, 0, 100, 0, 10, True)
        self.current_drunkenness = util.bind(consts.game.get_player().drunkenness, 0, 100, 0, 10, True)
        heart_element = [Heart("NONE"), Heart("NONE"), Heart("NONE"), Heart("NONE"), Heart("NONE")]
        beer_element = [Beer("NONE"), Beer("NONE"), Beer("NONE"), Beer("NONE"), Beer("NONE")]

        for index, heart in enumerate(heart_element):
            hearts_index = index + 1

            if (self.current_health / 2) >= hearts_index:
                heart.set_state("FULL")
            elif 0 >= (self.current_health / 2) - hearts_index > -0.5:
                heart.set_state("HALF")
            elif 0.5 >= (self.current_health / 2) - hearts_index > -1:
                heart.set_state("LOW")
            else:
                heart.set_state("NONE")

        for index, beer in enumerate(beer_element):
            beers_index = index + 1

            if self.current_drunkenness / 2 >= beers_index:
                beer.set_state("FULL")
            elif 0 >= (self.current_drunkenness / 2) - beers_index > -0.5:
                beer.set_state("HALF")
            else:
                beer.set_state("NONE")

        bottle_img = util.Image(consts.MANIFEST["TEXTURES"]["SPRITES"]["beer_bottle"], (16, 80))
        from game import Bottle
        bottle_count = Text(f"x{len(consts.game.get_player().get_items_by_type(Bottle))}", "Pixellari", 16,
                            x=bottle_img.get_pos()[0] + 16, y=bottle_img.get_pos()[1])

        score_text = Text(f"Score: {consts.score}", "Pixellari", 24, x=bottle_img.get_pos()[0] + 4,
                          y=bottle_img.get_pos()[1] + bottle_img.get_size()[1] + 6)

        background = pygame.Surface((160, 128))
        background.set_alpha(127)
        background.fill(0)

        self.add_element_position("Background overlay", background, (16, 16))
        self.add_element_position("Hearts", heart_element, heart_pos)
        self.add_element_position("Beers", beer_element, beer_pos)
        self.add_element("Bottle img", bottle_img)
        self.add_element("Bottle count", bottle_count)
        self.add_element("Score", score_text)

    def render(self):
        super(GameOverlay, self).render()
        from game import Bottle
        self.components["Bottle count"].set_text(f"x{len(consts.game.get_player().get_items_by_type(Bottle))}")


class PauseOverlay(GUIScreen):

    def play_action(self):
        consts.LOGGER.debug("VALHALLA", "Going back to game")
        consts.game.pause(False)

    def settings_action(self):
        consts.last_screen = Screens.GAME
        consts.current_screen = Screens.SETTINGS

    def credits_action(self):
        consts.last_screen = Screens.GAME
        consts.current_screen = Screens.CREDITS

    def quit_action(self):
        consts.current_screen = Screens.MAIN_MENU
        consts.game.pause(False)

    def __init__(self):
        super().__init__()

        play_offset = (-164, -64)
        settings_offset = (-160 - 4, 8)
        credits_offset = (4, 8)
        quit_offset = (-164, 80)

        window_width, window_height = pygame.display.get_surface().get_size()

        paused_text = Text("Paused", "Pixellari", 48, x=(window_width / 2) - 75, y=(window_width / 8))

        play_text = Text("Back to game", "Pixellari", 26)
        play_button = Button(
            play_text,
            (328, 64),
            (window_width / 2 + play_offset[0], window_height / 2 + play_offset[1])
        )
        play_button.set_action(self.play_action)

        settings_text = Text("Settings", "Pixellari", 26)
        settings_button = Button(
            settings_text,
            (160, 64),
            (window_width / 2 + settings_offset[0], window_height / 2 + settings_offset[1])
        )
        settings_button.set_action(self.settings_action)

        credits_text = Text("Credits", "Pixellari", 26)
        credits_button = Button(
            credits_text,
            (160, 64),
            (window_width / 2 + credits_offset[0], window_height / 2 + credits_offset[1])
        )
        credits_button.set_action(self.credits_action)

        quit_text = Text("Quit to main menu", "Pixellari", 26)
        quit_button = Button(
            quit_text,
            (328, 64),
            (window_width / 2 + quit_offset[0], window_height / 2 + quit_offset[1])
        )
        quit_button.set_action(self.quit_action)

        background = pygame.Surface(pygame.display.get_surface().get_size())
        background.set_alpha(127)
        background.fill(0)

        self.add_element("Background overlay", background)
        self.add_element("Paused text", paused_text)
        self.add_element("Play", play_button)
        self.add_element("Settings", settings_button)
        self.add_element("Credits", credits_button)
        self.add_element("Quit", quit_button)


class GameOverOverlay(GUIScreen):

    def playerWon(self):
        if consts.game != None:
            return consts.game.get_player().health > 0 and consts.game.get_player().drunkenness > 9

    def play_action(self):
        consts.LOGGER.debug("VALHALLA", "Going back to game")
        consts.game.music.stop()
        if self.playerWon():
            consts.game.paused = False
            consts.game.scenes[consts.current_scene].entities["ENEMIES"].append(1)
            consts.game.game_over = False
        else:
            with open("data/score.dat", "w") as file:
                if consts.score >= consts.high_score:
                    file.write(str(consts.score))
            file.close()
            consts.game = Game()

    def quit_action(self):
        consts.game.music.stop()
        with open("data/score.dat", "w") as file:
            if consts.score >= consts.high_score:
                file.write(str(consts.score))
        file.close()
        consts.current_screen = Screens.MAIN_MENU
        consts.game.paused = False

    def __init__(self):
        super().__init__()

        play_offset = (-164, -64)
        quit_offset = (-164, 80)

        window_width, window_height = pygame.display.get_surface().get_size()

        game_result_str = ""
        if self.playerWon():
            game_result_str = "Level cleared!"
        else:
            if consts.game.get_player().drunkenness <= 0:
                game_result_str = "You ran out of beer!"
            else:
                game_result_str = "You died"
        game_over_text = Text("Game Over!", "Pixellari", 48, x=(window_width / 2) - 128, y=(window_height / 8))
        game_result_text = Text(game_result_str, "Pixellari", 32)
        game_result_text.set_pos((
            (window_width / 2) - game_result_text.get_size()[0] / 2,
            game_over_text.get_pos()[1] + game_over_text.get_size()[1]  # + (game_result_text.get_size()[1] / 2)
        ))

        play_text = Text("Play again" if not self.playerWon() else "Continue", "Pixellari", 26)
        play_button = Button(
            play_text,
            (328, 64),
            (window_width / 2 + play_offset[0], window_height / 2 + play_offset[1])
        )
        play_button.set_action(self.play_action)

        quit_text = Text("Quit to main menu", "Pixellari", 26)
        quit_button = Button(
            quit_text,
            # (window_width / 2 + quit_offset[0], window_height / 2 + quit_offset[1]),
            (328, 64),
            (play_button.get_pos()[0], play_button.get_pos()[1] + play_button.get_size()[1] + 8)
        )
        quit_button.set_action(self.quit_action)

        background = pygame.Surface(pygame.display.get_surface().get_size())
        background.set_alpha(127)
        background.fill(0)

        self.add_element("Background overlay", background)
        self.add_element("Game over text", game_over_text)
        self.add_element("Game result text", game_result_text)
        self.add_element("Play", play_button)
        self.add_element("Quit", quit_button)

    def render(self):
        super(GameOverOverlay, self).render()
        game_result_str = "You won" if self.playerWon() else "You lost"
        text_width, text_height = self.components["Game result text"].get_size()
        game_result_pos = (pygame.display.get_surface().get_size()[0] / 2 - text_width / 2,
                           self.components["Game result text"].get_pos()[1])
        self.components["Game result text"].set_pos(game_result_pos)
        self.components["Game result text"].set_text(game_result_str)


class SplashScreen(GUIScreen):

    def __init__(self):
        super().__init__()

        self.loading = 0

        window_width, window_height = pygame.display.get_surface().get_size()

        usw_logo = util.Image(consts.MANIFEST["TEXTURES"]["GUI"]["usw_logo"])
        usw_logo = pygame.transform.scale(usw_logo.render(), (192, 192))

        usw_logo_width, usw_logo_height = usw_logo.get_size()
        self.add_element_position("USW logo", usw_logo,
                                  (window_width / 2 - usw_logo_width / 2, window_height / 2 - (usw_logo_height / 2)))

        caption_str = "A game created by students at the"
        usw_str = "University of South Wales"

        caption_text = Text(caption_str, "Pixellari", 26)
        self.usw_text = Text(usw_str, "Pixellari", 26)

        caption_text_width, caption_text_height = caption_text.get_size()
        usw_text_width, usw_text_height = self.usw_text.get_size()

        caption_text.set_pos((
            window_width / 2 - caption_text_width / 2,
            (window_height / 2 + usw_logo_height / 2) + caption_text_height
            # window_height / 2 + (caption_text_height / 2
        ))
        self.usw_text.set_pos((
            window_width / 2 - usw_text_width / 2,
            (window_height / 2 + usw_logo_height / 2) + (usw_text_height / 2) + caption_text_height + 16))

        self.loadedPercent_text = Text("0%", "Pixellari", 24)
        self.loadedPercent_text.set_pos((self.usw_text.get_pos()[0] + (self.usw_text.get_size()[0] / 2) - (
                self.loadedPercent_text.get_size()[0] / 2), self.usw_text.get_pos()[1] + 28))
        self.loadedPercent_text.set_color((0, 0, 0))

        self.add_element("Caption", caption_text)
        self.add_element("USW", self.usw_text)

    def handle_key_event(self):
        super(SplashScreen, self).handle_key_event()

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            consts.current_screen = Screens.QUIT

    def render(self):
        super(SplashScreen, self).render()

        loading_bar_thickness = 2
        loading_bar_width = self.usw_text.get_size()[0]
        loaded_width = util.bind(self.loading, 0, 100, 1, loading_bar_width - (loading_bar_thickness * 2), True)
        loadingbar_pos = (self.usw_text.get_pos()[0], self.usw_text.get_pos()[1] + 32)

        loading_bar = pygame.Surface((loading_bar_width, 32))
        loading_bar.fill((255, 255, 255))

        loaded_bar = pygame.Surface((loaded_width, 32 - (loading_bar_thickness * 2)))
        loaded_bar.fill((255, 0, 0))

        self.loadedPercent_text.set_pos((loadingbar_pos[0] + (loading_bar.get_size()[0] / 2) - (
               self.loadedPercent_text.get_size()[0] / 2), loadingbar_pos[1] + (32 / 2) - (
                                                self.loadedPercent_text.get_size()[1] / 2) + 2))
        pygame.display.get_surface().blit(loading_bar, (loadingbar_pos[0], loadingbar_pos[1]))
        pygame.display.get_surface().blit(loaded_bar, (
        loadingbar_pos[0] + loading_bar_thickness, loadingbar_pos[1] + loading_bar_thickness))
        pygame.display.get_surface().blit(self.loadedPercent_text.render(), self.loadedPercent_text.get_pos())

        if self.loading <= 100:
            self.loadedPercent_text.set_text(f"{self.loading}%")

        self.loading += 1

    def loaded(self):
        return self.loading >= 250


class MainMenu(GUIScreen):

    def continue_action(self):
        consts.LOGGER.debug("VALHALLA", "Continue button pressed")
        consts.current_screen = Screens.GAME
        consts.LOGGER.info("VALHALLA", "Initializing new game")

    def play_action(self):
        if not consts.SETTINGS["HUMAN_SOUNDS"]["SKIP_WARNING"]:
            consts.current_screen = Screens.SOUND_WARNING
        else:
            consts.LOGGER.debug("VALHALLA", "Play button pressed")
            consts.current_screen = Screens.GAME
            consts.LOGGER.info("VALHALLA", "Initializing new game")
            consts.game = Game()
            consts.start_time = pygame.time.get_ticks()

    def settings_action(self):
        consts.LOGGER.debug("VALHALLA", "Settings button pressed")
        consts.last_screen = Screens.MAIN_MENU
        consts.current_screen = Screens.SETTINGS

    def credits_action(self):
        consts.LOGGER.debug("VALHALLA", "Credits button pressed")
        consts.last_screen = Screens.MAIN_MENU
        consts.current_screen = Screens.CREDITS

    def quit_action(self):
        consts.LOGGER.debug("VALHALLA", "Quit button pressed")
        consts.current_screen = Screens.QUIT

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()

        # Buttons offset
        self.continue_offset = (-164, -128)
        self.play_offset = (-164, -64)
        self.settings_offset = (-160 - 4, 8)
        self.credits_offset = (4, 8)
        self.quit_offset = (-164, 80)

        # Text offset
        version_offset = (-166, -32)

        controls_title_offset = (6, -86)
        move_offset = (8, -56)
        attack_offset = (8, -32)

        logo_temp_text = Text("THE BEERZERKER", "Pixellari", 48, x=(window_width / 2) - 196, y=(window_height / 6))
        continue_text = Text("Continue", "Pixellari", 26)
        self.continue_button = Button(
            continue_text,
            (328, 64),
            (window_width / 2 + self.continue_offset[0], window_height / 2 + self.continue_offset[1])
        )
        self.continue_button.set_action(self.continue_action)

        play_text = Text("Play", "Pixellari", 26)
        self.play_button = Button(
            play_text,
            (328, 64),
            (window_width / 2 + self.play_offset[0], window_height / 2 + self.play_offset[1])
        )
        self.play_button.set_action(self.play_action)

        settings_text = Text("Settings", "Pixellari", 26)
        self.settings_button = Button(
            settings_text,
            (160, 64),
            (window_width / 2 + self.settings_offset[0], window_height / 2 + self.settings_offset[1])
        )
        self.settings_button.set_action(self.settings_action)

        credits_text = Text("Credits", "Pixellari", 26)
        self.credits_button = Button(
            credits_text,
            (160, 64),
            (window_width / 2 + self.credits_offset[0], window_height / 2 + self.credits_offset[1])
        )
        self.credits_button.set_action(self.credits_action)

        quit_text = Text("Quit", "Pixellari", 26)
        self.quit_button = Button(
            quit_text,
            (328, 64),
            (window_width / 2 + self.quit_offset[0], window_height / 2 + self.quit_offset[1])
        )
        self.quit_button.set_action(self.quit_action)

        version_text = Text(f"Version {consts.version}", "Pixellari", 26)
        version_text.set_pos(
            (
                pygame.display.get_surface().get_size()[0] - version_text.get_size()[0] - 4,
                pygame.display.get_surface().get_size()[1] - version_text.get_size()[1] - 8
            )
        )

        formatted_score = f"{consts.high_score:,.1e}"
        score_text_str = formatted_score if consts.high_score >= 1000000000 else f"{consts.high_score:,}"
        score_text = Text(f"Highest score: {score_text_str}", "Pixellari", 26)
        score_text.set_pos(
            (
                pygame.display.get_surface().get_size()[0] - score_text.get_size()[0] - 4,
                pygame.display.get_surface().get_size()[1] - score_text.get_size()[1] - version_text.get_size()[1] - 8
            )
        )

        version_text_link = Link(version_text, "https://github.com/PlaceholderGames/2020-yr1-group-3/releases/latest")

        controls_text = Text("Controls:", "Pixellari", 28)
        move_text = Text("WASD / arrow keys to move", "Pixellari", 26)
        sprint_text = Text("Hold shift to sprint", "Pixellari", 26)
        attack_text = Text("Left click to attack", "Pixellari", 26)

        attack_text.set_pos((8, window_height - attack_text.get_size()[1] - 6))
        sprint_text.set_pos((8, attack_text.get_pos()[1] - attack_text.get_size()[1] - 4))
        move_text.set_pos((8, sprint_text.get_pos()[1] - sprint_text.get_size()[1] - 4))
        controls_text.set_pos((8, move_text.get_pos()[1] - move_text.get_size()[1] - 6))

        self.add_element("Logo", logo_temp_text)
        self.add_element("Play", self.play_button)
        self.add_element("Settings", self.settings_button)
        self.add_element("Credits", self.credits_button)
        self.add_element("Quit", self.quit_button)

        self.add_element("High Score", score_text)
        self.add_element("Version", version_text_link)
        self.add_element("Controls text", controls_text)
        self.add_element("Move controls text", move_text)
        self.add_element("Sprint control text", sprint_text)
        self.add_element("Attack controls text", attack_text)

    def render(self):
        super(MainMenu, self).render()

        window_width, window_height = pygame.display.get_surface().get_size()
        if consts.game is None:
            self.play_offset = (-164, -64)
            self.settings_offset = (-160 - 4, 8)
            self.credits_offset = (4, 8)
            self.quit_offset = (-164, 80)
        else:
            self.add_element("Continue", self.continue_button)
            self.continue_offset = (-164, -64)
            self.play_offset = (-164, 8)
            self.settings_offset = (-164, 80)
            self.credits_offset = (4, 80)
            self.quit_offset = (-164, 152)

        continue_text = Text("Continue", "Pixellari", 26)
        self.continue_button = Button(
            continue_text,
            (328, 64),
            (window_width / 2 + self.continue_offset[0], window_height / 2 + self.continue_offset[1])
        )
        self.continue_button.set_action(self.continue_action)

        play_text = Text("Play" if consts.game is None else "New game", "Pixellari", 26)
        self.play_button = Button(
            play_text,
            (328, 64),
            (window_width / 2 + self.play_offset[0], window_height / 2 + self.play_offset[1])
        )
        self.play_button.set_action(self.play_action)

        settings_text = Text("Settings", "Pixellari", 26)
        self.settings_button = Button(
            settings_text,
            (160, 64),
            (window_width / 2 + self.settings_offset[0], window_height / 2 + self.settings_offset[1])
        )
        self.settings_button.set_action(self.settings_action)

        credits_text = Text("Credits", "Pixellari", 26)
        self.credits_button = Button(
            credits_text,
            (160, 64),
            (window_width / 2 + self.credits_offset[0], window_height / 2 + self.credits_offset[1])
        )
        self.credits_button.set_action(self.credits_action)

        quit_text = Text("Quit", "Pixellari", 26)
        self.quit_button = Button(
            quit_text,
            (328, 64),
            (window_width / 2 + self.quit_offset[0], window_height / 2 + self.quit_offset[1])
        )
        self.quit_button.set_action(self.quit_action)

        self.add_element("Play", self.play_button)
        self.add_element("Settings", self.settings_button)
        self.add_element("Credits", self.credits_button)
        self.add_element("Quit", self.quit_button)


class SettingScreen(GUIScreen):

    def back_action(self):
        consts.LOGGER.debug("VALHALLA", "Back button pressed")
        consts.current_screen = consts.last_screen

    def save_action(self):
        consts.LOGGER.debug("VALHALLA", "Save button pressed")
        consts.SETTINGS = {
            "FULLSCREEN": self.fullscreen_checkbox.state,
            "HUMAN_SOUNDS": {
                "VALUE": self.human_sound_checkbox.state,
                "SKIP_WARNING": consts.SETTINGS["HUMAN_SOUNDS"]["SKIP_WARNING"]
            },
            "MUSIC": self.music_checkbox.state
        }
        util.save_to_settings_file()
        self.showSavingText = 32

    def handle_key_event(self):
        super(SettingScreen, self).handle_key_event()

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            consts.current_screen = consts.last_screen

    def __init__(self):
        super().__init__()

        self.showSavingText = 0

        window_width, window_height = pygame.display.get_surface().get_size()

        screen_title = Text("Settings", "Pixellari", 32)
        screen_title.set_pos((screen_title.get_size()[0] / 2, screen_title.get_size()[1]))

        note_text = Text("Settings marked with '*' require a game restart.", "Pixellari", 26)
        note_text.set_pos((screen_title.get_pos()[0], screen_title.get_pos()[1] + screen_title.get_size()[1]))

        self.fullscreen_checkbox = Checkbox(Text("Fullscreen*", "Pixellari", 26))
        self.fullscreen_checkbox.set_pos(
            (screen_title.get_pos()[0], note_text.get_pos()[1] + (note_text.get_size()[1] * 2)))
        self.fullscreen_checkbox.state = consts.SETTINGS['FULLSCREEN']

        self.human_sound_checkbox = Checkbox(Text("Enable Human Sounds", "Pixellari", 26))
        self.human_sound_checkbox.set_pos((self.fullscreen_checkbox.get_pos()[0],
                                           self.fullscreen_checkbox.get_pos()[1] + self.fullscreen_checkbox.get_size()[
                                               1] + 4))
        self.human_sound_checkbox.state = consts.SETTINGS['HUMAN_SOUNDS']['VALUE']

        self.music_checkbox = Checkbox(Text("Music", "Pixellari", 26))
        self.music_checkbox.set_pos((self.human_sound_checkbox.get_pos()[0], self.human_sound_checkbox.get_pos()[1] + self.human_sound_checkbox.get_size()[1] + 4))
        self.music_checkbox.state = consts.SETTINGS['MUSIC']

        back_button = Button(
            Text("Back", "Pixellari", 26),
            (128, 64),
            (screen_title.get_pos()[0], window_height - (64 + 18))
        )
        back_button.set_action(self.back_action)

        save_button = Button(
            Text("Save", "Pixellari", 26),
            (128, 64),
            (back_button.get_pos()[0] + back_button.get_size()[0] + 16, window_height - (64 + 18))
        )
        save_button.set_action(self.save_action)

        self.add_element("Settings title", screen_title)
        self.add_element("Note Text", note_text)

        self.add_element("Fullscreen", self.fullscreen_checkbox)
        self.add_element("Human Sound", self.human_sound_checkbox)
        self.add_element("Music", self.music_checkbox)

        self.add_element("Back button", back_button)
        self.add_element("Save button", save_button)

    def render(self):
        super(SettingScreen, self).render()

        window_width, window_height = pygame.display.get_surface().get_size()
        saving_text = Text("Settings saved to file", "Pixellari", 26)
        saving_text.set_pos((window_width - (saving_text.get_size()[0] + 16),
                             window_height - (saving_text.get_size()[1] + 18)))

        if self.showSavingText > 0:
            self.components["Saving text"] = saving_text
            self.showSavingText -= 1

        if self.showSavingText == 1:
            self.showSavingText = 0
            self.components.pop("Saving text")
            consts.current_screen = consts.last_screen


class CreditScreen(GUIScreen):

    def back_action(self):
        consts.LOGGER.debug("VALHALLA", "Back button pressed")
        consts.current_screen = consts.last_screen

    def handle_key_event(self):
        super(CreditScreen, self).handle_key_event()

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            consts.current_screen = consts.last_screen

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()

        back_offset = (-64, 192)
        screen_title = Text("Credits", "Pixellari", 32)
        screen_title.set_pos((screen_title.get_size()[0] / 2, screen_title.get_size()[1]))

        bitheral_link = "https://bitheral.net"
        bartosz_link = "https://github.com/BartoszTrylockSW"
        connor_link = "https://github.com/SirJinxy"
        munknorr_link = "http://munknorr.com"

        lead_programmer_title = Text(
            "Lead Programmer",
            "Pixellari",
            30,
            x=screen_title.get_pos()[0],
            y=screen_title.get_pos()[1] + (screen_title.get_size()[1] * 2)
        )
        lead_programmer_credit = Link(Text(
            "Bitheral",
            "Pixellari",
            26,
            x=lead_programmer_title.get_pos()[0],
            y=lead_programmer_title.get_pos()[1] + lead_programmer_title.get_size()[1]
        ), bitheral_link)

        programmer_title = Text(
            "Programmers",
            "Pixellari",
            30,
            x=screen_title.get_pos()[0],
            y=lead_programmer_title.get_pos()[1] + lead_programmer_title.get_size()[1] +
              lead_programmer_credit.get_size()[1] * 2
        )
        programmer_credit = Link(Text(
            "Bartosz Swieszkowski",
            "Pixellari",
            26,
            x=programmer_title.get_pos()[0],
            y=programmer_title.get_pos()[1] + programmer_title.get_size()[1]
        ), bartosz_link)

        artist_title = Text(
            "Artists",
            "Pixellari",
            30,
            x=screen_title.get_pos()[0],
            y=programmer_title.get_pos()[1] + programmer_title.get_size()[1] + programmer_credit.get_size()[1] * 2
        )
        artist_credit_1 = Link(Text(
            "Bartosz Swieszkowski",
            "Pixellari",
            26,
            x=artist_title.get_pos()[0],
            y=artist_title.get_pos()[1] + artist_title.get_size()[1]
        ), bartosz_link)
        artist_credit_2 = Link(Text(
            "Connor Hughes",
            "Pixellari",
            26,
            x=artist_title.get_pos()[0],
            y=artist_credit_1.get_pos()[1] + artist_credit_1.get_size()[1] + 4
        ), connor_link)

        audio_design_title = Text(
            "Audio Design",
            "Pixellari",
            30,
            x=screen_title.get_pos()[0],
            y=artist_title.get_pos()[1] + (artist_credit_1.get_size()[1] * 4)
        )
        audio_design_credit = Link(Text(
            "Bitheral",
            "Pixellari",
            26,
            x=audio_design_title.get_pos()[0],
            y=audio_design_title.get_pos()[1] + audio_design_title.get_size()[1]
        ), bitheral_link)

        music_title = Text(
            "Music",
            "Pixellari",
            30,
            x=lead_programmer_title.get_pos()[0] + lead_programmer_title.get_size()[0] + 32,
            y=lead_programmer_title.get_pos()[1]
        )
        music_credit = Link(Text(
            "Munknörr / Damián Schneider",
            "Pixellari",
            26,
            x=music_title.get_pos()[0],
            y=music_title.get_pos()[1] + music_title.get_size()[1]
        ), munknorr_link)

        back_text = Text("Back", "Pixellari", 26)
        back_button = Button(
            back_text,
            (128, 64),
            (screen_title.get_pos()[0], window_height - (64 + 18))
        )
        back_button.set_action(self.back_action)

        self.add_element("Credit title", screen_title)

        self.add_element("Lead Programmer title", lead_programmer_title)
        self.add_element("Lead Programmer credit", lead_programmer_credit)

        self.add_element("Programmer title", programmer_title)
        self.add_element("Programmer credit", programmer_credit)

        self.add_element("Artist title", artist_title)
        self.add_element("Artist credit 1", artist_credit_1)
        self.add_element("Artist credit 2", artist_credit_2)

        self.add_element("Audio design title", audio_design_title)
        self.add_element("Audio design credit", audio_design_credit)

        self.add_element("Music title", music_title)
        self.add_element("Music credit", music_credit)

        self.add_element("Back button", back_button)
