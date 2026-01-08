# UN Job Description (JD) Analysis Tool# UN JD Parser & Filter







































































It's a simple tool assisting people who search for UN jobs. Recommend use the '.exe' file in the releases area directly.

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

### Method 1: Use the Executable

You can get the latest '.exe' file in the releases area.

Or

To create a standalone `.exe` file:
```bash
pyinstaller --noconfirm --onefile --windowed --add-data "app/static;app/static" --name "UN_JD_Analysis_Tool" run.py
```
The result will be in the `dist/` folder. 

### 🛡️ Security Note for Windows Users
Since this is a standalone `.exe` without a paid digital signature, Windows SmartScreen or your browser might flag it as "unsupported" or "suspicious". 
1. **In Browser**: Choose "Keep" or "Trust" when downloading.
2. **On Run**: Click **"More info"** and then **"Run anyway"** in the blue pop-up.
3. This is a common behavior for open-source tools; the source code is fully available here for your review to ensure safety.

### Method 2: Run from Source (For Developers)

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
