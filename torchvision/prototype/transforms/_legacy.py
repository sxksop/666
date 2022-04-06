from __future__ import annotations

import warnings
from typing import Any, Dict

from torchvision.prototype.features import ColorSpace
from torchvision.prototype.transforms import Transform
from typing_extensions import Literal

from ._meta import ConvertImageColorSpace
from ._transform import _RandomApplyTransform


class Grayscale(Transform):
    def __init__(self, num_output_channels: Literal[1, 3] = 1) -> None:
        deprecation_msg = (
            f"The transform `Grayscale(num_output_channels={num_output_channels})` "
            f"is deprecated and will be removed in a future release."
        )
        if num_output_channels == 1:
            replacement_msg = (
                "transforms.ConvertImageColorSpace(old_color_space=ColorSpace.RGB, color_space=ColorSpace.GRAY)"
            )
        else:
            replacement_msg = (
                "transforms.Compose(\n"
                "    transforms.ConvertImageColorSpace(old_color_space=ColorSpace.RGB, color_space=ColorSpace.GRAY),\n"
                "    transforms.ConvertImageColorSpace(old_color_space=ColorSpace.GRAY, color_space=ColorSpace.RGB),\n"
                ")"
            )
        warnings.warn(f"{deprecation_msg} Instead, please use\n\n{replacement_msg}")

        super().__init__()
        self.num_output_channels = num_output_channels
        self._rgb_to_gray = ConvertImageColorSpace(old_color_space=ColorSpace.RGB, color_space=ColorSpace.GRAY)
        self._gray_to_rgb = ConvertImageColorSpace(old_color_space=ColorSpace.GRAY, color_space=ColorSpace.RGB)

    def _transform(self, input: Any, params: Dict[str, Any]) -> Any:
        output = self._rgb_to_gray(input)
        if self.num_output_channels == 3:
            output = self._gray_to_rgb(output)
        return output


class RandomGrayscale(_RandomApplyTransform):
    def __init__(self, p: float = 0.1) -> None:
        warnings.warn(
            "The transform `RandomGrayscale(p=...)` is deprecated and will be removed in a future release. "
            "Instead, please use\n\n"
            "transforms.RandomApply(\n"
            "    transforms.Compose(\n"
            "        transforms.ConvertImageColorSpace(old_color_space=ColorSpace.RGB, color_space=ColorSpace.GRAY),\n"
            "        transforms.ConvertImageColorSpace(old_color_space=ColorSpace.GRAY, color_space=ColorSpace.RGB),\n"
            "    )\n"
            "    p=...,\n"
            ")"
        )

        super().__init__(p=p)
        self._rgb_to_gray = ConvertImageColorSpace(old_color_space=ColorSpace.RGB, color_space=ColorSpace.GRAY)
        self._gray_to_rgb = ConvertImageColorSpace(old_color_space=ColorSpace.GRAY, color_space=ColorSpace.RGB)

    def _transform(self, input: Any, params: Dict[str, Any]) -> Any:
        return self._gray_to_rgb(self._rgb_to_gray(input))