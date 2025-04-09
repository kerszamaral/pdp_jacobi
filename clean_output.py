from pathlib import Path



def clean_folder(folder: Path) -> None:
    for file in folder.glob("*.txt"):
        print(f"Cleaning {file}...")
        with open(file, "r") as f:
            lines = f.readlines()

        start_of_skip = "vtune: Collection started"
        end_of_skip = "vtune: Collection stopped"
        
        start = 0
        end = 0
            
        for i, line in enumerate(lines):
            if start_of_skip in line:
                start = i
            if end_of_skip in line:
                end = i
                break
        
        print(f"Cleaning {file}...")
        print(f"Start line: {start}, End line: {end}")
        new_file = file.with_suffix(".txt")
        with open(new_file, "w") as f:
            f.writelines(lines[:start+1])
            f.writelines(lines[end:])
        print(f"Cleaned {file} and saved to {new_file}")
        
if __name__ == "__main__":
    folder = Path("out")
    clean_folder(folder)
    print("Cleaning completed.")