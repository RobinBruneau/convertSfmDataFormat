import argparse
import os

from utils.idr_utils import read_idr_data
from utils.nerf_utils import write_nerf_data, write_neuralangelo_data, write_neus2_data, write_instantngp_data

def parse_args():
    parser = argparse.ArgumentParser(description="Converts an IDR format folder to a Instant-ngp or NeuS2 .json file.")
    parser.add_argument("--idr_folder_path", default="data/", help="Input path of the IDR folder.")
    parser.add_argument("--output_format", default="neuralangelo", help="Output format of the .json file.")
    parser.add_argument("--output_path", default=None, help="Output path of the NeRF folder.")
    parser.add_argument("--use-scale-matrix", action="store_true", default=False, help="Use scale matrix.")
    parser.add_argument("--bit_depth", default=16, type=int, help="Bit depth of the images.")
    parser.add_argument("--copy_images", action="store_true", help="Copy images to the output folder.")
    parser.add_argument("--downscale_factor", default=None, type=int, help="Downscale factor of the images.")
    parser.add_argument("--size", default=None, type=int, help="Size of the images.")
    args = parser.parse_args()
    return args

if __name__ == "__main__":

    # Parse arguments
    args = parse_args()
    IDR_FOLDER_PATH = args.idr_folder_path
    OUTPUT_FORMAT = args.output_format
    OUTPUT_PATH = args.output_path
    USE_SCALE_MATRIX = args.use_scale_matrix
    if OUTPUT_PATH is None:
        OUTPUT_PATH = os.path.join(IDR_FOLDER_PATH, "nerf/")
    BIT_DEPTH = args.bit_depth
    COPY_IMAGES = args.copy_images
    DOWNSCALE_FACTOR = args.downscale_factor
    SIZE = args.size

    # Read IDR data
    views_data, intrinsics_data, poses_data = read_idr_data(IDR_FOLDER_PATH, USE_SCALE_MATRIX, size=SIZE)

    # Write Instant-ngp or NeuS2 .json file
    if OUTPUT_FORMAT == "neuralangelo":
        write_neuralangelo_data(views_data, intrinsics_data, poses_data, OUTPUT_PATH, bit_depth=BIT_DEPTH, copy_images=COPY_IMAGES, downscale_factor=DOWNSCALE_FACTOR)
    elif OUTPUT_FORMAT == "neus2":
        write_neus2_data(views_data, intrinsics_data, poses_data, OUTPUT_PATH, bit_depth=BIT_DEPTH, copy_images=COPY_IMAGES, downscale_factor=DOWNSCALE_FACTOR)
    elif OUTPUT_FORMAT == "instant-ngp":
        write_instantngp_data(views_data, intrinsics_data, poses_data, OUTPUT_PATH, bit_depth=BIT_DEPTH, copy_images=COPY_IMAGES, downscale_factor=DOWNSCALE_FACTOR)
    else:
        write_nerf_data(views_data, intrinsics_data, poses_data, OUTPUT_PATH, bit_depth=BIT_DEPTH, copy_images=COPY_IMAGES, downscale_factor=DOWNSCALE_FACTOR)

    # import scipy.io
    # mat_dict = {'K':[], 'poses':[]}
    # for i, (view_id, view_data) in enumerate(views_data.items()):
    #     K = view_data["intrinsics"]
    #     c2w = view_data["c2w"]
    #     if i == 0:
    #         mat_dict['K'] = np.array(K, dtype=np.float64)
    #     mat_dict['poses'].append(np.linalg.inv(c2w))
    # mat_dict['poses'] = np.array(mat_dict['poses'], dtype=np.float64)
    # scipy.io.savemat(os.path.join(OUTPUT_PATH, 'cameras.mat'), mat_dict)