# G'day Salary Information Dashboard

![homepage](https://user-images.githubusercontent.com/90821623/174084300-c0ac6e54-4513-404a-8b6c-c42f0af62b55.gif)

> G'day Salary aims to provide salary information in IT field for candidates or graduates who do not have experience or limited experience in this field.

> This information board was built by three backbone data, salary, programming languages, and database systems.

---

### Table of Contents

- [Description](#description)
- [How To Broswe The Website](#how-to-broswe-the-website)
- [System Architecture](#system-architecture)
- [License](#license)
- [Author Info](#author-info)

---

## Description

G'day Salary applies the concept of data pipeline to extract, transform, and load (ETL) data to databases in order for dashboard to demonstrate useful information for visitors.

In order to achieve the goal above, here are five important processing stages.

1. Data Ingestion: Auto scrape human resource website.
2. Data Lake: Store all raw data into AWS S3
3. Data Preparation & Computation: Transform raw data to useful information.
4. Data Warehouse: Store all information into AWS RDS(MySQL), MongoDB(NoSQL), AWS S3.
5. Data Visualisation & Analytics: Visualise all valuable information to users.

#### Technologies

- Python: Flask, FlaskRESTful, BeautifulSoup, Boto3, OAuth2, mysql-connector, pymongo etc.
- Dockerfile
- HTML
- CSS
- Javascript
- Bootstrap
- Chart.js
- AWS: EC2, S3, RDS, CloudFront(CDN)
- MongoDB
- Nginx: https, Reverse proxy
- Git

[Back To The Top](#read-me-template)

---

## How To Broswe The Website
![Jun-17-2022 00-13-49](https://user-images.githubusercontent.com/90821623/174089821-90bd8076-1566-4ac5-87e0-af7f89fb868b.gif)



[Back To The Top](#read-me-template)

---

## System Architecture

![System Architecture](https://bootcamp-assignment.s3.ap-southeast-2.amazonaws.com/data_pipeline.png)

[Back To The Top](#read-me-template)

---

## Author Info

- Linkedin - [@Wilson](https://www.linkedin.com/in/wei-cheng-huang-wilson/)
- Website - [G'day Salary](https://www.engineersalaryquery.website/)

[Back To The Top](#read-me-template)
