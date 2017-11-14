
# Flight Data Visualization from 2007
The data set is obtained from [RITA](http://stat-computing.org/dataexpo/2009/the-data.html) and contains flight delay and performance information on the year of 2007.

2007 is the year with the highest number of delays for the past 15 years so it will be interesting to look at the data and uncover any trends that can help us understand more about what is happening with flights on 2007.


**Summary:** 2007 has the number of flight delays in the past decade. These visualization attempts to explain the trends with time and location and the causes of the high number in flight delays in 2007. Focusing in Chicago, the city with the highest number of delays, the visualization trues to uncover the causes of the flight delays and cancellations there.

**Design:**

__Initial Design:__  https://public.tableau.com/profile/fillarry.susanto#!/vizhome/Flights2007-Story/Story1

*Page 1* - Line graph is used to show trend with time (months), different color is used to show which line corresponds to which type of arrival. Start and end axes from 1 to 12 because other numbers does not have any meaning since we are talking about months. Legend is also included to identify which color corresponds to which type of delay.
Color hue is used to show the ordinal comparison of the number of delays per state. Comparing the map graphs left to right makes it easier to get a sense of comparison between arrival and departure delays in different state. Legends is included to get a sense what the color hue means in number of delays.

*Page 2* - Both color hue and size is used to accentuate the highest numbers of arrival delays per city. Map is used to point out the location of the high delays. Legend on size is also used to tell the reader approximately how many delays there are. Tooltip is available for users to know the exact number of delays when mouse is hovered on the point on the map.
Bar graph is used to contrast the different number of delays per reason. It is ordered from highest to lowest so it is easy to identify which reason has the most effect. Actual numbers are also shown on top of the bar graph for even better comparison.

*Page 3* - Line chart is used again to show effect with time. Different color line represent the different cancellation reasons, which is shown in legend. Extra annotation is also added beside each end of line so the reader can quickly identify which line corresponds to which reason.

__After feedback:__ https://public.tableau.com/profile/fillarry.susanto#!/vizhome/Flights2007-Story-V2/Story1?publish=yes

Changed the wording of the page headings for the story so they are clearer and more connected.

*Page 1* - Did not change 1 2 3 for month to Jan, Feb, Mar, etc because unable to create line graph as it is not numeric anymore. Made sure text is visible.

*Page 2* - Change color pallete for the map graph to red and add borders. Change title of the graph to indicate total time. Added transition to focus on Chicago after the map graph.

*Page 3* - Did not change 1 2 3 for month to Jan, Feb, Mar, etc because unable to create line graph as it is not numeric anymore. Changed line color of "Weather". Addeed title to the graph pointing out that it is cancellation in Chicago.

**Feedback:**

"The narratives at the top of the plots are weird and disconnected between each other. Also, it sounds more like a conclusion then a heading and introduction to the charts that each page represent. Also the text on the first page seems to be incomplete or covered by the map diagrams. Also, instead of month 1 2 3 change it to Jan Feb March, that will easier to understand. Indicate in the title for the bar graph in the second page of the story that it is about the total time of delay not number of delays which is what you have been showing the previous graphs. Also, change the color between carrier and weather, they will be hard to differentiate for the deutans." - MH

"The color dot for Dallas-Fort Worth cannot be seen due to the similar shade with background. Change it to something that is more contrasting so we can see the dots on the map for the map diagram on the second page of the story. Also, add the legend for the color even though it's redundant, or else the color will not mean anything. In addition, on the first page, make the "These maps exclude Alaska" text more noticable by boxing it or changing the font color. - LS

"The visualization that I observed seems to compose of three things:
a. Departure/Arrival delay per origin/destination state (both peaks around mid/end of year, makes sense due to holiday season)
b. Comparison between arrival delay causes in 2007 at Chicago (interesting that late aircraft is the major cause by far)
c. Comparison plot between cancellation causes in 2007 at Chicago

The questions that I have is as follows:
- for part b, why only shows the bar plot for Chicago while there are two other cities in the  map above it?
- for part c, plot legend/axis does not clearly show that it represent Chicago (I misunderstood it was for overall USA at first sight)

For me, the three visualizations are fine by themselves but both the content and the results don't really relate to each other. -RS"

**Resources:**

Information on the dataset is obtained from:
- http://aspmhelp.faa.gov/index.php/Types_of_Delay
- http://stat-computing.org/dataexpo/2009/the-data.html
- https://www.bts.gov/explore-topics-and-geography/topics/airline-time-performance-and-causes-flight-delays
- https://www.rita.dot.gov/bts/help/aviation/html/understanding.html



```python

```
