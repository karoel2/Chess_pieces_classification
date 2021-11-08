#Chess_pieces_classification

Bachelor project focused on teaching and analyzing chess.

<i>This repository only contain neural network and data generators. For Chess Tutor app check: https://github.com/Kacper777777/Chess-Tutor</i>

One of its functionality is to recreate a chess state from a screenshot. It is done in three steps. Firstly data is preprocessed, then the screenshot is passed to first CNN to localize the chessboard. Then each cell of the original chessboard is forwarded to second CNN for multilabel object classification. 

Generating images of a chessboard in a random state on a random website from dataser page for training CNN. Require downloading WebScreenshots Kaggle dataset: https://www.kaggle.com/ds/202248.
