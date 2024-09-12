# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Tuple

import cv2
from numpy import uint8, zeros

from cvp.cv.stitching.types import (
    BLEND_KEYS,
    BUNDLE_ADJUSTER_KEYS,
    BUNDLE_ADJUSTER_MAP,
    DEFAULT_ETC_MATCH_CONF,
    DEFAULT_ORB_MATCH_CONF,
    ESTIMATOR_KEYS,
    ESTIMATOR_MAP,
    EXPOS_COMP_KEYS,
    EXPOSURE_COMPENSATOR_MAP,
    FEATURES_FINDER_KEYS,
    FEATURES_FINDER_MAP,
    FEATURES_FINDER_ORB,
    MATCHER_AFFINE,
    MATCHER_KEYS,
    SEAM_FINDER_KEYS,
    SEAM_FINDER_MAP,
    STITCHER_MODE_KEYS,
    STITCHER_MODE_MAP,
    WARP_KEYS,
    WAVE_CORRECT_KEYS,
    WAVE_CORRECT_MAP,
)


@dataclass
class StitcherProps:
    stitcher_mode_index: int = 0
    """Scenario for stitcher operation.

    PANORAMA
        Mode for creating photo panoramas. Expects images under perspective
        transformation and projects resulting pano to sphere.
        - `cv2.detail.BestOf2NearestMatcher`
        - `cv2.SphericalWarper`
    SCANS
        Mode for composing scans. Expects images under affine transformation does
        not compensate exposure by default.
        - `cv2.detail.AffineBestOf2NearestMatcher`
        - `cv2.AffineWarper`
    """

    work_size: Tuple[int, int] = field(default_factory=lambda: (0, 0))
    """Resolution for image registration step."""

    seam_size: Tuple[int, int] = field(default_factory=lambda: (0, 0))
    """Resolution for seam estimation step."""

    # ------------------
    # Details parameters
    # ------------------

    work_mega_pixel: float = 0.6
    """Resolution for image registration step."""

    features_finder_index: int = 0
    """Type of features used for images matching."""

    matcher_index: int = 0
    """Matcher used for pairwise image matching."""

    estimator_index: int = 0
    """Type of estimator used for transformation estimation."""

    match_conf: float = 0.3
    """Confidence for feature matching step.

    The recommended default values are:
    - ORB is 0.3
    - other feature types is 0.65
    """

    conf_thresh: float = 0.1
    """Threshold for two images are from the same panorama confidence."""

    bundle_adjuster_index: int = 0
    """Bundle adjustment cost function."""

    ba_refine_mask: str = "xxxxx"
    """Set refinement mask for bundle adjustment.

    It looks like 'x_xxx', where 'x' means refine respective parameter and '_' means
    don't refine, and has the following format:<fx><skew><ppx><aspect><ppy>. The default
    mask is 'xxxxx'. If bundle adjustment doesn't support estimation of selected
    parameter then the respective flag is ignored.
    """

    wave_correct_index: int = 0
    """Perform wave effect correction."""

    warp_index: int = 0
    """Warp surface type."""

    seam_mega_pixel: float = 0.1
    """Resolution for image registration step."""

    seam_find_index: int = 0
    """Seam estimation method."""

    compose_mega_pixel: float = -1.0
    """Resolution for compositing step. Use -1 for original resolution."""

    expos_comp_index: int = 0
    """Exposure compensation method."""

    expos_comp_nr_feeds: int = 1
    """Number of exposure compensation feed."""

    expos_comp_nr_filtering: float = 2.0
    """Number of filtering iterations of the exposure compensation gains."""

    expos_comp_block_size: int = 32
    """BLock size in pixels used by the exposure compensator."""

    blend_index: int = 0
    """Blending method."""

    blend_strength: int = 5
    """Blend Strength"""

    range_width: int = -1
    """Uses range_width to limit number of images to match with."""

    use_cuda: bool = False
    """Try to use CUDA. The default value is no. All default values are for CPU mode."""

    @property
    def stitcher_mode(self):
        key = STITCHER_MODE_KEYS[self.stitcher_mode_index]
        return STITCHER_MODE_MAP[key]

    @property
    def expos_comp_type(self):
        key = EXPOS_COMP_KEYS[self.expos_comp_index]
        return EXPOSURE_COMPENSATOR_MAP[key]

    def create_bundle_adjuster(self):
        key = BUNDLE_ADJUSTER_KEYS[self.bundle_adjuster_index]
        adjuster = BUNDLE_ADJUSTER_MAP[key]()
        adjuster.setConfThresh(self.conf_thresh)
        adjuster.setRefinementMask(self.ba_refine_mask_array)
        return adjuster

    def create_features_finder(self):
        key = FEATURES_FINDER_KEYS[self.features_finder_index]
        return FEATURES_FINDER_MAP[key]()

    @property
    def seam_finder(self):
        key = SEAM_FINDER_KEYS[self.seam_find_index]
        return SEAM_FINDER_MAP[key]

    @property
    def estimator(self):
        key = ESTIMATOR_KEYS[self.estimator_index]
        return ESTIMATOR_MAP[key]

    def create_estimator(self):
        return self.estimator()

    @property
    def wave_correct(self):
        key = WAVE_CORRECT_KEYS[self.wave_correct_index]
        return WAVE_CORRECT_MAP[key]

    @property
    def matcher_key(self):
        return MATCHER_KEYS[self.matcher_index]

    @property
    def warp_key(self):
        return WARP_KEYS[self.warp_index]

    @property
    def blend_key(self):
        return BLEND_KEYS[self.blend_index]

    @property
    def adjusted_match_conf(self):
        if self.match_conf <= 0.0:
            ff_name = FEATURES_FINDER_KEYS[self.features_finder_index].upper()
            if ff_name == FEATURES_FINDER_ORB:
                return DEFAULT_ORB_MATCH_CONF
            else:
                return DEFAULT_ETC_MATCH_CONF
        else:
            return self.match_conf

    @property
    def ba_refine_mask_array(self):
        mask = zeros((3, 3), uint8)
        if self.ba_refine_mask[0] == "x":
            mask[0, 0] = 1
        if self.ba_refine_mask[1] == "x":
            mask[0, 1] = 1
        if self.ba_refine_mask[2] == "x":
            mask[0, 2] = 1
        if self.ba_refine_mask[3] == "x":
            mask[1, 1] = 1
        if self.ba_refine_mask[4] == "x":
            mask[1, 2] = 1
        return mask

    def get_matcher(self):
        use_cuda = self.use_cuda
        matcher_name = self.matcher_key
        match_conf = self.adjusted_match_conf
        range_width = self.range_width

        if matcher_name == MATCHER_AFFINE:
            return cv2.detail.AffineBestOf2NearestMatcher(False, use_cuda, match_conf)
        elif range_width == -1:
            return cv2.detail.BestOf2NearestMatcher(use_cuda, match_conf)
        else:
            return cv2.detail.BestOf2NearestRangeMatcher(
                range_width, use_cuda, match_conf
            )

    def get_compensator(self, use_filter=False):
        if self.expos_comp_type == cv2.detail.ExposureCompensator_CHANNELS:
            return cv2.detail.ChannelsCompensator(self.expos_comp_nr_feeds)
        elif self.expos_comp_type == cv2.detail.ExposureCompensator_CHANNELS_BLOCKS:
            compensator = cv2.detail.BlocksChannelsCompensator(
                self.expos_comp_block_size,
                self.expos_comp_block_size,
                self.expos_comp_nr_feeds,
            )
            if use_filter:
                nr_iterations = int(self.expos_comp_nr_filtering)
                compensator.setNrGainsFilteringIterations(nr_iterations)
            return compensator
        else:
            return cv2.detail.ExposureCompensator.createDefault(self.expos_comp_type)
