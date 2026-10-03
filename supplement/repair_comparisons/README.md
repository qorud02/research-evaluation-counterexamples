# Repair comparisons and caller contracts

These files accompany the three implementation counterexamples in the Letter.

Run with Python 3.12 and NumPy 2.3.5:

    python deephit_uncensored_shape_controls.py
    python arxivroll_permutation_repair_compare.py

Both scripts download and SHA-256-check one pinned source file before extracting functions. They require internet access on execution. The source files are not redistributed. The first writes a JSON result beside the script; the second prints JSON. The recorded ranking experiment executed locally retained source functions whose LF-normalized bytes match the pinned source, and retains both hashes as provenance.

The survival comparison covers 24 designed uncensored one-event conditions and two rejected input contracts. Four sample sizes, two integer horizons and three prediction types provide the grid. For n=2, the horizons induce the same target split. The released column-input score differs from the patient-paired mean-squared-error oracle in 16 conditions; the single-column normalization agrees in all 24. All eight constant-prediction controls agree, and the two unsupported contracts are rejected. For all event indicators equal to one, broadcast minus paired Brier equals twice the population covariance of prediction and target. Censoring/IPCW and original empirical tables require separate validation.

The ranking comparison covers all six permutations of one three-model tie-free fixture. Five original outputs differ from baseline after restoring model identities. Replacing the rank helper with model-aligned descending ranks, preserving benchmark order, gives agreement in all six. Ties, missing scores, mixed score directions and the original paper score matrices require separate policies or data.

The source-contract JSON provides pinned URLs, hashes and line ranges for the actual loaders and callers. Original source excerpts and personal workspace paths are excluded; the linked original files supply the code context.
