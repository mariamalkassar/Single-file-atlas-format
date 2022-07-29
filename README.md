
Since the regions in the mapZebrain are hierarchical, it would be possible to have a single tif (plus the hiearchy json), where each voxel encodes a value corresponding to the "lowest/smallest" hierarchy region that covers that voxel. There is an ability to decode the single tif file and generate all the masks on the user computer.

# Media files:
- <b>mask.tif.zip:</b> </br>
This file contains the tif file of the leaves of the hierarchy regions. </br>
- <b>regions-leaves-info.json:</b> </br>
This file contains a dictionary where the key is the regions IDs and the values are: name, color, and all the leaves IDs of the regions that form the region mask. in case the regions is a leaf, the leaves IDs array will be empty.</br>
<i>This JSON file will be used in RegionMaskDecoder calss.</i></br>

- <b>regions_hierarchy.json:</b> </br>
This file contais a dictionary that describes the regions hierarchy.</br>
<i>This file will not be used to decode the regions mask. It is only for the user to know the hierarchy.</i></br>

- <b>region_mask_decoder.py</b> </br>
This python file contains the RegionMaskDecoder class.</br>
<i>The following steps will describe how to use it. -- IT IS VERY EASY :) -</i></br>

# Pre-requirements:
Install these 3 libraries: numpy, skimage and tifffile.

# How to use:
1- Set the paths: </br>
- The path to the regions' data JSON file. </br>
<code>json_file_path = "/path/to/the/regions-leaves-info.json"</code>

- The path to the regions' combined mask that contains all the leaves of the hierarchy regions. Each leaf has its own color specified in the JSON file.</br>
<code>mask_file_path = "path/to/the/mask.tif"</code>

- The destination directory to save the generated masks </br>
<code>output_directory_path = "path/to/the/destination/directory"</code>


2- Create an object of RegionMaskDecoder class:</br>
<code>regions_decoder = RegionMaskDecoder(json_file_path, mask_file_path, output_directory_path)</code>

3- Use this function to extract ONLY one region from the mask.
   <code> regions_decoder.generate_regions_tif_files([971]) </code>

   Use this function to extract many regions from the mask.
   Example: [971, 923] a list of region IDS.
   You can choose to save the generate files combined or separate by entering the last attribute (True, False correspondingly)
   <code>regions_decoder.generate_regions_tif_files([971, 923], False) </code>
    
   Use this function to extract all the regions from the mask.
   <code>regions_decoder.generate_all_tif_files() </code>
