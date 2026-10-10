"""White-paper raw art -> clean RGBA cutout (flood from the edges, no halo). Shared by pack_tilo.py."""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi


def cutout(path, thresh=236, pocket_min=1500):
    im = np.array(Image.open(path).convert("RGB")).astype(np.float32)
    nearwhite = im.min(axis=2) >= thresh
    lab, n = ndi.label(nearwhite)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge))
    # enclosed white pockets between limbs/body (not eye whites: those are small and bordered by dark pupils)
    sizes = ndi.sum(nearwhite, lab, range(1, n + 1))
    for i in range(1, n + 1):
        if i in edge or sizes[i - 1] < pocket_min: continue
        m = lab == i
        if im[m].min(axis=1).mean() > 250 and not _is_eye(m, im): bg |= m
    fg = ~bg
    fg = ndi.binary_opening(fg, iterations=1)           # drop specks of paper noise
    lab2, n2 = ndi.label(fg)                              # keep real shapes (body + sparkles), drop dust
    keep = [i for i in range(1, n2 + 1) if (lab2 == i).sum() > 150]
    fg = np.isin(lab2, keep)
    hard = ndi.binary_erosion(fg, iterations=1)          # eat the anti-aliased white fringe
    alpha = ndi.gaussian_filter(hard.astype(np.float32), 0.9)
    alpha[~ndi.binary_dilation(hard, iterations=2)] = 0
    # decontaminate: colours of the outer band come from the nearest solid interior pixel, never from white paper
    core = ndi.binary_erosion(hard, iterations=3)
    idx = ndi.distance_transform_edt(~core, return_distances=False, return_indices=True)
    rgb = im[idx[0], idx[1]]
    rgb[core] = im[core]
    return np.dstack([rgb, alpha * 255]).clip(0, 255).astype(np.uint8)


def _is_eye(mask, im):
    # an eye white has a dark pupil inside its bounding box; a paper pocket does not
    ys, xs = np.where(mask)
    box = im[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return (box.max(axis=2) < 120).sum() > 40
