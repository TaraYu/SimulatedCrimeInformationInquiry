# Simulated Crime Information Inquiry
Our system is built for population and crime incident information at different neighborhoods in
Edmonton.Python implements this system’s interface and through SQL to achieve query. For the
plot part, we use import matplot to plan the plot. We use folium to the visualization of spatial data in
Leaflet maps.
## And here is the user guide:

When the program starts, it will prompt the user to input the database file name and choose a task
number(1-4), or exit the program by input E (and the user can select to exit anytime during the
program is running, if the user does not input exit, the program will start again when finishing a task )
1) If user input number 1, the program prompt user input a range of years (start year and end
year) and crime type. Then it will show the number of this type of crime per month in a bar
plot.
2) If user input number 2, the program prompt user input a number N, then it will show the
N-most populous and N-least populous neighborhoods with their population count in a map
by a html file.
3) if user input number 3, the program prompt user input a range of years and crime type and
a number N, then it will show the Top-N neighborhoods and their crime count where the
given crime type occurred most within the given range in a html file and open by the web
browser.
4) if user input number 4, the program prompt user input a range of year and a number N,
then show the Top-N neighborhoods with the highest crimes to population ratio within the
provided range. Also, show the most frequent crime type in each of these neighborhoods in a
html file.

This project was completed with Yifei Ma, Yuanming Chang