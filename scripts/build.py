import os
import json
import arrow
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
    "-V",
    type=str,
    dest="version",
    default=None,
    help="the version string to include in the viruses.json file"
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

                with open(os.path.join(isolate_path, "sequences.json"), "r") as f:
                    isolate["sequences"] = json.load(f)

                with open(os.path.join(isolate_path, "sequences.fa"), "r") as f:
                    sid = None
                    seq = list()

                    for line in f:
                        if line[0] == ">":
                            if sid:
                                for sequence in isolate["sequences"]:
                                    if sequence["_id"] == sid:
                                        sequence["sequence"] = "".join(seq)
                                        break

                            sid = line.rstrip().replace(">", "")
                            seq = list()

                        elif line:
                            seq.append(line.rstrip())

                    if sid:
                        for sequence in isolate["sequences"]:
                            if sequence["_id"] == sid:
                                sequence["sequence"] = "".join(seq)

                virus["isolates"].append(isolate)

            viruses.append(virus)

    with open(args.output, "w") as f:
        json.dump({
            "data": viruses,
            "version": args.version,
            "created_at": arrow.utcnow().isoformat()
        }, f, indent=4)
