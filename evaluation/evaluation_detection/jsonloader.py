from evalutils.io import FileLoader
from pathlib import Path
import json


class NODE21Loader(FileLoader):
    def load(self, *, fname: Path):
        #fname = '/input/predictions.json'
        if str(fname).endswith(".json"):
        
            print('fname ', fname)
            with open(fname, 'r') as f:
                entries = json.load(f)
            cases = []

            for e in entries:
                # Find case name through input file name
                inputs = e['inputs']
                name = None
                for inp in inputs:
                    if inp["interface"]["slug"] == "generic-medical-image":
                        name = inp["image"]["name"]
                        break  # expecting only a single input
                if name is None:
                    raise ValueError(f"No filename found for pk {e['pk']}")

                # Find output value for this case
                outputs = e['outputs']

                for outp in outputs:
                    if outp["interface"]["slug"] == "results-json-file":
                        for i in outp["value"][0]["outputs"][0]["boxes"]:
                            slice_nb = None
                            probability = None
                            x_min = None
                            y_min = None
                            x_max = None
                            y_max = None
                            slice_nb  = i["corners"][0][2]
                            boxes = i["corners"]
                            x_min, y_min, x_max, y_max = boxes[2][0], boxes[2][1], boxes[0][0], boxes[0][1]
                            probability = i['probability']
                            entry = {"name": name,
                                     "slice": slice_nb,
                                     "probability": probability,
                                     "x_min":x_min,
                                     "y_min":y_min,
                                     "x_max":x_max,
                                     "y_max":y_max
                                    }
                            cases += [entry]

                        if slice_nb is None:
                            raise ValueError(f"No slice number found for pk {e['pk']}")
                        if probability is None:
                            raise ValueError(f"No probability found for pk {e['pk']}")

            return cases
        else:
            print('it is not a json file, skipping this file.')



