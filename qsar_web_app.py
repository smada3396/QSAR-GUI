import streamlit as st
import os
from pathlib import Path
import base64
import subprocess
import sys

# Page configuration
st.set_page_config(
    page_title="QSAR Molecular Visualization Tool",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    body {
        background: #f4f6fa;
    }
    .main-header {
        font-size: 2.8rem;
        font-weight: 900;
        color: #2563eb;
        text-align: center;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }
    .sub-header {
        font-size: 1.25rem;
        color: #4b5563;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    .receptor-card {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        padding: 2.2rem 2rem 2rem 2rem;
        border-radius: 18px;
        color: white;
        text-align: center;
        box-shadow: 0 6px 24px rgba(239,68,68,0.08);
        margin-bottom: 1.5rem;
    }
    .receptor-card-beta {
        background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
        padding: 2.2rem 2rem 2rem 2rem;
        border-radius: 18px;
        color: white;
        text-align: center;
        box-shadow: 0 6px 24px rgba(20,184,166,0.08);
        margin-bottom: 1.5rem;
    }
    .info-block {
        background: rgba(255, 255, 255, 0.18);
        padding: 1.1rem 1.5rem;
        border-radius: 12px;
        margin: 1.2rem 0.5rem 1.2rem 0;
        display: inline-block;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .stButton > button {
        background: linear-gradient(90deg, #2563eb 0%, #1e40af 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.7rem 2.2rem;
        font-weight: bold;
        font-size: 1.1rem;
        margin-top: 0.7rem;
        margin-bottom: 0.7rem;
        box-shadow: 0 2px 8px rgba(37,99,235,0.08);
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #1e40af 0%, #2563eb 100%);
        transform: translateY(-2px) scale(1.04);
    }
    .viewer-container {
        border: 2px solid #e5e7eb;
        border-radius: 16px;
        padding: 18px 18px 0 18px;
        margin: 32px 0 24px 0;
        background: #f9fafb;
        box-shadow: 0 4px 16px rgba(0,0,0,0.04);
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }
    .ngl-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    .stSelectbox > div {
        font-size: 1.1rem;
        font-weight: 500;
    }
    .stSidebar {
        background: #f1f5f9 !important;
    }
    .stSidebar [data-testid="stSidebarNav"] {
        margin-top: 2rem;
    }
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4 {
        color: #2563eb !important;
    }
    .st-expanderHeader {
        font-size: 1.1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def get_ligand_list(folder_name):
    folder_path = Path("PDB OF CE") / folder_name
    if not folder_path.exists():
        return []
    ligands = []
    
    # Handle different file naming patterns
    if "T50" in folder_name:
        # T50 files: either *_top_complex.pdb or *_out_complex.pdb
        for file in folder_path.glob("*_complex.pdb"):
            ligand_name = file.stem.replace("_top_complex", "").replace("_out_complex", "")
            ligands.append(ligand_name)
    else:
        # CE files: combined_*_out.pdb
        for file in folder_path.glob("combined_*.pdb"):
            ligand_name = file.stem.replace("combined_", "").replace("_out", "")
            ligands.append(ligand_name)
    
    return sorted(ligands)

def create_ngl_viewer(pdb_content, structure_name):
    pdb_encoded = base64.b64encode(pdb_content.encode()).decode()
    html_code = f"""
    <div class='viewer-container'>
        <div class='ngl-title'>Molecular Structure: {structure_name}</div>
        <div id='ngl-viewer' style='width: 100%; height: 520px; border: 1px solid #ddd; border-radius: 12px;'></div>
    </div>
    <script src='https://unpkg.com/ngl@0.10.4/dist/ngl.js'></script>
    <script>
        var stage = new NGL.Stage("ngl-viewer");
        stage.setParameters({{ backgroundColor: "white" }});
        
        var pdbData = atob("{pdb_encoded}");
        stage.loadFile(new Blob([pdbData], {{type: "chemical/x-pdb"}}), {{ext: "pdb"}}).then(function (component) {{
            // Default representation - let NGL Viewer decide based on PDB content
            component.addRepresentation("cartoon");
            
            // Try different selections for ligands
            component.addRepresentation("ball+stick", {{ sele: "hetero" }});
            component.addRepresentation("ball+stick", {{ sele: "UNL" }});
            component.addRepresentation("ball+stick", {{ sele: "not protein" }});
            
            component.autoView();
        }});
        
        // Prevent page scroll when zooming
        var viewerDiv = document.getElementById("ngl-viewer");
        viewerDiv.addEventListener('wheel', function(event) {{
            event.preventDefault();
        }}, {{ passive: false }});
    </script>
    """
    return html_code

def open_pdb_file(file_path):
    try:
        if sys.platform == "win32":
            os.startfile(str(file_path))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(file_path)])
        else:
            subprocess.run(["xdg-open", str(file_path)])
        return True
    except Exception as e:
        st.error(f"Could not open the PDB file. Error: {str(e)}")
        return False

def main():
    st.markdown('<h1 class="main-header">🧬 QSAR Molecular Visualization Tool</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Interactive 3D visualization of ERα and ERβ receptor-PFAS ligand structures</p>', unsafe_allow_html=True)
    st.sidebar.title("Navigation")
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "Home"
    
    # Handle page navigation from buttons
    if st.session_state.page != "Home":
        page = st.session_state.page
        st.session_state.page = "Home"  # Reset for next time
    else:
        page = st.sidebar.selectbox(
            "Choose a page:",
            ["Home", "ERα Receptor", "ERβ Receptor", "About"]
        )
    
    if page == "Home":
        show_home_page()
    elif page == "ERα Receptor":
        show_alpha_page()
    elif page == "ERβ Receptor":
        show_beta_page()
    elif page == "About":
        show_about_page()

def show_home_page():
    st.markdown("## Welcome to QSAR Molecular Visualization Tool")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="receptor-card">
            <h2 style='font-size:2rem;font-weight:800;'>🧬 ERα Receptor</h2>
            <p style='font-size:1.1rem;'>Estrogen Receptor Alpha - Primary target for estrogen signaling</p>
            <div class="info-block">
                <strong>106</strong><br>
                <small>Ligands</small>
            </div>
            <div class="info-block">
                <strong>3D</strong><br>
                <small>Visualization</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="receptor-card-beta">
            <h2 style='font-size:2rem;font-weight:800;'>🧬 ERβ Receptor</h2>
            <p style='font-size:1.1rem;'>Estrogen Receptor Beta - Secondary estrogen receptor subtype</p>
            <div class="info-block">
                <strong>106</strong><br>
                <small>Ligands</small>
            </div>
            <div class="info-block">
                <strong>3D</strong><br>
                <small>Visualization</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    ### How to Use This Tool
    1. **Select a Receptor**: Choose between ERα (primary estrogen receptor) or ERβ (secondary estrogen receptor)
    2. **Choose a Ligand**: Select from 106 available PFAS ligands
    3. **Visualize**: Use the embedded 3D viewer or download the PDB file
    ### Available Features
    - **PFAS Ligands**: Each ligand is combined with the selected receptor
    - **3D Visualization**: Interactive molecular viewer built into the browser
    - **Cross-platform**: Works on any device with a web browser
    - **Easy Download**: Direct download links for all combined structures
    """)

def show_alpha_page():
    st.markdown("## 🧬 ERα Receptor Visualization")
    st.markdown("**Estrogen Receptor Alpha - Primary target for estrogen signaling**")
    
    # Select dataset
    dataset = st.selectbox(
        "Choose a dataset:",
        ["Commonly Exposed Set", "Top 50 Set"],
        index=0
    )
    
    # Get ligands based on selected dataset
    if dataset == "Commonly Exposed Set":
        folder_name = "Alpha CE Combined"
    else:  # Top 50 Set
        folder_name = "Alpha T50 Combined"
    
    alpha_ligands = get_ligand_list(folder_name)
    if not alpha_ligands:
        st.error(f"No combined PDB files found in '{folder_name}' folder. Please run the combine_pdb.py script first.")
        return
    
    st.markdown("### Select a Ligand")
    selected_ligand = st.selectbox(
        f"Choose a PFAS ligand to visualize with ERα ({dataset}):",
        alpha_ligands,
        index=0
    )
    if selected_ligand:
        # Different file naming patterns for different datasets
        if dataset == "Top 50 Set":
            file_name = f"{selected_ligand}_top_complex.pdb"
        else:  # Commonly Exposed Set
            file_name = f"combined_{selected_ligand}_out.pdb"
        
        file_path = Path("PDB OF CE") / folder_name / file_name
        if file_path.exists():
            file_size = file_path.stat().st_size / 1024
            st.info(f"**File Size:** {file_size:.1f} KB")
            pdb_content = file_path.read_text()
            st.download_button(
                label="📁 Download PDB File",
                data=pdb_content,
                file_name=file_name,
                mime="chemical/x-pdb",
                key="alpha_download"
            )
            st.markdown("### 🧬 Interactive 3D Molecular Viewer")
            st.markdown("**Rotate, zoom, and explore the molecular structure directly in your browser**")
            viewer_html = create_ngl_viewer(pdb_content, f"ERα + {selected_ligand}")
            st.components.v1.html(viewer_html, height=600)
            st.markdown("""
            **Viewer Controls:**
            - **Mouse**: Rotate the structure
            - **Scroll**: Zoom in/out (page will not scroll)
            - **Right-click + drag**: Pan the view
            - **Double-click**: Reset view
            """)
            st.markdown("### File Preview")
            with st.expander("View PDB file content (first 50 lines)"):
                lines = pdb_content.split('\n')[:50]
                st.code('\n'.join(lines))
        else:
            st.error(f"❌ Combined PDB file not found: {file_path}")

def show_beta_page():
    st.markdown("## 🧬 ERβ Receptor Visualization")
    st.markdown("**Estrogen Receptor Beta - Secondary estrogen receptor subtype**")
    
    # Select dataset
    dataset = st.selectbox(
        "Choose a dataset:",
        ["Commonly Exposed Set", "Top 50 Set"],
        index=0
    )
    
    # Get ligands based on selected dataset
    if dataset == "Commonly Exposed Set":
        folder_name = "Beta CE Combined"
    else:  # Top 50 Set
        folder_name = "Beta T50 Combined"
    
    beta_ligands = get_ligand_list(folder_name)
    if not beta_ligands:
        st.error(f"No combined PDB files found in '{folder_name}' folder. Please run the combine_pdb.py script first.")
        return
    
    st.markdown("### Select a Ligand")
    selected_ligand = st.selectbox(
        f"Choose a PFAS ligand to visualize with ERβ ({dataset}):",
        beta_ligands,
        index=0
    )
    if selected_ligand:
        # Different file naming patterns for different datasets
        if dataset == "Top 50 Set":
            file_name = f"{selected_ligand}_out_complex.pdb"
        else:  # Commonly Exposed Set
            file_name = f"combined_{selected_ligand}_out.pdb"
        
        file_path = Path("PDB OF CE") / folder_name / file_name
        if file_path.exists():
            file_size = file_path.stat().st_size / 1024
            st.info(f"**File Size:** {file_size:.1f} KB")
            pdb_content = file_path.read_text()
            st.download_button(
                label="📁 Download PDB File",
                data=pdb_content,
                file_name=file_name,
                mime="chemical/x-pdb",
                key="beta_download"
            )
            st.markdown("### 🧬 Interactive 3D Molecular Viewer")
            st.markdown("**Rotate, zoom, and explore the molecular structure directly in your browser**")
            viewer_html = create_ngl_viewer(pdb_content, f"ERβ + {selected_ligand}")
            st.components.v1.html(viewer_html, height=600)
            st.markdown("""
            **Viewer Controls:**
            - **Mouse**: Rotate the structure
            - **Scroll**: Zoom in/out (page will not scroll)
            - **Right-click + drag**: Pan the view
            - **Double-click**: Reset view
            """)
            st.markdown("### File Preview")
            with st.expander("View PDB file content (first 50 lines)"):
                lines = pdb_content.split('\n')[:50]
                st.code('\n'.join(lines))
        else:
            st.error(f"❌ Combined PDB file not found: {file_path}")

def show_about_page():
    st.markdown("## About QSAR Molecular Visualization Tool")
    st.markdown("""
    ### Overview
    This tool provides an interactive web-based interface for visualizing QSAR (Quantitative Structure-Activity Relationship) molecular structures, specifically focusing on Estrogen Receptor (ER) interactions with PFAS ligands.
    ### Features
    - **Dual Receptor Support**: ERα and ERβ receptor visualization
    - **PFAS Ligands**: Comprehensive library of per- and polyfluoroalkyl substances
    - **Combined Structures**: Pre-combined receptor-ligand complexes
    - **Embedded 3D Viewer**: Interactive molecular visualization using NGL Viewer
    - **Multiple Output Options**: Download, open with default viewer, or copy file paths
    - **Cross-platform Compatibility**: Works on any device with a web browser
    - **No Installation Required**: Everything works in your browser
    ### Technical Details
    - **File Format**: PDB (Protein Data Bank) format
    - **Combined Files**: Each file contains both receptor and ligand structures
    - **3D Viewer**: NGL Viewer for interactive molecular visualization
    - **File Organization**: 
      - `Alpha Combined/`: ERα receptor + ligand complexes
      - `Beta Combined/`: ERβ receptor + ligand complexes
    ### Viewer Features
    - **Interactive 3D Visualization**: Rotate, zoom, and pan molecular structures
    - **Multiple Representations**: Cartoon and ball+stick views
    - **Color Coding**: Chain-based coloring for easy identification
    - **Hetero Atoms**: Ligands displayed as ball+stick representation
    - **Responsive Design**: Works on desktop, tablet, and mobile devices
    ### Recommended Molecular Viewers (for downloaded files)
    - **PyMOL**: Professional molecular visualization
    - **VMD**: Visual Molecular Dynamics
    - **ChimeraX**: UCSF ChimeraX
    - **Jmol**: Java-based molecular viewer
    - **Online viewers**: NGL Viewer, Mol* Viewer
    ### Usage Instructions
    1. Navigate to the desired receptor page (ERα or ERβ)
    2. Select a ligand from the dropdown menu
    3. Use the embedded 3D viewer to explore the structure
    4. Choose additional actions:
       - Download the PDB file
       - Open with your default molecular viewer
       - Copy the file path for manual access
    ### Data Source
    The combined PDB files are generated from individual receptor and ligand structures, providing ready-to-use complexes for molecular visualization and analysis.
    """)

if __name__ == "__main__":
    main() 