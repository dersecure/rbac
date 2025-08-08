"""
Script to create the RBAC (Role-Based Access Control) definitions for the SunSpec models.
This iterates through all the SunSpec models and generates json files of the format from
pysunspec2.

This script also generates the roles_to_rights.md file with a list of all the models and
the read/write access levels for each role.

Note: if there are changes to the sunspec models, update the submodule with:
    git submodule update --remote sunspec-models
"""

import os
import json
import glob
import subprocess
import re
import natsort


ROLES = ['DEROwnerSunSpec', 'DERInstallerSunSpec', 'DERVendorSunSpec', 'ServiceProviderSunSpec', 'GridOperatorSunSpec']
MEASUREMENT_MODELS = [101, 102, 103, 111, 112, 113, 701]


def update_submodule():
    """
    Update the sunspec-models submodule to the latest version.
    """
    try:
        subprocess.run(['git', 'submodule', 'update', '--remote', 'sunspec-models'], check=True)
        print("Submodule updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating submodule: {e}")


def empty_rbac_directory():
    """
    Empty the rbac directory to ensure no old files remain.
    """
    rbac_dir = "rbac"
    if not os.path.exists(rbac_dir):
        os.makedirs(rbac_dir)
    else:
        for file in glob.glob(os.path.join(rbac_dir, "*.json")):
            os.remove(file)
        print(f"Cleared existing files in {rbac_dir} directory.")


def generate_rbac():
    """
    Generate the RBAC (Role-Based Access Control) definitions for the SunSpec models.
    """
    empty_rbac_directory()

    for json_file in glob.glob("sunspec-models/json/*.json"):
        model_name = os.path.basename(json_file).replace(".json", "")

        if model_name == "schema":
            continue

        # Don't create RBAC definitions for vendor provided models
        match = re.search(r"(\d+)", model_name)
        model_id = int(match.group(1)) if match else None
        if model_id and model_id > 10000:
            continue

        with open(json_file, "r") as f:
            model = json.load(f)

        rbac = replace_points(model, model_id)

        output_file = os.path.join("rbac", os.path.basename(json_file))
        with open(output_file, "w") as f:
            json.dump(rbac, f, indent=4)
        print(f"Generated RBAC for {os.path.basename(json_file)}")


def replace_points(obj, model_id):
    """
    Recursively replace the 'points' in the object with a filtered version,
    keeping only 'desc' and 'name', and adding 'read_roles' and 'write_roles'

    :param obj: (dict) The json sunspec model object
    :param model_id: (int) The model ID
    """
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            if k == "points" and isinstance(v, list):
                new_points = []
                for item in v:
                    filtered = filter_point(item)

                    # If the point is "L" or "ID", give it all read roles for SunSpec discovery
                    if isinstance(filtered, dict) and filtered.get("name") in ("L", "ID"):
                        filtered["read_roles"] = ROLES.copy()

                    # If the model in MEASUREMENT_MODELS, allow read access to all roles
                    if model_id in MEASUREMENT_MODELS:
                        filtered["read_roles"] = ROLES.copy()

                    new_points.append(filtered)
                new_obj[k] = new_points
            elif isinstance(v, (dict, list)):
                new_obj[k] = replace_points(v, model_id)
            else:
                new_obj[k] = v
        return new_obj
    elif isinstance(obj, list):
        return [replace_points(item, model_id) for item in obj]
    else:
        return obj


def filter_point(item):
    """
    Filter the point item to keep only the 'desc' and 'name' keys,
    and add 'read_roles' and 'write_roles' as empty lists.
    """
    if isinstance(item, dict):
        filtered = {}
        for key in ("desc", "name"):
            if key in item:
                filtered[key] = item[key]
        filtered["read_roles"] = []
        filtered["write_roles"] = []
        return filtered
    return item


def generate_roles_to_rights():
    """
    Generate the roles_to_rights.md file with a list of all the models and the read/write access levels for each role.
    """
    with open("roles_to_rights.md", "w") as f:
        f.write("# Roles to Rights Mapping\n\n")
        # Write the main index table header
        f.write("| Model | RBAC Reference |\n")
        f.write("|-------|----------------|\n")

        # Generate individual model markdown files and index entries
        for json_file in sorted(
            glob.glob("rbac/*.json"),
            key=lambda x: (
                int(re.search(r"(\d+)", os.path.basename(x)).group(1))
                if re.search(r"(\d+)", os.path.basename(x))
                else 0
            ),
        ):
            model_name = os.path.basename(json_file).replace(".json", "")
            model_id = int(re.search(r"(\d+)", model_name).group(1)) if re.search(r"(\d+)", model_name) else None
            with open(json_file, "r") as mf:
                model = json.load(mf)

            point_roles = find_roles(model)
            if len(point_roles) == 0:
                print(f"No points found in model {model_name}. Skipping.")
                continue

            # Place ID and L at the top of the points list; sort other points by the depth in the group hierarchy
            special_points = {k: v for k, v in point_roles.items() if k.endswith(".ID") or k.endswith(".L")}
            other_points = dict(
                sorted(
                    ((k, v) for k, v in point_roles.items() if not (k.endswith(".ID") or k.endswith(".L"))),
                    key=lambda item: item[0].count("."),
                )
            )
            point_roles = {**special_points, **other_points}
            if not point_roles:
                print(f"No relevant points found in model {model_name}. Skipping.")
                continue

            # Write entry in the index table
            model_md_filename = f"model_{model_id}_rbac.md"
            f.write(f"| {model_id} | [RBAC Roles-to-Rights Model {model_id} Table](/doc/{model_md_filename}) |\n")

            # Write the individual model markdown file
            with open(os.path.join("doc", model_md_filename), "w") as model_md:
                model_md.write(f"# RBAC Reference for Model {model_id}\n\n")
                model_md.write(
                    "| Model | Point | DEROwnerSunSpec | DERInstallerSunSpec | DERVendorSunSpec | ServiceProviderSunSpec | GridOperatorSunSpec |\n"
                )
                model_md.write(
                    "|-------|-------|------------------|---------------------|------------------|------------------------|---------------------|\n"
                )

                for pt_name, pt in point_roles.items():
                    read_roles = set(pt.get("read", []))
                    write_roles = set(pt.get("write", []))
                    role_values = {role: "" for role in ROLES}
                    for role in ROLES:
                        if role in read_roles:
                            role_values[role] += "R"
                        if role in write_roles:
                            role_values[role] += "W"
                    model_md.write(
                        f"| {model_id} | {pt_name} | "
                        f"{role_values.get('DEROwnerSunSpec', '')} | "
                        f"{role_values.get('DERInstallerSunSpec', '')} | "
                        f"{role_values.get('DERVendorSunSpec', '')} | "
                        f"{role_values.get('ServiceProviderSunSpec', '')} | "
                        f"{role_values.get('GridOperatorSunSpec', '')} |\n"
                    )


def find_roles(obj):
    def collect_point_roles(obj, parent_path=None, result=None):
        if result is None:
            result = {}
        if parent_path is None:
            parent_path = []
        if isinstance(obj, dict):
            # If this dict is a group with a name, add it to the path
            group_name = obj.get("name") if obj.get("type") == "group" and "name" in obj else None
            if group_name:
                parent_path = parent_path + [group_name]
            for k, v in obj.items():
                if k == "points" and isinstance(v, list):
                    for pt in v:
                        pt_name = pt.get("name") if isinstance(pt, dict) else None
                        if pt_name:
                            fq_name = ".".join(parent_path + [pt_name])
                            read_roles = pt.get("read_roles", []) if isinstance(pt, dict) else []
                            write_roles = pt.get("write_roles", []) if isinstance(pt, dict) else []
                            result[fq_name] = {"read": list(read_roles), "write": list(write_roles)}
                elif isinstance(v, (dict, list)):
                    collect_point_roles(v, parent_path, result)
        elif isinstance(obj, list):
            for item in obj:
                collect_point_roles(item, parent_path, result)
        return result

    return collect_point_roles(obj)


if __name__ == "__main__":
    update_submodule()
    generate_rbac()
    generate_roles_to_rights()
    print("RBAC generation completed.")
