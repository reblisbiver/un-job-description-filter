# UN Job Description (JD) Analysis Tool# UN JD Parser & Filter








































































*Disclaimer: This tool is not affiliated with the United Nations. It is designed to assist applicants in organizing their job search data.*---This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.## 📄 License```pyinstaller --noconfirm --onefile --windowed --add-data "app/static;app/static" --name "UN_JD_Analysis_Tool" run.py```bashTo build the standalone executable yourself:## 📦 Building the EXE- `storage/`: Local folder where processed data and file backups are kept.- `run.py`: Entry point for the application (launches FastAPI + WebView).  - `static/`: Frontend assets.  - `main.py`: Backend API and data persistence.  - `parser.py`: Core regex-based extraction logic.- `app/`: Contains the backend (FastAPI) and frontend (HTML/JS/CSS).## 🛠 Project Structure   ```   python run.py   ```bash4. **Run the app**:   ```   pip install -r requirements.txt   ```bash3. **Install dependencies**:   ```   source .venv/bin/activate  # Windows: .venv\Scripts\activate   python -m venv .venv   ```bash2. **Create a virtual environment**:   ```   cd JDfilter   git clone https://github.com/yourusername/JDfilter.git   ```bash1. **Clone the repository**:### Method 2: Development / Run from Source3. Run the application.2. Download `UN_JD_Analysis_Tool.exe`.1. Go to the [Releases](https://github.com/yourusername/JDfilter/releases) page. (Coming soon)You can directly run the bundled app without installing Python:### Method 1: Download Executable (Windows)## 🚀 Getting Started*The interface is clean and professional, built with FastAPI, Tailwind CSS, and FontAwesome.*## 📸 Interface- **Desktop Experience**: Packaged as a standalone Windows `.exe` using `pywebview`.- **Status Tracking**: Mark JDs as "Finished" or delete unwanted entries.- **Export**: Export your analyzed JD list to CSV for further processing.- **Persistent Storage**: Automatically saves metadata and builds a local library in the `storage` folder.- **Excel-like Management**: View all JDs in a sortable/filterable list.- **Multi-format Support**: Drag and drop `.pdf` or `.docx` files directly.- **Automated Parsing**: Extracts Job Title, Job ID, Deadline, and Duty Station from UN Inspira/ESCAP format JDs.## 🌟 Features![Python](https://img.shields.io/badge/python-3.12-blue.svg)![License](https://img.shields.io/badge/license-MIT-blue.svg)A clean, efficient desktop-style application to parse, extract, and manage United Nations Job Descriptions. Turn messy PDFs and Word documents into an organized, Excel-like list view automatically.
A lightweight desktop application designed to automatically parse United Nations Job Descriptions (JDs) from `.docx` and `.pdf` files. It extracts key information like Job Title, Job ID, Deadline, and Duty Station into an organized, Excel-like list view for easy tracking and management.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)

## 🌟 Key Features

- **Automated Parsing**: Quickly extract Job Title, ID, Deadline, and Duty Station from UN Inspira/ESCAP layouts.
- **Support for Multiple Formats**: Handles both Microsoft Word (`.docx`) and PDF (`.pdf`) files.
- **Persistence**: Automatically saves your parsing history locally in a JSON database.
- **File Management**: 
    - Auto-backups uploaded files to a local `storage` folder.
    - Direct access to original files from the interface.
    - Precise deletion of single entries and their associated files.
- **Status Tracking**: Mark JDs as "Finished" and filter views to stay organized.
- **Exporting**: One-click export of your curated list to a CSV file (compatible with Excel).
- **Standalone EXE**: Can be bundled into a single executable for Windows without needing a Python environment.

## 🚀 Getting Started

### Method 1: Run from Source (For Developers)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/UN-JD-Parser.git
   cd UN-JD-Parser
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python run.py
   ```

### Method 2: Use the Executable

**You can get the latest '.exe' file in the releases area.**

Or

To create a standalone `.exe` file:
```bash
pyinstaller --noconfirm --onefile --windowed --add-data "app/static;app/static" --name "UN_JD_Analysis_Tool" run.py
```
The result will be in the `dist/` folder. 

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.12)
- **GUI Wrapper**: PyWebView (Native Windows integration)
- **Frontend**: Tailwind CSS, JavaScript (Vanilla ES6), FontAwesome
- **Parsing Engine**: `python-docx`, `PyPDF2`, Regular Expressions (Regex)
- **Bundling**: PyInstaller

## 📂 Project Structure

```text
├── app/
│   ├── parser.py    # Regex parsing logic
│   ├── main.py      # FastAPI backend and API routes
│   └── static/      # HTML/JS/CSS frontend
├── storage/         # Local data store (created on first run)
│   ├── data.json    # Metadata database
│   └── files/       # Backup of JD files
├── run.py           # Entry point (launches server and GUI)
└── requirements.txt # Python dependencies
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 中文说明

**UN JD Parser** 是一款专为联合国岗位描述（JD）设计的自动化解析工具。

- **主要功能**：自动提取岗位名称、ID、截止日期和工作地点；支持 `.docx` 和 `.pdf`；支持历史记录保存与导出；支持标记任务完成状态。
- **技术栈**：基于 Python FastAPI 和 Tailwind CSS，通过 PyWebView 提供原生窗口体验。
- **便携性**：可打包为单文件 EXE，无需安装 Python 即可运行。
