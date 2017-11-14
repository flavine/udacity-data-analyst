"""
This .py file contains all the queries used to obtain the analysis for the bandung_indonesia.osm
"""
#how many amenities are there and what type?
QUERY1=""" SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='amenity'
GROUP BY value
ORDER BY num DESC
LIMIT 10;
"""
#how many tourism spots are there and what type?
QUERY2 = """ SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='tourism'
GROUP BY value
ORDER BY num DESC
LIMIT 10;
"""

#highest religion?
QUERY3= """SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='place_of_worship') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='religion'
GROUP BY nodes_tags.value
ORDER BY num DESC
LIMIT 3;
"""

#type of food cuisine that is most popular?
QUERY4="""SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='cuisine'
GROUP BY nodes_tags.value
ORDER BY num DESC
LIMIT 5;
"""

#list of cities
QUERY5=""" SELECT tags.value, COUNT(*) as count 
FROM (SELECT * FROM nodes_tags UNION ALL 
      SELECT * FROM ways_tags) tags
WHERE tags.key LIKE '%city'
GROUP BY tags.value
ORDER BY count DESC
LIMIT 5;
"""


