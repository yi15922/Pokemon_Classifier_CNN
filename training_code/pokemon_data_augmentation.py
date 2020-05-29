import os
import random
from scipy import ndarray

# image processing library
import skimage as sk
from skimage import transform
from skimage import util
from skimage import io

def random_rotation(image_array: ndarray):
    # pick a random degree of rotation between 25% on the left and 25% on the right
    random_degree = random.uniform(-25, 25)
    return sk.transform.rotate(image_array, random_degree)

def random_noise(image_array: ndarray):
    # add random noise to the image
    return sk.util.random_noise(image_array)

def random_scale(image_array: ndarray):
    # scales the images by a random factor from 10% to 200%
    # resizes the images back to 256x256 to ensure data consistency
    # antialiasing is enabled for feature preservation
    random_scale_factor = random.uniform(.1, 2)
    rescaled_image = sk.transform.rescale(image_array, random_scale_factor, anti_aliasing=True)
    resized_image = sk.transform.resize(rescaled_image, (256, 256), anti_aliasing=True)
    return resized_image

def horizontal_flip(image_array: ndarray):
    # horizontal flip doesn't need skimage, it's easy as flipping the image array of pixels !
    return image_array[:, ::-1]

# dictionary of the transformations we defined earlier
available_transformations = {
    'rotate': random_rotation,
    'noise': random_noise,
    'horizontal_flip': horizontal_flip,
    'random_scale': random_scale
}

folder_path = 'pokemon/base_pokemon'
num_files_desired = 5000

# find all files paths from the folder
images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

num_generated_files = 0
while num_generated_files <= num_files_desired:
    # random image from the folder
    image_path = random.choice(images)
    # get the image number
    split_path = os.path.split(image_path);
    image_number = split_path[1]
    # read image as an two dimensional array of pixels
    image_to_transform = sk.io.imread(image_path)
    # random num of transformation to apply
    num_transformations_to_apply = random.randint(1, len(available_transformations))

    num_transformations = 0
    transformed_image = None
    while num_transformations <= num_transformations_to_apply:
        # random transformation to apply for a single image
        key = random.choice(list(available_transformations))
        transformed_image = available_transformations[key](image_to_transform)
        num_transformations += 1
        new_file_path = 'pokemon/augmented_pokemon/%s_augmented_image_%s.jpg' % (image_number, num_generated_files)
        # write image to the disk
        io.imsave(new_file_path, transformed_image)
        num_generated_files += 1