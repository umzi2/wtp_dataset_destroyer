#https://github.com/umzi2/Float-lens-blur
import numpy as np
import cv2


def generate_circle(x: int, y: int, radius: int, center: int) -> bool:
    """
    Checks if the point (x, y) is inside a circle with the given radius and center.

    Args:
        x (int): The x-coordinate of the point.
        y (int): The y-coordinate of the point.
        radius (int): The radius of the circle.
        center (int): The coordinate of the circle's center (both x and y are the same).

    Returns:
        bool: True if the point is inside the circle, otherwise False.
    """
    return (x - center) ** 2 + (y - center) ** 2 <= radius ** 2


def lens_blur(image: np.ndarray, dimension: float) -> np.ndarray:
    """
    Applies lens blur effect to an image.

    Args:
        image (np.ndarray): Input image as a numpy array.
        dimension (float): Kernel size for the blur effect.

    Returns:
        np.ndarray: Image with the applied lens blur.
    """
    image_array = image
    kernel = disk_kernel(dimension)
    convolved = cv2.filter2D(image_array, -1, kernel, borderType=cv2.BORDER_REPLICATE)
    return convolved


def disk_kernel(kernel_size: float) -> np.ndarray:
    """
    Generates a disk-shaped kernel for use in convolution.

    Args:
        kernel_size (float): Size of the kernel.

    Returns:
        np.ndarray: Disk-shaped kernel as a numpy array.
    """
    kernel_dim = int(np.ceil(kernel_size) * 2 + 1)

    fraction = kernel_size % 1
    if fraction != 0:
        kernel = np.zeros((kernel_dim, kernel_dim), dtype=np.float32)
        circle_center_coord = kernel_dim // 2
        circle_radius = circle_center_coord - 1

        for i in range(kernel_dim):
            for j in range(kernel_dim):
                kernel[i, j] = generate_circle(i, j, circle_radius, circle_center_coord)

        kernel2 = np.zeros((kernel_dim, kernel_dim), dtype=np.float32)
        circle_center_coord = kernel_dim // 2
        circle_radius = circle_center_coord

        for i in range(kernel_dim):
            for j in range(kernel_dim):
                kernel2[i, j] = generate_circle(i, j, circle_radius, circle_center_coord)

        kernel = np.clip(kernel + kernel2 * fraction, 0, 1)
    else:
        kernel = np.zeros((kernel_dim, kernel_dim), dtype=np.float32)
        circle_center_coord = kernel_dim // 2
        circle_radius = circle_center_coord

        for i in range(kernel_dim):
            for j in range(kernel_dim):
                kernel[i, j] = generate_circle(i, j, circle_radius, circle_center_coord)

    kernel /= np.sum(kernel)
    return kernel
