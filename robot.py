#!/usr/bin/python
""" Check if a given sequence of moves for a robot is circular or not
    http://www.geeksforgeeks.org/check-if-a-given-sequence-of-moves-for-a-robot-is-circular-or-not/

    Given a sequence of moves for a robot, check if the sequence is circular or not.
    A sequence of moves is circular if first and last positions of robot are same.
    A move can be on of the following.
    G - Go one unit
    L - Turn left
    R - Turn right

    Examples:

    Input: path[] = "GLGLGLG"
    Output: Given sequence of moves is circular

    (PYBABIES series)
"""
__author__ = 'GarryY'
__version__ = '1.0'

import sys

pos0 = (0,0)

#TODO - need more elegant next move calculation alg
def moveit(pos, direction, move):
    next_direction = direction
    next_pos = pos
    if move == 'G':
        next_pos = (pos[0]+direction[0], pos[1]+direction[1])
    elif move == 'L':
        modifier = 1 if direction[0] else -1
        next_direction = tuple(e*modifier for e in reversed(direction))
    elif move == 'R':
        modifier = -1 if direction[0] else 1
        next_direction = tuple(e*modifier for e in reversed(direction))
    else:
        next_pos = next_direction = None

    print pos, direction, move, '|', next_pos, next_direction

    return next_pos, next_direction

def move_robot(moves):
    pos = pos0
    direction = (1,0)
    for move in moves:
        pos, direction = moveit(pos, direction, move)
    return pos

def is_circular(pos):
    return pos == pos0

valid_moves = "GLR"
if len(sys.argv) <= 1:
    print 'No moves specified'
    sys.exit(1)
#moves = 'GLLG'
moves = sys.argv[1].upper()
if not all([(m in valid_moves) for m in moves]):
    print 'Not valid moves found'
    sys.exit(1)

last_pos = move_robot(moves)
print 'Given sequence of moves is %s (pos=%s)' % ('circular' if is_circular(last_pos) else 'NOT circular', last_pos)

