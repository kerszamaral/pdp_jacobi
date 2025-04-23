from pathlib import Path
from argparse import ArgumentParser

def get_percentage(string: str) -> str:
    """
    Extracts the percentage from a string formatted as ": XX.XX%".
    """
    start = string.find('(') + 1
    end = string.find(' out of')
    return string[start:end].strip()

def gen_efficiency(folder: Path, outfile: Path):
    print(f"Generating efficiency data from {folder} to {outfile}")
    with outfile.open('w') as outf:
        header = "Input1 Input2 Logical_Core_Usage_Seq(%) Logical_Core_Usage_MP(%) Threads"
        outf.write(header + "\n")
        input_pairs = set()
        threads = set()
        for file in folder.glob("*.txt"):
            name = file.stem
            parts = name.split("_")
            input1 = int(parts[2])
            input2 = int(parts[3])
            input_pairs.add((input1, input2))
            if len(parts) > 4:
                threads.add(int(parts[4]))
        input_pairs = sorted(input_pairs)
        threads = sorted(threads)
        
        for input1, input2 in input_pairs:
            outf.write(f"{input1} {input2}")
            seq_file = folder / f"laplace_seq_{input1}_{input2}.txt"
            with seq_file.open('r') as seqf:
                for line in seqf:
                    if "Effective Physical Core Utilization" in line:
                        seq_eff = float(get_percentage(line))/1
                        outf.write(f" {seq_eff}")
                        break
            for thread_num in threads:
                mp_file = folder / f"laplace_mp_{input1}_{input2}_{thread_num}.txt"
                with mp_file.open('r') as mpf:
                    for line in mpf:
                        if "Effective Physical Core Utilization" in line:
                            mp_eff = float(get_percentage(line))/thread_num
                            outf.write(f" {mp_eff} {thread_num}")
                            break
            outf.write("\n")
        print(f"Efficiency data written to {outfile}")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--folder", "-f",
                        nargs="?",
                        type=Path,
                        default=Path("vtune_results"),
                        )
    parsed = parser.parse_args()
    folder: Path = parsed.folder
    outfile = Path("efficiency.txt")
    gen_efficiency(folder, outfile)
