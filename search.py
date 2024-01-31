import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.animation as animation
import math
from matplotlib.path import Path

from utils import *
from grid import *


def move_up(current):
    temp1 = current[0]
    temp2 = current[1]
    temp2 = temp2+1
    if 50 >= temp1 >= 0 and 50 >= temp2 >= 0 and not check_enclosure(Point(temp1, temp2)):
        return Point(temp1, temp2)
    return 0


def move_down(current):
    temp1 = current[0]
    temp2 = current[1]
    temp2 = temp2-1
    if 50 >= temp1 >= 0 and 50 >= temp2 >= 0 and not check_enclosure(Point(temp1, temp2)):
        return Point(temp1, temp2)
    return 0


def move_left(current):
    temp1 = current[0]
    temp2 = current[1]
    temp1 = temp1-1
    if 50 > temp1 >= 0 and 50 > temp2 >= 0 and not check_enclosure(Point(temp1, temp2)):
        return Point(temp1, temp2)
    return 0


def move_right(current):
    temp1 = current[0]
    temp2 = current[1]
    temp1 = temp1+1
    if 50 > temp1 >= 0 and 50 > temp2 >= 0 and not check_enclosure(Point(temp1, temp2)):
        return Point(temp1, temp2)
    return 0


def check_enclosure(point):
    for poly in enclosure_vertices:
        path = Path(poly)
        if path.contains_point(point.to_tuple(), radius=0.1) or path.contains_point(point.to_tuple(), radius=-0.1):
            return True
    return False


def check_turf(point):
    for poly in turf_vertices:
        path = Path(poly)
        if path.contains_point(point.to_tuple(), radius=0.1) or path.contains_point(point.to_tuple(), radius=-0.1):
            return True
    return False


def get_child(node):
    child_node = [move_up(node), move_right(node), move_down(node), move_left(node)]
    child_node = [c for c in child_node if c is not 0]
    return child_node


def breadth_first(source, dest):
    count = 0
    current = Node(source, 0, 0)
    frontier = Queue()
    frontier.push(current)
    reached = [current.state]
    while frontier:
        current = frontier.pop()
        child = expand(current)
        count = count+1
        for c in child:
            s = c.state
            if s == dest:
                print("Nodes Expanded = " + str(count))
                return c
            if c.state not in reached:
                reached.append(c.state)
                frontier.push(c)
    return 0


def expand(node):
    s = node.state
    child = get_child(s.to_tuple())
    for c in child:
        cost = calculate_cost(node, c)
        yield Node(c, node, cost)


def depth_first(source, dest):
    count = 0
    current = Node(source, 0, 0)
    frontier = Stack()
    frontier.push(current)
    reached = [current.state]
    while frontier:
        current = frontier.pop()
        child = expand(current)
        count = count + 1
        for c in child:
            s = c.state
            if s == dest:
                print("Nodes Expanded = " + str(count))
                return c
            if c.state not in reached:
                reached.append(c.state)
                frontier.push(c)
    return 0


def best_first(source, dest):
    count=0
    current = Node(source, 0, 0)
    frontier = PriorityQueue()
    frontier.push(current, calculate_distance(source, dest))
    reached = [current.state]
    while frontier:
        current = frontier.pop()
        if current.state == dest:
            print("Nodes Expanded = " + str(count))
            return current
        child = expand(current)
        count=count+1
        for c in child:
            s = c.state
            if c.state not in reached or c.cost < current.cost:
                reached.append(s)
                frontier.push(c, calculate_distance(dest, c.state))
    return 0


def a_star(source, dest):
    count = 0
    current = Node(source, 0, 0)
    frontier = PriorityQueue()
    frontier.push(current, calculate_distance(source, dest))
    reached = [current.state]
    while frontier:
        current = frontier.pop()
        if current.state == dest:
            print("Nodes Expanded = " + str(count))
            return current
        child = expand(current)
        count = count + 1
        for c in child:
            s = c.state
            if c.state not in reached or c.cost < current.cost:
                reached.append(s)
                frontier.push(c, (calculate_distance(dest, c.state)+calculate_cost(current, c.state)+current.cost))
    return 0


def calculate_distance(dest, child):
    x1, y1 = dest.to_tuple()
    x2, y2 = child.to_tuple()
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_cost(parent, child):
    if check_turf(child):
        child.cost = parent.cost + 1.5
    else:
        child.cost = parent.cost + 1
    return child.cost


def retrieve_path(solution_node, s):
    path = []
    path.append(solution_node)
    current = solution_node
    while s.state != path[-1].state:
        current = current.parent
        path.append(current)
    return path


def gen_polygons(worldfilepath):
    polygons = []
    with open(worldfilepath, "r") as f:
        lines = f.readlines()
        lines = [line[:-1] for line in lines]
        for line in lines:
            polygon = []
            pts = line.split(';')
            for pt in pts:
                xy = pt.split(',')
                polygon.append(Point(int(xy[0]), int(xy[1])))
            polygons.append(polygon)
    return polygons


if __name__ == "__main__":
    epolygons = gen_polygons('TestingGrid/world1_enclosures.txt')
    tpolygons = gen_polygons('TestingGrid/world1_turfs.txt')
    enclosure_vertices=[]
    turf_vertices = []

    source = Point(8, 10)
    dest = Point(43, 45)


    fig, ax = draw_board()
    draw_grids(ax)
    draw_source(ax, source.x, source.y)  # source point
    draw_dest(ax, dest.x, dest.y)  # destination point

    # Draw enclosure polygons
    for polygon in epolygons:
        for p in polygon:
            draw_point(ax, p.x, p.y)
    for polygon in epolygons:
        zone=[]
        for p in polygon:
            zone.append((p.x, p.y))
        enclosure_vertices.append(zone)
    for polygon in epolygons:
        for i in range(0, len(polygon)):
            draw_line(ax, [polygon[i].x, polygon[(i + 1) % len(polygon)].x],
                      [polygon[i].y, polygon[(i + 1) % len(polygon)].y])

    # Draw turf polygons
    for polygon in tpolygons:
        for p in polygon:
            draw_green_point(ax, p.x, p.y)
    for polygon in tpolygons:
        zone=[]
        for t in polygon:
            zone.append((p.x, p.y))
        turf_vertices.append(zone)
    for polygon in tpolygons:
        for i in range(0, len(polygon)):
            draw_green_line(ax, [polygon[i].x, polygon[(i + 1) % len(polygon)].x],
                            [polygon[i].y, polygon[(i + 1) % len(polygon)].y])

    print("Breadth First Search Summary: ")
    solt = breadth_first(source, dest)
    print("solution cost: " + str(solt.cost))
    res_path = []
    nodes = retrieve_path(solt, Node(source, 0, 0))
    for r in nodes:
        res_path.append(r.state)
    res_path.reverse()

    for i in range(len(res_path) - 1):
        draw_result_line(ax, [res_path[i].x, res_path[i + 1].x], [res_path[i].y, res_path[i + 1].y], 'red')
        plt.pause(0.1)

    #plt.show()

    print("Depth First Search Summary: ")
    solt = depth_first(source, dest)
    print("solution cost: " + str(solt.cost))
    res_path1 = []
    nodes = retrieve_path(solt, Node(source, 0, 0))
    for r in nodes:
        res_path1.append(r.state)
    res_path1.reverse()

    for i in range(len(res_path1) - 1):
        draw_result_line(ax, [res_path1[i].x, res_path1[i + 1].x], [res_path1[i].y, res_path1[i + 1].y], 'yellow')
        plt.pause(0.1)

    #plt.show()

    print("Greedy Best First Search Summary: ")
    solt = best_first(source, dest)
    print("solution cost: " + str(solt.cost))
    res_path = []
    nodes = retrieve_path(solt, Node(source, 0, 0))
    for r in nodes:
        res_path.append(r.state)
    res_path.reverse()

    for i in range(len(res_path) - 1):
        draw_result_line(ax, [res_path[i].x, res_path[i + 1].x], [res_path[i].y, res_path[i + 1].y], 'orange')
        plt.pause(0.1)

    #plt.show()

    print("A* Search Summary: ")
    solt = a_star(source, dest)
    print("solution cost: " + str(solt.cost))
    res_path = []
    nodes = retrieve_path(solt, Node(source, 0, 0))
    for r in nodes:
        res_path.append(r.state)
    res_path.reverse()

    for i in range(len(res_path) - 1):
        draw_result_line(ax, [res_path[i].x, res_path[i + 1].x], [res_path[i].y, res_path[i + 1].y], 'blue')
        plt.pause(0.1)

    plt.show()





