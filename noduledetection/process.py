
import SimpleITK
import numpy as np

from pandas import DataFrame
from scipy.ndimage import center_of_mass, label

from evalutils import DetectionAlgorithm
from evalutils.validators import (
    UniquePathIndicesValidator,
    UniqueImagesValidator,
)


class Noduledetection(DetectionAlgorithm):
    def __init__(self):
        super().__init__(
            validators=dict(
                input_image=(
                    UniqueImagesValidator(),
                    UniquePathIndicesValidator(),
                )
            ),
        )

    def predict(self, *, input_image: SimpleITK.Image) -> DataFrame:
        # Extract a numpy array with image data from the SimpleITK Image
        image_data = SimpleITK.GetArrayFromImage(input_image)

        # Detection: Compute connected components of the maximum values
        # in the input image and compute their center of mass
        sample_mask = image_data >= np.max(image_data)
        labels, num_labels = label(sample_mask)
        candidates = center_of_mass(
            input=sample_mask, labels=labels, index=np.arange(num_labels) + 1
        )

        # Scoring: Score each candidate cluster with the value at its center
        candidate_scores = [
            image_data[tuple(coord)]
            for coord in np.array(candidates).astype(np.uint16)
        ]

        # Serialize candidates and scores as a list of dictionary entries
        data = self._serialize_candidates(
            candidates=candidates,
            candidate_scores=candidate_scores,
            ref_image=input_image,
        )

        # Convert serialized candidates to a pandas.DataFrame
        return DataFrame(data)


if __name__ == "__main__":
    Noduledetection().process()
