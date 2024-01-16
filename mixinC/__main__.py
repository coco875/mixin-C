import argparse
import os
import re

def get_c_files(repertory):
    for root, dirs, files in os.walk(repertory):
        for file in files:
            if file.endswith(".c"):
                yield os.path.join(root, file)

def main(repertory="./test"):
    mixin = {}
    for file in get_c_files(repertory):
        with open(file, "r") as f:
            name = ""
            code = ""
            parentesis = 0
            text = f.read()
            for line in text.split("\n"):
                parentesis += line.count("{") - line.count("}")
                if name != "":
                    code += line+"\n"
                if line.startswith("OVERWRITE"):
                    name = re.findall(r"OVERWRITE\((.*)\)", line)[0]
                    code = ""
                    continue
                if parentesis == 0 and code != "":
                    if not name in mixin:
                        mixin[name] = {}
                    if "overwrites" in mixin[name]:
                        print("WARNING: cannot overwrite {} with {} because it is already overwritten by {}".format(
                            name, re.findall((r".* ([\w_]+)\(", code)),re.findall((r".* ([\w_]+)\(", mixin[name]["overwrites"])))
                        )
                    else:
                        mixin[name]["overwrites"] = code
                    name = ""
                    code = ""
            for functions, add_end_funciton in re.findall(r"ADD_END\((.*)\)\n(.*)", text):
                for function_name in functions.split(","):
                    function_name = function_name.strip()
                    if not function_name in mixin:
                        mixin[function_name] = {}
                    if not "add_end" in mixin[function_name]:
                        mixin[function_name]["add_end"] = []
                    mixin[function_name]["add_end"].append(re.findall(r"([\w_]+)\(", add_end_funciton)[0])
    return mixin

def copy_with_apply_mixin(repertory="./test", output="./output", mixin={}):
    for file in get_c_files(repertory):
        out = ""
        ignore = False
        parentesis = 0
        code = ""
        name = ""
        with open(file, "r") as f:
            text = f.read()
            for line in text.split("\n"):
                parentesis += line.count("{") - line.count("}")
                if line.startswith("OVERWRITE"):
                    continue
                if line.startswith("ADD_END"):
                    continue
                for func in mixin:
                    if re.match(".* {}\(.*".format(func), line):
                        print(func, line)
                        ignore = True
                        name = func
                        break
                if not ignore:
                    out += line + "\n"
                else:
                    code += line + "\n"
                if parentesis == 0:
                    ignore = False
                    if name != "":
                        if "overwrites" in mixin[name]:
                            code = re.sub(r"[\w_]+\((.*)", r"{}(\1".format(name), mixin[name]["overwrites"])
                        if "add_end" in mixin[name]:
                            for func in mixin[name]["add_end"]:
                                code = re.sub(r"return (.*);", r"return {}(\1);".format(func), code)
                    out += code
                    code = ""
                    name = ""
        with open(os.path.join(output, os.path.basename(file)), "w") as f:
            f.write(out)
    return text

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--files", default="./test", help="Files to parse")
    parser.add_argument("-o", "--output", default="./output", help="Output file")
    args = parser.parse_args()
    mixin = main(args.files)
    copy_with_apply_mixin(args.files, args.output, mixin)
    print(mixin)
