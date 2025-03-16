# Company Profiles App

This is a web application built with **FastAPI** (Python backend), **HTMX** (frontend interactivity), and **ECharts** (data visualization). It allows users to select a company and view its profile, along with roles distribution visualizations across states.

---

## **Features**

- **Company Profile**: Displays details about the selected company (e.g., name, industry, headquarters, website).
- **Bar Chart**: Visualizes the distribution of roles across states for the selected company.
- **Pie Chart**: Shows the distribution of roles by job family for the selected company.
- **Dynamic Updates**: Uses HTMX to dynamically load data without refreshing the page.

---

## **Technologies Used**

- **Backend**: FastAPI (Python)
- **Frontend**: HTMX, Tailwind CSS, ECharts
- **Data**: CSV files (`company_attributes.csv`, `job_post_by_job_family.csv`, `job_post_by_city.csv`)

---

## **Prerequisites**

Before running the app, ensure you have the following installed:

1. **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
2. **Pip**: Python package manager (comes with Python).
3. **FastAPI**: Install via pip.
4. **Uvicorn**: ASGI server for running FastAPI apps.

---

## **Setup Instructions**

### **1. Clone the Repository**

Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/company-profiles-app.git
cd company-profiles-app
```

---

### **2. Install Dependencies**

Install the required Python packages:

```bash
pip install fastapi uvicorn pandas
```

---

### **3. Prepare Data Files**

Place your CSV files (`company_attributes.csv`, `job_post_by_job_family.csv`, `job_post_by_city.csv`) in the `static/data/` directory.

---

### **4. Run the Application**

Start the FastAPI server using Uvicorn:

```bash
venv\Scripts\activate
uvicorn main:app --reload
```

- The `--reload` flag enables auto-reloading when you make changes to the code.
- The app will be available at `http://127.0.0.1:8000`.

---

### **5. Access the Application**

Open your browser and navigate to:

```
http://127.0.0.1:8000
```

---

## **Project Structure**

```
company-profiles-app/
├── static/
│   ├── Google.png
│   ├── data/
│   │   ├── company_attributes.csv
│   │   ├── job_post_by_job_family.csv
│   │   └── job_post_by_city.csv
│   └── styles/
│       └── styles.css
├── templates/
│   └── index.html
│   └── company-profile.html
├── main.py
└── README.md
```

- **`static/data/`**: Contains the CSV files used for data.
- **`templates/`**: Contains the HTML template for the frontend.
- **`main.py`**: The FastAPI backend code.
- **`README.md`**: This file.

---

## **Endpoints**

### **1. Home Page**
- **URL**: `/`
- **Method**: `GET`
- **Description**: Renders the main page with a dropdown to select a company.

### **2. Company Profile**
- **URL**: `/company/{company_id}`
- **Method**: `GET`
- **Description**: Returns the HTML for the company profile.

### **3. Role Distribution**
- **URL**: `/data/distribution/{company_id}`
- **Method**: `GET`
- **Description**: Returns JSON data for the bar chart and pie chart.

---

## **Frontend Details**

### **HTML (HTMX)**
- The frontend uses **HTMX** to dynamically load the company profile and charts without refreshing the page.
- The dropdown triggers an HTMX request to fetch the company profile and update the page.

### **ECharts**
- **Bar Chart**: Shows the distribution of roles across states.
- **Pie Chart**: Shows the distribution of roles by job family.

### **Tailwind CSS**
- Used for styling the frontend components.

---

## **Customization**

### **Add More Companies**
- Add more companies to the `company_attributes.csv` file.

### **Modify Charts**
- Update the ECharts configuration in the `index.html` file to customize the charts.

### **Add More Visualizations**
- Use the existing data to create additional visualizations (e.g., line charts, scatter plots).

---

## **Troubleshooting**

### **1. CSV Files Not Found**
- Ensure the CSV files are placed in the `static/data/` directory.

### **2. HTMX Not Working**
- Check the browser console for errors. Ensure HTMX is properly included in the HTML file.

### **3. Charts Not Rendering**
- Verify that the backend is returning the correct JSON data for the charts.

---

## **Contributing**

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Contact**

For questions or feedback, please contact:
- **Your Name**: your.email@example.com
- **GitHub**: [your-username](https://github.com/your-username)

---

Enjoy using the Company Profiles App! 🚀

---

Let me know if you need further assistance!