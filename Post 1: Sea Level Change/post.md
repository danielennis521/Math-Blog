# A Close Look at Sea Level Rise
## Causes and importance
Anthropogenic climate change has lead to an increase in sea levels during the last century. There are two primary mechanisms for this, the first and more obvious is the melting of glaciers on land putting more water into the ocean, the second is thermal expansion due to the increase in ocean temperatures. I find that people are often surprised by the second mechanism because they think of thermal expansion as a small change, the key thing to remember here is that a change on the order of a few feet is small given that the average depth of the ocean is over 12000 feet! 

The consequences of sea level rise are serious and deserve consideration. Commerce is incredibly important to our modern economies, historically this has meant that major cities were built close to the ocean. Even if low lying cities aren't in danger of sinking into the ocean the higher sea level make storm surge a bugger problem; hurricanes also lose a lot of energy when they hti the land, pushing coastlines inland means storms will be more powerful when they hit populatied areas.

## The Mean is Not Enough
Often times you'll see sea level rise expressed as an average over some time period 'x inches in the last y years' or 'an average of x mm per decade since y'. These aren't inherently bad but they can easily be misleading or just non-informative. 

## Changes in sea level change
For simplicity I'm focused only on the East Coast of the United States. Below is pictured the sea level in millimeters by year at 5 locations.
![daily sea level](https://github.com/danielennis521/Math-Blog/blob/main/Post%201%3A%20Sea%20Level%20Change/Sea%20Level%20Changes/graphs/basic%20sea%20level.png)
The ranges are wildly different between locations because they are measured against a fixed reference point at each site. for this reason it's common to graph the "anomoly", that is, the distance from the mean over the whole time series. There are two things we need to deal with to make this data easier to work with. First, we can see outliers that are either a result of error or possibly natural disaster; these point need to be removed so that they dont bias our analyses. Second, we want to average the data by year since the seasonal variability is of no interest for our purposes. 



(discuss need to clean and aggregate data)
(explain method for filtering outliers)
(introduce refined yearly data)
![yearly sea level](https://github.com/danielennis521/Math-Blog/blob/main/Post%201%3A%20Sea%20Level%20Change/Sea%20Level%20Changes/graphs/yearly%20sea%20level.png)

## Non-linear fit and acceleration

![quadratic fit](https://github.com/danielennis521/Math-Blog/blob/main/Post%201%3A%20Sea%20Level%20Change/Sea%20Level%20Changes/graphs/quadratic%20regression.png)

![rate of change CIs](https://github.com/danielennis521/Math-Blog/blob/main/Post%201%3A%20Sea%20Level%20Change/Sea%20Level%20Changes/graphs/rate%20of%20change%20CIs.png)
