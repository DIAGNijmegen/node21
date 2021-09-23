from evalutils import DetectionEvaluation
from evalutils.validators import ExpectedColumnNamesValidator
from jsonloader import NODE21Loader
import json
from sklearn.metrics import roc_auc_score

class Evaluation_detection(DetectionEvaluation):
    def __init__(self):
        super().__init__(
            file_loader=NODE21Loader(),
            validators=(
                ExpectedColumnNamesValidator(
                    expected=("name", "slice", "probability", "x_min", "y_min", "x_max", "y_max")
                ),
            ),
            join_key="name",
            detection_radius=1.0,
            detection_threshold=0.5,
           
        )
        
    def get_points(self, *, case, key):
        """
        Converts the set of ground truth or predictions for this case, into
        points that represent true positives or predictions
        """
        all_points = []
        
        try:
            points = case.loc[key]
        except KeyError:
            # There are no ground truth/prediction points for this case
            return []
        
        slice_group = points.groupby('slice')
        
        for name, group in slice_group:
            max_score = -1
            for _, p in group.iterrows():
                if p["probability"] > max_score:
                    max_score = p["probability"]
                    all_points.append((max_score, p["slice"]))
        return all_points


    def score_aggregates(self):
        all_points_gt = []
        all_points_pred = []
        
        preds = self._cases.loc['predictions']
        name_group =self._cases.loc['ground_truth'].groupby('name')
        for j, i in name_group:
            pred_group = preds[preds['name']==str(j)]
            slices = i.groupby('slice')
            for l,m in slices:
                slice_group = pred_group[pred_group['slice']==int(l)]
                if len(slice_group)<1:
                    #print('adding 0 prediction for the slice ', l)
                    all_points_pred.append((0, l))
                else:
                    all_points_pred.append((max(slice_group["probability"]), l))
                max_score = -1
                for _, p in m.iterrows():
                    if p["probability"] > max_score:
                        max_score = p["probability"]
                        all_points_gt.append((max_score, p["slice"]))
                        
       
        auc_prob_node = roc_auc_score([i[0] for i in all_points_gt], [i[0] for i in all_points_pred])
              
        return {
            "AUC": auc_prob_node,
        }

if __name__ == "__main__":
    Evaluation_detection().evaluate()

    
    