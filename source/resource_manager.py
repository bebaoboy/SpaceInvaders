import importlib
import pygame

from source import spritesheet, level
from source.levels import \
    level1, level2, level3, level4, level5, \
    level6, level7, level8, level9, level10, \
    level11

from source.resource_path import resource_path

enemy_pic = {
    'r': None,
    'b': None,
    'y': None,
    'g': None,
    'p': None,
    'o': None
}

explosion_pic = {
    'r': None,
    'b': None,
    'y': None,
    'g': None,
    'p': None,
    'o': None,
    'w': None
}

collectibles_pic = {
    'coin': None,
    'health_bag': None
}


class ResourceManager:
    def __init__(self):
        self.levels: list[type(level.Level)] = []

        for colors, lists in enemy_pic.items():
            enemy_pic[colors] = pygame.image.load(
                resource_path('graphics/' + colors.split('_')[0] + '.png')).convert_alpha()

        for colors, lists in explosion_pic.items():
            explosion_pic[colors] = pygame.image.load(
                resource_path('graphics/' + colors.split('_')[0] + '_ex.png')).convert_alpha()

        for coll, lists in collectibles_pic.items():
            if coll == 'coin':
                collectibles_pic[coll] = spritesheet.SpriteSheet(resource_path('graphics/coin.png'))
            else:
                collectibles_pic[coll] = pygame.image.load(
                    resource_path('graphics/' + coll + '.png')).convert_alpha()

    @staticmethod
    def import_level_by_name(module_name, class_name):
        # load the module, will raise ImportError if module cannot be loaded
        try:
            m = importlib.import_module(module_name)
            # spec = importlib.util.spec_from_file_location(module_name, full_path)
            # m = importlib.util.module_from_spec(spec)
            # spec.loader.exec_module(m)
            # get the class, will raise AttributeError if class cannot be found
            class_ = getattr(m, class_name)
            return class_
        except ImportError as err:
            print(err)

            # loaded_level = self.import_level_by_name(f'source.levels.level{i}',
            #                                          f'{os.getcwd()}/source/levels/level{i}.py', f'Level{i}')

    def exec_code(self, s):
        exec(s)
