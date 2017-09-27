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
    help="the path to input viruses.json file",
)

parser.add_argument(
    "-o",
    type=str,
    dest="output",
    default="src",
    help="the output path for divided source directory tree"
)

args = parser.parse_args()

shutil.rmtree(args.output, ignore_errors=True)
os.mkdir(args.output)

with open(args.src, "r") as export_handle:
    data = json.load(export_handle)

    for virus in data["data"]:
        first_letter = virus["lower_name"][0]

        try:
            os.mkdir(os.path.join(args.output, first_letter))
        except FileExistsError:
            pass
        
        virus_path = os.path.join(args.output, first_letter, virus["lower_name"].replace(" ", "_").replace("/", "_"))
        os.mkdir(virus_path)

        isolates = virus.pop("isolates")

        for key in DELETED_KEYS:
            virus.pop(key, None)

        with open(os.path.join(virus_path, "virus.json"), "w") as f:
            json.dump(virus, f, indent=4)

        for isolate in isolates:
            isolate_path = os.path.join(virus_path, isolate["id"])
            os.mkdir(isolate_path)

            sequences = isolate.pop("sequences")

            with open(os.path.join(isolate_path, "isolate.json"), "w") as f:
                json.dump(isolate, f, indent=4)

            fasta_dict = dict()

            with open(os.path.join(isolate_path, "sequences.json"), "w") as f:
                for sequence in sequences:
                    fasta_dict[sequence["_id"]] = sequence.pop("sequence")

                json.dump(sequences, f, indent=4)

            with open(os.path.join(isolate_path, "sequences.fa"), "w") as f:
                output = "\n".join(">{}\n{}".format(sid, s) for sid, s in fasta_dict.items())
                f.write(output)
