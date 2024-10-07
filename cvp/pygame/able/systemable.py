# -*- coding: utf-8 -*-

from pygame import system as pg_system


class Systemable:
    @staticmethod
    def system_get_cpu_instruction_sets():
        return pg_system.get_cpu_instruction_sets()

    @staticmethod
    def system_get_total_ram():
        return pg_system.get_total_ram()

    @staticmethod
    def system_get_pref_path(org: str, app: str):
        return pg_system.get_pref_path(org, app)

    @staticmethod
    def system_get_pref_locales():
        return pg_system.get_pref_locales()

    @staticmethod
    def system_get_power_state():
        return pg_system.get_power_state()
