# Counterexample Tests for Computational Research Evaluation

## Abstract

Evaluation software can execute successfully while computing a quantity that differs from the intended statistic. Small examples can expose such differences before a costly attempt to reproduce a complete experiment. This experience report examines four selected public research implementations using counterexamples with fully specified synthetic inputs. Two reproductions execute extracted evaluation functions; two reconstruct the relevant arithmetic or resampling procedure in NumPy. In a survival evaluator, a column-shaped time array changes a patient-level target into a two-dimensional broadcast result: both perfect and reversed predictions receive a Brier score of 0.5. In an image reconstruction evaluator, interpreting an NHWC array as NCHW changes a synthetic structural similarity score from 0.623556 to 0.822187. In a ranking evaluator, swapping two model rows reverses their reported relative score changes after model identities are restored. In a two-sample bootstrap demonstration, shared row indices produce standard errors ranging from 0.008666 to 0.159597 under different orderings of unchanged samples. The cases illustrate tests for observation identity, axis meaning, model alignment, and sampling independence. Their evidence concerns pinned code and synthetic calculations; evaluation of the original fitted models and empirical datasets remains a separate task. A reproducible supplement records the inputs, scripts, and outputs for each case.

Keywords: research software; computational reproducibility; metamorphic testing; evaluation metrics; bootstrap; array shapes

## Introduction

Research software often connects several calculations that are individually plausible. A data loader may return an array with one extra axis; an evaluation function may accept that array without rejecting it; a downstream table may then display an ordinary floating-point number. Successful execution establishes that the program completed. Establishing that the number represents the intended observation, model, or sampling distribution requires further evidence.

Complete experimental reproduction is valuable, but it can require unavailable datasets, substantial computing resources, or an old dependency stack. A smaller verification task is to identify a mathematical property that the evaluator must satisfy and construct inputs that make that property easy to check. For example, an uncensored binary prediction that exactly matches its target must have zero mean squared error. A model-specific output must retain its association with that model when the input rows are permuted. Independent samples must remain independent in the resampling procedure unless the design supplies an actual pairing.

Metamorphic testing addresses situations in which an exact expected output is difficult to obtain by checking relationships between executions. Prior work has applied this approach to scientific software [1]. The present report uses a related approach for research evaluation code and combines it with examples whose expected behavior can be calculated directly. The contribution is a documented set of four cases and a practical account of how to preserve the distinction between executable code evidence and evidence about an original study's reported results.

The cases cover survival evaluation, image reconstruction, model ranking, and two-sample resampling. They were selected from earlier code investigations because their inputs and observed outputs could be recorded compactly. This is a purposive collection of cases. It supplies examples of failure mechanisms and regression tests; it supplies no estimate of the frequency of these mechanisms in research software.

## Materials and Methods

### Case selection and evidence records

Each case identifies a public repository and a fixed commit. The examined versions are Dynamic-DeepHit at b2e208f65233405079a462b703a94556ad30d1f4 [2], DBAE at 533f5648a3a1ca419c402c656e305536267c14c8 [3], ArxivRoll at 709b0c5738b1710a4ac6988d70b32ffb1d21458b [4], and Experimental Selection Correction at a5fc1167d4c28477920d0d10b9bd35adf9e614a1 [5]. Conclusions are attached to these versions and to the particular operations described below.

The supplement contains four NumPy-based reproduction scripts and machine-readable outputs. The survival and ranking scripts retrieve pinned source files, verify their hashes, and execute the selected functions on small arrays. The image example translates the reviewed convolution and structural similarity arithmetic into NumPy. The resampling example implements a synthetic linear estimator and compares shared-index and independent-index bootstraps. These distinctions matter: running an extracted function verifies that function's behavior, whereas translating a procedure also introduces a dependency on the accuracy of the translation.

The synthetic data contain no human participant records. All reported numbers are generated by the supplied scripts. Randomized examples use recorded seeds. The bootstrap uses 600 observations in each of two independent samples and 3,000 draws. Population parameters are used only to generate the example; the numerical findings concern the finite arrays that the script actually creates.

### Specifying the expected property

The first step is to identify the entities represented by array positions. An axis can represent patients, channels, models, benchmarks, or observations from a particular sample. A test should state which transformations preserve the quantity being estimated and which transformations intentionally change it. For a model table, permuting models changes presentation order but should leave each model's result unchanged after the inverse permutation. For a two-sample estimator, independently reordering sample rows preserves the observations and the point estimate.

The second step is to choose a small input with an interpretable expected result. For a binary mean squared error, exact targets provide an oracle. For ranking, unique scores remove the ambiguity of ties. For image similarity, explicit layout conversion identifies the intended channel and spatial axes. For resampling, the observed standard error is a Monte Carlo quantity, so finite draws require an explanation of variability rather than an assertion of exact equality.

The third step is to compare the released operation with a narrowly specified alternative. The comparison may be an input normalization, an inverse permutation, a correct channel layout, or independent resampling. A changed number alone is insufficient. Its interpretation depends on whether the alternative matches the stated mathematical operation and on whether other relevant parts of the calculation remain fixed.

### Reproduction procedure

The four reproductions use NumPy and do not train models or load the original empirical datasets. Each script prints a JSON object containing its inputs or generation settings and its results. In the image example, convolution uses an 11 by 11 Gaussian window with standard deviation 1.5, zero padding, and per-channel arithmetic. In the bootstrap example, ordinary least squares estimates the coefficients in both samples, and the standard deviation across bootstrap estimates uses the sample correction with one degree of freedom.

All four scripts were rerun in isolated local executions for this report. Their outputs matched the retained numerical records exactly. The accompanying verification manifest records the runtime version, NumPy version, and script SHA-256 values. A complete original experiment would require additional data, models, and runtime checks; those are outside the executions reported here.

## Results

### Survival time arrays and observation identity

The Dynamic-DeepHit example uses two uncensored synthetic patients with survival times 1 and 3 and an evaluation horizon of 2. The event vector is one-dimensional, while the time vector is supplied first as a column array of shape (2, 1). The perfect prediction vector is (1, 0); reversing it gives (0, 1).

The examined Brier function constructs its target by multiplying the time indicator by the event vector. With shapes (2, 1) and (2,), NumPy broadcasts this operation to shape (2, 2). The subtraction of a prediction vector then compares values across the broadcast matrix rather than within each patient's intended record. Consequently, both perfect and reversed predictions receive a score of 0.5. Passing the same time values as shape (2,) produces scores of 0 and 1 respectively.

The cause-specific concordance calculation also changes under this representation choice. In the released function, an index tuple returned by a condition on a two-dimensional time array is used when selecting entries of a pairwise comparison matrix. In the supplied example, the perfect predictions receive a concordance value of 0.5 with column-shaped times and 1.0 with one-dimensional times. The patient data and predictions are unchanged.

This case supplies a regression test with an exact oracle. Input validation should check that predictions, event indicators, and survival times represent the same number of observations with the required dimensionality. A normalization rule can convert a supported column vector into a flat vector. More general multi-column inputs require explicit rejection or a documented interpretation; flattening every array would erase potentially meaningful axes.

### Image layout and the meaning of an axis

The DBAE example examines the structural similarity calculation in the reconstruction evaluator. The reviewed evaluation route supplies RGB images in NHWC layout: batch, height, width, and channel. The similarity function treats the second axis as the number of channels, consistent with NCHW layout: batch, channel, height, and width. For an input with shape (1, 128, 128, 3), this interpretation produces 128 channels and a spatial domain of 128 by 3.

The synthetic original image is generated uniformly on the unit interval. A band of rows in the comparison image is shifted along one spatial axis. Applying the reviewed similarity arithmetic directly to the NHWC arrays produces 0.8221873479020841. Transposing both arrays into NCHW layout before applying the same arithmetic produces 0.6235561674821463.

An additional check interchanges height and width. Under the intended NCHW interpretation, the score remains 0.6235561674821463 for these inputs and this isotropic window. Under the NHWC interpretation, the score becomes 0.8246057307192767. This check is specific to the symmetric window and the transformations used here; image operations with anisotropic kernels or direction-dependent processing require different expected relationships.

These values are produced by the NumPy translation of the reviewed arithmetic. As an additional check, the four pinned PyTorch SSIM functions were executed on the same four synthetic layouts using PyTorch 2.14.1+cpu. Their scores agreed with the NumPy calculations to within 1e-6; the largest absolute difference was 8.47e-8. Broader arrays and dtypes would extend this validation. Evaluation of the original reconstructed images would then be needed to quantify the effect on a reported experimental table. The present result isolates the importance of supplying the intended channel layout.

### Model order and rank alignment

The ArxivRoll example uses three models and two benchmarks with unique scores. The public score rows are A=(0.9, 0.6), B=(0.7, 0.8), and C=(0.5, 0.4). The private score rows are A=(0.5, 0.8), B=(0.9, 0.4), and C=(0.7, 0.6). Identical unmatched score matrices make the unmatched component of the relative calculation zero.

The released calculation returns relative values (0.7, -0.7, 0). Swapping only the rows for A and B in both input matrices and restoring the model names after evaluation produces (-0.7, 0.7, 0). Every model retains exactly the same benchmark scores. The signs attached to A and B nevertheless reverse.

The relevant conversion uses a sorting operation that returns model indices in score order, then handles the returned rows as though they were ranks attached to the original model identities. Reversing the second array axis changes benchmark column order and does not convert the sorted indices into ranks aligned with model identities. An evaluator that uses positional arrays needs an explicit mapping from sorted positions back to model identities.

A practical regression test should perform each chosen model permutation, apply its inverse to the model-specific output, and compare the restored result with the baseline. A production implementation must also specify score direction, treatment of ties, and missing values. The tie-free example demonstrates an alignment failure without deciding those additional policies.

### Resampling independent samples

The Experimental Selection Correction example examines a shared-index resampling procedure in the public R Markdown analysis. The investigation focuses on the resampling relationship between distinct experimental and observational samples. The accompanying synthetic example implements a linear two-sample estimator in NumPy rather than running the original R analysis.

The estimator first fits an experimental slope b from the surrogate variable regressed on treatment. It then regresses the observational outcome on treatment and on the surrogate residualized using b. Equivalently, if an observational regression on treatment and the unadjusted surrogate yields coefficients gamma_d and gamma_z, the estimate is gamma_d + b times gamma_z. This specifies the two-sample calculation implemented in the example.

The point estimate is 0.34842188382146694 in the initial order. Sorting the unchanged samples by quantities derived from their fitted influence terms gives point estimates differing only at floating-point precision. The bootstrap results are more sensitive. Shared indices give standard errors of 0.11171462028566888 in the initial order, 0.15959700583839062 with similarly ordered influence terms, and 0.008666245094473918 with oppositely ordered terms. Independent indices give 0.11178535449971456, 0.11145168119898748, and 0.11372528522867129 respectively.

Sharing an index vector across unrelated samples introduces a pairing defined by their row positions. Sorting can change that pairing while retaining the same observations. In a two-sample bootstrap for independently sampled data, the resampling distributions should preserve the sampling design [6]. Where samples contain genuine paired observations, a shared index can instead be appropriate. The research design determines the correct procedure.

The independent-index values in this experiment vary because 3,000 draws approximate a resampling distribution. Their similarity provides a numerical comparison; the structural issue is the arbitrary cross-sample coupling introduced by shared positions. Analysis of the actual experimental and observational datasets is needed before assessing the magnitude of any effect in the original empirical application.

### Summary of the executed comparisons

| Case | Synthetic comparison | Observed result | Execution type |
| --- | --- | --- | --- |
| Dynamic-DeepHit | Perfect and reversed predictions with column-shaped times | Both Brier 0.5; flat times give 0 and 1 | Extracted functions |
| DBAE | NHWC input and explicit NCHW conversion | SSIM 0.822187 and 0.623556 | NumPy arithmetic translation |
| ArxivRoll | Swap A and B, then restore model identities | Relative values change from (0.7, -0.7, 0) to (-0.7, 0.7, 0) | Extracted functions |
| Experimental Selection Correction | Reorder unchanged samples | Shared-index SE 0.008666 to 0.159597; independent-index SE 0.111452 to 0.113725 in the two sorted conditions | Synthetic NumPy estimator |

## Discussion

The cases share a useful testing principle: preserve the scientific entity while changing a representation choice. A patient remains the same patient after a supported vector conversion. An image channel remains a channel after a layout conversion. A model retains its benchmark scores after a table permutation. An independent sample retains its observations after its rows are reordered. When the reported quantity changes, the investigation can focus on the operation that has lost that identity or dependence structure.

These checks are inexpensive relative to model training and empirical reanalysis. They also offer clearer diagnoses than a large discrepancy between two complete experimental runs. A two-patient example identifies broadcasting directly. A three-model example separates model alignment from data quality and tie handling. The bootstrap example shows why row position is an inappropriate substitute for a sampling relationship in an independent-sample design.

The approach requires domain judgment. A transformation that is valid for one statistic may be invalid for another. Survival metrics may incorporate censoring weights. Image operations may be directional. Ranking systems may use explicit tie policies. Sample rows may encode meaningful pairs or clusters. A test author should derive the expected relationship from the estimator and sampling design before treating a difference as a failure.

Small examples also provide a practical basis for maintenance. Each case can become a regression test that identifies the original mechanism and checks a proposed repair. Assertions about dimensionality and entity alignment should be placed at the boundaries between loaders, evaluators, and summary tables. Resampling code should expose its sampling unit and dependence assumptions. Recording inputs, expected relationships, source versions, and execution outputs allows another reviewer to evaluate the claim independently.

The evidence remains narrower than a full reproduction. The cases were selected after discovery, so successful counterexamples cannot support an estimate of general defect prevalence. Two cases depend on translations or synthetic estimators. Original trained models, reconstructed images, and empirical records were not re-evaluated. The fixed versions may also differ from current repositories or from the exact versions used for published tables. A subsequent study could test the original frameworks, run broader input families, and reproduce the original empirical calculations. Those steps would establish how far each local mechanism propagates into a published result.

## Conclusion

Four reproducible examples show how an evaluator can retain ordinary numerical outputs while changing observation identity, axis meaning, model alignment, or sampling dependence. Tests based on exact small inputs and justified representation changes make these mechanisms visible. They are useful preliminary checks for computational reproduction and useful regression tests for evaluation software. Connecting a local mechanism to an original study's reported result requires the original evaluation path and empirical material.

## Data Accessibility

The accompanying supplement provides four NumPy-based reproduction scripts, their JSON outputs, and a verification manifest with runtime and file hashes. Each script records its source version or reviewed procedure. All experimental inputs in this report are synthetic and can be recreated from the scripts.

## References

1. Lin X, Simon M, Niu N. Exploratory Metamorphic Testing for Scientific Software. Computing in Science and Engineering. 2020;22(2):78-87. https://doi.org/10.1109/MCSE.2018.2880577

2. Dynamic-DeepHit contributors. Evaluation functions in utils_eval.py. GitHub repository chl8856/Dynamic-DeepHit; commit b2e208f65233405079a462b703a94556ad30d1f4. https://github.com/chl8856/Dynamic-DeepHit/blob/b2e208f65233405079a462b703a94556ad30d1f4/utils_eval.py

3. DBAE contributors. Reconstruction evaluation in eval_reconstruction.py. GitHub repository aailab-kaist/DBAE; commit 533f5648a3a1ca419c402c656e305536267c14c8. https://github.com/aailab-kaist/DBAE/blob/533f5648a3a1ca419c402c656e305536267c14c8/eval_reconstruction.py

4. ArxivRoll contributors. Relative ranking calculations in rs.py. GitHub repository liangzid/ArxivRoll; commit 709b0c5738b1710a4ac6988d70b32ffb1d21458b. https://github.com/liangzid/ArxivRoll/blob/709b0c5738b1710a4ac6988d70b32ffb1d21458b/rs.py

5. Experimental Selection Correction contributors. Bootstrap procedures in ESC_main_code_ext.Rmd. GitHub repository OpportunityInsights/Experimental-Selection-Correction-Replication-Code; commit a5fc1167d4c28477920d0d10b9bd35adf9e614a1. https://github.com/OpportunityInsights/Experimental-Selection-Correction-Replication-Code/blob/a5fc1167d4c28477920d0d10b9bd35adf9e614a1/code/ESC_main_code_ext.Rmd

6. Efron B. Bootstrap Methods: Another Look at the Jackknife. Annals of Statistics. 1979;7(1):1-26. https://doi.org/10.1214/aos/1176344552
