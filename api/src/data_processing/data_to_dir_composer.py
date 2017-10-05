import os
import string
import shutil
import glob
import tqdm

from api.src.common.config import DataConfig
from api.src.common.utils import ensure_dir, print_info


AVAILABLE_CHARS = string.ascii_lowercase + string.digits

PATHS = {
    'empslocal': os.path.join(DataConfig.PATHS['RAW_DATA'], 'empslocal', 'dataset5'),
    'massey': os.path.join(DataConfig.PATHS['RAW_DATA'], 'massey', 'images')
}


def parse_empslocal_dataset():
    empslocal = PATHS['empslocal']
    training_volunteers_range = ['A', 'B', 'C', 'D']
    validation_volunteers_range = ['E']
    for volunteer_folder in tqdm.tqdm(os.listdir(empslocal)):
        for letter_folder in os.listdir(os.path.join(empslocal, volunteer_folder)):
            for img_file in os.listdir(os.path.join(empslocal, volunteer_folder, letter_folder)):
                if img_file.startswith('depth'):
                    continue
                src_path = os.path.join(empslocal, volunteer_folder, letter_folder, img_file)
                if volunteer_folder in training_volunteers_range:
                    dst_folder_path = os.path.join(DataConfig.PATHS['TRAINING_PROCESSED_DATA'], letter_folder.lower())
                elif volunteer_folder in validation_volunteers_range:
                    dst_folder_path = os.path.join(DataConfig.PATHS['VALID_PROCESSED_DATA'], letter_folder.lower())
                else:
                    raise ValueError("Unknown range for this volunteer: ", volunteer_folder)
                dst_path = os.path.join(dst_folder_path, str(len(os.listdir(dst_folder_path))) + '.png')
                shutil.copy(src_path, dst_path)
    print_info('Processed empslocal')


def parse_massey_data():
    massey = PATHS['massey']
    training_volunteers_range = [1, 2, 3, 4]
    validation_volunteers_range = [5]
    for file_name in tqdm.tqdm(os.listdir(massey)):
        sign, volunteer_number = parse_massey_file_name(file_name)
        src_path = os.path.join(massey, file_name)
        if volunteer_number in training_volunteers_range:
            dst_folder_path = os.path.join(DataConfig.PATHS['TRAINING_PROCESSED_DATA'], sign.lower())
        elif volunteer_number in validation_volunteers_range:
            dst_folder_path = os.path.join(DataConfig.PATHS['VALID_PROCESSED_DATA'], sign.lower())
        else:
            raise ValueError("Unknown range for this volunteer: ", volunteer_number)
        dst_path = os.path.join(dst_folder_path, str(len(os.listdir(dst_folder_path))) + '.png')
        shutil.copy(src_path, dst_path)
    print_info('Processed massey')

DATASET_FUNCTIONS = [
    parse_empslocal_dataset,
    parse_massey_data
]


def create_letter_dirs():
    for sign in AVAILABLE_CHARS:
        ensure_dir(os.path.join(DataConfig.PATHS['TRAINING_PROCESSED_DATA'], sign))
        ensure_dir(os.path.join(DataConfig.PATHS['VALID_PROCESSED_DATA'], sign))


def clear_dirs():
    for sign in AVAILABLE_CHARS:
        for file in glob.glob(os.path.join(DataConfig.PATHS['TRAINING_PROCESSED_DATA'], sign, '*')):
            os.remove(file)
        for file in glob.glob(os.path.join(DataConfig.PATHS['VALID_PROCESSED_DATA'], sign, '*')):
            os.remove(file)


def parse_massey_file_name(file_name):
    components = file_name.split('_')
    return components[1], int(components[0][-1])


def main(args):
    create_letter_dirs()
    clear_dirs()
    for data_function in DATASET_FUNCTIONS:
        data_function()


if __name__ == '__main__':
    main(None)