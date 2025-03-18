import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Load data from CSV files
company_data = pd.read_csv('static/data/company_attributes.csv')
job_post_by_city = pd.read_csv('static/data/job_post_by_city.csv')
job_post_by_job_family = pd.read_csv('static/data/job_post_by_job_family.csv')

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/data/distribution/{company_id}', response_class=JSONResponse)
async def get_distribution(company_id: int):
    # Merge job postings data by company ID
    merged_data = pd.merge(job_post_by_job_family, job_post_by_city, on='company_id')
    
    print(merged_data, 'merged Daara')
    # Filter data for the specified company ID
    company_data_filtered = merged_data[merged_data['company_id'] == company_id]
    
    print(company_data_filtered, 'company filtered')
    if company_data_filtered.empty:
        raise HTTPException(status_code=404, detail="Company ID not found")

    # Group data by job family (role) and state
    distribution = company_data_filtered.groupby(['job_family', 'state_name']).size().unstack(fill_value=0)

    # Prepare data  bar chart
    roles = distribution.index.tolist()  # List of job families (roles)
    states = distribution.columns.tolist()  # List of states
    series_data = []

    for role in roles:
        total_roles = distribution.loc[role].sum()
        if total_roles > 0:
            series_data.append({
                'name': role,
                'type': 'bar',
                'data': distribution.loc[role].tolist()
            })

    # Prepare data for the pie chart - Roles
    pie_roles_data = [
        {'name': role, 'value': int(distribution.loc[role].sum())}
        for role in roles if distribution.loc[role].sum() > 0
    ]

    # Prepare data for pie chart - States
    state_totals = company_data_filtered['state_name'].value_counts()
    pie_states_data = [
        {'name': state, 'value': int(count)}
        for state, count in zip(state_totals.index, state_totals)
    ]

    # response data
    response_data = {
        'states': states,
        'roles': roles,
        'series': series_data,
        'pie_roles_data': pie_roles_data,
        'pie_states_data': pie_states_data
    }
    
    return JSONResponse(content=response_data)

@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    # Render the home page with company data
    return templates.TemplateResponse('index.html', {"request": request, "data": company_data})

@app.get("/company/{company_id}", response_class=HTMLResponse)
async def get_profile(company_id: int, request: Request):

        # Filter company data for the specified company ID
    company_info_filtered = company_data[company_data['company_id'] == company_id]
    if company_info_filtered.empty:
        raise HTTPException(status_code=404, detail="Company not found")

    company_info = company_info_filtered.to_dict(orient='records')[0]
    
     # Ensure fields are not NaN or empty
    company_info['industry_list'] = company_info.get('industry_list', 'N/A') if pd.notna(company_info.get('industry_list')) else 'N/A'
    # Render the company profile page
    return templates.TemplateResponse('company_profile.html', {"request": request, 'company': company_info})

# venv\Scripts\activate
# uvicorn main:app --reload
