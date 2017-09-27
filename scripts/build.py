import os
import json
import shutil
import argparse


DELETED_KEYS = [
    "user",
    "version",
    "imported",
    "last_indexed_version",
    "verified"
]

parser = argparse.ArgumentParser(description="Building a viruses.json file from a virtool-databse src directory")

parser.add_argument(
    "src",
    type=str,
    help="the path to the database src directory",
)

parser.add_argument(
    "-f",
    type=str,
    dest="output",
    default="viruses.json",
    help="the output path for the viruses.json file"
)

args = parser.parse_args()


if __name__ == "__main__":
    src_path = args.src

    viruses = list()

    for alpha in os.listdir(src_path):
        virus_paths = [os.path.join(src_path, alpha, virus) for virus in os.listdir(os.path.join(src_path, alpha))]

        for virus_path in virus_paths:
            with open(os.path.join(virus_path, "virus.json"), "r") as f:
                virus = json.load(f)

            virus["isolates"] = list()

            isolate_ids = [i for i in os.listdir(virus_path) if i != "virus.json" and i[0] != "."]

            for isolate_path in [os.path.join(virus_path, i) for i in isolate_ids]:
                with open(os.path.join(isolate_path, "isolate.json"), "r") as f:
                    isolate = json.load(f)
                    isolate["sequences"] = list()


                seq_ids = [s for s in os.listdir(isolate_path) if s != "isolate.json" and s[0] != "."]

                for seq_path in [os.path.join(isolate_path, s) for s in seq_ids]:
                    with open(os.path.join(seq_path, "sequence.json"), "r") as f:
                        sequence = json.load(f)

                    with open(os.path.join(seq_path, "sequence.fa"), "r") as f:
                        seq = list()

                        for line in f:
                            if line[0] == ">":
                                continue

                            seq.append(line.rstrip())

                        sequence["sequence"] = "".join(seq)

                    isolate["sequences"].append(sequence)

                virus["isolates"].append(isolate)

            viruses.append(virus)

    with open(args.output, "w") as f:
        json.dump(viruses, f)
