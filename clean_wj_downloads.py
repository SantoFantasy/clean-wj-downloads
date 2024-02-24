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
    to_be_deleted = []
    for item in sorted_local_mods:
        if item not in sorted_wabbajack_mods:
            to_be_deleted.append(item)
    return to_be_deleted


def sanity_check(sorted_wabbajack_mods: list, sorted_local_mods: list):
    """
    Performs a sanity check to determine which mods should be deleted and which mods should be kept.

    Args:
      sorted_wabbajack_mods (list): A list of mods sorted by Wabbajack.
      sorted_local_mods (list): A list of local mods.

    Returns:
      bool: True if the mods to be kept match the mods in sorted_wabbajack_mods, False otherwise.
    """
    to_be_deleted = []
    to_be_kept = []
    with open("to_be_deleted.txt", "w") as f:
        f.write("")
    with open("to_be_kept.txt", "w") as f:
        f.write("")

    for item in sorted_local_mods:
        if item not in sorted_wabbajack_mods:
            to_be_deleted.append(item)
            with open("to_be_deleted.txt", "a") as f:
                f.write(item + "\n")
        else:
            to_be_kept.append(item)
            with open("to_be_kept.txt", "a") as f:
                f.write(item + "\n")

    to_be_kept_by_lines = []
    with open("to_be_kept.txt", "r") as f:
        for item in f:
            if item.strip() in sorted_wabbajack_mods:
                to_be_kept_by_lines.append(item.strip())
    if len(to_be_kept_by_lines) == len(to_be_kept):
        return True
    else:
        return False


def delete_old_mods(to_be_deleted: list, local_mods_dir: str):
    """
    Deletes the old mods from the specified directory.

    Args:
      to_be_deleted (list): List of mod files to be deleted.
      local_mods_dir (str): Path to the directory containing the mod files.

    Returns:
      None
    """
    for item in to_be_deleted:
        os.remove(os.path.join(local_mods_dir, item))


def main(args: str):
    """
    Extracts modlist from a Wabbajack mod archive, compares it with local mods,
    and performs various operations based on the comparison.

    Args:
      args (str): Path to the Wabbajack mod archive.

    Returns:
      None
    """
    wabbajack_mods = args
    # unzip modlist from wabbajack_mods
    with zipfile.ZipFile(wabbajack_mods, "r") as zip_ref:
        zip_ref.extract("modlist")
    modlist_json = None
    modlist = []
    with open("modlist", "r") as f:
        modlist_json = json.load(f)
    os.remove("modlist")
    for item in modlist_json["Archives"]:
        modlist.append(item["Name"])
    sorted_wabbajack_mods = sorted(modlist)
    with open("sorted_wabbajack_mods.txt", "a") as f:
        for item in sorted_wabbajack_mods:
            f.write(item + "\n")
    # get local mods
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
                to_be_deleted = to_delete(sorted_wabbajack_mods, sorted_local_mods)
                delete_old_mods(to_be_deleted, local_mods_dir)
                print("Mods were deleted.")
                print(
                    "Check the to_be_deleted.txt file for the list of mods that were deleted."
                )
            else:
                print("No mods were deleted.")
        else:
            print("Your local mods are not in sync with the wabbajack modlist.")
    clean_up_support_files = input("Do you want to delete the support files? (y/N): ")
    if clean_up_support_files.lower() == "y":
        os.remove("sorted_local_mods.txt")
        os.remove("sorted_wabbajack_mods.txt")
    print("Done.")
    print("Sanity check files still exist. If you want to delete them, do it manually.")


if __name__ == "__main__":
    try:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help" or sys.argv[1] == None:
            print("Usage: \n\t$ python modstokeep.py <wabbajack file>")
            sys.exit(0)
        elif sys.argv[1].endswith(".wabbajack"):
            modlist = sys.argv[1]
        else:
            print("The file you provided is not a Wabbajack mod archive.")
            sys.exit(0)
    except IndexError:
        print("Usage: \n\t$ python modstokeep.py <wabbajack file>")
        sys.exit(1)
    main(modlist)

else:
    print("This script is not meant to be imported.")
    sys.exit(1)
