# -*- coding: utf-8 -*-

import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'


class SortPoints:
    def __init__(self, points):
        self.points = points

    def sortX(self):
        return sorted(self.points, key=lambda p: p.x)

    def sortY(self):
        return sorted(self.points, key=lambda p: p.y)


def inputPoints(file_name):
    points = []
    with open(file_name, 'r') as file:
        for line in file:
            x, y = map(float, line.split())
            points.append(Point(x, y))
    return points


def calculateDistance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


def naiveClosestPair(points):
    n = len(points)
    min_distance = float('inf')
    closest_pair = None
    for i in range(n):
        for j in range(i + 1, n):
            distance = calculateDistance(points[i], points[j])
            if distance < min_distance:
                min_distance = distance
                closest_pair = (points[i], points[j])
    return min_distance, closest_pair


def closestPairDivideAndConquer(points_sorted_by_x, points_sorted_by_y, ax=None, steps=[]):
    n = len(points_sorted_by_x)

    # use naive for small input size (base case)
    if n <= 3:
        return naiveClosestPair(points_sorted_by_x)

    # divide step: split points into left and right halves
    mid = n // 2
    left_half = points_sorted_by_x[:mid]
    right_half = points_sorted_by_x[mid:]
    
    midpoint = points_sorted_by_x[mid].x

    # create y-sorted list left and right
    left_half_y = [p for p in points_sorted_by_y if p.x <= midpoint]
    right_half_y = [p for p in points_sorted_by_y if p.x > midpoint]

    # add division step for visualization
    if ax is not None:
        steps.append(("division", midpoint))

    # recursively find pairs left and right
    d_left, pair_left = closestPairDivideAndConquer(left_half, left_half_y, ax, steps)
    d_right, pair_right = closestPairDivideAndConquer(right_half, right_half_y, ax, steps)

    # find min distance and pair
    d = min(d_left, d_right)
    closest_pair = pair_left if d_left < d_right else pair_right

    # merge 
    strip = [p for p in points_sorted_by_y if abs(p.x - midpoint) < d]

    if ax is not None:
        steps.append(("strip", (strip, d)))  # 'strip' ve 'd' tuple 
        print(f"Current step: {steps[-1]}")


    for i in range(len(strip)):
        for j in range(i + 1, min(i + 7, len(strip))):  # Check at most 6 points ahead
            distance = calculateDistance(strip[i], strip[j])
            if distance < d:
                d = distance
                closest_pair = (strip[i], strip[j])

    # Add closest pair found in this step
    if ax is not None:
        steps.append(("closest_pair", closest_pair))

    return d, closest_pair


def closestPair(points, ax=None):
    points_sorted_by_x = sorted(points, key=lambda p: p.x)
    points_sorted_by_y = sorted(points, key=lambda p: p.y)
    steps = []
    d, closest_pair = closestPairDivideAndConquer(points_sorted_by_x, points_sorted_by_y, ax, steps)
    return d, closest_pair, steps


def animateClosestPair(points):
    fig, ax = plt.subplots()
    ax.set_xlim(min(p.x for p in points) - 10, max(p.x for p in points) + 10)
    ax.set_ylim(min(p.y for p in points) - 10, max(p.y for p in points) + 10)
    ax.set_title("Closest Pair of Points")

    # Scatter plot of all points
    x_coords = [p.x for p in points]
    y_coords = [p.y for p in points]
    ax.scatter(x_coords, y_coords, color="blue", s=10)
    # Add legend
    red_line = plt.Line2D([], [], color="red", linestyle="--", label="Division Line")
    orange_points = plt.Line2D([], [], color="orange", marker="o", linestyle="None", label="Strip Points")
    green_line = plt.Line2D([], [], color="green", linewidth=2, label="Closest Pair")
    lightblue_fill = plt.Line2D([], [], color="lightblue", alpha=0.2, linestyle="None", label="Left Region")
    lightgreen_fill = plt.Line2D([], [], color="lightgreen", alpha=0.2, linestyle="None", label="Right Region")
    ax.legend(handles=[red_line, orange_points, green_line, lightblue_fill, lightgreen_fill], loc="upper right")


    # Run closest pair algorithm and collect steps
    _, closest_pair, steps = closestPair(points, ax)

    lines = []

    def update(frame):
        nonlocal lines
        # Clear previous highlights
        for line in lines:
            line.remove()
        lines = []

        step = steps[frame]  # Get current step
        print(f"Processing step: {step}")  

        # Check if it's the last frame
        if frame == len(steps) - 1:
            print("Animation completed!")
        
            # print closest pairs
            if step[0] == "closest_pair":  
                p1, p2 = step[1]
                ax.text(
                    0.5, 0.9,  
                    f"Closest Pair: {p1} and {p2}\nDistance: {calculateDistance(p1, p2):.2f}",
                    transform=ax.transAxes,  
                    fontsize=12, color="black", ha="center", bbox=dict(facecolor='white', alpha=0.8)
                )
        
            ani.event_source.stop()  
            return  

        action = step[0]

        if action == "division":
            midpoint = step[1]
            # Draw division line
            line = ax.axvline(x=midpoint, color="red", linestyle="--", label="Division Line")
            lines.append(line)

            # Highlight left and right regions (optional visualization)
            ax.fill_betweenx(
                [min(p.y for p in points), max(p.y for p in points)],
                min(p.x for p in points), midpoint,
                color="lightblue", alpha=0.2, label="Left Region"
            )
            ax.fill_betweenx(
                [min(p.y for p in points), max(p.y for p in points)],
                midpoint, max(p.x for p in points),
                color="lightgreen", alpha=0.2, label="Right Region"
            )

        elif action == "strip":
            strip_points, d = step[1]  
            x_strip = [p.x for p in strip_points]
            y_strip = [p.y for p in strip_points]
            scatter = ax.scatter(x_strip, y_strip, color="orange", s=30, label="Strip Points")
            lines.append(scatter)

            # midpoint
            for prev_step in reversed(steps[:frame]):
                if prev_step[0] == "division":
                    midpoint = prev_step[1]
                    break
            print(f"Midpoint: {midpoint}, d: {d}")  
            ax.axvline(x=midpoint - d, color="orange", linestyle=":", label="Strip Boundary")
            ax.axvline(x=midpoint + d, color="orange", linestyle=":")

        elif action == "closest_pair":
            p1, p2 = step[1]
            # Highlight closest pair
            line = ax.plot([p1.x, p2.x], [p1.y, p2.y], color="green", linewidth=2, label="Closest Pair")
            lines.extend(line)







    ani = FuncAnimation(fig, update, frames=len(steps), repeat=False, interval=1000)
    plt.show()

# --------------------------------------------------------------------------------------------------------------------------------------------------
# main 

points = inputPoints('test_points.txt')
# points = inputPoints('points_.txt')

# print the closest pair of the divide and conquer
# print(closestPair(points))

# print closest pair naive
# print(naiveClosestPair(points))

animateClosestPair(points)


