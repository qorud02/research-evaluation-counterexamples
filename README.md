# Counterexample Tests for Computational Research Evaluation

Three implementation counterexamples examine patient targets, image channel layout and model-aligned ranks. The Letter connects fixtures to released callers and provides repair comparisons with positive controls.

- [Letter PDF](Counterexample_Tests_Letter.pdf)
- [Letter source](letter.md)
- [Metadata](metadata.yaml)
- [Reproducibility archive](reproducibility_archive.zip)
- [Repair comparisons and caller evidence](supplement/repair_comparisons/README.md)
- [Extended four-case account](extended_report.md)
- [Submission and review](https://github.com/ReScience/submissions/issues/137)

The archive retains the original fixture suite and adds 24 designed uncensored Brier comparisons and all six row permutations of the three-model ranking fixture. The original PyTorch/NumPy SSIM cross-check is included. A separate two-sample resampling illustration reconstructs a simplified synthetic estimator and is distinguished from the three implementation cases.

Use Python 3.12 and NumPy 2.3.5. The optional image cross-check uses PyTorch. Pinned-source runners require internet access and verify SHA-256 before extracting functions. Original source files are not redistributed. Expected relations apply to the stated input contracts, including all-event-one survival fixtures and tie-free higher-is-better rankings. Original empirical tables were not recalculated.

Original fixture and loader code: MIT. Manuscript and extended report: CC BY 4.0. Retrieved upstream functions remain subject to their original terms. Source versions and hashes are recorded in the archives.

The original submission remains available at commit 85deb605936e7e4c22021db47a7622b99545e8b8. This repository records the revision as a later commit on the same submission.
