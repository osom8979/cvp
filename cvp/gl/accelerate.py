# -*- coding: utf-8 -*-


def load_accelerate():
    # [IMPORTANT]
    # Do not change the import order!
    # Prevents modules from being preloaded.
    from OpenGL.acceleratesupport import ACCELERATE_AVAILABLE

    return ACCELERATE_AVAILABLE
