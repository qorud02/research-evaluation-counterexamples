# Counterexample Tests for Computational Research Evaluation

Four synthetic counterexamples test observation identity, image-axis meaning, model alignment, and sampling independence in public computational research evaluation code.

Author: Kyunghan Bae, UNICUP COMPANY, Republic of Korea. Correspondence: ceo@unicupcompany.com.

## Manuscript and submission material

- [Letter PDF](Counterexample_Tests_Letter.pdf)
- [Letter source](letter.md)
- [Author metadata](metadata.yaml)
- [Cover letter](Cover_Letter_ReScience_C.pdf)
- [Author information](Author_Information.pdf)
- [Extended report](extended_report.md)
- [Reproducibility archive](reproducibility_archive.zip)

## Run the comparisons

See [supplement instructions](supplement/README.md). The four principal comparisons use Python and NumPy. An additional original-function comparison uses PyTorch.

All inputs are synthetic. The source-download runners check fixed source hashes before extracting the evaluation functions. The image comparison was cross-checked against the pinned PyTorch functions; the maximum absolute difference was 8.47e-8.

## License

The original Python scripts are licensed under MIT. The manuscript and extended report use CC BY 4.0. Retrieved third-party source files retain their original terms.
