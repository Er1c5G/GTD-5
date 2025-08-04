from jinja2 import Template

with open("template.html", "r") as file:
    template_str = file.read()


jinjaTemplate = Template(template_str)

emailData = {
    "sites": [
        {
        "name": "PTAIBC01DS1",
        "dataReceived": "True",
        "dataCalculated": "True",
        "fileSize": "3.12MB",
        "remarks": "Raw file is OK"
        },
        {
        "name": "NLSNBC01DS1",
        "dataReceived": "False",
        "dataCalculated": "False",
        "fileSize": "",
        "remarks": "No raw file found"
        },
        {
        "name": "FSJNBC01DS2",
        "dataReceived": "False",
        "dataCalculated": "False",
        "fileSize": "",
        "remarks": "No raw file found"
        },
        {
        "name": "VANCBC03DS1",
        "dataReceived": "False",
        "dataCalculated": "False",
        "fileSize": "",
        "remarks": "No raw file found"
        },
        {
        "name": "HANYBC01DS1",
        "dataReceived": "False",
        "dataCalculated": "False",
        "fileSize": "",
        "remarks": "No raw file found"
        },
        {
        "name": "LNGLBC01DS1",
        "dataReceived": "False",
        "dataCalculated": "False",
        "fileSize": "",
        "remarks": "No raw file found"
        }
    ]
}


emailContent = jinjaTemplate.render(emailData)

print(emailContent)
