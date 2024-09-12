# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import lru_cache
from typing import Final, Sequence

import cv2


@lru_cache
def _stitcher_mode_map():
    result = OrderedDict()
    result["PANORAMA"] = cv2.Stitcher_PANORAMA
    result["SCANS"] = cv2.Stitcher_SCANS
    return result


@lru_cache
def _exposure_compensator_map():
    result = OrderedDict()
    result["GainBlocks"] = cv2.detail.ExposureCompensator_GAIN_BLOCKS
    result["Gain"] = cv2.detail.ExposureCompensator_GAIN
    result["Channel"] = cv2.detail.ExposureCompensator_CHANNELS
    result["ChannelBlocks"] = cv2.detail.ExposureCompensator_CHANNELS_BLOCKS
    result["No"] = cv2.detail.ExposureCompensator_NO
    return result


@lru_cache
def _bundle_adjuster_map():
    result = OrderedDict()
    result["Ray"] = cv2.detail.BundleAdjusterRay
    result["Reproj"] = cv2.detail.BundleAdjusterReproj
    result["Affine"] = cv2.detail.BundleAdjusterAffinePartial
    result["No"] = cv2.detail.NoBundleAdjuster
    return result


FEATURES_FINDER_SURF: Final[str] = "SURF"
FEATURES_FINDER_ORB: Final[str] = "ORB"
FEATURES_FINDER_SIFT: Final[str] = "SIFT"
FEATURES_FINDER_BRISK: Final[str] = "BRISK"
FEATURES_FINDER_AKAZE: Final[str] = "AKAZE"


@lru_cache
def _features_finder_map():
    result = OrderedDict()
    try:
        # noinspection PyUnresolvedReferences
        _surf_create_func = cv2.xfeatures2d_SURF.create
        _surf_create_func()  # check if the function can be called
        result[FEATURES_FINDER_SURF] = _surf_create_func
    except (AttributeError, cv2.error):
        pass

    # if SURF not available, ORB is default
    result[FEATURES_FINDER_ORB] = cv2.ORB.create

    try:
        result[FEATURES_FINDER_SIFT] = cv2.SIFT.create
    except AttributeError:
        pass

    try:
        result[FEATURES_FINDER_BRISK] = cv2.BRISK.create
    except AttributeError:
        pass

    try:
        result[FEATURES_FINDER_AKAZE] = cv2.AKAZE.create
    except AttributeError:
        pass

    return result


_SEAM_FINDER_VORONOI_SEAM: Final[int] = cv2.detail.SeamFinder_VORONOI_SEAM
_SEAM_FINDER_NO: Final[int] = cv2.detail.SeamFinder_NO


@lru_cache
def _seam_finder_map():
    result = OrderedDict()
    result["GraphCutColor"] = cv2.detail.GraphCutSeamFinder("COST_COLOR")
    result["GraphCutColorGrad"] = cv2.detail.GraphCutSeamFinder("COST_COLOR_GRAD")
    result["DpColor"] = cv2.detail.DpSeamFinder("COLOR")
    result["DpColorGrad"] = cv2.detail.DpSeamFinder("COLOR_GRAD")
    result["Voronoi"] = cv2.detail.SeamFinder.createDefault(_SEAM_FINDER_VORONOI_SEAM)
    result["No"] = cv2.detail.SeamFinder.createDefault(_SEAM_FINDER_NO)
    return result


@lru_cache
def _estimator_map():
    result = OrderedDict()
    result["Homography"] = cv2.detail.HomographyBasedEstimator
    result["Affine"] = cv2.detail.AffineBasedEstimator
    return result


@lru_cache
def _wave_correct_map():
    result = OrderedDict()
    result["Horiz"] = cv2.detail.WAVE_CORRECT_HORIZ
    result["Vert"] = cv2.detail.WAVE_CORRECT_VERT
    result["No"] = None
    return result


@lru_cache
def _timelapse_map():
    result = OrderedDict()
    result["AsIs"] = cv2.detail.Timelapser_AS_IS
    result["Crop"] = cv2.detail.Timelapser_CROP
    return result


MATCHER_HOMOGRAPHY: Final[str] = "Homography"
MATCHER_AFFINE: Final[str] = "Affine"


@lru_cache
def _matcher_keys() -> Sequence[str]:
    return MATCHER_HOMOGRAPHY, MATCHER_AFFINE


@lru_cache
def _warp_keys() -> Sequence[str]:
    return (
        "spherical",
        "plane",
        "affine",
        "cylindrical",
        "fisheye",
        "stereographic",
        "compressedPlaneA2B1",
        "compressedPlaneA1.5B1",
        "compressedPlanePortraitA2B1",
        "compressedPlanePortraitA1.5B1",
        "paniniA2B1",
        "paniniA1.5B1",
        "paniniPortraitA2B1",
        "paniniPortraitA1.5B1",
        "mercator",
        "transverseMercator",
    )


BLEND_MULTIBAND: Final[str] = "Multiband"
BLEND_FEATHER: Final[str] = "Feather"
BLEND_NO: Final[str] = "No"


@lru_cache
def _blend_keys() -> Sequence[str]:
    return BLEND_MULTIBAND, BLEND_FEATHER, BLEND_NO


STITCHER_MODE_MAP = _stitcher_mode_map().copy()
EXPOSURE_COMPENSATOR_MAP = _exposure_compensator_map().copy()
BUNDLE_ADJUSTER_MAP = _bundle_adjuster_map().copy()
FEATURES_FINDER_MAP = _features_finder_map().copy()
SEAM_FINDER_MAP = _seam_finder_map().copy()
ESTIMATOR_MAP = _estimator_map().copy()
WAVE_CORRECT_MAP = _wave_correct_map().copy()
TIMELAPSE_MAP = _timelapse_map().copy()

STITCHER_MODE_KEYS: Final[Sequence[str]] = tuple(STITCHER_MODE_MAP.keys())
EXPOS_COMP_KEYS: Final[Sequence[str]] = tuple(EXPOSURE_COMPENSATOR_MAP.keys())
BUNDLE_ADJUSTER_KEYS: Final[Sequence[str]] = tuple(BUNDLE_ADJUSTER_MAP.keys())
FEATURES_FINDER_KEYS: Final[Sequence[str]] = tuple(FEATURES_FINDER_MAP.keys())
SEAM_FINDER_KEYS: Final[Sequence[str]] = tuple(SEAM_FINDER_MAP.keys())
ESTIMATOR_KEYS: Final[Sequence[str]] = tuple(ESTIMATOR_MAP.keys())
WAVE_CORRECT_KEYS: Final[Sequence[str]] = tuple(WAVE_CORRECT_MAP.keys())
TIMELAPSE_KEYS: Final[Sequence[str]] = tuple(TIMELAPSE_MAP.keys())

MATCHER_KEYS: Final[Sequence[str]] = _matcher_keys()
WARP_KEYS: Final[Sequence[str]] = _warp_keys()
BLEND_KEYS: Final[Sequence[str]] = _blend_keys()

DEFAULT_ORB_MATCH_CONF: Final[float] = 0.3
DEFAULT_ETC_MATCH_CONF: Final[float] = 0.65
