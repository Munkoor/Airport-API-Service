# Airport API Service

Airport API Service - a reliable and convenient tool for accessing up-to-date
information about airports worldwide, simplifying data management and expanding
possibilities within the aviation industry.

### Features
1. **CRUD Functionality:** The API service provides Create, Read, Update, and Delete operations for various airport-related models, allowing you to manage data efficiently.

2. **JWT Authentication:** Secure your API with JSON Web Token (JWT) authentication. Users can obtain and use tokens to access protected endpoints.

3. **Throttling:** The service includes throttling mechanisms to prevent abuse and ensure fair usage of resources.

4. **Docker:** Docker is used for containerization and easy deployment. You can run the service in a Docker container with minimal configuration.

5. **Media Files:** The API supports the handling of media files, making it suitable for managing images, videos, or other multimedia content.

6. **API Documentation(Swagger):** is an API documentation and testing tool that allows you to automatically generate API documentation from a description of the API structure in YAML or JSON file format.


### DB Structure
![img_6.png](Screenshots of API/img_6.png)



### Installation

Python 3.10.x must be already installed

```commandline
git clone https://github.com/Munkoor/Airport-API-Service.git
cd APIService
pythone -m venv venv
source venv//Scripts//activate
pip install -r requirements.txt
pythone manage.py runserver
```

### Screenshots of different pages of Browsable API
![img.png](Screenshots of API/img.png)
![img_1.png](Screenshots of API/img_1.png)
![img_2.png](Screenshots of API/img_2.png)
![img_3.png](Screenshots of API/img_3.png)
![img_4.png](Screenshots of API/img_4.png)
![img_5.png](Screenshots of API/img_5.png)


