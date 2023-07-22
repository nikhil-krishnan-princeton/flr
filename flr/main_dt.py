"""

"""
import os
import pickle
import warnings

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from utils import load_credit_risk, evaluate

# ignore some warnings, especially for lbgfs optimization
warnings.filterwarnings('ignore')

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--n_repeats", type=int, default=2)  # number of repeats of the experiments
args = parser.parse_args()
print(args)
N_REPEATS = args.n_repeats


def single_main(random_state=42):
    (X_train, y_train), (X_test, y_test) = load_credit_risk(random_state=random_state)
    is_normalization = True
    if is_normalization:
        std = StandardScaler()
        std.fit(X_train)
        X_train = std.transform(X_train)
        X_test = std.transform(X_test)

    model = DecisionTreeClassifier(random_state=random_state)
    model.fit(X_train, y_train)

    scores = evaluate(model, X_test, y_test)
    params = {'feature_importances_': model.feature_importances_}
    history = {'scores': scores, 'params': params}

    return history


def main():
    history = {}
    for i in range(N_REPEATS):
        random_state = i * 100
        his = single_main(random_state=random_state)
        # print(i, his)
        history[i] = his

    out_f = f'out/DT-R_{N_REPEATS}.dat'
    os.makedirs(os.path.dirname(out_f), exist_ok=True)
    with open(out_f, 'wb') as f:
        pickle.dump(history, f)

    # format results
    with open(out_f, 'rb') as f:
        history = pickle.load(f)

    for metric in ['loss', 'accuracy']:
        scores = []
        parmas = []
        for i_repeat, his in history.items():
            scores.append(his['scores'][metric])
            parmas.append(his['params'])
            print(f'i_repeat:{i_repeat}, {metric}:', scores[-1], parmas[-1])
        print('DT:', metric, np.mean(scores), np.std(scores), scores)


if __name__ == '__main__':
    main()
