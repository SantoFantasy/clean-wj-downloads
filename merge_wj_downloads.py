import os
import sys
import json
import zipfile


def to_delete(sorted_wabbajack_mods: list, sorted_local_mods: list):
    """
    Returns a list of mods that should be deleted from the local mods directory.

    Parameters:
    sorted_wabbajack_mods (list): A list of mods from Wabbajack.
    sorted_local_mods (list): A list of mods from the local mods directory.

    Returns:
    list: A list of mods that should be deleted.
    """
    merged_to_be_deleted = []
    for item in sorted_local_mods:
        if item not in sorted_wabbajack_mods:
            merged_to_be_deleted.append(item)
    return merged_to_be_deleted


def sanity_check(sorted_wabbajack_mods: list, sorted_local_mods: list):
    """
    Performs a sanity check to determine which mods should be deleted and which mods should be kept.

    Args:
      sorted_wabbajack_mods (list): A list of mods sorted by Wabbajack.
      sorted_local_mods (list): A list of local mods.

    Returns:
      bool: True if the mods to be kept match the mods in sorted_wabbajack_mods, False otherwise.
    """
    merged_to_be_deleted = []
    merged_to_be_kept = []
    with open("merged_to_be_deleted.txt", "w") as f:
        f.write("")
    with open("merged_to_be_kept.txt", "w") as f:
        f.write("")

    for item in sorted_local_mods:
        if item not in sorted_wabbajack_mods:
            merged_to_be_deleted.append(item)
            with open("merged_to_be_deleted.txt", "a") as f:
                f.write(item + "\n")
        else:
            merged_to_be_kept.append(item)
            with open("merged_to_be_kept.txt", "a") as f:
                f.write(item + "\n")

    merged_to_be_kept_by_lines = []
    with open("merged_to_be_kept.txt", "r") as f:
        for item in f:
            if item.strip() in sorted_wabbajack_mods:
                merged_to_be_kept_by_lines.append(item.strip())
    if len(merged_to_be_kept_by_lines) == len(merged_to_be_kept):
        return True
    else:
        return False


def delete_old_mods(merged_to_be_deleted: list, local_mods_dir: str):
    """
    Deletes the old mods from the specified directory.

    Args:
      merged_to_be_deleted (list): List of mod files to be deleted.
      local_mods_dir (str): Path to the directory containing the mod files.

    Returns:
      None
    """
    for item in merged_to_be_deleted:
        os.remove(os.path.join(local_mods_dir, item))


def main(modlist1: str, modlist2: str):
    """
    Extracts modlist from a Wabbajack mod archive, compares it with local mods,
    and performs various operations based on the comparison.

    Args:
      args (str): Path to the Wabbajack mod archive.

    Returns:
      None
    """
    modlist1_json = None
    modlist2_json = None
    modlist1_files = []
    modlist2_files = []
    with zipfile.ZipFile(modlist1, "r") as z:
        with z.open("modlist") as f:
            modlist1_json = json.load(f)
    for item in modlist1_json["Archives"]:
        modlist1_files.append(item["Name"])
    with zipfile.ZipFile(modlist2, "r") as z:
        with z.open("modlist") as f:
            modlist2_json = json.load(f)
    for item in modlist2_json["Archives"]:
        modlist2_files.append(item["Name"])
    full_modlist = modlist1_files
    full_modlist.extend(x for x in modlist2_files if x not in modlist1_files)
    sorted_wabbajack_mods = sorted(full_modlist)
    local_mods_dir = input("Enter the path to your downloaded mods directory: ")
    if os.path.exists(local_mods_dir):
        local_mods = os.listdir(local_mods_dir)
        sorted_local_mods = sorted(local_mods)
        with open("sorted_local_mods.txt", "a") as f:
            for item in sorted_local_mods:
                f.write(item + "\n")
        if sanity_check(sorted_wabbajack_mods, sorted_local_mods):
            print("Your local mods are in sync with the wabbajack modlist.")
            delte_local_mods = input(
                "Do you want to delete the mods that are not in sync with the wabbajack modlist? (y/N): "
            )
            if delte_local_mods.lower() == "y":
                merged_to_be_deleted = to_delete(sorted_wabbajack_mods, sorted_local_mods)
                delete_old_mods(merged_to_be_deleted, local_mods_dir)
                print("Mods were deleted.")
                print(
                    "Check the merged_to_be_deleted.txt file for the list of mods that were deleted."
                )
            else:
                print("No mods were deleted.")
        else:
            print("Your local mods are not in sync with the wabbajack modlist.")
    clean_up_support_files = input("Do you want to delete the support files? (y/N): ")
    if clean_up_support_files.lower() == "y":
        os.remove("sorted_local_mods.txt")
    print("Done.")
    print("Sanity check files still exist. If you want to delete them, do it manually.")


if __name__ == "__main__":
    try:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help" or sys.argv[1] == None:
            print(
                "Usage: \n\t$ python merge_wj_downloads.py <wabbajack file 1> <wabbajack file 2>"
            )
            sys.exit(0)
        elif sys.argv[1].endswith(".wabbajack") and sys.argv[2].endswith(".wabbajack"):
            modlist1 = sys.argv[1]
            modlist2 = sys.argv[2]
        else:
            print("The file you provided is not a Wabbajack mod archive.")
            sys.exit(0)
    except IndexError:
        print("Usage: \n\t$ python merge_wj_downloads.py <wabbajack file 1> <wabbajack file 2>")
        sys.exit(1)
    main(modlist1, modlist2)

else:
    print("This script is not meant to be imported.")
    sys.exit(1)
