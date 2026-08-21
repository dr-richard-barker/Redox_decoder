# Arabidopsis Redox Transcriptional Autoencoder and Spaceflight ROS Validation

**Author:** Richard Barker<sup>1,*</sup>  
<sup>1</sup>Department of Agricultural and Biological Engineering, Purdue University, West Lafayette, IN, USA  
<sup>*</sup>Correspondence: dr-richard-barker

---

## Abstract

Reactive oxygen species (ROS) serve as central secondary messengers in plant stress signaling, yet resolving ROS-specific transcriptional networks from confounding developmental and organ-level variations remains a key challenge. We built a **Conditional Variational Autoencoder (CVAE)** framework trained on 232 harmonized *Arabidopsis thaliana* transcriptomic studies comprising 4,332 samples across 20,869 TAIR10 AGI genes. Integrating single-cell reference deconvolution from the Salk Arabidopsis Developmental Atlas (ADA, 29,993 cells) allowed cell-type aware disentanglement of redox signatures. We evaluated three CVAE architectures (33-dim baseline, 37-dim time-aware, and 41-dim developmental stage conditioned) using rigorous Leave-One-Study-Out (LOSO) cross-validation. Projecting 879 spaceflight samples from 38 NASA Open Science Data Repository (OSDR) studies onto the redox latent space demonstrates significant spaceflight-induced ROS signature shifts ($p = 2.11 \times 10^{-66}$), with primary localization to root epidermal and vascular tissue layers.

---

## 1. Introduction

Plants constantly integrate environmental inputs through reactive oxygen species (ROS) cascades, including hydrogen peroxide ($H_2O_2$), superoxide ($O_2^{\bullet-}$), and singlet oxygen ($^1O_2$). In spaceflight microgravity, physical stress triggers systemic ROS accumulation. However, cross-study analysis across heterogeneous hardware, light regimes, and growth stages requires robust batch correction and latent disentanglement.

---

## 2. Results

### 2.1 CVAE Latent Disentanglement of GEO Redox Corpus
Training the 32-dimensional continuous CVAE on 4,332 samples across 15 redox stimulus categories yielded clear latent space clustering by stimulus class while controlling for tissue composition.

### 2.2 Model Architecture Benchmark & LOSO Validation
Across 232 leave-one-study-out folds, the 41-dim DevStage conditioned CVAE achieved the highest generalizability and stimulus classification accuracy:
- **Original 33-dim Baseline**: Validation loss = 3860.9, LOSO MSE = 0.1824, Stimulus accuracy = 78.4%.
- **Time-Aware 37-dim CVAE**: Validation loss = 4095.4, LOSO MSE = 0.1745, Stimulus accuracy = 82.1%.
- **DevStage 41-dim CVAE**: Validation loss = 4206.9, LOSO MSE = 0.1691, Stimulus accuracy = 85.6%.

### 2.3 OSDR Spaceflight ROS Shift Validation
Spaceflight samples exhibited marked elevation in CVAE reconstruction error (mean SF error = 0.2736 vs ground = 0.1313, $p = 2.11 \times 10^{-66}$), confirming substantial ROS transcriptional perturbation during orbital flight. Latent Dim 1 showed strong discrimination between spaceflight and ground control samples ($t = -13.23, p = 3.33 \times 10^{-39}$).

### 2.4 Decoded Spaceflight Case Studies (What, When, and Where)
To demonstrate the translational utility of the CVAE and multi-view ggPlantMap framework, we decoded four representative NASA OSDR experiments (**Figure 11**):
1. **OSD-678 (Root Flight)**: Predicted an acute primary root oxidative burst ($42\%\text{ }H_2O_2, 38\%\text{ }O_2^{\bullet-}$), estimated at $<1.2\text{ hours}$ post-induction, localized to the root apical meristem and central vascular stele.
2. **OSD-223 (Rosette Leaf Flight)**: Predicted chloroplastic photo-oxidative stress ($48\%\text{ High Light}, 26\%\text{ }^1O_2$), estimated at $\sim 16.5\text{ hours}$ (chronic acclimation), localized to palisade and spongy mesophyll layers.
3. **OSD-624 (Root Hypoxia-ROS Cross-talk)**: Predicted mitochondrial superoxide retrograde signaling ($45\%\text{ }O_2^{\bullet-}, 32\%\text{ }H_2O_2$), estimated at $\sim 6.0\text{ hours}$, localized to the central stele and endodermis.
4. **OSD-38 (Whole Seedling Flight)**: Predicted systemic oxidative response ($35\%\text{ }H_2O_2, 28\%\text{ }O_2^{\bullet-}$), estimated at $\sim 3.8\text{ hours}$, spanning cotyledons, hypocotyl, and root tissues.

---

## 3. Discussion & Conclusion

The CVAE framework provides a generalizable, interpretable latent model of plant redox biology. Coupled with single-cell deconvolution and ggPlantMap spatial mapping, it resolves organ- and cell-type specific ROS dynamics during spaceflight.

---

## References

1. Ecker, J. R. et al. Single-cell developmental atlas of *Arabidopsis thaliana*. *Nature Plants* 11, 204–218 (2025).
2. Barker, R. et al. OSDR Plant Spaceflight Omics Database. *npj Microgravity* 9, 45 (2023).
