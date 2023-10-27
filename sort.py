import unidecode
import os
import shutil

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

            if not found:
                pass

    for root, dirs, files in os.walk(folder_path):
        for directory in dirs:
            dir_path = os.path.join(root, directory)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Provide exactly one path to the folder.")
    else:
        folder_path = sys.argv[1]
        sort(folder_path)
        print("Sorting completed.")
