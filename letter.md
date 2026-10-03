# Counterexample Tests for Computational Research Evaluation

## Abstract

Small counterexamples can expose an evaluation error before a complete computational reproduction. This letter presents four selected examples involving survival metrics, image similarity, model ranking, and two-sample resampling. Synthetic inputs isolate changes in observation identity, axis meaning, model alignment, and sampling independence. The accompanying scripts record source versions, inputs, and numerical outputs so that each local claim can be checked separately from the original study.

## Small tests before complete reproduction

An evaluator can finish successfully while calculating a quantity different from the intended statistic. Small examples provide a preliminary check: state a property required by the estimator, choose interpretable inputs, and test whether a representation change preserves the scientific entity. Metamorphic testing has been applied to scientific software [1]. The four cases below combine such relationships with direct numerical comparisons.

The selected cases concern fixed versions of Dynamic-DeepHit [2], DBAE [3], ArxivRoll [4], and Experimental Selection Correction [5]. All inputs are synthetic. Two scripts retrieve pinned sources, verify their hashes, and execute selected functions. The image and resampling examples implement the reviewed arithmetic or a synthetic estimator in NumPy. The supplement supplies exact inputs, source versions, execution types, outputs, and runtime information.

## Four evaluation checks

Observation identity matters in survival evaluation. For two uncensored patients with times 1 and 3, event indicators (1, 1), and horizon 2, the perfect prediction is (1, 0). The examined Dynamic-DeepHit Brier function multiplies a time array of shape (2, 1) by an event vector of shape (2,), broadcasting the target to shape (2, 2). Perfect and reversed predictions both score 0.5. Flat times give scores 0 and 1 and change the perfect prediction's cause-specific concordance from 0.5 to 1. Validation should establish supported dimensionality and consistent observation counts.

Axis meaning matters in image similarity. The examined DBAE evaluation route supplies images in NHWC layout, while its similarity calculation interprets them as NCHW. A synthetic RGB array of shape (1, 128, 128, 3) is consequently treated as 128 channels over a spatial domain of 128 by 3. The NumPy comparison uses an isotropic 11 by 11 Gaussian window with standard deviation 1.5. It gives a structural similarity score of 0.822187 for that interpretation and 0.623556 after explicit conversion to NCHW. Interchanging height and width gives 0.824606 in the former calculation and leaves the latter unchanged. The four pinned PyTorch functions were also executed on these layouts using PyTorch 2.14.1+cpu; their scores agreed with NumPy to within 1e-6, with maximum absolute difference 8.47e-8. The expected symmetry follows from this window and fixture; directional image operations need a different test.

Model alignment matters in ranking. With three models and two benchmarks with distinct scores, ArxivRoll gives relative outputs (0.7, -0.7, 0). Swapping the first two models in both input matrices and restoring identities in the output gives (-0.7, 0.7, 0), although every model retains its scores. The calculation treats indices returned in score order as ranks attached to original model positions. An inverse-permutation test exposes the misalignment. Score direction, ties, and missing values require explicit policies.

Sampling independence matters in a two-sample bootstrap. The Experimental Selection Correction example examines shared row indices across distinct experimental and observational samples. A synthetic estimator first fits an experimental slope b for the surrogate regressed on treatment, then an observational outcome regression on treatment and the surrogate residualized using b. Equivalently, its estimate is gamma_d + b times gamma_z, where the gamma coefficients come from the observational regression on treatment and the unadjusted surrogate.

With 600 observations in each sample and 3,000 bootstrap draws, the point estimate is 0.348422. Reordering the unchanged samples leaves that estimate unchanged up to floating-point precision. Shared-index bootstrap standard errors are 0.111715 in the initial ordering, 0.159597 with similarly ordered fitted influence terms, and 0.008666 with oppositely ordered terms. Independent indices give 0.111785, 0.111452, and 0.113725. Independent sampling calls for independent resampling [6]; genuine paired observations can justify shared indices. The relevant test follows the sampling design. Monte Carlo variation explains differences between the independently resampled finite estimates.

## Implications for reproduction

The tests preserve patients under supported vector conversion, channels under layout conversion, model identities under permutation, and independent samples under separate row reorderings. Expected relationships follow the statistic: censoring weights, anisotropic image operations, ranking policies, clusters, and genuine pairs can change which transformations are valid.

Each example supplies a regression test with a recorded source version, expected relationship, and output. The executions establish local function or synthetic-procedure behavior. Estimating effects on published tables requires original models, empirical records, and evaluation paths. Broader inputs would extend the evidence. This purposive collection illustrates failure mechanisms; a prevalence estimate requires a separate sampling design.

## Code and data

The supplement contains executable scripts, source hashes, recorded outputs, and an extended account of the four comparisons. All experimental inputs can be regenerated. The code and manuscript are available at https://github.com/qorud02/research-evaluation-counterexamples.

## References

1. Lin X, Simon M, Niu N. Exploratory Metamorphic Testing for Scientific Software. Computing in Science and Engineering. 2020;22(2):78–87. https://doi.org/10.1109/MCSE.2018.2880577

2. Dynamic-DeepHit contributors. utils_eval.py. Commit b2e208f65233405079a462b703a94556ad30d1f4. https://github.com/chl8856/Dynamic-DeepHit/blob/b2e208f65233405079a462b703a94556ad30d1f4/utils_eval.py

3. DBAE contributors. eval_reconstruction.py. Commit 533f5648a3a1ca419c402c656e305536267c14c8. https://github.com/aailab-kaist/DBAE/blob/533f5648a3a1ca419c402c656e305536267c14c8/eval_reconstruction.py

4. ArxivRoll contributors. rs.py. Commit 709b0c5738b1710a4ac6988d70b32ffb1d21458b. https://github.com/liangzid/ArxivRoll/blob/709b0c5738b1710a4ac6988d70b32ffb1d21458b/rs.py

5. Experimental Selection Correction contributors. ESC_main_code_ext.Rmd. Commit a5fc1167d4c28477920d0d10b9bd35adf9e614a1. https://github.com/OpportunityInsights/Experimental-Selection-Correction-Replication-Code/blob/a5fc1167d4c28477920d0d10b9bd35adf9e614a1/code/ESC_main_code_ext.Rmd

6. Efron B. Bootstrap Methods: Another Look at the Jackknife. Annals of Statistics. 1979;7(1):1–26. https://doi.org/10.1214/aos/1176344552
