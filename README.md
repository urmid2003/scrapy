# Scrapy Project for Zomato Reviews and Menu

This repository contains two Scrapy projects:
1. **Reviews Scraper**: Scrapes reviews from Zomato restaurant pages.
2. **Menu Scraper**: Scrapes menus from Zomato restaurant pages.

Both projects are deployed on Scrapyd and store the scraped data in a MySQL database via pipelines. Additionally, the data is visualized on a dashboard to compare different restaurants' review ratings, page ratings, and menus.

## Setup Instructions

### Prerequisites
- Python (>=3.7)
- Virtual Environment support (e.g., `venv` or `virtualenv`)
- MySQL database
- VS Code (recommended for development)
- Scrapyd (for deployment)

### Steps

#### 1. Create a Virtual Environment
```bash
python -m venv env
```
Activate the virtual environment:
- On Windows:
  ```bash
  .\env\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source env/bin/activate
  ```

#### 2. Install Requirements
```bash
pip install -r requirements.txt
```

#### 3. Navigate to the Project Folder
Use VS Code or your terminal to `cd` into the respective folder:
```bash
cd zomato_comp_item_analysis/
```
Or:
```bash
cd zomato_competiton_analysis/
```

#### 4. Run the Spider
To start scraping data, use the following command:
```bash
scrapy crawl <spider-name>
```
Replace `<spider-name>` with the name of the spider defined in the project.

### Deployment Instructions

#### 1. Package and Deploy the Project
Navigate to the spiders folder of each project:
```bash
cd zomato_comp_item_analysis//spiders
```
Or:
```bash
cd zomato_competiton_analysis/spiders
```

Deploy the project to Scrapyd using the following command:
```bash
scrapyd-deploy
```
This will package and upload the Scrapy project to the Scrapyd server.

### Data Storage

#### 1. Scraping Process
- Data is defined and structured using Scrapy **Items**.
- Scraped data is passed through a pipeline where it is cleaned and validated.

#### 2. Database Integration
- The pipeline dumps the data into a MySQL database using an API.
- Ensure your database credentials and API endpoints are properly configured in the pipeline settings.
![image](https://github.com/user-attachments/assets/629c39da-2e47-4e66-9fa5-b63e24bcac78)
![image](https://github.com/user-attachments/assets/62954d18-5276-483d-8abe-2b87c343e8c4)



### Dashboard
A dashboard has been created to visualize and compare:
- **Review Ratings**: Compare customer feedback across restaurants.
- **Page Ratings**: Analyze the Zomato page ratings.
- **Menus**: Compare available menu items and prices.

The dashboard provides a comprehensive view of restaurant performance and offerings, helping with data-driven decision-making.
![image](https://github.com/user-attachments/assets/b6ad6150-5fba-4508-82cd-287358ff1cca)
![image](https://github.com/user-attachments/assets/d1be50e9-027d-4f22-8397-f4f6813f5f7b)



## Repository Structure
```
root
├── reviews_scraper
│   ├── spiders
│   ├── pipelines.py
│   ├── items.py
│   ├── settings.py
│   └── ...
├── menu_scraper
│   ├── spiders
│   ├── pipelines.py
│   ├── items.py
│   ├── settings.py
│   └── ...
├── requirements.txt
└── README.md
```



