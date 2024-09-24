import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection
import warnings

# Function from matplotlib 
# Draw colored path
def colored_line(x, y, c, ax, **lc_kwargs):
    """
    Plot a line with a color specified along the line by a third value.

    It does this by creating a collection of line segments. Each line segment is
    made up of two straight lines each connecting the current (x, y) point to the
    midpoints of the lines connecting the current point with its two neighbors.
    This creates a smooth line with no gaps between the line segments.

    Parameters
    ----------
    x, y : array-like
        The horizontal and vertical coordinates of the data points.
    c : array-like
        The color values, which should be the same size as x and y.
    ax : Axes
        Axis object on which to plot the colored line.
    **lc_kwargs
        Any additional arguments to pass to matplotlib.collections.LineCollection
        constructor. This should not include the array keyword argument because
        that is set to the color argument. If provided, it will be overridden.

    Returns
    -------
    matplotlib.collections.LineCollection
        The generated line collection representing the colored line.
    """
    if "array" in lc_kwargs:
        warnings.warn('The provided "array" keyword argument will be overridden')

    # Default the capstyle to butt so that the line segments smoothly line up
    default_kwargs = dict()
    default_kwargs.update(lc_kwargs)

    # Compute the midpoints of the line segments. Include the first and last points
    # twice so we don't need any special syntax later to handle them.
    x = np.asarray(x)
    y = np.asarray(y)
    x_midpts = np.hstack((x[0], 0.5 * (x[1:] + x[:-1]), x[-1]))
    y_midpts = np.hstack((y[0], 0.5 * (y[1:] + y[:-1]), y[-1]))

    # Determine the start, middle, and end coordinate pair of each line segment.
    # Use the reshape to add an extra dimension so each pair of points is in its
    # own list. Then concatenate them to create:
    # [
    #   [(x1_start, y1_start), (x1_mid, y1_mid), (x1_end, y1_end)],
    #   [(x2_start, y2_start), (x2_mid, y2_mid), (x2_end, y2_end)],
    #   ...
    # ]
    coord_start = np.column_stack((x_midpts[:-1], y_midpts[:-1]))[:, np.newaxis, :]
    coord_mid = np.column_stack((x, y))[:, np.newaxis, :]
    coord_end = np.column_stack((x_midpts[1:], y_midpts[1:]))[:, np.newaxis, :]
    segments = np.concatenate((coord_start, coord_mid, coord_end), axis=1)

    lc = LineCollection(segments, **default_kwargs)
    lc.set_array(c)  # set the colors of each segment

    return ax.add_collection(lc)

# Load data from csv
# odom_data = np.loadtxt("/home/user/Desktop/proj/ros_proj/path.csv",
#                  delimiter=",", dtype=float, skiprows=1)
odom_data = np.loadtxt("../read_rosbag/path.csv",
                 delimiter=",", dtype=float, skiprows=1)
x = odom_data[:, 0]
y = odom_data[:, 1]

# Create plot
fig, ax = plt.subplots()
fig.set_size_inches(15,12)
color = np.linspace(0, 2, x.size)
lines = colored_line(x, y, color, ax, linewidth=4, cmap="plasma")

# Calc axis limits
min_x = np.floor(np.min(x))
max_x = np.ceil(np.max(x))
min_y = np.floor(np.min(y))
max_y = np.ceil(np.max(y))

# Set similar scale for x and y
plot_size_x = max_x - min_x
plot_size_y = max_y - min_y
delta_size = plot_size_x - plot_size_y

if delta_size > 0:
    x_ticks = np.arange(min_x, max_x, 0.2)
    y_ticks = np.arange(min_y, max_y + delta_size, 0.2)
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y + delta_size)
else:
    x_ticks = np.arange(min_x, max_x + delta_size, 0.2)
    y_ticks = np.arange(min_y, max_y, 0.2)    
    ax.set_xlim(min_x, max_x + delta_size)
    ax.set_ylim(min_y, max_y)

ax.set_xticks(x_ticks)
ax.set_yticks(y_ticks)

# Plot and save
ax.set_title("Odometry path")
fig.colorbar(lines, ticks = [], label='start ---> finish')

plt.grid()
plt.savefig('path.png')
plt.show()
