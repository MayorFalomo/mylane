import pandas as pd
from fastapi import Request
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates 
import numpy as np

companyData = pd.read_csv('static/data/company_attributes.csv')
companyStates = pd.read_csv('static/data/job_post_by_city.csv')
companyRoles =  pd.read_csv('static/data/job_post_by_job_family.csv')

app = FastAPI()

template = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/data/distribution/{company_id}', response_class=JSONResponse)
async def get_distribution(company_id: int):
    # Merge the dataframes
    merged_df = pd.merge(companyRoles, companyStates, on='company_id')

    # Filter the merged dataframe by the given company_id
    company_data = merged_df[merged_df['company_id'] == company_id]
    
    if company_data.empty:
        raise HTTPException(status_code=404, detail="Company ID not found")
    
    # Group by state and job family to get the distribution for the bar chart
    distribution_data = company_data.groupby(['state_name', 'job_family']).size().unstack(fill_value=0)
    # print(distribution_data, 'distribution')
    
    states = distribution_data.index.tolist() 
    job_families = distribution_data.columns.tolist()
    # print(job_families, 'roles')
    series_data = []

    for job_family in job_families:
        # Only include job families that have at least one role in any state
        if distribution_data[job_family].sum() > 0:
            series_data.append({
                'name': job_family,
                'type': 'bar',  # Specify bar chart type
                'data': distribution_data[job_family].tolist() 
            })

    # Prepare data for the pie chart
    pie_data = []
    for job_family in job_families:
        total_roles = distribution_data[job_family].sum()
        if total_roles > 0:
            pie_data.append({
                'name': job_family,
                'value': int(total_roles)  # Convert numpy.int64 to Python int
            })
    
    response_data = {
        'states': states,
        'job_families': [series['name'] for series in series_data],  # Legend labels for the bar chart
        'series': series_data,
        'pie_data': pie_data
    }
    
    return JSONResponse(content=response_data)

@app.get('/', response_class=HTMLResponse) #Here I'm specifying the kind of response I'm gonna be sending back which is an HTMLResponse
async def home(request: Request):
    return template.TemplateResponse('index.html', {"request": request, "data": companyData, })
# Here we define the route as company and give a params of compnay_id and define the response as an HTMLResponse
@app.get("/company/{company_id}", response_class=HTMLResponse)
async def get_profile(company_id: int, request: Request):
    company = companyData[companyData['company_id'] == company_id] # Here we check if the comapny Id provided matches one in the file
    
    if company.empty:
        raise HTTPException(status_code=404, detail="Company not found")
    
    company_info = company.to_dict(orient='records')[0]
    
    return template.TemplateResponse('company_profile.html', {"request": request, 'company': company_info})

# venv\Scripts\activate
# uvicorn main:app --reload
