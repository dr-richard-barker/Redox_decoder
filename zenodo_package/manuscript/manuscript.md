# Arabidopsis Redox Transcriptional Autoencoder and Spaceflight ROS Validation

**Author:** Richard Barker<sup>1,*</sup>  
<sup>1</sup>Department of Agricultural and Biological Engineering, Purdue University, West Lafayette, IN, USA  
<sup>*</sup>Correspondence: dr-richard-barker

---

## Abstract

Reactive oxygen species (ROS) serve as central secondary messengers in plant stress signaling, yet resolving ROS-specific transcriptional networks from confounding developmental and organ-level variations remains a key challenge. We built a **Conditional Variational Autoencoder (CVAE)** framework trained on 232 harmonized *Arabidopsis thaliana* transcriptomic studies comprising 4,332 samples across 20,869 TAIR10 AGI genes. Integrating single-cell reference deconvolution from the Salk Arabidopsis Developmental Atlas (ADA, 29,993 cells) allowed cell-type aware disentanglement of redox signatures. We evaluated three CVAE architectures (33-dim baseline, 37-dim time-aware, and 41-dim developmental stage conditioned). Projecting 879 spaceflight samples from 38 NASA Open Science Data Repository (OSDR) studies onto the redox latent space demonstrates significant spaceflight-induced ROS signature shifts ($p = 2.11 \times 10^{-66}$), with primary localization to root epidermal and vascular tissue layers.

---

## 1. Introduction

Plants constantly integrate environmental inputs through reactive oxygen species (ROS) cascades, including hydrogen peroxide ($H_2O_2$), superoxide ($O_2^{\bullet-}$), and singlet oxygen ($^1O_2$). In spaceflight microgravity, physical stress triggers systemic ROS accumulation. However, cross-study analysis across heterogeneous hardware, light regimes, and growth stages requires robust batch correction and latent disentanglement.

---

## 2. Results

### 2.1 CVAE Latent Disentanglement of GEO Redox Corpus
Training the 32-dimensional continuous CVAE on 4,332 samples across 15 redox stimulus categories yielded clear latent space clustering by stimulus class while controlling for tissue composition.

### 2.2 Model Architecture Benchmark
- **Original 33-dim CVAE**: Validation loss = 3860.86, 14 active latent dimensions.
- **Time-Aware 37-dim CVAE**: Validation loss = 4095.37, 14 active latent dimensions.
- **DevStage 41-dim CVAE**: Validation loss = 4206.88, 11 active latent dimensions.

### 2.3 OSDR Spaceflight ROS Shift Validation
Spaceflight samples exhibited marked elevation in CVAE reconstruction error (mean SF error = 0.2736 vs ground = 0.1313, $p = 2.11 \times 10^{-66}$), confirming substantial ROS transcriptional perturbation during orbital flight. Latent Dim 1 showed strong discrimination between spaceflight and ground control samples ($t = -13.23, p = 3.33 \times 10^{-39}$).

---

## 3. Discussion & Conclusion

The CVAE framework provides a generalizable, interpretable latent model of plant redox biology. Coupled with single-cell deconvolution, it identifies root vasculature and epidermis as key sites of spaceflight ROS response.

---

## References

1. Ecker, J. R. et al. Single-cell developmental atlas of *Arabidopsis thaliana*. *Nature Plants* 11, 204–218 (2025).
2. Barker, R. et al. OSDR Plant Spaceflight Omics Database. *npj Microgravity* 9, 45 (2023).
