# Markdown Image Converter

This Python script is designed to convert markdown files by processing images and handling local and network image links. The script utilizes PyQt5 for the graphical user interface (GUI) and includes functionality to choose source and target file paths, toggle between modifying the source file and creating a new file, and provide a progress bar and tooltip during the conversion process.

## Features

- **GUI Interface:** The script includes a graphical user interface created using PyQt5, allowing users to interactively choose source and target file paths.

- **Image Processing:** The script processes both local and network image links in a markdown file. It downloads network images and saves them to a specified folder while copying local images to the same folder.

- **Conversion Options:** Users can choose to modify the source file or create a new file during the conversion process.

- **Progress Feedback:** The GUI provides an indeterminate progress bar and tooltips to keep users informed about the conversion progress.

## Usage

1. **Run the Script:**
   - Execute the script using Python.
   ```bash
   python script_name.py
   ```

2. **Choose Source File:**

- Click the "Choose Source File" button to select the markdown file you want to convert.

3. **Choose Target Folder:**

- Click the "Choose Target Folder" button to specify the folder where converted images will be saved.

4. **Toggle Modification:**

- Use the toggle switch to choose between modifying the source file or creating a new file.

5. **Initiate Conversion:**

- Click the "Export" button to start the conversion process. The progress bar and tooltips will indicate the progress.

## Dependencies

- Python 3.x
- PyQt5
- qfluentwidgets

Install 

he required dependencies using the following:

```bash
pip install PyQt5 qfluentwidgets
```

**Note:** Ensure you have the required Python dependencies installed before running the script.

Make sure to replace "script_name.py" with the actual name of your script file. Additionally, if your project includes a license file, you may want to replace the "LICENSE" link with the actual link to your license file.