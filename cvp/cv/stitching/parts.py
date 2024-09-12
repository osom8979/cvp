# -*- coding: utf-8 -*-

import os

import cv2


class StitcherPart:
    def __init__(self, filename: str):
        self.filename = filename
        self.original = self.read_image(filename)

    @staticmethod
    def read_image(filename: str):
        if not os.path.isfile(filename):
            filename = cv2.samples.findFile(filename)

        if not os.path.isfile(filename):
            raise FileNotFoundError(f"Not found file: '{filename}'")

        return cv2.imread(filename)

    def clear(self) -> None:
        pass
