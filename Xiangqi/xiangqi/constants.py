# Board
RANKS = 10
FILES = 9

RANK_RANGE = range(RANKS, 0, -1)
FILES_RANGE = range(FILES, 0, -1)

# Pieces
ADVISOR = 'advisor'
CANNON = 'cannon'
CHARIOT = 'chariot'
ELEPHANT = 'elephant'
GENERAL = 'general'
HORSE = 'horse'
SOLDIER = 'soldier'

PIECES_REFERENCE = {
    ADVISOR: 'A',
    CANNON: 'C',
    CHARIOT: 'R',  # R for Rook
    ELEPHANT: 'E',
    GENERAL: 'G',
    HORSE: 'H',
    SOLDIER: 'S'
}

PIECES_UNITS = {
    ADVISOR: 2,
    CANNON: 2,
    CHARIOT: 2,
    ELEPHANT: 2,
    GENERAL: 1,
    HORSE: 2,
    SOLDIER: 5
}

PIECES_STARTING_POINTS = {
    ADVISOR: ['14', '16'],
    CANNON: ['32', '38'],
    CHARIOT: ['11', '19'],
    ELEPHANT: ['13', '17'],
    GENERAL: ['15'],
    HORSE: ['12', '18'],
    SOLDIER: ['41', '43', '45', '47', '49']
}
