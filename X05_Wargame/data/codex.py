# [mov(pix),melee_ability,distance_ability,distance_range,strength,resist]

CODEX = {'archers': [[160, 4, 5, 360, 3, 4], 'infantry'],
         'spearmen': [[180, 5, 0, 0, 6, 5], 'infantry'],
         'swordsmen': [[180, 6, 0, 0, 5, 5], 'infantry'],
         'cavalry': [[280, 7, 0, 0, 6, 6], 'cavalry'],
         'canon': [[120, 1, 5, 800, 9, 8], 'artillery']}


def get_stats(name):
    return CODEX[name][0]


def get_category(name):
    return CODEX[name][1]
