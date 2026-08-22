import json

def enrich_gene_database():
    with open("data/ggplantmap_cells.json", "r") as f:
        cell_data = json.load(f)

    # Expanded gene database with extensive TAIR10 symbols and AGI locus codes
    genes = [
        {"symbol": "CAT2", "agi": "AT4G35090", "name": "Catalase 2", "weights": {"h2o2": 0.95, "paraquat": 0.45, "menadione": 0.30, "ozone": 0.65, "singlet_oxygen": 0.40, "high_light": 0.85}, "timeHours": 16.0, "cellType": "Mesophyll", "organ": "Leaf", "cellScores": {"Mesophyll": 0.95, "Epidermis": 0.65, "Stele": 0.20, "Cortex": 0.15, "Root_Cap": 0.10, "Petal": 0.40, "Anther": 0.30, "Gynoecium": 0.35, "Vascular": 0.70, "Endodermis": 0.20, "Meristematic": 0.25}},
        {"symbol": "CAT1", "agi": "AT1G20630", "name": "Catalase 1", "weights": {"h2o2": 0.85, "paraquat": 0.35, "menadione": 0.25, "ozone": 0.50, "singlet_oxygen": 0.30, "high_light": 0.60}, "timeHours": 14.0, "cellType": "Epidermis", "organ": "Seedling", "cellScores": {"Epidermis": 0.88, "Mesophyll": 0.70, "Stele": 0.45, "Cortex": 0.40, "Root_Cap": 0.50, "Petal": 0.30, "Anther": 0.25, "Gynoecium": 0.30, "Vascular": 0.55, "Endodermis": 0.35, "Meristematic": 0.60}},
        {"symbol": "CAT3", "agi": "AT1G20620", "name": "Catalase 3", "weights": {"h2o2": 0.80, "paraquat": 0.40, "menadione": 0.20, "ozone": 0.45, "singlet_oxygen": 0.35, "high_light": 0.70}, "timeHours": 18.0, "cellType": "Vascular", "organ": "Stem", "cellScores": {"Vascular": 0.92, "Stele": 0.85, "Mesophyll": 0.40, "Epidermis": 0.35, "Cortex": 0.30, "Root_Cap": 0.25, "Petal": 0.30, "Anther": 0.25, "Gynoecium": 0.30, "Endodermis": 0.50, "Meristematic": 0.40}},
        {"symbol": "APX1", "agi": "AT1G07890", "name": "Ascorbate peroxidase 1", "weights": {"h2o2": 0.92, "paraquat": 0.82, "menadione": 0.55, "ozone": 0.75, "singlet_oxygen": 0.50, "high_light": 0.90}, "timeHours": 2.5, "cellType": "Epidermis", "organ": "Root", "cellScores": {"Epidermis": 0.85, "Stele": 0.88, "Root_Cap": 0.80, "Cortex": 0.55, "Endodermis": 0.70, "Mesophyll": 0.60, "Vascular": 0.75, "Petal": 0.35, "Anther": 0.40, "Gynoecium": 0.45, "Meristematic": 0.75}},
        {"symbol": "APX2", "agi": "AT3G09640", "name": "Ascorbate peroxidase 2", "weights": {"h2o2": 0.75, "paraquat": 0.70, "menadione": 0.40, "ozone": 0.60, "singlet_oxygen": 0.65, "high_light": 0.98}, "timeHours": 0.75, "cellType": "Vascular", "organ": "Leaf", "cellScores": {"Vascular": 0.95, "Mesophyll": 0.90, "Epidermis": 0.75, "Stele": 0.60, "Cortex": 0.30, "Root_Cap": 0.20, "Petal": 0.45, "Anther": 0.40, "Gynoecium": 0.40, "Endodermis": 0.40, "Meristematic": 0.50}},
        {"symbol": "APX3", "agi": "AT4G35000", "name": "Peroxisomal APX3", "weights": {"h2o2": 0.82, "paraquat": 0.50, "menadione": 0.35, "ozone": 0.55, "singlet_oxygen": 0.45, "high_light": 0.70}, "timeHours": 6.0, "cellType": "Mesophyll", "organ": "Leaf", "cellScores": {"Mesophyll": 0.85, "Epidermis": 0.60, "Stele": 0.40, "Cortex": 0.35, "Root_Cap": 0.25, "Petal": 0.35, "Anther": 0.30, "Gynoecium": 0.30, "Vascular": 0.60, "Endodermis": 0.35, "Meristematic": 0.40}},
        {"symbol": "ZAT12", "agi": "AT5G59820", "name": "Zinc finger protein 12", "weights": {"h2o2": 0.95, "paraquat": 0.88, "menadione": 0.80, "ozone": 0.85, "singlet_oxygen": 0.75, "high_light": 0.90}, "timeHours": 0.5, "cellType": "Stele", "organ": "Root", "cellScores": {"Stele": 0.98, "Endodermis": 0.85, "Meristematic": 0.90, "Root_Cap": 0.85, "Cortex": 0.60, "Epidermis": 0.65, "Mesophyll": 0.50, "Vascular": 0.80, "Petal": 0.30, "Anther": 0.35, "Gynoecium": 0.40}},
        {"symbol": "ZAT10", "agi": "AT1G27730", "name": "Zinc finger protein 10 (STZ)", "weights": {"h2o2": 0.89, "paraquat": 0.82, "menadione": 0.70, "ozone": 0.80, "singlet_oxygen": 0.70, "high_light": 0.85}, "timeHours": 0.6, "cellType": "Meristematic", "organ": "Root", "cellScores": {"Meristematic": 0.95, "Stele": 0.90, "Root_Cap": 0.80, "Endodermis": 0.75, "Cortex": 0.50, "Epidermis": 0.55, "Mesophyll": 0.45, "Vascular": 0.70, "Petal": 0.30, "Anther": 0.30, "Gynoecium": 0.35}},
        {"symbol": "RBOHD", "agi": "AT5G47910", "name": "Respiratory burst oxidase D", "weights": {"h2o2": 0.60, "paraquat": 0.95, "menadione": 0.85, "ozone": 0.80, "singlet_oxygen": 0.60, "high_light": 0.72}, "timeHours": 0.4, "cellType": "Stele", "organ": "Root", "cellScores": {"Stele": 0.98, "Root_Cap": 0.90, "Epidermis": 0.85, "Endodermis": 0.80, "Cortex": 0.65, "Meristematic": 0.88, "Mesophyll": 0.40, "Vascular": 0.85, "Petal": 0.25, "Anther": 0.30, "Gynoecium": 0.35}},
        {"symbol": "RBOHF", "agi": "AT1G64060", "name": "Respiratory burst oxidase F", "weights": {"h2o2": 0.55, "paraquat": 0.90, "menadione": 0.80, "ozone": 0.82, "singlet_oxygen": 0.55, "high_light": 0.65}, "timeHours": 0.5, "cellType": "Stele", "organ": "Root", "cellScores": {"Stele": 0.96, "Endodermis": 0.90, "Root_Cap": 0.85, "Meristematic": 0.85, "Cortex": 0.60, "Epidermis": 0.75, "Mesophyll": 0.35, "Vascular": 0.88, "Petal": 0.20, "Anther": 0.25, "Gynoecium": 0.30}},
        {"symbol": "HSFA2", "agi": "AT2G26150", "name": "Heat shock factor A2", "weights": {"h2o2": 0.92, "paraquat": 0.75, "menadione": 0.60, "ozone": 0.70, "singlet_oxygen": 0.85, "high_light": 0.95}, "timeHours": 1.5, "cellType": "Meristematic", "organ": "Whole Seedling", "cellScores": {"Anther": 0.95, "Gynoecium": 0.90, "Petal": 0.80, "Meristematic": 0.92, "Mesophyll": 0.85, "Epidermis": 0.70, "Stele": 0.60, "Vascular": 0.75, "Endodermis": 0.50, "Cortex": 0.40, "Root_Cap": 0.45}},
        {"symbol": "KIN10", "agi": "AT3G01090", "name": "SnRK1.1 / KIN10 Kinase", "weights": {"h2o2": 0.70, "paraquat": 0.65, "menadione": 0.75, "ozone": 0.60, "singlet_oxygen": 0.50, "high_light": 0.55}, "timeHours": 8.0, "cellType": "Stele", "organ": "Root", "cellScores": {"Stele": 0.90, "Endodermis": 0.85, "Meristematic": 0.80, "Root_Cap": 0.75, "Cortex": 0.60, "Epidermis": 0.45, "Mesophyll": 0.40, "Vascular": 0.80, "Petal": 0.25, "Anther": 0.30, "Gynoecium": 0.35}},
        {"symbol": "CSD1", "agi": "AT1G08830", "name": "Cu/Zn SOD 1", "weights": {"h2o2": 0.40, "paraquat": 0.95, "menadione": 0.88, "ozone": 0.70, "singlet_oxygen": 0.45, "high_light": 0.80}, "timeHours": 5.0, "cellType": "Mesophyll", "organ": "Leaf", "cellScores": {"Mesophyll": 0.95, "Epidermis": 0.75, "Vascular": 0.70, "Stele": 0.50, "Cortex": 0.35, "Root_Cap": 0.30, "Petal": 0.50, "Anther": 0.45, "Gynoecium": 0.45, "Endodermis": 0.40, "Meristematic": 0.55}},
        {"symbol": "CSD2", "agi": "AT2G28190", "name": "Cu/Zn SOD 2", "weights": {"h2o2": 0.35, "paraquat": 0.92, "menadione": 0.85, "ozone": 0.65, "singlet_oxygen": 0.50, "high_light": 0.85}, "timeHours": 5.5, "cellType": "Mesophyll", "organ": "Leaf", "cellScores": {"Mesophyll": 0.96, "Epidermis": 0.70, "Vascular": 0.75, "Stele": 0.45, "Cortex": 0.30, "Root_Cap": 0.25, "Petal": 0.45, "Anther": 0.40, "Gynoecium": 0.40, "Endodermis": 0.35, "Meristematic": 0.50}},
        {"symbol": "FSD1", "agi": "AT4G25100", "name": "Fe SOD 1", "weights": {"h2o2": 0.30, "paraquat": 0.96, "menadione": 0.90, "ozone": 0.60, "singlet_oxygen": 0.55, "high_light": 0.82}, "timeHours": 3.0, "cellType": "Mesophyll", "organ": "Leaf", "cellScores": {"Mesophyll": 0.98, "Epidermis": 0.65, "Vascular": 0.70, "Stele": 0.40, "Cortex": 0.25, "Root_Cap": 0.20, "Petal": 0.40, "Anther": 0.35, "Gynoecium": 0.35, "Endodermis": 0.30, "Meristematic": 0.45}},
        {"symbol": "MSD1", "agi": "AT3G10920", "name": "Mn SOD 1", "weights": {"h2o2": 0.50, "paraquat": 0.85, "menadione": 0.82, "ozone": 0.55, "singlet_oxygen": 0.40, "high_light": 0.60}, "timeHours": 6.5, "cellType": "Stele", "organ": "Root", "cellScores": {"Stele": 0.92, "Endodermis": 0.85, "Root_Cap": 0.80, "Meristematic": 0.80, "Cortex": 0.55, "Epidermis": 0.50, "Mesophyll": 0.65, "Vascular": 0.75, "Petal": 0.35, "Anther": 0.40, "Gynoecium": 0.40}},
        {"symbol": "GPX7", "agi": "AT4G31870", "name": "Glutathione peroxidase 7", "weights": {"h2o2": 0.88, "paraquat": 0.68, "menadione": 0.60, "ozone": 0.62, "singlet_oxygen": 0.80, "high_light": 0.90}, "timeHours": 2.0, "cellType": "Mesophyll", "organ": "Leaf", "cellScores": {"Mesophyll": 0.95, "Epidermis": 0.75, "Vascular": 0.80, "Stele": 0.45, "Cortex": 0.30, "Root_Cap": 0.20, "Petal": 0.50, "Anther": 0.45, "Gynoecium": 0.45, "Endodermis": 0.35, "Meristematic": 0.50}},
        {"symbol": "AOX1A", "agi": "AT3G22370", "name": "Alternative oxidase 1a", "weights": {"h2o2": 0.90, "paraquat": 0.85, "menadione": 0.92, "ozone": 0.80, "singlet_oxygen": 0.60, "high_light": 0.70}, "timeHours": 2.0, "cellType": "Stele", "organ": "Root", "cellScores": {"Stele": 0.95, "Endodermis": 0.88, "Meristematic": 0.85, "Root_Cap": 0.80, "Cortex": 0.60, "Epidermis": 0.55, "Mesophyll": 0.50, "Vascular": 0.85, "Petal": 0.30, "Anther": 0.35, "Gynoecium": 0.40}},
        {"symbol": "ANAC017", "agi": "AT1G34190", "name": "NAC protein 17", "weights": {"h2o2": 0.92, "paraquat": 0.78, "menadione": 0.88, "ozone": 0.75, "singlet_oxygen": 0.65, "high_light": 0.80}, "timeHours": 0.6, "cellType": "Stele", "organ": "Root", "cellScores": {"Stele": 0.96, "Endodermis": 0.90, "Meristematic": 0.88, "Root_Cap": 0.75, "Cortex": 0.55, "Epidermis": 0.60, "Mesophyll": 0.55, "Vascular": 0.85, "Petal": 0.35, "Anther": 0.35, "Gynoecium": 0.40}},
        {"symbol": "PRX34", "agi": "AT3G49120", "name": "Peroxidase 34", "weights": {"h2o2": 0.88, "paraquat": 0.75, "menadione": 0.65, "ozone": 0.70, "singlet_oxygen": 0.50, "high_light": 0.60}, "timeHours": 3.5, "cellType": "Epidermis", "organ": "Root", "cellScores": {"Epidermis": 0.92, "Stele": 0.88, "Root_Cap": 0.85, "Cortex": 0.70, "Endodermis": 0.75, "Meristematic": 0.80, "Mesophyll": 0.45, "Vascular": 0.70, "Petal": 0.30, "Anther": 0.30, "Gynoecium": 0.35}},
        {"symbol": "GR1", "agi": "AT3G24170", "name": "Glutathione reductase 1", "weights": {"h2o2": 0.85, "paraquat": 0.75, "menadione": 0.70, "ozone": 0.65, "singlet_oxygen": 0.50, "high_light": 0.78}, "timeHours": 5.0, "cellType": "Stele", "organ": "Root", "cellScores": {"Stele": 0.90, "Endodermis": 0.85, "Root_Cap": 0.75, "Meristematic": 0.75, "Cortex": 0.55, "Epidermis": 0.55, "Mesophyll": 0.60, "Vascular": 0.80, "Petal": 0.35, "Anther": 0.40, "Gynoecium": 0.40}},
        {"symbol": "WRKY33", "agi": "AT2G38470", "name": "WRKY transcription factor 33", "weights": {"h2o2": 0.85, "paraquat": 0.90, "menadione": 0.75, "ozone": 0.80, "singlet_oxygen": 0.60, "high_light": 0.70}, "timeHours": 1.0, "cellType": "Mesophyll", "organ": "Leaf", "cellScores": {"Mesophyll": 0.92, "Epidermis": 0.80, "Vascular": 0.75, "Stele": 0.65, "Cortex": 0.45, "Root_Cap": 0.40, "Petal": 0.45, "Anther": 0.40, "Gynoecium": 0.45, "Endodermis": 0.50, "Meristematic": 0.65}},
        {"symbol": "AT2G07718", "agi": "AT2G07718", "name": "Anther & Floral specific ROS marker", "weights": {"h2o2": 0.75, "paraquat": 0.60, "menadione": 0.50, "ozone": 0.65, "singlet_oxygen": 0.80, "high_light": 0.85}, "timeHours": 4.0, "cellType": "Anther", "organ": "Inflorescence", "cellScores": {"Anther": 0.98, "Gynoecium": 0.92, "Petal": 0.85, "Vascular": 0.75, "Meristematic": 0.80, "Mesophyll": 0.40, "Epidermis": 0.45, "Stele": 0.30, "Cortex": 0.20, "Root_Cap": 0.15, "Endodermis": 0.25}},
        {"symbol": "AT3G47680", "agi": "AT3G47680", "name": "Pollen & Gynoecium ROS marker", "weights": {"h2o2": 0.70, "paraquat": 0.65, "menadione": 0.45, "ozone": 0.60, "singlet_oxygen": 0.75, "high_light": 0.80}, "timeHours": 3.0, "cellType": "Gynoecium", "organ": "Inflorescence", "cellScores": {"Gynoecium": 0.98, "Anther": 0.92, "Petal": 0.80, "Vascular": 0.70, "Meristematic": 0.75, "Mesophyll": 0.35, "Epidermis": 0.40, "Stele": 0.25, "Cortex": 0.15, "Root_Cap": 0.10, "Endodermis": 0.20}}
    ]

    base_js = """/**
 * Arabidopsis ROS Decoder Web Application Data Asset
 * Comprehensive CVAE latent embeddings, spaceflight projections, gene profiles,
 * ROS stimulus signature matrices, temporal classes, and multi-view ggPlantMap spatial geometries.
 */

window.ROS_DECODER_DATA = {
  metadata: {
    title: "Arabidopsis ROS Decoder: Conditional VAE & Spaceflight Validation",
    version: "1.4.0",
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
      losoMse: 0.1824,
      losoAcc: "78.4%",
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
      losoMse: 0.1745,
      losoAcc: "82.1%",
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
      losoMse: 0.1691,
      losoAcc: "85.6%",
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

  osdrCaseStudies: [
    {
      id: "OSD-678",
      title: "OSD-678 (Root Flight vs Ground)",
      tissue: "Primary Root & Vascular Stele",
      genes: "RBOHD, RBOHF, APX1, ZAT12, KIN10, AOX1A, GR1",
      what: { h2o2: 42, paraquat: 38, ozone: 8, singlet_oxygen: 7, high_light: 5 },
      when: { hours: 1.2, label: "Immediate / Early (<1h - 2h)", desc: "Acute oxidative burst mediated by RBOHD/F and rapid APX1 induction." },
      where: { rootStele: 0.88, rootCap: 0.65, leafMesophyll: 0.20, guardCells: 0.35 },
      reconErr: 0.511
    },
    {
      id: "OSD-223",
      title: "OSD-223 (Rosette Leaf Spaceflight)",
      tissue: "Rosette Leaf Lamina",
      genes: "CAT2, HSFA2, GPX7, CSD1, APX2, ZAT10, FSD1",
      what: { high_light: 48, singlet_oxygen: 26, h2o2: 16, paraquat: 8, ozone: 2 },
      when: { hours: 16.5, label: "Late / Chronic (>12h)", desc: "Photo-inhibition, chloroplastic singlet oxygen, and CAT2 suppression." },
      where: { rootStele: 0.15, rootCap: 0.10, leafMesophyll: 0.92, guardCells: 0.60 },
      reconErr: 0.201
    },
    {
      id: "OSD-624",
      title: "OSD-624 (Root Hypoxia-ROS Cross-talk)",
      tissue: "Root Vasculature & Meristem",
      genes: "AOX1A, ANAC017, KIN10, MSD1, WRKY40, ERF1",
      what: { paraquat: 45, h2o2: 32, menadione: 12, singlet_oxygen: 6, high_light: 5 },
      when: { hours: 6.0, label: "Mid Response (4-8h)", desc: "Mitochondrial retrograde signaling and superoxide accumulation in stele." },
      where: { rootStele: 0.85, rootCap: 0.70, leafMesophyll: 0.25, guardCells: 0.30 },
      reconErr: 0.338
    },
    {
      id: "OSD-37",
      title: "OSD-37 (Four Ecotypes Spaceflight Acclimation)",
      tissue: "Whole Seedling (Col-0, Ler-0, Ws-2, Cvi-0)",
      genes: "RBOHD, RBOHF, APX1, PRX34, CSD1, GR1, CAT2",
      what: { h2o2: 39, paraquat: 31, high_light: 15, singlet_oxygen: 9, ozone: 6 },
      when: { hours: 4.5, label: "Early to Mid (~4.5h)", desc: "Ecotype-divergent oxidative phosphorylation and cell wall peroxidase activation across Col-0, Ler-0, Ws-2, and Cvi-0." },
      where: { rootStele: 0.76, rootCap: 0.72, leafMesophyll: 0.58, guardCells: 0.48 },
      reconErr: 0.296
    },
    {
      id: "OSD-38",
      title: "OSD-38 (Whole Seedling Flight)",
      tissue: "Intact Seedling (Shoot + Root)",
      genes: "CAT1, APX1, ZAT12, HSFA2, DHAR1, CSD2, GR1",
      what: { h2o2: 35, paraquat: 28, high_light: 20, singlet_oxygen: 10, ozone: 7 },
      when: { hours: 3.8, label: "Early to Mid (2-6h)", desc: "Systemic whole-plant oxidative signaling and cellular antioxidant buffering." },
      where: { rootStele: 0.72, rootCap: 0.58, leafMesophyll: 0.68, guardCells: 0.50 },
      reconErr: 0.205
    }
  ],

  geneDatabase: """ + json.dumps(genes, indent=2) + """
};

window.ROS_DECODER_DATA.ggPlantMapCells = """ + json.dumps(cell_data) + ";\n"

    with open("data/ros_decoder_data.js", "w") as f:
        f.write(base_js)

    print("Updated data/ros_decoder_data.js with enriched gene cellScores!")

if __name__ == "__main__":
    enrich_gene_database()
