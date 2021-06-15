import SimpleITK as sitk
import numpy as np
import scipy.ndimage as ndi

def generate_2d(X_ct, p_lambda = 0.85):
    '''
    Generate 2D digitally reconstructed radiographs from CT scan. (DRR, fake CXR, simulated CXR)
    X_ct: CT scan
    p-lambda:  β controls the boosting of X-ray absorption as the tissue density increases.
    We have chosen β=0.85 for our experiments after performing a visual comparison with real chest X-rays.
    '''
    X_ct[X_ct > 400] = 400
    X_ct[X_ct < -1000] = -1000
    X_ct += 1024
    # 1424 524 698.748232
    X_ct = X_ct/1000.0
    X_ct *= p_lambda
    X_ct[X_ct > 1] = 1
    #1.0 0.4454 0.5866707652
    X_ct_2d = np.mean(np.exp(X_ct), axis=1)
    return X_ct_2d

def resample(image, voxel_spacing, new_spacing=None, new_shape=None, order=3):
    """ Resamples the scan according to the either new spacing or new shape
        When new_spacing and new_shape are provided, new_shape has the priority
        use order = 1 for nearest neighbor and order = 3 for cubic interpolation
        @author: Joris + Gabriel
    """
    assert new_spacing is not None or new_shape is not None
    if np.dtype(image[0, 0, 0]) is np.dtype(np.int16) and np.min(image) < 0 and np.max(image) > 50 and order == 1:
        warnings.warn("Order 1 selected for image that looks as a scan, try using order 3")
    if np.dtype(image[0, 0, 0]) in [np.dtype(np.uint8), np.dtype(np.int16)] and np.min(image) == 0 and np.max(
            image) <= 50 and order == 3:
        warnings.warn("Order 3 selected for image that looks as a reference mask, try using order 1")

    if new_shape is not None:
        new_shape = np.array(new_shape)
        real_resize_factor = new_shape / image.shape
        new_spacing = voxel_spacing / real_resize_factor
    elif new_spacing is not None:
        if voxel_spacing[0] == voxel_spacing[1]:
            voxel_spacing = np.flipud(voxel_spacing)
        scan_sz_mm = [sz * voxel_spacing[idx]  for idx, sz in enumerate(image.shape)]
        new_shape = [round(float(sz_mm)/float(new_spacing[idx])) for idx, sz_mm in enumerate(scan_sz_mm)]
        new_shape = np.array(new_shape)
        real_resize_factor = new_shape / image.shape
    
    new_spacing = np.flipud(new_spacing)

    image = ndi.interpolation.zoom(image, real_resize_factor, mode='nearest', order=order)
    return image, new_spacing
