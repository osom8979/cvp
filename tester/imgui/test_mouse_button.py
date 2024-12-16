# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.imgui.mouse_button import ButtonState, MouseButton


class DeltaTestCase(TestCase):
    def test_dragging(self):
        btn = MouseButton()
        btn.update(False, (0, 0))
        self.assertFalse(btn._down.changed)
        self.assertFalse(btn._down.value)
        self.assertFalse(btn._dragging.changed)
        self.assertFalse(btn._dragging.value)
        self.assertEqual(ButtonState.normal, btn._state)
        self.assertIsNone(btn.pivot)

        btn.update(False, (1, 1))
        self.assertFalse(btn._down.changed)
        self.assertFalse(btn._down.value)
        self.assertFalse(btn._dragging.changed)
        self.assertFalse(btn._dragging.value)
        self.assertEqual(ButtonState.normal, btn._state)
        self.assertIsNone(btn.pivot)

        btn.update(True, (2, 1))
        self.assertTrue(btn._down.changed)
        self.assertTrue(btn._down.value)
        self.assertFalse(btn._dragging.changed)
        self.assertFalse(btn._dragging.value)
        self.assertEqual(ButtonState.ready, btn._state)
        self.assertTupleEqual((2, 1), btn.pivot)

        btn.update(True, (2, 1))
        self.assertFalse(btn._down.changed)
        self.assertTrue(btn._down.value)
        self.assertFalse(btn._dragging.changed)
        self.assertFalse(btn._dragging.value)
        self.assertEqual(ButtonState.ready, btn._state)
        self.assertTupleEqual((2, 1), btn.pivot)

        btn.update(True, (2, 2))
        self.assertFalse(btn._down.changed)
        self.assertTrue(btn._down.value)
        self.assertTrue(btn._dragging.changed)
        self.assertTrue(btn._dragging.value)
        self.assertEqual(ButtonState.dragging, btn._state)
        self.assertTupleEqual((2, 1), btn.pivot)

        btn.update(True, (3, 2))
        self.assertFalse(btn._down.changed)
        self.assertTrue(btn._down.value)
        self.assertFalse(btn._dragging.changed)
        self.assertTrue(btn._dragging.value)
        self.assertEqual(ButtonState.dragging, btn._state)
        self.assertTupleEqual((2, 1), btn.pivot)

        btn.update(False, (3, 3))
        self.assertTrue(btn._down.changed)
        self.assertFalse(btn._down.value)
        self.assertTrue(btn._dragging.changed)
        self.assertFalse(btn._dragging.value)
        self.assertEqual(ButtonState.normal, btn._state)
        self.assertIsNone(btn.pivot)

    def test_click(self):
        btn = MouseButton()
        btn.update(False, (0, 0))
        self.assertFalse(btn._down.changed)
        self.assertFalse(btn._down.value)
        self.assertFalse(btn._dragging.changed)
        self.assertFalse(btn._dragging.value)
        self.assertEqual(ButtonState.normal, btn._state)
        self.assertIsNone(btn.pivot)

        btn.update(False, (1, 1))
        self.assertFalse(btn._down.changed)
        self.assertFalse(btn._down.value)
        self.assertFalse(btn._dragging.changed)
        self.assertFalse(btn._dragging.value)
        self.assertEqual(ButtonState.normal, btn._state)
        self.assertIsNone(btn.pivot)

        btn.update(True, (1, 1))
        self.assertTrue(btn._down.changed)
        self.assertTrue(btn._down.value)
        self.assertFalse(btn._dragging.changed)
        self.assertFalse(btn._dragging.value)
        self.assertEqual(ButtonState.ready, btn._state)
        self.assertTupleEqual((1, 1), btn.pivot)

        btn.update(True, (1, 1))
        self.assertFalse(btn._down.changed)
        self.assertTrue(btn._down.value)
        self.assertFalse(btn._dragging.changed)
        self.assertFalse(btn._dragging.value)
        self.assertEqual(ButtonState.ready, btn._state)
        self.assertTupleEqual((1, 1), btn.pivot)

        btn.update(False, (1, 1))
        self.assertTrue(btn._down.changed)
        self.assertFalse(btn._down.value)
        self.assertFalse(btn._dragging.changed)
        self.assertFalse(btn._dragging.value)
        self.assertEqual(ButtonState.normal, btn._state)
        self.assertIsNone(btn.pivot)

        btn.update(False, (1, 1))
        self.assertFalse(btn._down.changed)
        self.assertFalse(btn._down.value)
        self.assertFalse(btn._dragging.changed)
        self.assertFalse(btn._dragging.value)
        self.assertEqual(ButtonState.normal, btn._state)
        self.assertIsNone(btn.pivot)


if __name__ == "__main__":
    main()
