
# A Close Look at Sea Level Rise
## Causes and importance
Anthropogenic climate change has lead to an increase in sea levels during the last century. There are two primary mechanisms for this, the first and more obvious is the melting of glaciers on land putting more water into the ocean, the second is thermal expansion due to the increase in ocean temperatures. I find that people are often surprised by the second mechanism because they think of thermal expansion as a small change, the key thing to remember here is that a change on the order of a few feet is small given that the average depth of the ocean is over 12000 feet! 

The consequences of sea level rise are serious and deserve consideration. Commerce is incredibly important to our modern economies, historically this has meant that major cities were built close to the ocean. Even if low lying cities aren't in danger of sinking into the ocean the higher sea level make storm surge a bigger problem; hurricanes also lose a lot of energy when they hit the land, pushing coastlines inland means storms will be more powerful when they hit populated areas.

## The Data
For simplicity I'm focused only on the East Coast of the United States. Below is pictured the sea level in millimeters by year at 5 locations.

![daily sea level](https://danielennis521.github.io/Math-Blog/Post%201%3A%20Sea%20Level%20Change/Sea%20Level%20Changes/graphs/basic%20sea%20level.png)

The ranges are wildly different between locations because they are measured against a fixed reference point at each site. For this reason, it's common to graph the "anomoly", that is, the distance from the mean over the whole time series. There are two things we need to tackle to make this data easier to work with. First, we can see outliers are either a result of error or possibly natural disaster; these points need to be removed so that they don't bias our analyses. Second, we want to average the data by year since the seasonal variability is of no interest for our purposes. 

We could remove outliers by hand since they're are not that many and we're looking at just 5 locations, but I wanted to design my analysis to be flexible enough to work on it's own in the event that I want to try it on more or different data. To achieve this we're filtering out points based on z-scores; the catch here is that since our data is obviously non-stationary, it has a trend that isn't flat. If we simply take the z-score of the sea level data as an outlier in the early part of our data, it might be missed since that value is "typical" later in the time series. To handle this we'll do an inital fit of the data and then compute the deviations from that trend curve, those deviations will give us a stationary time series that we can then filter based on the z-scores (Please see ending notes for nuances about this method and alternatives that may in general work better).

With the data appropriately filtered we compute the average level for each year so we don't see the seasonal variations, allowing us to focus on the long term trend.

![yearly sea level](https://danielennis521.github.io/Math-Blog/Post%201%3A%20Sea%20Level%20Change/Sea%20Level%20Changes/graphs/yearly%20sea%20level.png)

## Change at a Given Time
Often times you'll see sea level rise expressed as an average over some time period 'x inches in the last y years' or 'an average of x mm per decade since y'. These aren't inherently bad but they can easily be misleading or just non-informative. What we'd really like to know is what the current rate of change is. This can be estimated by considering the mean over a shorter time span, say the last 10 years, but this smaller sample size means our estimate is more likely to reflect shorter term fluctuations rather then the underlying trend. A longer mean will be less biased by short term effects but if our rate of change is itself changing then it will bias us towards the old rate of change. 
In order to incorporate the whole time series into our estimates we need a more flexible model. The approach will be to fit a polynomial to each dataset and then derive estimates for acceleration and instantaneous rates of change from that model.

## Non-linear fit and acceleration
To keep things simple we're fitting a quadratic polynomial to the yearly sea level data, $sea\ level = \beta_0 + \beta_1 \* year + \beta_2 \* year^2$. The fits in the figure below were obtained using the sklearn-learn python library.

![quadratic fit](https://danielennis521.github.io/Math-Blog/Post%201%3A%20Sea%20Level%20Change/Sea%20Level%20Changes/graphs/quadratic%20regression.png)

From basic calculus we know that $2 \* \beta_2$ is our estimated acceleration in sea level rise. We can therefore test for a significant change in the rate of sea level rise by constructing confidence intervals for $\beta_2$. The 95% confidence intervals are summarised in the table below:

![confidence intervals](https://danielennis521.github.io/Math-Blog/Post%201%3A%20Sea%20Level%20Change/Sea%20Level%20Changes/graphs/Confidence%20Intervals.png)

Each interval contains only positive values making the results consistent with the hypothesis that the rate of sea level rise is increasing (at least along the east coast at the 95% confidence level. Note, that relative to the interval width the lower bound values are well above 0, implying the statement actually holds at much higher confidence levels).  

We now turn our attention to estimating the rate of change at a particular point in time, in particular, we want to try and estimate the current rate of change. The rate of change at a given time is given by the derivative, $\beta_1 + 2 \* \beta_2 \* year$. Below are the rates of change and the associated confidence intervals,

![rate of change CIs](https://danielennis521.github.io/Math-Blog/Post%201%3A%20Sea%20Level%20Change/Sea%20Level%20Changes/graphs/rate%20of%20change%20CIs.png)

I want to pause and say a little about the construction of the confidence intervals. The most intuitive way to do this is to simply replace $\beta_1$ and $beta_2$ in our expression with their respective confidence intervals. Unfortunately the resulting interval is in general too wide, that is, it overstates the uncertainty in our estimate. This is due to covariance structure; $\beta_0$, $\beta_1$, and $beta_2$ are not independent of eachother because they are "working together" to fit the data. If we fix the value of $\beta_0$ then we'll have some ranges of plausible values for the others but if we fix $\beta_0$ at another value the ranges for the other parameters will change. 

## Comparison to Other Analyses
An paper published in [nature](https://www.nature.com/articles/s43247-024-01761-5) used satelite data to look at the sea level across the entire globe since 1993; the authors found an acceleration of 0.077 mm/year^2. Below are the accelerations for each of the locations in our analysis,

![Accelerations](https://danielennis521.github.io/Math-Blog/Post%201%3A%20Sea%20Level%20Change/Sea%20Level%20Changes/graphs/Acceleration.png)

While these are obviously much higher than the global average that isn't surprising. Looking at a map of that global satelite data created by [NOAA](https://www.climate.gov/news-features/understanding-climate/climate-change-global-sea-level) we can see that the sea level change along the US east coast has been changing much faster than much of the rest of the world. It's also worth noting that our analysis started with the 1970s so the different time frames may be affecting the regression analysis. 

## The Dangers of Extrapolation
This kind of analysis is very useful for getting us more accurate estimates of how the sea level has been changing. Being able to get a point estimate for the current rate of change is also incredibly valuable for understanding where the sea level will be in the next decade. It is, however, important to keep in mind that it isn't safe to assume this trend will hold forever. This analysis makes no reference to the actually physics involved nor the material realities that will ultimately limit how much the sea level can possibly rise. There's only so much ice that can melt and water can only heat up and undergo thermal expansion. It would be unreasonable to project sea levels out 100 years from now based on this analysis.

## Conclusion
This acceleration is in sea level rise is deeply concering and has severe implications for life in low-lying coastal areas. Rising sea levels mean it now takes less storm surge to reach further inland, it causes more erosion, it allows storms and waves to pass over natural barriers like coral reefs that traditionally absorb much of the energy before landfall. Analyzing the shifts in sea level rise can help give us a better picture of how our enviornment is changing and what we might expect in the near term.

