"""
    Author:  Nathan Dow / Bitheral
    Created: 27/10/2020
"""

import pygame
import math
import pytmx

import consts
from enums import Direction
from util import bind, Spritesheet, lerp, Image, ValhallaException

from random import randint, random


class Entity(object):

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.health = 100
        self.screen = pygame.display.get_surface()
        self.rect = pygame.rect.Rect((0,0, 32, 32))
        self.rect_colour = (255, 255, 255)
        self.speed = 1.4
        self.texture = None
        self.range_size = 50
        self.range = pygame.draw.circle(pygame.display.get_surface(), (255, 0, 255), (self.rect.x + (self.rect.width / 2), self.rect.y + (self.rect.height / 2)), self.range_size)

    def get_health(self):
        return self.health

    def take_damage(self, damage):
        self.health -= damage

    def heal(self, healing):
        self.health += healing

    def draw(self):
        if self.texture is None:
            pygame.draw.rect(self.screen, self.rect_colour, self.rect)
        else:
            self.screen.blit(self.texture, (self.rect.x, self.rect.y))

        if consts.SETTINGS["DEBUG_OVERLAY"]:
            pygame.draw.circle(pygame.display.get_surface(), (255, 0, 255),
                               (self.rect.x + (self.rect.width / 2), self.rect.y + (self.rect.height / 2)),
                               self.range_size)

    def update(self):
        # self.clock.tick(120)
        if self.rect.x + 32 >= self.screen.get_size()[0]:
            self.rect.x = self.screen.get_size()[0] - 32
        if self.rect.y + 32 >= self.screen.get_size()[1]:
            self.rect.y = self.screen.get_size()[1] - 32

        if self.get_health() < 100:
            if int(consts.time_since_start / 1000) % 2 == 0:
                self.heal(0.1)

        self.range.update(self.rect.x, self.rect.y, self.range_size, self.range_size)

    def collides(self, other):
        if self is not other:
            return self.rect.colliderect(other.rect)

    def in_range(self, other):
        return math.sqrt((self.range.x - other.range.x) ** 2 + (self.range.y - other.range.y) ** 2) <= (
                    self.range_size * 2)


# Uses player as a rectangle
# https://stackoverflow.com/questions/32061507/moving-a-rectangle-in-pygame
class Player(Entity):
    def __init__(self):
        super().__init__()
        self.items = []
        self.attacking = 0
        self.position = (self.rect.x, self.rect.y)
        self.atkr = pygame.rect.Rect((self.screen.get_size()[0] / 2, self.screen.get_size()[1] / 2, 16, 32))
        self.facing_direction = Direction.RIGHT
        self.attack_direction = Direction.RIGHT
        self.drunkenness = 100
        self.speed = 1.6
        self.rect_colour = (81, 81, 81)
        self.sprinting = False

        self.enemies_killed = 0
        self.bottles_drunk = 0

        self.texture = Image(consts.MANIFEST["TEXTURES"]["SPRITES"]["player"]).render()
        # upper_body = pygame.transform.scale(Spritesheet(consts.MANIFEST["TEXTURES"]["SPRITES"]["player"]).image_at((0,0, 32, 32), -1), (15, 15))
        # lower_body = pygame.transform.scale(Spritesheet(consts.MANIFEST["TEXTURES"]["SPRITES"]["player"]).image_at((0, 32, 32, 32), -1), (15, 15))
        # self.texture.blit(upper_body, (0, 0))
        # self.texture.blit(lower_body, (0, 15))

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def handle_keys(self):
        key = pygame.key.get_pressed()
        self.sprinting = bool(key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT])

        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.facing_direction = Direction.LEFT
            self.rect.move_ip(-self.speed, 0)
            self.atkr.move_ip(-self.speed, 0)
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.facing_direction = Direction.RIGHT
            self.rect.move_ip(self.speed, 0)
            self.atkr.move_ip(self.speed, 0)
        if key[pygame.K_UP] or key[pygame.K_w]:
            self.facing_direction = Direction.UP
            self.rect.move_ip(0, -self.speed)
            self.atkr.move_ip(0, -self.speed)
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            self.facing_direction = Direction.DOWN
            self.rect.move_ip(0, self.speed)
            self.atkr.move_ip(0, self.speed)

    def handle_mouse(self):
        mouse = pygame.mouse.get_pos()

        if pygame.event.get(pygame.MOUSEBUTTONDOWN) and pygame.mouse.get_pressed()[0]:
            self.attacking = 50

    def draw(self):
        super(Player, self).draw()
        if self.attacking != 0:
            self.screen.blit(pygame.transform.rotate(
                Spritesheet(consts.MANIFEST["TEXTURES"]["SPRITESHEETS"]["items"]).image_at((64, 0, 32, 32), -1),
                self.facing_direction.value), (self.atkr.x, self.atkr.y))
            # pygame.draw.rect(self.screen, (56, 56, 56), self.atkr)

    def update(self):
        super(Player, self).update()

        self.speed = 2 if self.sprinting else 1.6

        self.attack_rects = {
            "UP": pygame.rect.Rect((self.rect.x, self.rect.y - self.rect.height, self.rect.width, self.rect.height)),
            "RIGHT": pygame.rect.Rect((self.rect.x + self.rect.width, self.rect.y, self.rect.width, self.rect.height)),
            "DOWN": pygame.rect.Rect((self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height)),
            "LEFT": pygame.rect.Rect((self.rect.x - self.rect.width, self.rect.y, self.rect.width, self.rect.height)),
        }

        if self.attacking != 0:
            self.attacking -= 1
        elif self.attacking < 0:
            self.attacking = 0

        self.atkr = self.attack_rects[self.facing_direction.name]
        # if not self.sprinting:
        #     self.drunkenness -= 0.05
        # else:
        #     self.drunkenness -= 0.25

        if self.drunkenness > 100:
            self.drunkenness = 100

        for index, item in enumerate(self.items):
            if type(item) == Bottle:
                if self.drunkenness < 90:
                    if consts.SETTINGS["HUMAN_SOUNDS"]["VALUE"]:
                        pygame.mixer.Sound(consts.MANIFEST["AUDIO"]["SOUNDS"]["GAME"]["drink_use"]).play()
                    self.items.pop(index)
                    self.drunkenness += 20
                    self.bottles_drunk += 1

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        for index, item_entity in enumerate(self.items):
            if item_entity == item:
                self.items.pop(index)

    def get_items_by_type(self, classType):
        item_list = []
        for item in self.items:
            if type(item) == classType:
                item_list.append(item)
        return item_list


class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__()
        # Limit enemy spawn to window size
        self.rect = pygame.rect.Rect(
            (
                x,
                y,
                32,
                32
            )
        )
        self.rect_colour = (255, 0, 0)
        self.speed = 1
        self.hurting = 0

        randomId = int(round(random()))
        self.texture = pygame.transform.scale(
            Spritesheet(consts.MANIFEST["TEXTURES"]["SPRITESHEETS"]["guards"]).image_at(((randomId) * 32, 0, 32, 32),
                                                                                        -1), (32, 32))

    def follow(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        if abs(dx) <= self.screen.get_size()[0] and abs(dy) <= self.screen.get_size()[1]:
            move_x = abs(dx) > abs(dy)
            if abs(dx) > self.speed and abs(dy) > self.speed:
                move_x = random() < 0.5
            if move_x:
                self.rect.x += min(dx, self.speed) if dx > 0 else max(dx, -self.speed)
            else:
                self.rect.y += min(dy, self.speed) if dy > 0 else max(dy, -self.speed)

    def draw(self):
        super(Enemy, self).draw()
        healthPercent = self.health
        if self.hurting != 0:
            # Health bar - background
            pygame.draw.rect(self.screen, (24, 102, 19), (self.rect.x, self.rect.y - 32, 32, 16))
            pygame.draw.rect(self.screen, (58, 196, 51),
                             (self.rect.x, self.rect.y - 32, bind(healthPercent, 0, 100, 0, 32, True), 16))
        # pygame.draw.rect(self.screen, (255, 0, 0), self.rect)

    def update(self):
        super(Enemy, self).update()
        if self.hurting != 0:
            # consts.LOGGER.debug("VALHALLA", f"Enemy health: {self.health}")
            self.hurting -= 1


class DroppedItem(Entity):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.rect = pygame.rect.Rect((
            randint(0, self.screen.get_size()[0] - 32),
            randint(0, self.screen.get_size()[1] - 32),
            32, 32
        ))
        self.rect_colour = (0, 255, 0)

    def draw(self):
        super(DroppedItem, self).draw()

    def picked_up(self, player):
        return player.rect.colliderect(self.rect)


class Bottle(DroppedItem):
    def __init__(self, x, y):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.rect = pygame.rect.Rect((
            x,
            y,
            32, 32
        ))
        self.rect_colour = (0, 255, 0)

        self.sprite = Image(consts.MANIFEST["TEXTURES"]["SPRITES"]["beer_bottle"], transparency=True)

    def draw(self):
        # super(Bottle, self).draw()
        self.screen.blit(self.sprite.render(), (self.rect.x, self.rect.y))


class Collidable(object):
    def __init__(self, rect, inverse=False, show_collider=True):
        self.draw_rect = pygame.rect.Rect(rect)
        self.inverse = inverse
        self.show = show_collider
        self.collisionThickness = 2
        self.collideEdges = {
            "TOP": pygame.rect.Rect((self.draw_rect.x + self.collisionThickness, self.draw_rect.y,
                                     self.draw_rect.width - self.collisionThickness, self.collisionThickness)),
            "RIGHT": pygame.rect.Rect((self.draw_rect.x + (self.draw_rect.width - self.collisionThickness),
                                       self.draw_rect.y + self.collisionThickness,
                                       self.collisionThickness, self.draw_rect.height - self.collisionThickness)),
            "BOTTOM": pygame.rect.Rect((self.draw_rect.x + self.collisionThickness,
                                        self.draw_rect.y + (self.draw_rect.height - self.collisionThickness),
                                        self.draw_rect.width - self.collisionThickness, self.collisionThickness)),
            "LEFT": pygame.rect.Rect((self.draw_rect.x, self.draw_rect.y + self.collisionThickness,
                                      self.collisionThickness, self.draw_rect.height - self.collisionThickness)),
            "TOP_LEFT": pygame.rect.Rect((self.draw_rect.x, self.draw_rect.y,
                                          self.collisionThickness, self.collisionThickness)),
            "TOP_RIGHT": pygame.rect.Rect(
                (self.draw_rect.x + (self.draw_rect.width - self.collisionThickness), self.draw_rect.y,
                 self.collisionThickness, self.collisionThickness)),
            "BOTTOM_LEFT": pygame.rect.Rect(
                (self.draw_rect.x, self.draw_rect.y + (self.draw_rect.height - self.collisionThickness),
                 self.collisionThickness, self.collisionThickness)),
            "BOTTOM_RIGHT": pygame.rect.Rect((self.draw_rect.x + (self.draw_rect.width - self.collisionThickness),
                                              self.draw_rect.y + (self.draw_rect.height - self.collisionThickness),
                                              self.collisionThickness, self.collisionThickness))

        }

    def update(self, entity):
        for edge in self.collideEdges:
            collisionEdge = self.collideEdges[edge]
            if not isinstance(entity, int):
                if collisionEdge.colliderect(entity.rect):
                    if edge == "TOP":
                        if not self.inverse:
                            entity.rect.y = self.draw_rect.y - entity.rect.height
                        else:
                            entity.rect.y = self.draw_rect.y + self.collisionThickness
                    elif edge == "RIGHT":
                        if not self.inverse:
                            entity.rect.x = self.draw_rect.x + self.draw_rect.width
                        else:
                            entity.rect.x = (self.draw_rect.x + self.draw_rect.width) - (
                                    entity.rect.width + self.collisionThickness)
                    elif edge == "BOTTOM":
                        if not self.inverse:
                            entity.rect.y = self.draw_rect.y + self.draw_rect.height
                        else:
                            entity.rect.y = ((
                                                     self.draw_rect.y + self.draw_rect.height) - self.collisionThickness) - entity.rect.height
                    elif edge == "LEFT":
                        if not self.inverse:
                            entity.rect.x = self.draw_rect.x - entity.rect.width
                        else:
                            entity.rect.x = self.draw_rect.x + self.collisionThickness
                    elif edge == "TOP_LEFT":
                        entity.rect.x = self.draw_rect.x - entity.rect.width
                        entity.rect.y = self.draw_rect.y - entity.rect.height
                    elif edge == "TOP_RIGHT":
                        entity.rect.x = self.draw_rect.x + self.draw_rect.width
                        entity.rect.y = self.draw_rect.y - entity.rect.height
                    elif edge == "BOTTOM_LEFT":
                        entity.rect.x = self.draw_rect.x - entity.rect.width
                        entity.rect.y = self.draw_rect.y + self.draw_rect.height
                    elif edge == "BOTTOM_RIGHT":
                        entity.rect.x = self.draw_rect.x + entity.rect.width
                        entity.rect.y = self.draw_rect.y + self.draw_rect.height

    def is_colliding(self, entity):
        return self.draw_rect.colliderect(entity.rect)

    def draw(self):
        surface = pygame.display.get_surface()
        if self.show:
            pygame.draw.rect(surface, (0, 0, 255), self.draw_rect)
        if consts.SETTINGS['DEBUG_OVERLAY']:
            for edge in self.collideEdges:
                collisonEdge = self.collideEdges[edge]
                pygame.draw.rect(surface, (255, 127, 127), collisonEdge)


class Portal(object):

    def __init__(self, rect, angle, target_scene, target_pos):
        self.rect = pygame.rect.Rect(rect)
        self.target_scene = target_scene
        self.target_coords = target_pos
        self.angle = angle
        self.surface = pygame.transform.rotate(pygame.Surface((self.rect[2], self.rect[3])), self.angle)
        self.collision_rect = pygame.rect.Rect(self.rect[0], self.rect[1], self.surface.get_rect()[2],
                                               self.surface.get_rect()[3])

    def update(self, player):
        if self.collision_rect.colliderect(player.rect):
            consts.LOGGER.debug("VALHALLA", "Player used Portal")
            consts.LOGGER.debug("VALHALLA",
                                f"Switched scenes from {consts.game.scenes[consts.current_scene].name[2:].upper()} to {consts.game.scenes[self.target_scene].name[2:].upper()}")
            consts.current_scene = self.target_scene
            player.rect.x, player.rect.y = self.target_coords

    def render(self):
        surface = pygame.display.get_surface()
        aligned_pos = (
            self.surface.get_rect()[0] + self.rect[0],
            self.surface.get_rect()[1] + self.rect[1],
            self.surface.get_rect()[2],
            self.surface.get_rect()[3]
        )
        pygame.draw.rect(surface, (0, 0, 64), self.collision_rect)


# DEPRECATED
class Scene(object):

    def __init__(self, *args):
        raise ValhallaException("Scene class has been deprecated, please use SceneTXM")


class SceneTXM(object):

    def __init__(self, txm_file):
        self.map_data = pytmx.load_pygame(txm_file, pixelalpha=True)
        self.name = txm_file.split("/")[1].split("\\")[1].split(".")[0]
        self.size = self.map_data.width * self.map_data.tilewidth, self.map_data.height * self.map_data.tileheight
        self.collides = []
        self.entities = {
            "ITEMS": [],
            "ENEMIES": []
        }
        self.portals = []

        self.item_length = 0
        self.enemy_length = 0

        mainSurface = pygame.display.get_surface()
        scaled_x = pygame.display.get_surface().get_size()[0] / self.size[0]
        scaled_y = pygame.display.get_surface().get_size()[1] / self.size[1]
        # offset_x = (mainSurface.get_size()[0] - self.size[0]) / 2 if (self.size[0] < mainSurface.get_size()[0]) else 0
        # offset_y = (mainSurface.get_size()[1] - self.size[1]) / 2 if (self.size[1] < mainSurface.get_size()[1]) else 0

        for tile_object in self.map_data.objects:
            if tile_object.type == 'collider':
                building = Collidable((tile_object.x * scaled_x, tile_object.y * scaled_y, tile_object.width * scaled_x,
                                       tile_object.height * scaled_y), show_collider=False)
                self.collides.append(building)
            elif tile_object.type == 'bottle':
                self.entities["ITEMS"].append(Bottle(tile_object.x * scaled_x, tile_object.y * scaled_y))
                self.item_length += 1
            elif tile_object.type == 'enemy':
                self.entities["ENEMIES"].append(Enemy(tile_object.x * scaled_x, tile_object.y * scaled_y))
                self.enemy_length += 1
            elif tile_object.type == 'interior':
                building = Collidable((tile_object.x * scaled_x, tile_object.y * scaled_y, tile_object.width * scaled_x,
                                       tile_object.height * scaled_y), True, False)
                self.collides.append(building)
            elif tile_object.type == "portal":
                if tile_object.properties['show']:
                    portal_to = tile_object.properties['scene_id']
                    portal_rect = (tile_object.x * scaled_x, tile_object.y * scaled_y, tile_object.width * scaled_x,
                                   tile_object.height * scaled_y)
                    player_loc = tile_object.properties['player_x'] * scaled_x, tile_object.properties[
                        'player_y'] * scaled_y
                    self.portals.append(Portal(portal_rect, tile_object.rotation, portal_to, player_loc))
            elif tile_object.type == 'player':
                # # if consts.game is not None:
                #     print("There is player object")
                #     player = consts.game.get_player()
                #     player.set_pos(tile_object.x * scaled_x, tile_object.y * scaled_y)
                pass
            else:
                raise ValhallaException(
                    f"[{txm_file}]: Type {tile_object.type} is valid object type. This occurred for Object {tile_object.id}")

    def render_map(self, surface):
        for layer in self.map_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.map_data.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.map_data.tilewidth, y * self.map_data.tileheight))

    def surface(self):
        surface = pygame.Surface(self.size)
        self.render_map(surface)
        return surface  # pygame.transform.scale(surface, pygame.display.get_surface().get_size())

    def render(self):
        for portal in self.portals:
            portal.render()

        for collide in self.collides:
            collide.draw()

        for item in self.entities["ITEMS"]:
            item.draw()

        for enemy in self.entities["ENEMIES"]:
            if isinstance(enemy, Enemy):
                enemy.draw()

    def remaining_enemies(self):
        return len(self.get_entities_by_type("ENEMIES"))

    def get_entities(self):
        return self.entities

    def get_entities_by_type(self, type):
        return self.entities[type]

    def update(self, player):
        for portal in self.portals:
            portal.update(player)

        for collide in self.collides:
            collide.update(player)

        for entityType in self.entities:
            for index, entity in enumerate(self.entities[entityType]):
                for collide in self.collides:
                    collide.update(entity)

                if type(entity) == Enemy:
                    if entity.in_range(player):
                        entity.follow(player)

                    if entity.collides(player) or player.collides(entity):
                        player.take_damage(0.2)

                    if player.attacking != 0:
                        if entity.rect.colliderect(player.atkr) or (
                                entity.rect.colliderect(player.rect) and entity.rect.colliderect(player.atkr)):
                            entity.hurting = 100
                            entity.health -= 0.8

                    if entity.health <= 0:
                        self.entities["ENEMIES"].pop(index)
                        player.enemies_killed += 1

                elif type(entity) == Bottle:
                    if entity.picked_up(player):
                        sound = pygame.mixer.Sound(consts.MANIFEST["AUDIO"]["SOUNDS"]["GAME"]["bottle_pickup"])
                        sound.set_volume(0.2)
                        sound.play()
                        player.add_item(entity)
                        self.entities["ITEMS"].pop(index)

                if type(entity) == Enemy or type(entity) == Bottle:
                    entity.update()


class Game:

    def __init__(self):
        self.music = pygame.mixer.Channel(2)
        self.player = Player()
        consts.current_scene = 0
        self.scenes = []

        self.msc = pygame.mixer.Sound(consts.MANIFEST["AUDIO"]["MUSIC"]["game"])
        self.msc.set_volume(0.01)
        if consts.SETTINGS["MUSIC"]:
            self.music.play(self.msc, -1)
        else:
            self.music.stop()

        import glob
        for sceneFile in glob.glob("assets/maps/*.tmx"):
            self.scenes.append(SceneTXM(sceneFile))

        size = self.scenes[0].map_data.width * self.scenes[0].map_data.tilewidth, self.scenes[0].map_data.height * self.scenes[0].map_data.tileheight
        scaled_x = pygame.display.get_surface().get_size()[0] / size[0]
        scaled_y = pygame.display.get_surface().get_size()[1] / size[1]
        for tile_ob in self.scenes[0].map_data.objects:
            if tile_ob.type == 'player':
                self.player.set_pos(tile_ob.x * scaled_x, tile_ob.y * scaled_y)

        self.game_over = False
        self.paused = False

    def get_player(self):
        return self.player

    def is_paused(self):
        return self.paused

    def pause(self, pause):
        from enums import Screens
        if consts.SETTINGS["MUSIC"]:
            if not self.music.get_busy():
                self.music.play(self.msc, -1)
            else:
                if pause:
                    self.music.pause()
                elif not pause and consts.current_screen == Screens.GAME:
                    self.music.unpause()
        self.paused = pause

    def is_game_over(self):
        return self.game_over

    def render(self):
        surface = pygame.display.get_surface()
        currentScene = self.scenes[consts.current_scene]

        surface.blit(pygame.transform.scale(currentScene.surface(), pygame.display.get_surface().get_size()), (0, 0))

        self.player.draw()
        currentScene.render()

    def update(self):
        consts.time_since_start = pygame.time.get_ticks() - consts.start_time
        currentScene = self.scenes[consts.current_scene]

        currentScene.update(self.player)

        consts.score = (self.player.enemies_killed * 500) + (self.player.bottles_drunk * 20) # int((self.player.health + self.player.drunkenness) + ((currentScene.enemy_length - currentScene.remaining_enemies()) * 2))

        if self.player.health <= 0 or currentScene.remaining_enemies() == 0 or self.player.drunkenness < 9:
            self.game_over = True
            consts.LOGGER.info("VALHALLA", "Game over! Going back to MAIN_MENU")

        self.player.update()
        self.player.handle_keys()
        self.player.handle_mouse()
