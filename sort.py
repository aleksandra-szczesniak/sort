import unidecode
import os
import shutil
import zipfile
import tarfile

extensions = {
    'images': ('.jpeg', '.png', '.jpg', '.svg'),
    'video': ('.avi', '.mp4', '.mov', '.mkv'),
    'documents': ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
    'audio': ('.mp3', '.ogg', '.wav', '.amr'),
    'archives': ('.zip', '.gz', '.tar')
}


def normalize(name):
    normalized_name = unidecode.unidecode(name)
    result = ""
    for char in normalized_name:
        if char.isalnum() or char == "_":
            result += char
        else:
            result += "_"
    return result


def extract_archive(archive_path, destination_folder):
    if archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)
    elif archive_path.endswith('.tar'):
        with tarfile.open(archive_path, 'r') as tar_ref:
            tar_ref.extractall(destination_folder)


def sort(folder_path):
    if not os.path.exists(folder_path):
        print("The specified path does not exist.")
        return

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()

            found = False

            for category, exts in extensions.items():
                if file_extension in exts:
                    found = True
                    category_folder = os.path.join(folder_path, category)
                    new_name = normalize(os.path.splitext(file)[0])
                    new_path = os.path.join(
                        category_folder, new_name + file_extension)

                    if not os.path.exists(new_path):
                        os.makedirs(category_folder, exist_ok=True)

                    shutil.move(file_path, new_path)

            if not found and file_extension in extensions['archives']:
                archive_folder = os.path.join(folder_path, 'archives')
                new_name = normalize(os.path.splitext(file)[0])
                new_folder_path = os.path.join(archive_folder, new_name)
                os.makedirs(archive_folder, exist_ok=True)
                extract_archive(file_path, new_folder_path)
                os.remove(file_path)

    for root, dirs, files in os.walk(folder_path):
        for directory in dirs:
            dir_path = os.path.join(root, directory)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


def print_category_files(folder_path):
    categories = list(extensions.keys())

    for category in categories:
        category_folder = os.path.join(folder_path, category)
        if os.path.exists(category_folder):
            files_in_category = [f for f in os.listdir(
                category_folder) if os.path.isfile(os.path.join(category_folder, f))]
            print(f"{category.capitalize()} files:")
            for file in files_in_category:
                print(file)
            print()


def print_known_extensions(folder_path):
    known_extensions = set()

    for exts in extensions.values():
        known_extensions.update(exts)

    folder_extensions = set()

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            folder_extensions.add(file_extension)

    print("Known file extensions in the destination folder:")
    for ext in known_extensions:
        if ext in folder_extensions:
            print(ext)


def print_unknown_extensions(folder_path):
    known_extensions = set()

    for exts in extensions.values():
        known_extensions.update(exts)

    folder_extensions = set()

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            folder_extensions.add(file_extension)

    unknown_extensions = folder_extensions - known_extensions

    print("Unknown file extensions in the destination folder:")
    for ext in unknown_extensions:
        print(ext)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Provide exactly one path to the folder.")
    else:
        folder_path = sys.argv[1]
        sort(folder_path)
        print("Sorting and extracting completed.")
        print_category_files(folder_path)
        print_known_extensions(folder_path)
        print_unknown_extensions(folder_path)
