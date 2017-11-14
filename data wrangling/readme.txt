List of .py files for this project:

1. tags.py - check if there are problematic tags or not
2. audit-streetname.py - audits all the streetname in the osm file and see if it matches the street type critereia
3. audit-postcode.py - audits all the postcode in the osm file and see if it starts with 4 and has 5 digits
4. keys.py - lists all the different key names and gives keys that are unusual (less than 5 occurence)
5. update.py - updates street names, keys and user/user id into correct format
6. data.py - converts osm into csv file in the right shape and matches pre existing schema
7. schema.py - schema for sql conversion
8. queries.py - list of sql queries used to obtain analysis

Also used the sample report: https://gist.github.com/carlward/54ec1c91b62a5f911c42#file-sample_project-md for inspiration!