# Restaurant Uptime & Downtime Monitoring System

This project is a Django-based backend system designed to monitor the uptime and downtime of restaurants in the US. The system generates reports that provide restaurant owners with insights into how often their stores go inactive during business hours.

## Project Overview

### Key Features

- **Efficient Data Loading**: We utilize a Django management command to load CSV files in batches, significantly reducing the time required to ingest large datasets.
- **Function-Based Views**: The project is implemented using Django's function-based views (FBVs), providing a simple and straightforward approach to handling requests and responses.
- **Report Generation and Retrieval**: The system offers two main API endpoints for generating and retrieving uptime/downtime reports, making it easy for restaurant owners to monitor their stores' status.

### API Endpoints

1. **`/trigger_report/`**
   - **Method**: POST
   - **Description**: Triggers the report generation process.
   - **Output**: Returns a JSON object containing a unique `report_id`, which can be used to check the status or retrieve the report.

   Example response:
   ```bash
   {
       "report_id": "abc123"
   }

2. **`/get_report/`**
   - **Method**: GET
   - **Description**: Retrieves the report status or the generated CSV report.
   - **Input**: report_id as a query parameter.
   - **Response**:
        - If the report is still generating, it returns {"status": "Running"}.
        - If the report generation is complete, it returns Complete along with a downloadable CSV file.
# Restaurant Uptime & Downtime Monitoring System

This project is a Django-based backend system designed to monitor the uptime and downtime of restaurants in the US. The system generates reports that provide restaurant owners with insights into how often their stores go inactive during business hours.

## Project Overview

### Key Features

- **Efficient Data Loading**: We utilize a Django management command to load CSV files in batches, significantly reducing the time required to ingest large datasets.
- **Function-Based Views**: The project is implemented using Django's function-based views (FBVs), providing a simple and straightforward approach to handling requests and responses.
- **Report Generation and Retrieval**: The system offers two main API endpoints for generating and retrieving uptime/downtime reports, making it easy for restaurant owners to monitor their stores' status.

### API Endpoints

1. **`/trigger_report/`**
   - **Method**: POST
   - **Description**: Triggers the report generation process.
   - **Output**: Returns a JSON object containing a unique `report_id`, which can be used to check the status or retrieve the report.

   Example response:
   ```bash
   {
       "report_id": "abc123"
   }

2. **`/get_report/`**
   - **Method**: GET
   - **Description**: Retrieves the report status or the generated CSV report.
   - **Input**: report_id as a query parameter.
   - **Response**:
        - If the report is still generating, it returns {"status": "Running"}.
        - If the report generation is complete, it returns Complete along with a downloadable CSV file.

### How to Set Up and Run the Project

1. **Clone the Repository**

   ```bash
   git clone https://github.com/krishna-teja18/restaurant-monitoring-system.git
   cd restaurant_status

2. **Set Up the Virtual Environment**

It's recommended to use a virtual environment to manage dependencies.

    python3 -m venv venv
    venv\Scripts\activate 

3. **Install Dependencies**

Install the required Python packages:

    pip install -r requirements.txt

4. **Apply Migrations**

Run the following commands to apply the migrations and set up the database:

    python manage.py migrate

5. **Load the CSV Data**

Use the provided Django management command to load the CSV data:

    python manage.py load_data

This command efficiently ingests the CSV data into the database, minimizing load times by processing the data in manageable chunks.

6. **Start the Development Server**

    ```bash
    python manage.py runserver

7. **Trigger a Report Generation**

Hit the following url in the browser to the /trigger_report/ endpoint:

    http://127.0.0.1:8000/trigger_report/

This will return a JSON response with a report_id.

8. **Retrieve the Generated Report**

After triggering the report, use the report_id obtained to poll the /get_report/ endpoint:

    http://127.0.0.1:8000/get_report/abc123

If the report is still processing, you will receive a status of Running. Once the report is complete, the endpoint will return a CSV file for download.

### Additional Implementation Details

- **Management Commands**: We've implemented custom Django management commands to handle large CSV files efficiently, loading data into the database in batches.
- **Function-Based Views**: The project uses function-based views for API endpoints, providing a clear and concise approach to handling requests.
- **CSV Report**: The generated report is a CSV file that details uptime and downtime metrics for each store, based on the data ingested from the provided sources.
