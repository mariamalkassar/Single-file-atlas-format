import time
from region_mask_decoder import *

# The path to the regions' data JSON file.
json_file_path = "regions-leaves-info.json"

# The path to the regions' combined mask
# Contains all the leaves of the hierarchy regions. Each leaf has its own color specified in the JSON file
mask_file_path = "mask.tif.zip"

# The destination directory to save the generated masks
output_directory_path = "./output"

if __name__ == '__main__':
    regions_decoder = RegionMaskDecoder(json_file_path, mask_file_path, output_directory_path)

    # Use this function to extract ONLY one region from the mask.
    regions_decoder.generate_regions_tif_files([971])
    t0 = time.time()
    # Use this function to extract many regions from the mask.
    # Example: [971, 923] a list of region IDS.
    # You can choose to save the generate files combined or separate by entering the last attribute (True, False correspondingly)
    regions_decoder.generate_regions_tif_files([971, 923], False)
    print(t0-time.time())
    # Use this function to extract all the regions from the mask.
    # regions_decoder.generate_all_tif_files()
