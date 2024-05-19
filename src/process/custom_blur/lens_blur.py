import cv2
import numpy as np
from functools import reduce


def as_3d(img: np.ndarray) -> (np.ndarray, bool):
    gray = False
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        gray = True
    return img, gray


# These scales bring the size of the below components to roughly the specified radius - I just hard coded these
kernel_scales = [1.4, 1.2, 1.2, 1.2, 1.2, 1.2]

# Kernel parameters a, b, A, B
# These parameters are drawn from <http://yehar.com/blog/?p=1495>
kernel_params = [
    # 1-component
    [[0.862325, 1.624835, 0.767583, 1.862321]],
    # 2-components
    [
        [0.886528, 5.268909, 0.411259, -0.548794],
        [1.960518, 1.558213, 0.513282, 4.56111],
    ],
    # 3-components
    [
        [2.17649, 5.043495, 1.621035, -2.105439],
        [1.019306, 9.027613, -0.28086, -0.162882],
        [2.81511, 1.597273, -0.366471, 10.300301],
    ],
    # 4-components
    [
        [4.338459, 1.553635, -5.767909, 46.164397],
        [3.839993, 4.693183, 9.795391, -15.227561],
        [2.791880, 8.178137, -3.048324, 0.302959],
        [1.342190, 12.328289, 0.010001, 0.244650],
    ],
    # 5-components
    [
        [4.892608, 1.685979, -22.356787, 85.91246],
        [4.71187, 4.998496, 35.918936, -28.875618],
        [4.052795, 8.244168, -13.212253, -1.578428],
        [2.929212, 11.900859, 0.507991, 1.816328],
        [1.512961, 16.116382, 0.138051, -0.01],
    ],
    # 6-components
    [
        [5.143778, 2.079813, -82.326596, 111.231024],
        [5.612426, 6.153387, 113.878661, 58.004879],
        [5.982921, 9.802895, 39.479083, -162.028887],
        [6.505167, 11.059237, -71.286026, 95.027069],
        [3.869579, 14.81052, 1.405746, -3.704914],
        [2.201904, 19.032909, -0.152784, -0.107988],
    ],
]


# Obtain specific parameters and scale for a given component count
def get_parameters(component_count: int = 2):
    parameter_index = max(0, min(component_count - 1, len(kernel_params)))
    parameter_dictionaries = [
        dict(zip(["a", "b", "A", "B"], b)) for b in kernel_params[parameter_index]
    ]
    return (parameter_dictionaries, kernel_scales[parameter_index])


# Produces a complex kernel of a given radius and scale (adjusts radius to be more accurate)
# a and b are parameters of this complex kernel
def complex_kernel_1d(radius: float, scale: float, a: float, b: float) -> np.ndarray:
    """
    Produces a complex kernel of a given radius and scale (adjusts radius to be more accurate).
    """
    kernel_radius = int(np.ceil(radius))
    kernel_size = kernel_radius * 2 + 1
    ax = np.linspace(-radius, radius, kernel_size, dtype=np.float32)
    ax = ax * scale * (1 / radius)
    kernel_complex = np.zeros((kernel_size,), dtype=np.complex64)
    kernel_complex.real = np.exp(-a * (ax**2)) * np.cos(b * (ax**2))
    kernel_complex.imag = np.exp(-a * (ax**2)) * np.sin(b * (ax**2))
    return kernel_complex.reshape((1, kernel_size))


def normalize_kernels(kernels, params):
    # Normalises with respect to A*real+B*imag
    total = 0

    for k, p in zip(kernels, params):
        # 1D kernel - applied in 2D
        for i in range(k.shape[1]):
            for j in range(k.shape[1]):
                # Complex multiply and weighted sum
                total += p["A"] * (
                    k[0, i].real * k[0, j].real - k[0, i].imag * k[0, j].imag
                ) + p["B"] * (k[0, i].real * k[0, j].imag + k[0, i].imag * k[0, j].real)

    scalar = 1 / np.sqrt(total)
    kernels = np.asarray(kernels) * scalar

    return kernels


# Combine the real and imaginary parts of an image, weighted by A and B
def weighted_sum(kernel, params):
    return np.add(kernel.real * params["A"], kernel.imag * params["B"])


def lens_blur(
    img: np.ndarray,
    radius: float = 3.0,
    components: int = 5,
    exposure_gamma: float = 5.0,
) -> np.ndarray:
    img, gray = as_3d(img)
    img = np.ascontiguousarray(np.transpose(img, (2, 0, 1)), dtype=np.float32)
    parameters, scale = get_parameters(components)
    components = [
        complex_kernel_1d(radius, scale, component_params["a"], component_params["b"])
        for component_params in parameters
    ]
    components = normalize_kernels(components, parameters)
    img = np.power(img, exposure_gamma)
    component_output = []
    for component, component_params in zip(components, parameters):
        channels = []
        component_real = np.real(component)
        component_imag = np.imag(component)
        component_real_t = component_real.transpose()
        component_imag_t = component_imag.transpose()
        for channel in range(img.shape[0]):
            inter_real = cv2.filter2D(
                img[channel], -1, component_real, borderType=cv2.BORDER_REPLICATE
            )
            inter_imag = cv2.filter2D(
                img[channel], -1, component_imag, borderType=cv2.BORDER_REPLICATE
            )

            final_1 = cv2.filter2D(
                inter_real, -1, component_real_t, borderType=cv2.BORDER_REPLICATE
            )
            final_2 = cv2.filter2D(
                inter_real, -1, component_imag_t, borderType=cv2.BORDER_REPLICATE
            )
            final_3 = cv2.filter2D(
                inter_imag, -1, component_real_t, borderType=cv2.BORDER_REPLICATE
            )
            final_4 = cv2.filter2D(
                inter_imag, -1, component_imag_t, borderType=cv2.BORDER_REPLICATE
            )
            final = final_1 - final_4 + 1j * (final_2 + final_3)  # type: ignore
            channels.append(final)
        component_image = np.stack(
            [weighted_sum(channel, component_params) for channel in channels]
        )
        component_output.append(component_image)
    output_image = reduce(np.add, component_output)
    output_image = np.clip(output_image, 0, None)
    output_image = np.power(output_image, 1.0 / exposure_gamma)
    output_image = np.clip(output_image, 0, 1)
    output_image = output_image.transpose(1, 2, 0)
    if gray:
        output_image = cv2.cvtColor(output_image, cv2.COLOR_RGB2GRAY)
    return output_image
