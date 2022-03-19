import source.enemy as enemy

enemy_stat = {
    # hp, dmg, score, shoot_cd, mlee cd
    'r': [50, 50, 15, 500, 5000],
    'b': [150, 200, 50, 2000, 7000],
    'y': [225, 25, 10, 5000, 5000],
    'g': [500, 50, 100, 2000, 10000],
    'y_boss': [35000, 75, 10000, 2000, 50000],
    'b_split_bouncy1': [150, 200, 50, 2000, 7000],
    'b_split_bouncy_raining': [150, 120, 500, 150, 7000],
    'p': [125, 50, 75, 3000, 5000],
    'p_gatling': [275, 50, 75, 2000, 5000],
    'o': [200, 100, 100, 2, 5000],
    'b_boss_rotate': [55000, 75, 10000, 5000, 50000]
}


def enemy_grid_deploy(rows, cols, col_distance=80, row_distance=55,
                      initial_x=70, initial_y=50, colors='', x_speed=1, y_speed=1):
    if type(colors) is list:
        assert (len(colors) == rows)
        for _ in colors:
            assert (len(_) == cols)

    enemies = [[enemy.Enemy()] * cols for _ in range(rows)]
    counter = 0

    for y in range(rows):
        for x in range(cols):
            color = colors if type(colors) is not list else colors[y][x]
            color = color if color in enemy_stat else color.split('_')[0]
            if color.split('_')[0] in enemy_stat:
                counter += 1
                enemies[y][x] = (enemy.Enemy(color,
                                             x * col_distance + initial_x,
                                             y * row_distance + initial_y,
                                             *enemy_stat[color]))
            else:
                # noinspection PyTypeChecker
                enemies[y][x] = None

    return enemy.EnemyArmy(enemies, counter, x_speed, y_speed)


def enemy_row_deploy(cols, col_distance=80,
                     initial_x=200, initial_y=100, colors='', x_speed=1, y_speed=1):
    if type(colors) is list:
        assert (len(colors[0]) == cols)

    enemies = [[enemy.Enemy()] * cols]
    counter = 0

    for x in range(cols):
        color = colors if type(colors) is not list else colors[0][x]
        color = color if color in enemy_stat else color.split('_')[0]
        if color.split('_')[0] in enemy_stat:
            counter += 1
            enemies[0][x] = (enemy.Enemy(color,
                                         x * col_distance + initial_x,
                                         initial_y,
                                         *enemy_stat[color]
                                         ))
        else:
            # noinspection PyTypeChecker
            enemies[0][x] = None

    return enemy.EnemyArmy(enemies, counter, x_speed, y_speed)


def enemy_col_deploy(rows, row_distance=55,
                     initial_x=70, initial_y=100, colors='', x_speed=1, y_speed=1):
    if type(colors) is list:
        assert (len(colors) == rows)

    enemies = [[enemy.Enemy()] for _ in range(rows)]
    counter = 0

    for y in range(rows):

        color = colors if type(colors) is not list else colors[y][0]
        color = color if color in enemy_stat else color.split('_')[0]
        if color.split('_')[0] in enemy_stat:
            counter += 1
            enemies[y][0] = (enemy.Enemy(color,
                                         initial_x,
                                         y * row_distance + initial_y,
                                         *enemy_stat[color]
                                         ))
        else:
            # noinspection PyTypeChecker
            enemies[y][0] = None

    return enemy.EnemyArmy(enemies, counter, x_speed, y_speed)
