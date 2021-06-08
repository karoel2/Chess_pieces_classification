# Chessboard-localization

Bachelor project focused on teaching and analyzing chess. 
One of its functionality is to recreate a chess state from a screenshot. It is done in three steps. Firstly data is processed, converted to greyscale and highlighted edges with the use of filters. Nextly the screenshot is passed to CNN to localize the chessboard. Then each cell of the original chessboard is forwarded to another CNN for multilabel object classification. 

Generating images of a chessboard in a random state on a random website page for training CNN. Require downloading WebScreenshots Kaggle dataset: https://www.kaggle.com/ds/202248.
Samples with standarized labels (class | center of object X | center of object Y | size | size)

0  0.233  0.638  0.45  0.72| 0  0.456  0.38  0.288  0.462
:-------------------------:|:-------------------------: 
![0](https://user-images.githubusercontent.com/25713523/121088066-7f2c9b00-c7e5-11eb-9692-90eb15793cc5.png)|![1](https://user-images.githubusercontent.com/25713523/121088069-7fc53180-c7e5-11eb-8b85-9bbd9c26aa5a.png)
0  0.493  0.513  0.45  0.72 | 0  0.386  0.378  0.472  0.755
![2](https://user-images.githubusercontent.com/25713523/121088071-805dc800-c7e5-11eb-97f5-f9b46fb192df.png)|![3](https://user-images.githubusercontent.com/25713523/121088073-805dc800-c7e5-11eb-8bf0-6824ab30a7f3.png)
