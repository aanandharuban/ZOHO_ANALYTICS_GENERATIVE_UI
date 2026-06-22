# Universal Analytical Dashboard (Generative UI MCP Server)

A flexible Model Context Protocol (MCP) server that empowers LLMs to dynamically visualize arbitrary datasets using custom HTML5 sandboxed widgets. 

Instead of hardcoding layout-specific constraints, this server exposes a generic entry-point tool that accepts raw arrays ($x$-axis categories, $y$-axis values, and metrics labels). The frontend utilizes **FastMCP Apps UI sandboxing**, rendering an interactive **Chart.js** dashboard directly inside the consumer chat interface.

---

## 🏗️ Project Architecture

The workspace is split into decoupled layers, isolating backend data orchestration from client-side visualization logic:

```text
fastmcp-local-demo/
│
├── venv/                   # Local Python Virtual Environment
├── server.py               # FastMCP Backend Protocol Handler
├── dashboard.html          # Custom HTML5/Tailwind/Chart.js Application
└── README.md               # Infrastructure Documentation
server.py: Boots the MCP engine, registers the absolute path of the layout asset, and exposes the render_dynamic_dashboard endpoint.dashboard.html: A standalone webpage using Tailwind CSS and Chart.js. It opens inside an isolated Iframe and processes incoming server data streams via the @modelcontextprotocol/ext-apps client framework.🛠️ Local Testing & Argument SchemaWhen interacting with this server via the local fastmcp dev inspector interface, the execution inputs are processed via raw JSON. To bypass validation restrictions (list_type errors), parameters must be formatted as explicit JSON arrays.Parameter Definition SchemaArgumentTypeDescriptionLocal Inspector Input ExampletitleStringHeader text displayed on the chart frame"Student Marks by Subject"x_axis_labelsList[str]Category labels ($X$-axis metrics)["Math", "Physics", "Chemistry"]y_axis_valuesList[int]Proportional values ($Y$-axis heights)[95, 88, 42]metric_labelStringDynamic hover indicator value label"Score"🚀 Step-by-Step Installation & Booting1. Rebuild the EnvironmentNavigate to the directory, purge any residual broken configurations, and assemble a native path mapping structure:PowerShell# Clean out legacy environment blocks
Remove-Item -Recurse -Force .\venv

# Provision a fresh Python environment
python -m venv venv

# Activate the local execution container
.\venv\Scripts\Activate.ps1
2. Install Required Core LibrariesInstalls FastMCP straight into your environment space:PowerShellpip install "fastmcp[apps]>=3.2.0"
3. Launching the Local Inspection UITo verify data validation constraints and test your canvas drawing engines locally:PowerShellfastmcp dev apps server.py
Open the resulting http://localhost:3000 link in your browser to access the manual test portal.🔌 Connecting to Claude DesktopTo deploy this interactive visual server directly inside Claude Desktop, link the application environment to the client platform profile layer.
