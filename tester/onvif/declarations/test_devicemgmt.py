# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.onvif.declarations import ONVIF_DEVICEMGMT


class DevicemgmtTestCase(TestCase):
    def test_default(self):
        ONVIF_DEVICEMGMT.load_document()
        self.assertIsNotNone(ONVIF_DEVICEMGMT.document)


if __name__ == "__main__":
    main()
