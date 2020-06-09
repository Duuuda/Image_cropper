from cv2 import imread, imwrite
from collections import namedtuple
from re import sub


class InvalidImagePath(Exception):
    pass


class MultiplicityError(Exception):
    pass


def crop(image_path, saving_path, number_of_horizontal_parts=3, number_of_vertical_parts=3):
    """
    :param image_path: 'test_pic.jpg'
    :param saving_path: 'test_dir/'
    :param number_of_horizontal_parts: 10
    :param number_of_vertical_parts: 3
    :return: None
    Function with that's params must cutting 'test_pic.jpg' image and save all fragments in 'test_dir' directory!!!
    """
    # get image name and format
    image_full_name = sub(r'.+/', '', image_path)
    dot_index = image_full_name.rfind('.')
    if dot_index == -1:
        raise InvalidImagePath('Your image has not format!')
    image_name, image_format = image_full_name[:dot_index], image_full_name[dot_index + 1:]

    # removing unnecessary items
    del image_full_name

    # init Vector2 class
    Vector2 = namedtuple('Vector', 'x y')

    # load image
    image = imread(image_path)

    # calculating the image size
    image_size = Vector2(*image.shape[1::-1])

    # checking for multiplicity
    if image_size.x % number_of_horizontal_parts:
        raise MultiplicityError('The width of the image is not a multiple of the number of horizontal parts!\n'
                                f'Your image has width: {image_size.x}\n'
                                f"You can't cut the image into {number_of_horizontal_parts} parts!")
    if image_size.y % number_of_vertical_parts:
        raise MultiplicityError('The height of the image is not a multiple of the number of vertical parts!\n'
                                f'Your image has height: {image_size.y}\n'
                                f"You can't cut the image into {number_of_vertical_parts} parts!")

    # calculating the part's sizes
    parts_sizes = Vector2(image_size.x // number_of_horizontal_parts, image_size.y // number_of_vertical_parts)

    # removing unnecessary items
    del Vector2

    # cutting image
    fragment_number = int()
    for y in range(0, image_size.y, parts_sizes.y):
        for x in range(0, image_size.x, parts_sizes.x):
            fragment_number += 1
            imwrite(saving_path + image_name + f'_fragment_{fragment_number}.' + image_format,
                    image[y: y + parts_sizes.y, x: x + parts_sizes.x])


if __name__ == '__main__':
    crop('test_pic.jpg', 'tetst_dir/', number_of_horizontal_parts=10)
