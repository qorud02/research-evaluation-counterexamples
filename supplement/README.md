# Counterexample Tests for Computational Research Evaluation

This supplement contains four synthetic counterexamples and their reference outputs. The fixtures cover survival-time shapes, RGB image layout, model-row ordering, and independently sampled datasets.

## Requirements

Use Python 3.12 and NumPy 2.3.5 to match the recorded environment. Install NumPy with:

```text
python -m pip install numpy==2.3.5
```

The survival and ranking scripts retrieve one source file each from a fixed GitHub commit, check its SHA-256 hash, and execute only the named evaluation functions. These two scripts require an Internet connection. The image and bootstrap scripts run locally with NumPy.

## Run the cases

Extract the ZIP into one directory, then run:

```text
python Dynamic_DeepHit_shape_reproducer.py
python DBAE_SSIM_axes_reproducer.py
python ArxivRoll_rank_reproducer.py
python ESC_independent_bootstrap_reproducer.py
```

Each command prints a JSON object. The corresponding `*_output.json` file records the reference output. The bootstrap uses two synthetic samples of 600 observations and 3,000 bootstrap draws. Its generator and resampling seeds are specified in the script.

## Comparisons

| Case | Comparison | Reference result |
| --- | --- | --- |
| Dynamic-DeepHit | Column versus flat survival-time vector | Perfect/reversed Brier scores: 0.5/0.5 versus 0/1 |
| DBAE | NHWC versus NCHW image layout | SSIM: 0.8221873479 versus 0.6235561675 |
| ArxivRoll | Model-row swap followed by restoring identities | Relative values: (0.7, -0.7, 0) versus (-0.7, 0.7, 0) |
| Experimental Selection Correction | Shared versus independent resampling indices | Shared-index SE: 0.008666 to 0.159597 across row orders |

All fixtures are synthetic. The survival and ranking cases execute functions from the pinned source; the image case implements the reviewed similarity arithmetic in NumPy; the bootstrap case uses a synthetic linear two-sample estimator.

`archive_manifest.json` records script and output hashes, the recorded runtime, and the pinned source URLs and hashes. `pinned_functions.py` performs hash-checked function extraction for the two direct-source cases.

## PyTorch comparison

`DBAE_PyTorch_crosscheck.py` compares the image fixture with the pinned original SSIM functions. It requires PyTorch and an Internet connection. The recorded check used PyTorch 2.14.1+cpu and float64 image tensors; all four layout comparisons agreed with the NumPy computation within 1e-6. The original Gaussian window is first constructed in float32 by the source function and then converted to the image dtype.

```text
python DBAE_PyTorch_crosscheck.py
```

The recorded comparison is in `DBAE_PyTorch_crosscheck.json`.

## License

The original scripts in this supplement are licensed under MIT. The externally retrieved source functions remain subject to their original repositories' terms and are executed locally from the pinned URLs. Their source text is not redistributed in this archive.
