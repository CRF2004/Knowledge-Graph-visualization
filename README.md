Knowledge Graph Visualization Tool

## Project Overview

This is a web-based knowledge graph visualization tool that allows users to display and interactively explore knowledge graph data through a simple interface.

## Quick Start

1. Download the project code
2. Run `app.py` to launch the application
3. The app will run on **localhost port 5000**

## Features

- **Data Loading Options**:
  - Select from preset knowledge graph files
  - Upload a custom JSON file
- **Interactive Visualization**:
  - Display knowledge graphs with dynamic rendering
  - Support for panning, zooming, and dragging
  - Click on nodes to view detailed information (displayed in the bottom-left panel)

## Data Format Requirements

If uploading a custom JSON file, ensure it follows this structure:

```
{
  "nodes": [
    {
      "id": "Unique Node ID",
      "label": "Node Label",
      "properties": {
        // Optional key-value attributes
      }
    }
    // More nodes...
  ],
  "relationships": [
    {
      "source": "Source Node ID",
      "target": "Target Node ID",
      "type": "Relationship Type"
    }
    // More relationships...
  ]
}
```

## Usage Instructions

1. After launching the app, choose either:
   - A preset file, or
   - Upload a local JSON file
2. Click the **"Load"** button to render the knowledge graph
3. In the visualization interface:
   - **Drag** with the mouse to move the graph
   - **Scroll** to zoom in/out
   - **Click** on nodes to view details

## Notes

- Ensure the uploaded JSON file follows the correct format
- Node IDs in `relationships` (`source` & `target`) must match `nodes` IDs
- For best performance, avoid extremely large graphs (>10,000 nodes)
