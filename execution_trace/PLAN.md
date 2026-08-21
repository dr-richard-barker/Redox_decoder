# Arabidopsis Redox-Stimulus Conditional VAE with Spaceflight Validation

## Summary

Build a conditional variational autoencoder (CVAE) that learns a generalizable redox-stimulus transcriptional latent space from a broad corpus of Arabidopsis GEO expression studies (all redox stimuli, both RNA-seq and microarray). Integrate the Salk Arabidopsis Developmental Atlas (ADA, 400k nuclei, GSE226097) as a deconvolution reference and scPlantFormer (pretrained plant single-cell foundation model) for enriched cell-type embeddings, enabling tissue- and developmental-stage-specific decomposition of bulk redox signatures. Validate the framework by projecting NASA OSDR Arabidopsis spaceflight transcriptomics data onto the redox latent space. Package everything as a deployable Streamlit web tool, a Zenodo deposition, and a full npj Microgravity manuscript (10 figures, results/supplementary tables, PDF + LaTeX).

**Sole author**: Richard Barker

---

## 1. Data Curation

### 1a. GEO Redox Corpus (Training Data)
- **Source**: NCBI GEO DataSets, user's query: `(ROS) OR (reactive oxygen) OR (H2O2) AND "Arabidopsis thaliana"[porgn:__txid3702]`
- **Current status**: 633 records retrieved and classified. 177 confirmed expression studies (84 microarray, 92 RNA-seq, 1 tiling array). 446 records with untyped `gdstype` — will re-query these via GEO accession pages to recover additional expression studies.
- **Curation scope (user decision: Broad)**: All redox stimuli (H2O2, paraquat/methyl viologen, menadione, ozone, singlet oxygen, high light, UV, heavy metals, herbicides, reductants, antioxidant mutants). Both RNA-seq and microarray platforms. All tissues. All timepoints.
- **Filtering criteria**: Keep only `gdstype` containing "Expression profiling". Exclude studies with <3 samples. Require treatment vs. control design (detectable from sample titles/series metadata). For studies without clear treatment/control, inspect series matrix headers.
- **Download method**: GEO series matrix files (`_series_matrix.txt.gz`) via FTP for microarray; processed RNA-seq count matrices via GEO supplementary files or re-quantification from SRA if needed. Use NCBI E-utilities `efetch` for series matrix retrieval.
- **Metadata extraction**: Parse each series matrix for sample annotations (GSM characteristics): stimulus type, tissue, timepoint, genotype, treatment concentration. Standardize into a unified metadata schema.
- **Output**: `/mnt/shared-workspace/shared/geo_redox_corpus/` — per-study expression matrices + unified metadata table. Checkpoint after download.

### 1b. NASA OSDR Spaceflight Data (Validation Arm)
- **Source**: NASA OSDR API (`https://osdr.nasa.gov/osdr/data/search`)
- **Current status**: 57 Arabidopsis studies found. Key transcriptomics studies identified:
  - RNA-seq: OSD-678, OSD-223, OSD-624, OSD-437, OSD-522, OSD-217, OSD-38, OSD-281, OSD-120
  - Microarray: OSD-7, OSD-205, OSD-147, OSD-44, OSD-17
- **API workflow**: 
  1. Search: `https://osdr.nasa.gov/osdr/data/search?term=Arabidopsis+spaceflight&size=200`
  2. Filter to transcriptomics (RNA-seq + microarray) studies
  3. Retrieve metadata: `https://osdr.nasa.gov/osdr/data/gds/{OSD_ID}/`
  4. Retrieve files: `https://osdr.nasa.gov/osdr/data/files/{OSD_ID}/`
  5. Download processed expression matrices (avoid raw FASTQ unless necessary)
- **Metadata extraction**: Parse OSDR ISA-Tab / SDRF metadata for: spaceflight vs. ground control, tissue, developmental stage, hardware, mission, light conditions.
- **Output**: `/mnt/shared-workspace/shared/osdr_spaceflight/` — per-study expression matrices + metadata. Checkpoint after download.

### 1c. Salk Arabidopsis Developmental Atlas (Deconvolution Reference)
- **Source**: `http://neomorph.salk.edu/ada/` (Ecker lab, Nature Plants 2025, GSE226097)
- **Data**: `.h5ad` files for 10 developmental stages: seed_0d, seed_125d, seedling_3d, seedling_6d, seedling_12d, rosette_21d, rosette_30d, stem, flower, silique. Plus MERFISH spatial datasets.
- **Download**: Direct `.h5ad` download from `http://neomorph.salk.edu:9000/view/{stage}.h5ad/`
- **Processing**: Load with scanpy/anndata in Python. Extract: gene names (AGI codes), cell-type annotations, developmental stage labels, count matrices. Build a consolidated reference AnnData with all stages merged.
- **Output**: `/mnt/shared-workspace/shared/salk_ada_reference/` — merged reference AnnData + cell-type signature matrix. Checkpoint.

### 1d. scPlantFormer (Foundation Model Embeddings)
- **Source**: scPlantFormer (pretrained on 1M Arabidopsis scRNA-seq cells, researchsquare 5219487)
- **Model weights**: Download from repository (check GitHub/HuggingFace availability)
- **Usage**: Generate cell embeddings for the ADA atlas cells. These embeddings augment the deconvolution reference by providing learned cell-type representations that capture cross-dataset biological variation.
- **Output**: `/mnt/shared-workspace/shared/scplantformer_embeddings/` — cell-level embedding matrix for ADA reference cells.

---

## 2. Preprocessing & Batch Correction

### 2a. Gene Universe Standardization
- **Target annotation**: TAIR10 / Araport11 AGI locus identifiers (e.g., AT1G01010)
- **Microarray probe mapping**: Use GPL platform annotation files from GEO to map probe IDs → AGI gene codes. Handle many-to-one (multiple probes per gene) by taking the probe with highest variance. Handle one-to-many (probe hits multiple genes) by discarding ambiguous probes.
- **RNA-seq gene IDs**: Already in AGI format in most Arabidopsis studies; verify and standardize.
- **Intersection**: Use the intersection of genes across all studies + the ADA atlas as the unified gene universe. Expected ~15,000-20,000 genes after intersection.

### 2b. Normalization
- **Microarray**: RMA-normalized values from GEO series matrix files (already log2-transformed). Quantile-normalize across studies.
- **RNA-seq**: If raw counts available → DESeq2 variance-stabilizing transformation (VST) or log1p(CPM). If only processed matrices → verify normalization state from series metadata, apply log1p if needed.
- **Cross-platform**: After gene mapping and within-platform normalization, apply ComBat (parametric) with study as the batch variable and stimulus/tissue as biological covariates to preserve.

### 2c. Batch Correction (Delegated Decision)
- **Method**: **ComBat (parametric)** for cross-study batch correction within each platform type, with stimulus type and tissue as preserved biological covariates. This is the established standard for bulk transcriptomics cross-study meta-analysis and handles the platform diversity (Agilent, Affymetrix, Illumina) in the corpus.
- **Rationale**: The corpus spans 15+ platforms, 100+ studies, and 15+ years. ComBat is specifically designed for this scenario (cross-batch correction in bulk expression data with biological covariate preservation). scVI is single-cell-oriented and requires raw counts; Harmony works on PCA embeddings but doesn't correct the expression matrix directly. ComBat gives us a corrected expression matrix that the CVAE can train on directly.
- **Cross-platform integration**: After ComBat within platform, merge RNA-seq and microarray matrices. The CVAE's conditioning on stimulus/tissue/stage provides additional disentanglement of residual platform effects. If cross-platform convergence is poor, add platform as an additional conditioning variable.
- **Validation of correction**: Check PCA before/after ComBat — verify that studies cluster by biology (stimulus/tissue) not by batch (platform/lab/year). Report kBET or silhouette scores.

---

## 3. Conditional VAE Architecture & Training

### 3a. Architecture
- **Type**: Conditional Variational Autoencoder (CVAE)
- **Encoder**: Input = gene expression vector (unified gene universe, ~15-20k genes) concatenated with conditioning variables. Architecture: 3-layer MLP encoder (genes → 1024 → 512 → 32 latent dims) with ReLU activations.
- **Latent space**: 32-dimensional, continuous. Encodes redox-stimulus transcriptional signatures.
- **Decoder**: 3-layer MLP decoder (32 + conditioning → 512 → 1024 → genes) with ReLU, output layer linear for reconstructed expression.
- **Conditioning variables** (concatenated to input and latent):
  - Stimulus type: one-hot encoded categorical (~15+ categories: H2O2, paraquat, menadione, ozone, singlet oxygen, high light, UV, heavy metal, herbicide, reductant, antioxidant mutant, etc.)
  - Tissue: one-hot encoded categorical (~8 categories: seedling, rosette/leaf, root, seed, flower, silique, stem, cell culture)
  - Developmental stage: continuous (from deconvolution proportions — see §4) or categorical (mapped to ADA atlas stages)
  - Timepoint: continuous (hours post-treatment, when available)
- **Loss**: ELBO = reconstruction loss (MSE on expression) + KL divergence (β-VAE with tunable β, start at 0.5, tune for disentanglement).
- **Implementation**: PyTorch. Model code in `/workspace/redox_cvae/model.py`.

### 3b. Training
- **Framework**: PyTorch + Lightning for training loop management.
- **Optimizer**: Adam, lr=1e-4, weight decay=1e-5.
- **Training**: 200 epochs, batch size 64, early stopping on validation reconstruction loss (patience 20).
- **GPU**: worker-0 has 1 GPU — use for training.
- **β tuning**: Sweep β ∈ {0.1, 0.5, 1.0, 2.0} on a held-out subset; select β that best disentangles stimulus from tissue in the latent space (measured by latent dimension stimulus-classifiability vs. tissue-classifiability).

### 3c. Validation: Leave-One-Study-Out Cross-Validation (User Decision)
- **Strategy**: For each of the ~200+ curated GEO studies, train the CVAE on all other studies and evaluate on the held-out study.
- **Metrics on held-out study**:
  - Reconstruction MSE (per-gene and per-sample)
  - Stimulus classification accuracy from latent (logistic regression on latent → stimulus type)
  - Latent space separation: silhouette score for stimulus clusters
  - Cross-study generalization: does the held-out study's samples cluster with the correct stimulus type in the latent space trained on the others?
- **Compute consideration**: ~200+ folds × ~15-30 min/fold on GPU = ~50-100 hours total. **Must chunk across sessions**, checkpointing after each batch of ~20 folds to `/mnt/shared-workspace/shared/cvae_loso_checkpoints/`.
- **Pilot**: First run 5 representative folds (one per major stimulus type) to validate the pipeline and estimate per-fold runtime before launching the full LOSO.

---

## 4. Deconvolution: ADA Atlas + scPlantFormer Integration

### 4a. Reference Construction
- **Primary reference**: Salk ADA atlas (400k nuclei, 10 developmental stages, cell-type annotated). Subsample to ~50k nuclei stratified by stage × cell-type for computational tractability.
- **Cell-type signature matrix**: Compute mean expression per cell-type × stage from the ADA atlas. This is the deconvolution reference matrix.
- **scPlantFormer augmentation**: Generate scPlantFormer embeddings for all ADA reference cells. Use these embeddings to:
  1. Validate/refine cell-type annotations (cluster embeddings, compare to ADA labels)
  2. Build an embedding-based cell-type signature that captures cross-dataset variation better than mean expression alone
  3. Provide an alternative deconvolution pathway: match bulk samples to scPlantFormer-embedded cell-type centroids

### 4b. Deconvolution Method (Delegated Decision)
- **Primary method**: **MuSiC** (Multi-Subject Single Cell deconvolution, R package). MuSiC handles cross-subject variation in the single-cell reference using a tree-based weighting approach, which is critical since the ADA atlas spans 10 developmental stages with inherent biological variability.
- **Secondary method**: **CIBERSORTx** (if accessible) or **SCDC** as a cross-validation deconvolution approach. Report concordance between methods.
- **scPlantFormer integration**: After MuSiC deconvolution, use scPlantFormer embeddings to validate the estimated proportions — project bulk samples into scPlantFormer embedding space and compare nearest-centroid assignments to MuSiC estimates.
- **Output per bulk sample**: Cell-type proportions (e.g., x% cortex, y% xylem, z% phloem...) + developmental stage proportions (e.g., seedling-stage signatures vs. rosette-stage signatures).

### 4c. Deconvolution Validation
- **Pseudo-bulk validation**: Create pseudo-bulk samples from ADA atlas cells with known proportions. Deconvolve and compare estimated vs. known proportions (R², RMSE).
- **Cross-platform validation**: Deconvolve GEO studies with known tissue composition and check if estimated proportions match expected tissue dominance.

---

## 5. Spaceflight Validation Analysis

### 5a. Data Preparation
- Process OSDR Arabidopsis spaceflight expression matrices through the same gene mapping, normalization, and batch correction pipeline.
- For each OSDR study: map genes to AGI codes, normalize, apply ComBat parameters fitted on the GEO corpus (transform-only mode).

### 5b. Redox Latent Space Projection
- Encode each spaceflight sample through the trained CVAE encoder (with conditioning: stimulus = "spaceflight/unknown", tissue from OSDR metadata, developmental stage from deconvolution).
- Project spaceflight samples onto the redox latent UMAP alongside GEO training samples.
- **Key analysis**: Do spaceflight samples cluster in a specific region of the redox latent space? Which ground-based redox stimulus does spaceflight most resemble?

### 5c. Tissue/Developmental Decomposition
- Deconvolve each spaceflight sample using MuSiC + ADA reference.
- Compare deconvolved tissue/developmental proportions: spaceflight vs. ground control.
- **Key analysis**: Which tissue/developmental cell types show the strongest redox signature shift under spaceflight? Are specific cell types (e.g., root tip, meristem) more redox-stressed in microgravity?

### 5d. Redox Signature Scoring
- Define a "redox signature score" from the CVAE latent: the projection onto the direction in latent space that best separates redox-stimulated from control samples in the GEO training data.
- Score each spaceflight sample: redox signature score (spaceflight vs. ground control).
- Test for statistical significance (Wilcoxon rank-sum, FDR correction).

---

## 6. Figures & Tables

### 6a. Figures (10 total, within npj Microgravity's 10 display-item limit)

| Fig | Title | Type | Tool |
|-----|-------|------|------|
| 1 | CVAE architecture and data pipeline overview | Schematic | GenerateImage |
| 2 | Redox latent space: UMAP colored by stimulus type and tissue | Data plot | Python (seaborn/matplotlib) |
| 3 | Deconvolution validation: predicted vs. known cell-type proportions | Data plot | Python (matplotlib) |
| 4 | Spaceflight projection onto the redox latent space | Data plot | Python (seaborn/matplotlib) |
| 5 | Tissue/developmental decomposition of spaceflight redox signature | Data plot | Python (matplotlib) |
| 6 | Web tool interface and workflow demonstration | Screenshot | Streamlit screenshot |
| 7 | Cross-study redox signature conservation heatmap | Data plot | Python (seaborn) |
| 8 | scPlantFormer embedding contribution to deconvolution accuracy | Data plot | Python (matplotlib) |
| 9 | Spatial ROS patterns across Arabidopsis tissues (ggPlantmap) | Spatial viz | R (ggPlantmap + ggplot2) |
| 10 | ROS synthesis pathways and cofactor visualization (ggkegg) | Pathway viz | R (ggkegg + ggplot2) |

- **Fig 1** (schematic): Architecture diagram showing data flow: GEO corpus → preprocessing → CVAE (with conditioning) → latent space; ADA atlas + scPlantFormer → deconvolution; OSDR spaceflight → projection. Must use GenerateImage.
- **Fig 9** (ggPlantmap): Use `ggPlantmap` R package (Jo & Kajala 2024, J Exp Bot) to overlay redox gene expression / redox signature scores onto pre-loaded Arabidopsis plant maps (seedling, root tip, rosette, etc.). ROI names must match between map and quantitative data.
- **Fig 10** (ggkegg): Use `ggkegg` R package (Bioconductor, Sato) to visualize KEGG ROS-related pathways (e.g., glutathione metabolism ko00480, ascorbate/aldarate metabolism ko00053, peroxisome ko04146) with expression/activity overlays. Note: user referred to this as "ggPath" — `ggkegg` is the matching grammar-of-graphics KEGG visualization package.
- **Export**: All figures as SVG (primary, per user preference) + PNG. SVG text kept editable (`svg.fonttype = 'none'` in matplotlib, `svglite::svglite()` in R).
- **Media output check**: Run `Read` with `mode='media_output_check'` on every figure after saving.

### 6b. Results Tables
- **Table R1**: CVAE LOSO cross-validation results — per-study reconstruction MSE, stimulus classification accuracy, silhouette score.
- **Table R2**: Spaceflight redox signature scores — per-OSDR-study, per-sample: redox score, tissue proportions, statistical test results.
- **Table R3**: Deconvolution validation metrics — pseudo-bulk R² and RMSE per cell type.

### 6c. Supplementary Tables
- **Table S1**: Full GEO corpus catalog — 633 records with accession, title, platform, stimulus, tissue, sample count, inclusion/exclusion status.
- **Table S2**: OSDR spaceflight study catalog — 57 Arabidopsis studies with accession, title, assay type, tissue, mission, factor.
- **Table S3**: CVAE hyperparameter sweep results — β values, latent dims, learning rates, validation metrics.
- **Table S4**: Full LOSO results — all ~200+ folds with per-fold metrics.
- **Table S5**: Cell-type signature matrix — mean expression per cell-type × developmental stage from ADA atlas.
- **Table S6**: scPlantFormer embedding validation — cell-type annotation concordance between ADA labels and scPlantFormer clustering.

---

## 7. Web Tool (Delegated Decision: Streamlit + Docker)

### 7a. Framework Choice
- **Streamlit** — provides built-in file upload, interactive widgets, and visualization components with minimal code. Single Docker image, easy to deploy to any cloud or run locally. Best balance of functionality and maintainability for this use case.

### 7b. Functionality
1. **Upload**: User uploads a count matrix (CSV/TSV/H5AD) + metadata file (CSV with columns: sample_id, stimulus, tissue, timepoint).
2. **Preprocessing**: Server-side gene mapping to AGI codes, normalization, ComBat transform (using fitted parameters from training).
3. **CVAE encoding**: Project samples into the redox latent space. Display UMAP plot with user samples overlaid on the training corpus.
4. **Deconvolution**: MuSiC deconvolution against ADA atlas. Display tissue/developmental proportion bar plots.
5. **Redox signature scoring**: Compute and display redox signature scores. Compare to spaceflight signature.
6. **Download**: User downloads results (latent coordinates, deconvolution proportions, redox scores) as CSV.
7. **Visualization**: Interactive UMAP (plotly), proportion bar plots, redox score distributions.

### 7c. Deployment
- Docker image containing: Streamlit app, trained CVAE weights (PyTorch), ADA reference matrix, ComBat fitted parameters, scPlantFormer model.
- `Dockerfile` + `docker-compose.yml` for one-command deployment.
- Model weights loaded at startup (~500MB-1GB total).

---

## 8. Zenodo Deposition

### 8a. Contents
- **Code**: Full Python/R source code (CVAE model, preprocessing pipeline, deconvolution, web tool, figure generation scripts)
- **Model weights**: Trained CVAE weights (PyTorch `.pt`), ComBat fitted parameters (R `.rds`), MuSiC reference matrix
- **Data**: Processed expression matrices (HDF5/Parquet), unified metadata tables, GEO/OSDR study catalogs
- **Figures**: All 10 figures (SVG + PNG)
- **Tables**: All results and supplementary tables (CSV/TSV)
- **Manuscript**: LaTeX source + compiled PDF
- **Documentation**: README with installation, usage, and reproduction instructions

### 8b. Metadata
- **Author**: Richard Barker (ORCID placeholder — user to provide)
- **License**: MIT (code), CC-BY 4.0 (data, figures, manuscript)
- **Title**: "Arabidopsis redox-stimulus conditional VAE with tissue-resolved spaceflight validation"
- **Description**: Brief abstract matching the manuscript abstract.
- **Keywords**: Arabidopsis, reactive oxygen species, conditional variational autoencoder, single-cell deconvolution, spaceflight, microgravity, transcriptomics

---

## 9. LaTeX Manuscript (npj Microgravity)

### 9a. Template
- Springer Nature LaTeX template (download from springernature.com/gp/authors/campaigns/latex-author-support)
- npj Microgravity formatting: Articles ≤5,000 words main text, ≤10 display items, ≤70 references, ~150-word unreferenced abstract.
- Structure: Title page → Abstract → Introduction (avoid as heading) → Results → Discussion → Methods → References → Figure Legends → Tables.

### 9b. Content Outline
- **Title**: "A conditional variational autoencoder reveals tissue-specific redox signatures in Arabidopsis spaceflight responses"
- **Abstract**: ~150 words, unreferenced.
- **Introduction**: Redox signaling in plants; limitations of bulk transcriptomics; need for tissue-resolved redox signatures; spaceflight as a redox-relevant environment.
- **Results**:
  1. CVAE learns a generalizable redox-stimulus latent space (Figs 1, 2, 7)
  2. Deconvolution with ADA atlas + scPlantFormer resolves tissue composition (Figs 3, 8)
  3. Spaceflight projects onto a distinct redox latent region (Fig 4)
  4. Tissue-specific redox signature shifts under microgravity (Fig 5, 9)
  5. ROS pathway remodeling under spaceflight (Fig 10)
  6. Web tool for community cross-referencing (Fig 6)
- **Discussion**: Generalizability of the redox latent space; tissue-specific vulnerability to microgravity redox stress; comparison to known spaceflight transcriptome signatures; tool accessibility.
- **Methods**: Data curation, preprocessing, batch correction, CVAE architecture and training, LOSO CV, deconvolution, spaceflight projection, statistical tests, web tool implementation, data availability.
- **References**: ≤70, formatted per Springer Nature style.

### 9c. Compilation
- LaTeX source in `/mnt/results/manuscript/` with `main.tex`, `references.bib`, figure includes.
- Compile to PDF with `pdflatex` + `bibtex`.
- Both `.tex` source and compiled `.pdf` in Zenodo deposition and `/mnt/results/`.

---

## 10. Compute/Resource Estimate

### 10a. Data Volume
- GEO series matrices: ~5-15 GB (200+ studies × 10-50 MB each)
- OSDR spaceflight data: ~3-8 GB (15+ transcriptomics studies)
- Salk ADA atlas: ~2-5 GB (.h5ad files for 10 stages)
- scPlantFormer model: ~200-500 MB
- **Total download**: ~15-30 GB
- **Total working disk**: ~40-60 GB (including intermediates)

### 10b. Compute Workload Classification
- **Data download/curation**: I/O bound, CPU-light. ~2-4 hours.
- **Gene mapping + normalization**: CPU-bound, parallelizable per study. ~1-2 hours.
- **ComBat batch correction**: CPU, ~30 min per platform group. ~1-2 hours total.
- **CVAE training (single fold)**: GPU, ~15-30 min per fold (estimated from ~5k-10k samples × ~20k genes, 200 epochs, early stopping).
- **LOSO CV (full)**: ~200+ folds × 20 min = ~67 hours GPU time. **Must chunk across sessions.**
- **Deconvolution (MuSiC)**: CPU, ~5-10 min per sample against 50k-cell reference. ~1-2 hours for all spaceflight samples.
- **scPlantFormer inference**: GPU, ~30 min for ADA reference cells.
- **Figure generation**: CPU/GPU, ~1-2 hours total.
- **Web tool + Zenodo + LaTeX**: CPU, ~2-4 hours.

### 10c. Execution Target
- **worker-0** (8 CPU, 32 GB, 1 GPU): Primary machine for all work. Sufficient for data curation, preprocessing, single-fold CVAE training, deconvolution, figure generation.
- **ManageMachine**: Create a second worker for parallel LOSO folds if needed (run 2 folds concurrently across 2 machines).
- **HPC tools**: Not needed — no HPC tool matches autoencoder training or MuSiC deconvolution. All compute fits in sandbox.
- **Checkpointing**: All intermediate results saved to `/mnt/shared-workspace/shared/` after each major step. LOSO fold results checkpointed after every batch of 20 folds.

### 10d. Memory Considerations
- Merged expression matrix: ~200 studies × ~5,000 samples × ~20,000 genes × 4 bytes = ~800 GB if dense. **Must use sparse matrices or process in chunks.** Use scipy.sparse for count matrices, and process ComBat per-platform-group to stay within 32 GB RAM.
- ADA atlas: 400k nuclei × 20k genes — load as sparse AnnData, subsample to 50k for deconvolution reference.
- CVAE training: batch size 64, gene vector ~20k → ~5 MB per batch. Well within GPU memory.

---

## 11. Session Sequence (Data → Model → Analysis)

### Session 1 (Current): Data Curation
1. Complete GEO corpus classification (resolve 446 untyped records)
2. Download all expression study series matrices from GEO
3. Pull OSDR Arabidopsis spaceflight transcriptomics data via API
4. Download Salk ADA atlas .h5ad files
5. Download/locate scPlantFormer model weights
6. Build unified metadata catalogs (Tables S1, S2)
7. Checkpoint all data to `/mnt/shared-workspace/shared/`

### Session 2: Preprocessing
1. Gene universe mapping (probe → AGI for all platforms)
2. Within-platform normalization
3. ComBat batch correction
4. Build merged expression matrix (sparse)
5. Prepare ADA reference for deconvolution (subsample, signature matrix)
6. Generate scPlantFormer embeddings for ADA cells
7. Pseudo-bulk deconvolution validation
8. Checkpoint processed data

### Session 3: CVAE Training + Pilot LOSO
1. Implement CVAE architecture in PyTorch
2. Hyperparameter sweep (β, latent dim)
3. Train final CVAE on full corpus
4. Run 5-fold pilot LOSO to estimate per-fold runtime
5. Begin full LOSO CV (batch 1 of ~20 folds)
6. Checkpoint model weights and fold results

### Session 4: Complete LOSO + Deconvolution
1. Complete remaining LOSO folds (batch 2-N)
2. Compile LOSO results table (Table R1, S4)
3. Run full deconvolution on GEO + OSDR samples
4. Deconvolution validation metrics (Table R3)
5. scPlantFormer embedding contribution analysis (Fig 8 data)

### Session 5: Spaceflight Analysis
1. Project OSDR spaceflight data onto redox latent space
2. Tissue/developmental decomposition of spaceflight signature
3. Redox signature scoring (spaceflight vs. ground control)
4. Statistical testing
5. Compile spaceflight results (Table R2)

### Session 6: Figures + Tables
1. Generate all 10 figures (Figs 1-10)
2. Compile all results tables (R1-R3) and supplementary tables (S1-S6)
3. Media output check on every figure
4. Save all to `/mnt/results/`

### Session 7: Web Tool
1. Build Streamlit app
2. Integrate trained CVAE + deconvolution pipeline
3. Dockerize
4. Test with example data
5. Screenshot for Fig 6

### Session 8: Zenodo + Manuscript
1. Prepare Zenodo deposition package
2. Write npj Microgravity LaTeX manuscript
3. Compile PDF
4. Final review and packaging

---

## 12. Assumptions & Delegated Decisions

### User-Confirmed Decisions
- **Scope**: Full pipeline + real results (multi-session)
- **Foundation model**: Both Salk ADA atlas (deconvolution reference) + scPlantFormer (embeddings), integrated
- **AE architecture**: Conditional VAE, conditioned on stimulus type + tissue + developmental stage + timepoint
- **Data curation**: Broad — all redox stimuli, both RNA-seq and microarray platforms
- **Scientific narrative**: General redox AE, spaceflight as validation context
- **Validation**: Leave-one-study-out cross-validation
- **Authorship**: Sole author, Richard Barker
- **Figures**: 10 figures (including ggPlantmap spatial ROS patterns and ggkegg pathway visualization)
- **Timeline**: No deadline, systematic across sessions

### Delegated Decisions (Agent, with Rationale)
- **Batch correction**: ComBat (parametric) with biological covariate preservation. Standard for bulk transcriptomics cross-platform meta-analysis. Rationale in §2c.
- **Web tool**: Streamlit + Docker. Best functionality-to-maintainability ratio for the required upload → encode → deconvolve → visualize workflow. Rationale in §7a.
- **Deconvolution**: MuSiC (primary) + SCDC/CIBERSORTx (secondary). MuSiC handles cross-subject reference variation, critical for the multi-stage ADA atlas. Rationale in §4b.
- **Gene annotation**: TAIR10/Araport11 AGI locus identifiers. Most stable and widely used; matches ADA atlas gene naming.
- **Latent dimensionality**: 32 dimensions. Standard for transcriptomic VAEs; balances expressiveness and interpretability.
- **"ggPath" → ggkegg**: No R package literally named "ggPath" exists. `ggkegg` (Bioconductor) is the grammar-of-graphics KEGG pathway visualization package matching the user's intent. Will use `ggkegg` for Fig 10.
- **scPlantFormer availability**: Model weights availability to be verified during Session 1. If unavailable, fall back to using only the ADA atlas for deconvolution and document the deviation.

### Key Assumptions
- GEO series matrix files contain sufficient metadata to classify stimulus type, tissue, and timepoint for most studies. Studies with ambiguous metadata will be inspected individually.
- OSDR processed expression matrices (not raw FASTQ) are available for most Arabidopsis transcriptomics studies, avoiding the need for re-alignment.
- The Salk ADA atlas .h5ad files are directly downloadable from the neomorph.salk.edu server.
- scPlantFormer model weights are publicly accessible. If not, the ADA atlas alone provides a sufficient deconvolution reference.
- The 32 GB RAM on worker-0 is sufficient for chunked processing (per-platform ComBat, sparse matrices, batched CVAE training).
- LOSO CV with ~200+ folds will require 3-5 sessions to complete, checkpointing every 20 folds.

---

## 13. Testing & Acceptance Criteria

- **Data curation**: ≥150 expression studies downloaded with complete metadata. All 633 GEO records classified (included/excluded with reason).
- **Preprocessing**: PCA of corrected data shows clustering by biology (stimulus/tissue), not by batch (platform/study). kBET or silhouette improvement documented.
- **CVAE**: LOSO reconstruction MSE within 1.5× of within-study reconstruction. Stimulus classification accuracy >70% on held-out studies. Latent UMAP shows stimulus-type separation.
- **Deconvolution**: Pseudo-bulk R² >0.8 for major cell types. Estimated proportions sum to ~1.0.
- **Spaceflight**: Spaceflight samples project to a distinguishable region of the redox latent space. Redox signature scores significantly different between spaceflight and ground control (FDR <0.05).
- **Web tool**: Successfully processes a test upload and returns latent scores + deconvolution proportions within 5 minutes.
- **Manuscript**: Compiles to PDF without errors. All 10 figures referenced. All tables included. Within npj Microgravity length limits (≤5,000 words, ≤10 display items, ≤70 references).
- **Zenodo**: Complete deposition package with code, models, data, figures, tables, manuscript. README with reproduction instructions.
