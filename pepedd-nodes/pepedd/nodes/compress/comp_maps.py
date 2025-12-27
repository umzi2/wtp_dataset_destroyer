from pepeline import JpegSamplingFactor, QuantizeTable

JpegSamplings = {
    "444": JpegSamplingFactor.R444,
    "440": JpegSamplingFactor.R440,
    "441": JpegSamplingFactor.R441,
    "422": JpegSamplingFactor.R422,
    "420": JpegSamplingFactor.R420,
    "411": JpegSamplingFactor.R411,
    "410": JpegSamplingFactor.R410,
}
QuantizeTables = {
    "default": QuantizeTable.Default,
    "flat": QuantizeTable.Flat,
    "mssim": QuantizeTable.CustomMsSsim,
    "psnr": QuantizeTable.CustomPsnrHvs,
    "im": QuantizeTable.ImageMagick,
    "ksc": QuantizeTable.KleinSilversteinCarney,
    "dxr": QuantizeTable.DentalXRays,
    "vdm": QuantizeTable.VisualDetectionModel,
    "idm": QuantizeTable.ImprovedDetectionModel,
}

InterpolationMap = {
    "b": "bilinear",
    "c": "bicubic",
    "l": "lanczos",
    "s": "spline",
    "g": "gauss",
    "a": "area",
}
if __name__ == "__main__":
    for i in [
        "yuv420p",
        "yuv422p",
        "yuv444p",
        "yuv420p10le",
        "yuv422p10le",
        "yuv444p10le",
        "yuv420p12le",
        "yuv422p12le",
        "yuv444p12le",
    ]:
        for ii in InterpolationMap.keys():
            print(f'"{i}_{ii}"', end=", ")
