import json
import os
import numpy as np
from skimage import io
import zipfile


class RegionMaskDecoder:
    """
        This class is used to wrap all the methods that deals with the regions' single mask.
    """

    def __init__(self, json_file_path, mask_file_path, output_directory):
        """
        mask_file_path can be either a .tif or a .zip containing a tif called mask.tif
        """
        self.mask_file_path = mask_file_path
        self.output_directory = output_directory

        # Result masks shape
        # Layers count: 359
        # Rows count: 974
        # Columns count: 597
        self.tif_data_shape = (359, 974, 597)

        # Load JSON file
        with open(json_file_path, 'r') as f:
            self.all_json_data = json.load(f)

        # Read the TIF image(mask) and change it to 8 Bit
        if self.mask_file_path.endswith('.zip'):
            with zipfile.ZipFile(self.mask_file_path) as zf:
                with zf.open('mask.tif') as f:
                    self.tif_data = np.asarray(io.imread(f), dtype=np.uint8)
        else:
            self.tif_data = np.asarray(io.imread(self.mask_file_path), dtype=np.uint8)

    def create_empty_mask(self):
        """
        This function creates an empty numpy array of the mask size
        :return: empty numpy array of size (359, 974, 597)
        """

        #  array type of unit8 to be the same type of the regions tif file's type
        return np.zeros(self.tif_data_shape, dtype=np.uint8)

    def save_voxels_data_to_tif_file(self, tif_voxels_data, tif_name):
        """
        this function writes the image data to a TIFF file.
        :param tif_voxels_data: data in a numpy array
        :param tif_name:  The name that will be used to save the data
        :return:
        """
        io.imsave(os.path.join(self.output_directory, tif_name), tif_voxels_data)

    def extract_mask_voxels_of_color_value(self, color):
        """
        this function extracts a specific region's data from the regions' mask
        :param color: The color value of the desired region's mask
        :return: a new mask contains only the required voxels
        """

        # Create an array of the desired colors values
        targeted_voxels_vals = [color]
        # Create a mask by looping over the targeted_voxels_vals and keep only the required pixels
        # mask = functools.reduce(np.logical_or, (self.tif_data == val for val in targeted_voxels_vals))
        mask = np.logical_or.reduce((self.tif_data == val for val in targeted_voxels_vals))
        # Set all the other voxels value to zero
        masked = np.where(mask, self.tif_data, 0)
        # change the remaining voxels color to white
        masked[np.where(masked == color)] = 255
        return masked

    def get_region_voxels_data(self, all_json_data, json_region_data):
        """
        this function returns the image data of the required region.

        :param all_json_data: Hierarchy JSON data
        :param json_region_data: the data of the required region (name, color, and leaves)
        :return: required region voxels data
        """

        # Create an empty array
        result = self.create_empty_mask()

        # if the current region does not have leaves (i.e. the region itself is a leaf)
        if len(json_region_data['leaves']) == 0:
            tif_data = self.extract_mask_voxels_of_color_value(json_region_data['color'])
            print("Processing => ", json_region_data['name'])
            result += tif_data
        else:
            # loop through all the leaves of our current region
            for leaf_region_id in json_region_data['leaves']:
                # get the data of the leaf region ID from JSON Data
                leaf_region_data = all_json_data[str(leaf_region_id)]
                tif_data = self.extract_mask_voxels_of_color_value(leaf_region_data['color'])
                print("Processing => ", leaf_region_data['name'])
                result += tif_data
        return result

    def generate_region_tif_file(self, region_id):
        """
        this function extracts the data from the mask and then save it as tif file.
        :param region_id: the id of region we want to extract and then download
        :return:
        """

        region_json_data = self.all_json_data[str(region_id)]
        region_voxels_data = self.get_region_voxels_data(self.all_json_data, region_json_data)
        self.save_voxels_data_to_tif_file(region_voxels_data, region_json_data['name'] + ".tif")

    def generate_regions_tif_files(self, regions_ids, is_merged_result=True):
        """
        this function extracts the voxels data from the mask and then save it as tif file.
        :param regions_ids: array of regions IDs
        :param is_merged_result: TRUE | FALSE
        if TRUE: all regions will be combined into one file
        if FALSE: all regions will be saved separately
        :return:--
        """

        result = self.create_empty_mask()
        # will be used for saving tif file
        tif_file_name = ''

        for region_id in regions_ids:
            region_json_data = self.all_json_data[str(region_id)]
            if is_merged_result:
                result += self.get_region_voxels_data(self.all_json_data, region_json_data)
                tif_file_name += region_json_data['name'] + "___"
            else:
                self.generate_region_tif_file(region_id)
        if is_merged_result:
            self.save_voxels_data_to_tif_file(result, tif_file_name + ".tif")

    def generate_all_tif_files(self):
        for region_id in self.all_json_data:
            self.generate_region_tif_file(region_id)
