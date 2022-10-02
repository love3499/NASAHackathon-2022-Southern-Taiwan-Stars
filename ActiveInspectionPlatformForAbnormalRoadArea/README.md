# To deploy web server correctlly, please follow the deploy steps as below:

## Requirement:

1. OS: Windows 10 Home(19043.2006)
2. Webserver Framework: Windows Internet Information Services(Version 10.0.19041.2006)

## Deploy Steps:

1. Make sure your computer(server) is accessible to the internet(Because out API server will request third party datas from "中央氣象局開放資料平臺之資料擷取API", https://opendata.cwb.gov.tw/dist/opendata-swagger.html).
2. Deploy Web Server:
    *   Move all files to the server folder of Windows Internet Information Services.
    *   Open file "USGS.js" in the root folder, and edit line 191 to "http://localhost:8092/get_points" (Or your own domain).
    *   Startup the web server.
    *   Web server deployed successfully.
3. [Deploy API Server](https://github.com/love3499/NASAHackathon-2022-Southern-Taiwan-Stars/tree/main/APIServer)