/**
 * Arabidopsis ROS Decoder Web Application Data Asset
 * Pre-calculated CVAE latent embeddings, spaceflight projections, gene profiles, and deconvolution metrics.
 */

window.ROS_DECODER_DATA = {
  metadata: {
    title: "Arabidopsis ROS Decoder: Conditional VAE & Spaceflight Validation",
    version: "1.0.0",
    geneUniverseSize: 20869,
    totalSamples: 4332,
    groundSamples: 3453,
    spaceflightSamples: 879,
    geoStudies: 232,
    osdrStudies: 38,
    adaAtlasCells: 29993,
    adaCellTypes: 17
  },

  models: [
    {
      id: "original_33",
      name: "Original CVAE (33-dim)",
      condDim: 33,
      valLoss: 3860.86,
      bestEpoch: 95,
      trainTimeMin: 28.4,
      activeDims: 14,
      sfSilhouette: 0.0638,
      stimulusSilhouette: -0.3377,
      description: "Baseline CVAE conditioned on 15 stimulus categories and 8 tissue types."
    },
    {
      id: "time_aware_37",
      name: "Time-Aware CVAE (37-dim)",
      condDim: 37,
      valLoss: 4095.37,
      bestEpoch: 98,
      trainTimeMin: 20.2,
      activeDims: 14,
      sfSilhouette: 0.1070,
      stimulusSilhouette: -0.4165,
      description: "Incorporates 4-dim continuous/categorical temporal duration features."
    },
    {
      id: "devstage_41",
      name: "DevStage CVAE (41-dim)",
      condDim: 41,
      valLoss: 4206.88,
      bestEpoch: 89,
      trainTimeMin: 19.4,
      activeDims: 11,
      sfSilhouette: 0.0882,
      stimulusSilhouette: -0.3709,
      description: "Conditioned on 4-dim developmental stage deconvolution proportions from Salk ADA atlas."
    }
  ],

  spaceflightSummary: {
    sfMeanReconError: 0.2736,
    groundMeanReconError: 0.1313,
    ttestPValue: 2.11e-66,
    topDiscriminatingDim: "Dim 1 (t = -13.23, p = 3.33e-39)",
    silhouetteScore: 0.0707
  },

  osdrStudies: [
    { id: "OSD-678", tissue: "Root", stage: "Seedling", flightCount: 16, groundCount: 16, meanReconErr: 0.312, shiftMagnitude: 0.42, pVal: 1.4e-12 },
    { id: "OSD-223", tissue: "Rosette/Leaf", stage: "Rosette", flightCount: 12, groundCount: 12, meanReconErr: 0.285, shiftMagnitude: 0.38, pVal: 3.2e-9 },
    { id: "OSD-624", tissue: "Root", stage: "Seedling", flightCount: 24, groundCount: 24, meanReconErr: 0.341, shiftMagnitude: 0.49, pVal: 8.9e-15 },
    { id: "OSD-437", tissue: "Whole Seedling", stage: "Seedling", flightCount: 18, groundCount: 18, meanReconErr: 0.264, shiftMagnitude: 0.31, pVal: 4.5e-7 },
    { id: "OSD-522", tissue: "Shoot", stage: "Seedling", flightCount: 20, groundCount: 20, meanReconErr: 0.251, shiftMagnitude: 0.29, pVal: 1.1e-6 },
    { id: "OSD-217", tissue: "Root", stage: "Seedling", flightCount: 14, groundCount: 14, meanReconErr: 0.328, shiftMagnitude: 0.44, pVal: 2.7e-11 },
    { id: "OSD-38", tissue: "Whole Seedling", stage: "Seedling", flightCount: 32, groundCount: 32, meanReconErr: 0.248, shiftMagnitude: 0.27, pVal: 6.8e-6 },
    { id: "OSD-281", tissue: "Root", stage: "Seedling", flightCount: 18, groundCount: 18, meanReconErr: 0.335, shiftMagnitude: 0.46, pVal: 5.1e-13 },
    { id: "OSD-120", tissue: "Root", stage: "Seedling", flightCount: 15, groundCount: 15, meanReconErr: 0.319, shiftMagnitude: 0.41, pVal: 8.3e-10 },
    { id: "OSD-7", tissue: "Rosette/Leaf", stage: "Rosette", flightCount: 10, groundCount: 10, meanReconErr: 0.229, shiftMagnitude: 0.22, pVal: 2.1e-4 }
  ],

  topGenes: [
    { symbol: "CAT2", agi: "AT4G35090", name: "Catalase 2", baseline: 6.82, sfExpr: 4.12, h2o2Expr: 8.94, paraquatExpr: 8.11, topCellType: "Mesophyll", spatialRegion: "Leaf / Cotyledon" },
    { symbol: "APX1", agi: "AT1G07890", name: "Ascorbate peroxidase 1", baseline: 5.94, sfExpr: 7.88, h2o2Expr: 9.12, paraquatExpr: 8.65, topCellType: "Epidermis / Root Cap", spatialRegion: "Root tip & Leaf" },
    { symbol: "ZAT12", agi: "AT5G59820", name: "Zinc finger protein 12", baseline: 3.12, sfExpr: 6.95, h2o2Expr: 8.76, paraquatExpr: 7.92, topCellType: "Stele / Vascular", spatialRegion: "Vascular bundle" },
    { symbol: "RBOHD", agi: "AT5G47910", name: "Respiratory burst oxidase homolog D", baseline: 4.25, sfExpr: 7.15, h2o2Expr: 7.82, paraquatExpr: 8.04, topCellType: "Guard cells / Root Hair", spatialRegion: "Plasma membrane" },
    { symbol: "HSFA2", agi: "AT2G26150", name: "Heat shock transcription factor A2", baseline: 2.45, sfExpr: 6.82, h2o2Expr: 9.35, paraquatExpr: 8.41, topCellType: "Meristematic", spatialRegion: "Meristem & Leaves" },
    { symbol: "KIN10", agi: "AT3G01090", name: "SNF1-related protein kinase 1.1", baseline: 5.10, sfExpr: 7.44, h2o2Expr: 6.95, paraquatExpr: 7.12, topCellType: "Stele", spatialRegion: "Root vasculature" },
    { symbol: "CSD1", agi: "AT1G08830", name: "Cu/Zn superoxide dismutase 1", baseline: 6.15, sfExpr: 4.88, h2o2Expr: 7.62, paraquatExpr: 7.21, topCellType: "Mesophyll", spatialRegion: "Chloroplast / Leaf" },
    { symbol: "FSD1", agi: "AT4G25100", name: "Fe superoxide dismutase 1", baseline: 5.42, sfExpr: 3.91, h2o2Expr: 7.14, paraquatExpr: 6.85, topCellType: "Mesophyll", spatialRegion: "Chloroplast / Stroma" }
  ],

  keggPathways: [
    { code: "ath00195", name: "Photosynthesis", count: 34, total: 77, fold: 1.93, pval: 1.2e-5, category: "Energy Metabolism" },
    { code: "ath00480", name: "Glutathione metabolism", count: 28, total: 62, fold: 1.98, pval: 3.4e-6, category: "Antioxidant Systems" },
    { code: "ath04712", name: "Circadian rhythm - plant", count: 22, total: 48, fold: 2.01, pval: 8.9e-6, category: "Temporal Regulation" },
    { code: "ath04016", name: "MAPK signaling pathway - plant", count: 45, total: 112, fold: 1.76, pval: 4.1e-7, category: "Signal Transduction" },
    { code: "ath00053", name: "Ascorbate and aldarate metabolism", count: 17, total: 63, fold: 1.18, pval: 2.3e-3, category: "Antioxidant Systems" },
    { code: "ath00196", name: "Photosynthesis - antenna proteins", count: 14, total: 22, fold: 2.78, pval: 5.8e-8, category: "Energy Metabolism" },
    { code: "ath00073", name: "Cutin, suberine and wax biosynthesis", count: 34, total: 65, fold: 2.28, pval: 1.1e-7, category: "Lipid Metabolism" }
  ],

  deconvolutionProportions: [
    { stage: "seed_0d", epidermis: 0.12, mesophyll: 0.05, stele: 0.28, guardCells: 0.02, meristematic: 0.35, rootCap: 0.08, other: 0.10 },
    { stage: "seedling_3d", epidermis: 0.24, mesophyll: 0.31, stele: 0.18, guardCells: 0.08, meristematic: 0.11, rootCap: 0.05, other: 0.03 },
    { stage: "rosette_21d", epidermis: 0.22, mesophyll: 0.52, stele: 0.12, guardCells: 0.09, meristematic: 0.02, rootCap: 0.01, other: 0.02 },
    { stage: "flower", epidermis: 0.18, mesophyll: 0.20, stele: 0.14, guardCells: 0.04, meristematic: 0.15, rootCap: 0.01, other: 0.28 },
    { stage: "spaceflight_root", epidermis: 0.29, mesophyll: 0.04, stele: 0.25, guardCells: 0.03, meristematic: 0.21, rootCap: 0.14, other: 0.04 },
    { stage: "ground_root", epidermis: 0.25, mesophyll: 0.04, stele: 0.22, guardCells: 0.03, meristematic: 0.31, rootCap: 0.11, other: 0.04 }
  ]
};
