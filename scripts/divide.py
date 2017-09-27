import os
import json
import shutil

DELETED_KEYS = [
    "user",
    "version",
    "imported",
    "last_indexed_version",
    "verified"
]

shutil.rmtree("src", ignore_errors=True)
os.mkdir("src")

with open("viruses.json", "r") as export_handle:
    for virus in json.load(export_handle):
        first_letter = virus["lower_name"][0]

        try:
            os.mkdir(os.path.join("src", first_letter))
        except FileExistsError:
            pass
        
        virus_path = os.path.join("src", first_letter, virus["lower_name"].replace(" ", "_").replace("/", "_"))
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
