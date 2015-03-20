import csv
import requests
from geopy.geocoders import GoogleV3

with open( '/Volumes/Data/Courses/Coding for Journalists/mb10.github.io/charts/OaklandSchools.csv','rU') as csv_file, open('/Volumes/Data/Courses/Coding for Journalists/mb10.github.io/charts/OaklandSchoolsNEW.csv', 'wb') as new_csv:
    reader = csv.DictReader(csv_file)
    geolocator = GoogleV3()
    fields = list(reader.fieldnames)
    fields.extend(["Normalized Address","Latitude","Longitude","Altitude"])
    writer = csv.DictWriter(new_csv, fields)
    writer.writeheader()
    for line in reader:
        address = line["Address"] + ', ' + line["City"] + ', ' + line["Zip"]
        location = geolocator.geocode(address)
        if location:
            url = "https://maps.googleapis.com/maps/api/elevation/json?locations={},{}".format(location.latitude, location.longitude)
            result = requests.get(url)
            result = result.json()
            line["Latitude"] = location.latitude
            line["Longitude"] = location.longitude
            line["Normalized Address"] = location.address
            line["Altitude"] = result['results'][0]['elevation']
            writer.writerow(line)
        else:
            raise StandardError("no address found for " + address)
