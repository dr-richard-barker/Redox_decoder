import os
import shutil
import json
import tarfile

def prepare_zenodo_package():
    manifest_path = "zenodo_deposition_manifest.json"
    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    package_dir = "zenodo_package"
    os.makedirs(package_dir, exist_ok=True)

    # Subdirectories
    subdirs = ["code", "web_tool", "manuscript", "figures", "tables", "metadata", "data"]
    for sd in subdirs:
        os.makedirs(os.path.join(package_dir, sd), exist_ok=True)

    print(f"=== Preparing Zenodo Deposition Package v{manifest.get('version', '1.0.0')} ===")

    # Copy files present in repository to the package structure
    file_count = 0
    
    # 1. Manuscript
    if os.path.exists("manuscript.pdf"):
        shutil.copy("manuscript.pdf", os.path.join(package_dir, "manuscript/manuscript.pdf"))
        file_count += 1
    if os.path.exists("manuscript.md"):
        shutil.copy("manuscript.md", os.path.join(package_dir, "manuscript/manuscript.md"))
        file_count += 1
    if os.path.exists("references.bib"):
        shutil.copy("references.bib", os.path.join(package_dir, "manuscript/references.bib"))
        file_count += 1

    # 2. Web tool & Docker
    if os.path.exists("web_app.py"):
        shutil.copy("web_app.py", os.path.join(package_dir, "web_tool/web_app.py"))
        file_count += 1
    if os.path.exists("Dockerfile"):
        shutil.copy("Dockerfile", os.path.join(package_dir, "web_tool/Dockerfile"))
        file_count += 1
    if os.path.exists("index.html"):
        shutil.copy("index.html", os.path.join(package_dir, "web_tool/index.html"))
        file_count += 1

    # 3. Code scripts
    for script in os.listdir("."):
        if script.endswith(".py") and script not in ["prepare_zenodo_package.py"]:
            shutil.copy(script, os.path.join(package_dir, "code", script))
            file_count += 1

    # 4. Tables
    for f in os.listdir("."):
        if f.startswith("Table_") and f.endswith(".csv"):
            shutil.copy(f, os.path.join(package_dir, "tables", f))
            file_count += 1

    # 5. Metadata
    for f in os.listdir("."):
        if f.endswith(".json") and not f.startswith("zenodo_package"):
            shutil.copy(f, os.path.join(package_dir, "metadata", f))
            file_count += 1

    # 6. Figures
    if os.path.exists("figures"):
        for fig in os.listdir("figures"):
            shutil.copy(os.path.join("figures", fig), os.path.join(package_dir, "figures", fig))
            file_count += 1

    # 7. Data assets
    if os.path.exists("data"):
        for d in os.listdir("data"):
            shutil.copy(os.path.join("data", d), os.path.join(package_dir, "data", d))
            file_count += 1

    # Create tar.gz archive
    archive_name = "zenodo_deposition_v1.0.0.tar.gz"
    with tarfile.open(archive_name, "w:gz") as tar:
        tar.add(package_dir, arcname="zenodo_deposition_v1.0.0")

    archive_size = os.path.getsize(archive_name) / (1024 * 1024)
    print(f"Successfully packaged {file_count} files into {package_dir}/ and created {archive_name} ({archive_size:.2f} MB)!")

if __name__ == "__main__":
    prepare_zenodo_package()
