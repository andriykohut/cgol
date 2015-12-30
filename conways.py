#!/usr/bin/env python3
import argparse
import curses
import itertools
import random
import time

from io import StringIO


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--population', type=int, dest='population')
    parser.add_argument('-s', '--step-duration', type=float, default=0.1, dest='step')
    args = parser.parse_args()
    try:
        stdscr = curses.initscr()
        # Properly initialize the screen
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        window = curses.newwin(curses.LINES, curses.COLS, 0, 0)
        window.box()
        window.noutrefresh()
        stdscr.noutrefresh()
        curses.doupdate()
        grid = init_grid(curses.LINES-1, curses.COLS//2-1)
        population = args.population if args.population else curses.LINES * curses.COLS // 15
        randomly_populate_grid(grid, population)
        while True:
            window.clear()
            gridio = grid_view(grid)
            window.addstr(gridio.getvalue())
            window.refresh()
            window.clear()
            step(grid)
            time.sleep(args.step)
            stdscr.noutrefresh()
            window.noutrefresh()
            curses.doupdate()
    except KeyboardInterrupt:
        pass
    finally:
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.endwin()


def randomly_populate_grid(grid, ncells):
    w = len(grid[0]) - 1
    h = len(grid) - 1
    populated = 0
    while populated < ncells:
        r = random.randint(0, h)
        c = random.randint(0, w)
        if not grid[r][c]:
            grid[r][c] = 1
            populated += 1


def init_grid(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]


def grid_view(grid):
    sio = StringIO()
    for row in grid:
        for cell in row:
            sio.write("██") if cell else sio.write('  ')
        sio.write('\n')
    return sio


def count_neighbours(grid, row, col):
    idxs = neighbour_idx(grid, row, col)
    return sum(1 for (r, c) in idxs if grid[r][c] == 1)


def neighbour_idx(grid, row, col):
    w = len(grid[0]) - 1
    h = len(grid) - 1
    product = itertools.product((row-1, row, row+1), (col-1, col, col+1))
    idxs = set((r, c) for (r, c) in product if ((0 <= r <= h) and (0 <= c <= w)))
    idxs.remove((row, col))
    return idxs


def step(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            neigbours = count_neighbours(grid, r, c)
            if grid[r][c]:
                if neigbours < 2:
                    grid[r][c] = 0
                elif neigbours > 3:
                    grid[r][c] = 0
            else:
                if neigbours == 3:
                    grid[r][c] = 1


if __name__ == "__main__":
    main()
