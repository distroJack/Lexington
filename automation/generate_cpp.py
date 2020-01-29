
# SYSTEM IMPORTS
import os
from sys import argv
import re
# PROJECT IMPORTS

# LOCAL IMPORTS

# generate_cpp class name ./path/to/file
#   will generate cpp AND associated header if one does not exist in the specified locations

CPP_FILE_TYPES = ["source", "header", "main"]

def parse_args():
    """Parse command line args into file (type, name, path)"""
    if len(argv) != 4:
        raise RuntimeError("generate script must take in 4 arguments")

    file_type = argv[1]

    if file_type not in CPP_FILE_TYPES:
        error_str = "file type '{}' not in list of accepted file types : {}"
        raise RuntimeError(error_str.format(file_type, CPP_FILE_TYPES))

    file_name = argv[2]
    file_path = argv[3]

    info_str = "Generating {} {} in location {}"
    print(info_str.format(file_type, file_name, file_path))

    return (file_type, file_name, file_path)


def generate_text(type: str, name: str, path: str):
    """Generate file from template based on type, name, and path"""
    if type == "source":
        if not os.path.isfile(os.path.join(path, name + ".hpp")):
            return { name + ".hpp" : generate_header(name, path),
                     name + ".cpp" : generate_source(name, path)}
        else:
            return { name + ".cpp" : generate_source(name, path)}

    elif type == "header":
        return { name + ".hpp" : generate_header(name, path)}

    elif type == "main":
        return { name + "Main.cpp" : generate_main(name, path)}

    else:
        error_str = "file type '{}' not in list of accepted file types : {}"
        raise RuntimeError(error_str.format(type, CPP_FILE_TYPES))


def generate_source(name: str, path: str):
    CamellName = name

    namespace = path.split("/")
    namespace.remove(".")

    # Format namespace to be semi-camell case (assumes cammell is correct)
    namespace = [name[0].upper() + name[1:] for name in namespace]

    forward_namespace_strs = ["namespace {} {{\n".format(name) for name in namespace]
    ForwardNamespace = "".join(forward_namespace_strs)

    backward_namespace_strs = ["}} // namespace {}\n".format(name) for name in namespace]
    BackwardNamespace = "".join(backward_namespace_strs)

    output_file = ""
    source_path = "./templates/Source.cpp"
    with open(source_path, "r") as fly:
        raw_template = fly.read()

        name_str_maps = {
            "CamellName": CamellName,
            "ForwardNamespace": ForwardNamespace,
            "BackwardNamespace": BackwardNamespace
        }

        output_file = raw_template.format(**name_str_maps)

    return output_file


def generate_header(name: str, path: str):
    CamellName = name

    namespace = path.split("/")
    namespace.remove(".")

    # Format namespace to be semi-camell case (assumes cammell is correct)
    namespace = [name[0].upper() + name[1:] for name in namespace]

    # https://stackoverflow.com/questions/2277352/split-a-string-at-uppercase-letters
    endif_space = [part.upper() for name in namespace
                                for part in re.findall('[A-Z][^A-Z]*', name)]

    ExpandedIfDefName = "_".join(endif_space) + "_H_"

    forward_namespace_strs = ["namespace {} {{\n".format(name) for name in namespace]
    ForwardNamespace = "".join(forward_namespace_strs)

    backward_namespace_strs = ["}} // namespace {}\n".format(name) for name in namespace]
    BackwardNamespace = "".join(backward_namespace_strs)

    output_file = ""
    header_path = "./templates/Header.hpp"
    with open(header_path, "r") as fly:
        raw_template = fly.read()

        name_str_maps = {
            "CamellName": CamellName,
            "ExpandedIfDefName": ExpandedIfDefName,
            "ForwardNamespace": ForwardNamespace,
            "BackwardNamespace": BackwardNamespace
        }

        output_file = raw_template.format(**name_str_maps)

    return output_file


def generate_main(name: str, path: str):
    CamellName = name

    namespace = path.split("/")
    namespace.remove(".")

    # bellow lines allow us to skip over any src/test directories present
    namespace.remove("src")
    namespace.remove("test")

    # Format namespace to be semi-camell case (assumes cammell is correct)
    namespace = [name[0].upper() + name[1:] for name in namespace]

    NameSpace = "::".join(namespace)

    output_file = ""
    main_path = "./templates/Main.cpp"
    with open(main_path, "r") as fly:
        raw_template = fly.read()

        name_str_maps = {
            "CamellName": CamellName,
            "NameSpace": NameSpace,
        }

        output_file = raw_template.format(**name_str_maps)

    return output_file

def create_files(path, output_files):

    os.makedirs(path, exist_ok=True)
    for name, text in output_files.items():
        file_on_path = os.path.join(path, name)
        print("Creating file : {}".format(file_on_path))
        with open(file_on_path, "w") as fly:
            fly.write(text)


if __name__ == "__main__":

    type, name, path = parse_args()
    output_files = generate_text(type, name, path)
    create_files(path, output_files)
