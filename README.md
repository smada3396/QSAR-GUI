# QSAR Molecular Visualization Tool

This repository contains a modern, user-friendly Streamlit web application for interactive 3D visualization of **106 PFAS ligand-receptor complexes** with ERα and ERβ receptors. All data and results for these receptor-ligand structures are included—no setup or data preparation required!

## What You Get

* **3D visualization** of all 106 PFAS ligand-receptor complexes using NGL Viewer
* **Interactive selection** between ERα and ERβ receptors
* **Dataset selection** between "Commonly Exposed Set" (CE) and "Top 50 Set" (T50)
* **Real-time molecular structure viewing** with customizable representations
* **Ready-to-use**: just install dependencies and launch the app

## Quick Start

1. **Install Python 3.9+** (recommended: 3.10 or 3.11)
2. **Install dependencies:**  
   ```
   pip install -r requirements.txt
   ```
3. **Run the app:**  
   ```
   streamlit run qsar_web_app.py
   ```
4. **Open your browser to** `http://localhost:8501`

## Included Data

* The `PDB_OF_CE/` folder contains all 106 receptor-ligand complex structures:
  * **Alpha_CE_Combined/**: 55 ERα receptor complexes (Commonly Exposed Set)
  * **Beta_CE_Combined/**: 55 ERβ receptor complexes (Commonly Exposed Set)  
  * **Alpha_T50_Combined/**: 50 ERα receptor complexes (Top 50 Set)
  * **Beta_T50_Combined/**: 50 ERβ receptor complexes (Top 50 Set)
* Each folder contains PDB files with combined receptor-ligand structures
* The app is preconfigured to use this data—no changes needed

## Features

### Interactive 3D Structure Viewer
* **NGL Viewer integration** for high-quality molecular visualization
* **Multiple representation options**: cartoon, ball+stick, surface
* **Ligand highlighting** with automatic detection and visualization
* **Responsive design** that works on desktop and mobile devices

### Receptor Selection
* **ERα (Estrogen Receptor Alpha)**: Red-themed interface
* **ERβ (Estrogen Receptor Beta)**: Teal-themed interface
* **Side-by-side comparison** capabilities

### Dataset Options
* **Commonly Exposed Set (CE)**: 55 PFAS ligands commonly found in environmental samples
* **Top 50 Set (T50)**: 50 PFAS ligands with highest predicted binding affinities

### User Interface
* **Modern, responsive design** with gradient backgrounds
* **Intuitive navigation** with sidebar controls
* **Real-time structure loading** and visualization
* **Professional styling** with custom CSS

## Technical Details

### Architecture
* **Frontend**: Streamlit web interface
* **3D Visualization**: NGL Viewer (WebGL-based)
* **Data Processing**: Python pathlib for file management
* **Caching**: Streamlit's built-in caching for performance

### Data Flow
1. **Data Loading**: App scans PDB_OF_CE directory structure
2. **Ligand Detection**: Automatic identification of ligand molecules in PDB files
3. **Visualization**: Interactive 3D views generated with NGL Viewer
4. **User Interaction**: Real-time selection and display updates

### File Structure
```
QSAR-GUI-Project/
├── qsar_web_app.py          # Main Streamlit application
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── PDB_OF_CE/              # Molecular structure data
    ├── Alpha_CE_Combined/   # 55 ERα CE complexes
    ├── Beta_CE_Combined/    # 55 ERβ CE complexes
    ├── Alpha_T50_Combined/  # 50 ERα T50 complexes
    └── Beta_T50_Combined/   # 50 ERβ T50 complexes
```

## Usage

1. **Start the application**:
   ```
   streamlit run qsar_web_app.py
   ```

2. **Open your browser** and navigate to `http://localhost:8501`

3. **Select your preferences**:
   - Choose receptor type (ERα or ERβ)
   - Select dataset (CE or T50)
   - Pick a specific ligand from the dropdown

4. **Explore the 3D structure**:
   - Rotate, zoom, and pan the molecular viewer
   - Toggle between different molecular representations
   - Examine ligand-receptor interactions

## Customization

### Adding New Ligands
1. Place new PDB files in the appropriate folder structure
2. Ensure file naming follows the expected pattern
3. Restart the application to load new data

### Modifying Visualizations
* Edit the NGL Viewer parameters in `qsar_web_app.py`
* Customize the CSS styling for different themes
* Add new representation options

### Extending Functionality
* Add new analysis features
* Implement additional visualization options
* Create new data export capabilities

## Requirements

* **Python 3.9+** (recommended: 3.10 or 3.11)
* **Streamlit** for web interface
* **Modern web browser** with WebGL support
* **Internet connection** for NGL Viewer library loading

## Browser Compatibility

* **Chrome/Chromium**: Full support
* **Firefox**: Full support  
* **Safari**: Full support
* **Edge**: Full support
* **Mobile browsers**: Responsive design support

## Performance

* **Fast loading**: Optimized file structure and caching
* **Smooth visualization**: WebGL-accelerated 3D rendering
* **Responsive interface**: Real-time updates and interactions
* **Memory efficient**: Lazy loading of molecular data

## Troubleshooting

### Common Issues
1. **App won't start**: Check Python version and dependencies
2. **3D viewer not loading**: Ensure WebGL is enabled in browser
3. **Slow performance**: Close other browser tabs, check internet connection
4. **File not found errors**: Verify PDB_OF_CE folder structure

### Getting Help
* Check the browser console for JavaScript errors
* Verify all dependencies are installed correctly
* Ensure file paths are correct for your system

## Contributing

To extend the application:

1. Fork the repository
2. Add new features or improvements
3. Update documentation
4. Submit pull request

## License

This application is designed for research and educational use. Please cite the original analysis when using this data.

## Contact

For questions or issues: Contact the development team

---

**Note**: This application provides interactive visualization of PFAS ligand-receptor complexes for research and educational purposes. The molecular structures represent computational docking results and should be validated experimentally for research applications. 