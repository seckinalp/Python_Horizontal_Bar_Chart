import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from matplotlib.widgets import Button

# Load the data into a pandas DataFrame
df = pd.read_csv('city_populations.csv', usecols=['name', 'group', 'year', 'value'])

#Define a dictionary to map region names to colors
color_dict = pd.DataFrame.from_dict({
    'North America': '#b000b5',
    'Latin America': '#133337',
    'Europe': '#ff4040',
    'Asia': '#5accd0',
    'Africa': '#9467bd',
    'Middle East': '#777777',
    'India': '#8c564b'
}, orient='index', columns=['color'])

# define a function to create bar chart for each year
def draw_barchart(year):
    #filter the data for the current year
    df_year = df[df['year'].eq(year)].sort_values(by = 'value', ascending= True).tail(10)
    
    # map region names to colors
    colors = df_year['group'].map(color_dict['color'].fillna('#808080'))
    
    #create the horizontal bar chart
    ax.clear()
    ax.barh(df_year['name'],df_year['value'],color = colors, alpha = 0.6)
    dx = df_year['value'].max() / 200
    for i, (value,name,group) in enumerate(zip(df_year['value'],df_year['name'],df_year['group'])):
        ax.text(value - dx, i, name, size = 14, weight = 600, ha = 'right', va = 'bottom')
        ax.text(value + dx, i,group, size = 14, weight = 400, ha = 'left', va = 'bottom')
        ax.text(value + dx, i - 0.25 , f'{value:,.3f}', size = 14, ha = 'left', va = 'center')

    # add some additional customization
    ax.text(1.0, 0.4, year, transform = ax.transAxes, color = '#777777', size = 46, ha = 'right', weight = 800)
    ax.text(0, 1.06, 'Population', transform = ax.transAxes, size = 12, color = '#777777')
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x',colors = '#777777', labelsize = 12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which = 'major', axis = 'x', linestyle = '-')
    ax.set_axisbelow(True)
    ax.text(0, 1.15, 'Populations of Cities from 1500 to 2023', transform = ax.transAxes, size = 24, weight = 600, ha = 'left', va = 'top')
    plt.box(False)
    
# define a variable to keep track of the animation status

is_animating = True

# define a function to keep track of animation status
def toggle_animation(event):
    global is_animating
    if is_animating:
        animator.event_source.stop()
    else:
        animator.event_source.start()
    is_animating = not is_animating
        
# set up the figure and axis
fig, ax = plt.subplots(figsize = (15,8), dpi = 100)
animator = animation.FuncAnimation(fig,draw_barchart, frames= range (1500,2023), interval = 100)

# add a toggle button

toggle_button_ax = plt.axes([0.45,0.05,0.1,0.075])
toggle_button = Button(toggle_button_ax, 'Start / Stop', color = '#777777', hovercolor='#777777')
toggle_button.on_clicked(toggle_animation)

fig.subplots_adjust(bottom= 0.2)
plt.show()