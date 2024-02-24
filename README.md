# Remove older versions

This is a simple utility to keep track of new mods in a modpack and delete the old ones.  
It's useful for [wabbajack](https://www.wabbajack.org/) modpacks, where the same list can be updated often and you don't want to keep the mods from older versions taking up space.

## Usage

1. Install [Python](https://www.python.org/downloads/) if you don't have it already.
2. Download the [clean_wj_downloads.py](./clean_wj_downloads.py) file from this repository.
3. Open a terminal and navigate to the folder where the file is located.
4. Run the script with the path to the modpack's `.wabbajack` file as an argument. For example:

  ```bat
  python3 clean_wj_downloads.py "C:\Users\YourUsername\Downloads\Wabbajack\downloads\modpack.wabbajack"
  ```

  or

  ```bash
  python3 clean_wj_downloads.py "/home/yourusername/Downloads/Wabbajack/downloads/modpack.wabbajack"
  ```

5. The script will ask for your mod downloads folder. This is the folder where the mods are downloaded to by wabbajack. For example:

  ```bat
  C:\Users\YourUsername\Downloads\Wabbajack\ModpackName\downloads
  ```

  or

  ```bash
  /home/yourusername/Downloads/Wabbajack/ModpackName/downloads
  ```

By default, the script will not delete any files unless you respond `y` to the prompts.  

- If you want to check, the sanity files are saved in the same folder as the script, with the name `to_be_kept.txt` and `to_be_deleted.txt` and those will not be deleted unless you remove them manually.  
- `sorted_local_mods.txt` and `sorted_wabbajack_mods.txt` are support files for debbuging and will be overwritten every time you run the script.  

## For multiple modpacks

If you are one of those who likes to hop between modpacks, the [merge_wj_downloads.py](./merge_wj_downloads.py) script is for you. This script will merge TWO and ONLY TWO `.wabbajack` files and fuction as the [clean_wj_downloads.py](./clean_wj_downloads.py) script. Since it's recommended to use the same downloads folder for all modpacks, it will ask for only one download folder when running the script.  
The usage is the same as the [clean_wj_downloads.py](./clean_wj_downloads.py), you just need to pass two files as arguments.  
Example:

  ```bat
  python3 merge_wj_downloads.py "C:\Users\YourUsername\Downloads\Wabbajack\downloads\first.wabbajack" "C:\Users\YourUsername\Downloads\Wabbajack\downloads\second.wabbajack"
  ```

  or

  ```bash
  python3 merge_wj_downloads.py "/home/yourusername/Downloads/Wabbajack/downloads/first.wabbajack" "/home/yourusername/Downloads/Wabbajack/downloads/second.wabbajack"
  ```

---
Both of these scripts are simple, codded in just a few minutes late at night waiting for licentia finish installing, but they are useful for me and I hope they can be useful for you too. Feel free to use and modify them as you wish.  
If you have any questions or suggestions, feel free to open an issue or a pull request.  
Enjoy!
