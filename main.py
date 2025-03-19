import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

# Initialize FastAPI and Jinja2 templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

company_data = pd.read_csv('static/data/company_attributes.csv')
job_post_by_city = pd.read_csv('static/data/job_post_by_city.csv')
job_post_by_job_family = pd.read_csv('static/data/job_post_by_job_family.csv')

# Route to serve the main page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "data": company_data})

# Route to fetch company profile
@app.get("/company/{company_id}", response_class=HTMLResponse)
async def get_company_profile(company_id: int, request: Request):
    # Filter company data for the specified company ID
    company_info_filtered = company_data[company_data['company_id'] == company_id]
    
    if company_info_filtered.empty:
        raise HTTPException(status_code=404, detail="Company not found")

    company_info = company_info_filtered.to_dict(orient='records')[0]
    
    # Ensure fields are not NaN or empty
    company_info['industry_list'] = company_info.get('industry_list', 'N/A') or 'N/A'
    
    # For showing the company profile page
    return templates.TemplateResponse('company_profile.html', {"request": request, 'company': company_info})

# Route to fetch role and city distribution data for the charts
@app.get("/data/distribution/{company_id}", response_class=JSONResponse)
async def get_distribution_data(company_id: int):
    # Filter data for the specified company ID
    city_data_filtered = job_post_by_city[job_post_by_city['company_id'] == company_id]
    job_family_data_filtered = job_post_by_job_family[job_post_by_job_family['company_id'] == company_id]

    if city_data_filtered.empty or job_family_data_filtered.empty:
        raise HTTPException(status_code=404, detail="Distribution data not found for the specified company")
    
    # For Nan values
    city_data_filtered = city_data_filtered.fillna(0).replace([float('inf'), float('-inf')], 0)
    job_family_data_filtered = job_family_data_filtered.fillna(0).replace([float('inf'), float('-inf')], 0)

    # Prepare data for the bar chart
    states = city_data_filtered['state_name'].tolist()
    position_counts = city_data_filtered['position_count'].tolist()
    
    print(states, 'states')
    # Prepare data for the pie chart 
    pie_roles_data = job_family_data_filtered[['job_family', 'position_count']].rename(
        columns={'job_family': 'name', 'position_count': 'value'}
    ).to_dict(orient='records')

    # Return the data as JSON
    return {
        "states": states,
        "position_counts": position_counts,
        "pie_roles_data": pie_roles_data
    }