/**
 * Arabidopsis ROS Decoder Web Application Data Asset
 * Pre-calculated CVAE latent embeddings, spaceflight projections, gene profiles,
 * ROS stimulus signature matrices, temporal classes, and ggPlantMap spatial geometries.
 */

window.ROS_DECODER_DATA = {
  metadata: {
    title: "Arabidopsis ROS Decoder: Conditional VAE & Spaceflight Validation",
    version: "1.1.0",
    author: "Richard Barker, Ph.D.",
    affiliation: "Department of Agricultural and Biological Engineering, Purdue University",
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

  // Comprehensive ROS Gene Knowledgebase for Multi-Gene Predictor
  geneDatabase: [
    { symbol: "CAT2", agi: "AT4G35090", name: "Catalase 2", weights: { h2o2: 0.95, paraquat: 0.45, menadione: 0.30, ozone: 0.65, singlet_oxygen: 0.40, high_light: 0.85 }, timeClass: "Late (>12h)", timeHours: 16, tissue: "Mesophyll", organ: "Leaf", cellType: "Mesophyll" },
    { symbol: "CAT1", agi: "AT1G20630", name: "Catalase 1", weights: { h2o2: 0.85, paraquat: 0.35, menadione: 0.25, ozone: 0.50, singlet_oxygen: 0.30, high_light: 0.60 }, timeClass: "Late (>12h)", timeHours: 14, tissue: "Seed / Seedling", organ: "Seedling", cellType: "Epidermis" },
    { symbol: "CAT3", agi: "AT1G20620", name: "Catalase 3", weights: { h2o2: 0.80, paraquat: 0.40, menadione: 0.20, ozone: 0.45, singlet_oxygen: 0.35, high_light: 0.70 }, timeClass: "Late (>12h)", timeHours: 18, tissue: "Vascular", organ: "Stem", cellType: "Vascular" },
    { symbol: "APX1", agi: "AT1G07890", name: "Ascorbate peroxidase 1", weights: { h2o2: 0.90, paraquat: 0.80, menadione: 0.55, ozone: 0.75, singlet_oxygen: 0.50, high_light: 0.92 }, timeClass: "Early (1-4h)", timeHours: 2.5, tissue: "Root Cap / Epidermis", organ: "Root", cellType: "Epidermis" },
    { symbol: "APX2", agi: "AT3G09640", name: "Ascorbate peroxidase 2", weights: { h2o2: 0.75, paraquat: 0.70, menadione: 0.40, ozone: 0.60, singlet_oxygen: 0.65, high_light: 0.98 }, timeClass: "Immediate (<1h)", timeHours: 0.75, tissue: "Vascular bundle", organ: "Leaf", cellType: "Vascular" },
    { symbol: "APX3", agi: "AT4G35000", name: "Peroxisomal ascorbate peroxidase 3", weights: { h2o2: 0.82, paraquat: 0.50, menadione: 0.35, ozone: 0.55, singlet_oxygen: 0.45, high_light: 0.70 }, timeClass: "Mid (4-12h)", timeHours: 6.0, tissue: "Mesophyll", organ: "Leaf", cellType: "Mesophyll" },
    { symbol: "ZAT12", agi: "AT5G59820", name: "Zinc finger protein 12", weights: { h2o2: 0.94, paraquat: 0.88, menadione: 0.80, ozone: 0.85, singlet_oxygen: 0.75, high_light: 0.90 }, timeClass: "Immediate (<1h)", timeHours: 0.5, tissue: "Stele / Vascular", organ: "Root", cellType: "Stele" },
    { symbol: "ZAT10", agi: "AT1G27730", name: "Zinc finger protein 10 (STZ)", weights: { h2o2: 0.89, paraquat: 0.82, menadione: 0.70, ozone: 0.80, singlet_oxygen: 0.70, high_light: 0.85 }, timeClass: "Immediate (<1h)", timeHours: 0.6, tissue: "Meristematic", organ: "Root", cellType: "Meristematic" },
    { symbol: "RBOHD", agi: "AT5G47910", name: "Respiratory burst oxidase homolog D", weights: { h2o2: 0.60, paraquat: 0.92, menadione: 0.85, ozone: 0.78, singlet_oxygen: 0.60, high_light: 0.72 }, timeClass: "Immediate (<1h)", timeHours: 0.4, tissue: "Guard cells / Root Hair", organ: "Leaf", cellType: "Guard_cells" },
    { symbol: "RBOHF", agi: "AT1G64060", name: "Respiratory burst oxidase homolog F", weights: { h2o2: 0.55, paraquat: 0.88, menadione: 0.80, ozone: 0.82, singlet_oxygen: 0.55, high_light: 0.65 }, timeClass: "Immediate (<1h)", timeHours: 0.5, tissue: "Vascular stele", organ: "Root", cellType: "Stele" },
    { symbol: "HSFA2", agi: "AT2G26150", name: "Heat shock factor A2", weights: { h2o2: 0.92, paraquat: 0.75, menadione: 0.60, ozone: 0.70, singlet_oxygen: 0.85, high_light: 0.95 }, timeClass: "Early (1-4h)", timeHours: 1.5, tissue: "Meristematic / Shoot", organ: "Whole Seedling", cellType: "Meristematic" },
    { symbol: "KIN10", agi: "AT3G01090", name: "SnRK1.1 / KIN10 Kinase", weights: { h2o2: 0.70, paraquat: 0.65, menadione: 0.75, ozone: 0.60, singlet_oxygen: 0.50, high_light: 0.55 }, timeClass: "Mid (4-12h)", timeHours: 8.0, tissue: "Stele / Root vasculature", organ: "Root", cellType: "Stele" },
    { symbol: "CSD1", agi: "AT1G08830", name: "Cu/Zn superoxide dismutase 1", weights: { h2o2: 0.40, paraquat: 0.95, menadione: 0.88, ozone: 0.70, singlet_oxygen: 0.45, high_light: 0.80 }, timeClass: "Mid (4-12h)", timeHours: 5.0, tissue: "Mesophyll / Chloroplast", organ: "Leaf", cellType: "Mesophyll" },
    { symbol: "CSD2", agi: "AT2G28190", name: "Cu/Zn superoxide dismutase 2", weights: { h2o2: 0.35, paraquat: 0.92, menadione: 0.85, ozone: 0.65, singlet_oxygen: 0.50, high_light: 0.85 }, timeClass: "Mid (4-12h)", timeHours: 5.5, tissue: "Mesophyll", organ: "Leaf", cellType: "Mesophyll" },
    { symbol: "FSD1", agi: "AT4G25100", name: "Fe superoxide dismutase 1", weights: { h2o2: 0.30, paraquat: 0.96, menadione: 0.90, ozone: 0.60, singlet_oxygen: 0.55, high_light: 0.82 }, timeClass: "Early (1-4h)", timeHours: 3.0, tissue: "Chloroplast stroma", organ: "Leaf", cellType: "Mesophyll" },
    { symbol: "MSD1", agi: "AT3G10920", name: "Mn superoxide dismutase 1", weights: { h2o2: 0.50, paraquat: 0.85, menadione: 0.82, ozone: 0.55, singlet_oxygen: 0.40, high_light: 0.60 }, timeClass: "Mid (4-12h)", timeHours: 6.5, tissue: "Mitochondria / Stele", organ: "Root", cellType: "Stele" },
    { symbol: "GPX1", agi: "AT2G31570", name: "Glutathione peroxidase 1", weights: { h2o2: 0.85, paraquat: 0.70, menadione: 0.65, ozone: 0.60, singlet_oxygen: 0.55, high_light: 0.75 }, timeClass: "Mid (4-12h)", timeHours: 4.5, tissue: "Chloroplast / Mesophyll", organ: "Leaf", cellType: "Mesophyll" },
    { symbol: "GPX7", agi: "AT4G31870", name: "Glutathione peroxidase 7", weights: { h2o2: 0.88, paraquat: 0.68, menadione: 0.60, ozone: 0.62, singlet_oxygen: 0.80, high_light: 0.90 }, timeClass: "Early (1-4h)", timeHours: 2.0, tissue: "Mesophyll", organ: "Leaf", cellType: "Mesophyll" },
    { symbol: "DHAR1", agi: "AT1G19570", name: "Dehydroascorbate reductase 1", weights: { h2o2: 0.80, paraquat: 0.60, menadione: 0.50, ozone: 0.70, singlet_oxygen: 0.45, high_light: 0.80 }, timeClass: "Mid (4-12h)", timeHours: 7.0, tissue: "Cytosol / Epidermis", organ: "Whole Seedling", cellType: "Epidermis" },
    { symbol: "GR1", agi: "AT3G24170", name: "Glutathione reductase 1", weights: { h2o2: 0.85, paraquat: 0.75, menadione: 0.70, ozone: 0.65, singlet_oxygen: 0.50, high_light: 0.78 }, timeClass: "Mid (4-12h)", timeHours: 5.0, tissue: "Stele / Vasculature", organ: "Root", cellType: "Stele" },
    { symbol: "WRKY33", agi: "AT2G38470", name: "WRKY transcription factor 33", weights: { h2o2: 0.70, paraquat: 0.85, menadione: 0.80, ozone: 0.90, singlet_oxygen: 0.65, high_light: 0.70 }, timeClass: "Immediate (<1h)", timeHours: 0.8, tissue: "Epidermis / Guard cells", organ: "Leaf", cellType: "Guard_cells" },
    { symbol: "WRKY40", agi: "AT1G80840", name: "WRKY transcription factor 40", weights: { h2o2: 0.75, paraquat: 0.80, menadione: 0.75, ozone: 0.85, singlet_oxygen: 0.70, high_light: 0.75 }, timeClass: "Immediate (<1h)", timeHours: 0.7, tissue: "Meristematic", organ: "Root", cellType: "Meristematic" },
    { symbol: "AOX1A", agi: "AT3G22370", name: "Alternative oxidase 1a", weights: { h2o2: 0.90, paraquat: 0.85, menadione: 0.92, ozone: 0.80, singlet_oxygen: 0.60, high_light: 0.70 }, timeClass: "Early (1-4h)", timeHours: 2.0, tissue: "Mitochondria / Stele", organ: "Root", cellType: "Stele" },
    { symbol: "ANAC017", agi: "AT1G34190", name: "NAC domain-containing protein 17", weights: { h2o2: 0.92, paraquat: 0.78, menadione: 0.88, ozone: 0.75, singlet_oxygen: 0.65, high_light: 0.80 }, timeClass: "Immediate (<1h)", timeHours: 0.6, tissue: "Endoplasmic reticulum / Stele", organ: "Root", cellType: "Stele" }
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
    { stage: "Seed (0d)", epidermis: 0.12, mesophyll: 0.05, stele: 0.28, guardCells: 0.02, meristematic: 0.35, rootCap: 0.08, other: 0.10 },
    { stage: "Seedling (3d)", epidermis: 0.24, mesophyll: 0.31, stele: 0.18, guardCells: 0.08, meristematic: 0.11, rootCap: 0.05, other: 0.03 },
    { stage: "Rosette (21d)", epidermis: 0.22, mesophyll: 0.52, stele: 0.12, guardCells: 0.09, meristematic: 0.02, rootCap: 0.01, other: 0.02 },
    { stage: "Flower", epidermis: 0.18, mesophyll: 0.20, stele: 0.14, guardCells: 0.04, meristematic: 0.15, rootCap: 0.01, other: 0.28 },
    { stage: "Spaceflight Root", epidermis: 0.29, mesophyll: 0.04, stele: 0.25, guardCells: 0.03, meristematic: 0.21, rootCap: 0.14, other: 0.04 },
    { stage: "Ground Root", epidermis: 0.25, mesophyll: 0.04, stele: 0.22, guardCells: 0.03, meristematic: 0.31, rootCap: 0.11, other: 0.04 }
  ]
};
