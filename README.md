# G'day Salary Dashboard

![homepage](https://user-images.githubusercontent.com/90821623/174084300-c0ac6e54-4513-404a-8b6c-c42f0af62b55.gif)

> G'day Salary aims to provide salary information in IT field for candidates or graduates who do not have experience or limited experience in this field.

> This information board was built by three backbone data, salary, programming languages, and database systems.

---

### Table of Contents

- [Description](#description)
- [How To Broswe The Website](#how-to-broswe-the-website)
- [System Architecture](#system-architecture)
- [Database Architecture](#database-architecture)
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
- Git, CronJob

[Back To The Top](#gday-salary-dashboard)

---

## How To Broswe The Website

![Jun-17-2022 01-58-22](https://user-images.githubusercontent.com/90821623/174114363-b9855dab-6eb4-4a42-a255-2726c16fc7a9.gif)
The GIF above displays how you can search for further detailed information via G'day Salary.

![PLtable](https://user-images.githubusercontent.com/90821623/174091879-ecf68f85-1b82-4341-a951-8c1041f3a5bf.gif)
The second GIF shows the average salary and the existing job posts containing salaries in IT around Australia.<br>
In addition, the tables demonstrate the number of job positions based on the programming language or database skills you currently have.<br>
Users can also click on the state's name to link to a dedicated page.

![Screen Shot 2022-06-17 at 00 37 58](https://user-images.githubusercontent.com/90821623/174094778-cd68c270-58cc-4876-8825-0803f1a7aca3.png)
The normal distribution graph explains Australia's salary distribution.

![Jun-17-2022 01-37-34](https://user-images.githubusercontent.com/90821623/174110497-e42712a2-999d-4ca6-b335-0c879e7f5f4b.gif)
The page provides each state's detailed information; especially, users can have a more precise number of job posts related to the region they are looking for a job position..<br>

![Jun-17-2022 01-50-48](https://user-images.githubusercontent.com/90821623/174113652-bd9bc72c-5fe4-4bec-9b40-ef4712015d11.gif)
The membership system offers members a place to share their previous work experiences with other members. This system is designed to increase the members' engagement on our website.<br>

[Back To The Top](#gday-salary-dashboard)

---

## ETL Data Pipeline

![Screen Shot 2022-06-17 at 14 21 35](https://user-images.githubusercontent.com/90821623/174224348-62ac79e0-cfee-43c5-bde7-c45fc10a1182.png)

[Back To The Top](#gday-salary-dashboard)

---

## Database Architecture
![Screen Shot 2022-06-17 at 14 20 14](https://user-images.githubusercontent.com/90821623/174224159-76963b8f-f0cd-46f0-ad6b-d9a1d8c30536.png)


[Back To The Top](#gday-salary-dashboard)
---

## Author Info

- Linkedin - [@Wilson](https://www.linkedin.com/in/wei-cheng-huang-wilson/)
- Website - [G'day Salary](https://www.engineersalaryquery.website/)

[Back To The Top](#gday-salary-dashboard)
