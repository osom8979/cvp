# -*- coding: utf-8 -*-

from typing import Final, Sequence, Tuple

from OpenGL.GL import GL_LINES, glBegin, glEnd, glVertex3fv

CUBE_VERTICES: Final[Sequence[Tuple[float, float, float]]] = (
    (+1.0, -1.0, -1.0),
    (+1.0, +1.0, -1.0),
    (-1.0, +1.0, -1.0),
    (-1.0, -1.0, -1.0),
    (+1.0, -1.0, +1.0),
    (+1.0, +1.0, +1.0),
    (-1.0, -1.0, +1.0),
    (-1.0, +1.0, +1.0),
)

CUBE_EDGES: Final[Sequence[Tuple[int, int]]] = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7),
)


def draw_simple_cube():
    glBegin(GL_LINES)
    for edge in CUBE_EDGES:
        for vertex in edge:
            glVertex3fv(CUBE_VERTICES[vertex])
    glEnd()
