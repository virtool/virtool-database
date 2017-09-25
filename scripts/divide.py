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

shutil.rmtree("src")
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

            for sequence in sequences:
                sequence_id = sequence["_id"]

                sequence_path = os.path.join(isolate_path, sequence_id)
                os.mkdir(sequence_path)

                sequence_text = sequence.pop("sequence")

                with open(os.path.join(sequence_path, "sequence.json"), "w") as f:
                    json.dump(sequence, f)

                with open(os.path.join(sequence_path, "sequence.fa"), "w") as f:
                    f.write(">{}\n{}\n".format(sequence_id, sequence_text))
