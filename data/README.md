# Data

Data was generated using the scripts in `/src`

Each sample has the following format:
```
{
  "att" : [ra, de, roll],
  "centroids" : [(x_i, y_i) for i in [N]],
  "stars" : [id_i for i in [N]],
  "mags" : [mag_i for i in [N]],
}

N = number of stars in the scene
```
- att = attitude of the star scene
- centroids = list of `[x, y]` coordinates for each star appearing in the scene
- stars = list of YBSC ids representing stars appearing in the scene, where star `stars[i]` has coordinates `centroids[i]`
- mags = list of YBSC recorded magnitudes, where star `stars[i]` has magnitude `mags[i]`

Example:
```
{
  "att": [0, 1, 0],
  "centroids": [[495.8049996459742, 203.77146541957825], [458.2948875714152, 56.62367534438502], [436.6387296386091, 217.3896789307384], [391.27215859842755, 146.44763727112547], [375.3885545578658, 406.54684465341927], [359.4653226253997, 246.79301843426262], [333.3641044152597, 169.76087727208306], [323.5162950197076, 422.8805278842765], [304.2265165931408, 286.9840634848685], [263.7861116261901, 439.5456788116458], [257.13002579963705, 5.733590384410377], [231.05566493930445, 417.4785461681713]],
  "stars": [8954, 8969, 8984, 9004, 9012, 9022, 9033, 9041, 9047, 9067, 9072, 9087],
  "mags": [5.68, 4.13, 4.5, 5.04, 5.49, 5.77, 5.55, 5.93, 5.61, 4.86, 4.01, 5.1]
}
```


Due to GitHub storage limits, data can be found in this [Google Drive](https://drive.google.com/drive/folders/15cAWefx6grDIfZjXOpS9bWfITwqcEcq0?usp=drive_link)