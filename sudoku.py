import pygame
import pygame.freetype
import sys
import copy
import math


class screenDefine:
    # Pygame Screen Initialization
    def __init__(self, screenParams):
        pygame.init()
        self.screen = pygame.display.set_mode(screenParams["dimensions"])
        pygame.display.set_caption(screenParams["caption"])
        self.screen.fill(screenParams["bgColor"])
        pygame.freetype.init()
        self.sudokuNums = pygame.freetype.SysFont("Consolas", 40, bold=True)
        self.dataFont = pygame.freetype.SysFont("Calibri", 24, bold=False)

    def returnScreenVar(self):
        return self.screen

    def returnNumFontVar(self):
        return self.sudokuNums

    def returnDataFontVar(self):
        return self.dataFont


class sudoku(screenDefine):
    # Boards available to play
    baseBoards = [
        [
            [0, 6, 0, 3, 0, 0, 8, 0, 4],
            [5, 3, 7, 0, 9, 0, 0, 0, 0],
            [0, 4, 0, 0, 0, 6, 3, 0, 7],
            [0, 9, 0, 0, 5, 1, 2, 3, 8],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [7, 1, 3, 6, 2, 0, 0, 4, 0],
            [3, 0, 6, 4, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 6, 0, 5, 2, 3],
            [1, 0, 2, 0, 0, 9, 0, 8, 0],
        ],
        [
            [3, 0, 6, 5, 0, 8, 4, 0, 0],
            [5, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 7, 0, 0, 0, 0, 3, 1],
            [0, 0, 3, 0, 1, 0, 0, 8, 0],
            [9, 0, 0, 8, 6, 3, 0, 0, 5],
            [0, 5, 0, 0, 9, 0, 6, 0, 0],
            [1, 3, 0, 0, 0, 0, 2, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 4],
            [0, 0, 5, 2, 0, 6, 3, 0, 0],
        ],
        [
            [1, 2, 3, 4, 5, 6, 7, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 3],
            [0, 0, 0, 0, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 5],
            [0, 0, 0, 0, 0, 0, 0, 0, 6],
            [0, 0, 0, 0, 0, 0, 0, 0, 7],
            [0, 0, 0, 0, 0, 0, 0, 0, 8],
        ],
    ]

    # Index of Board Selected
    sel = 0

    # Initializes Sudoku Board
    def __init__(self, screenParams):
        super().__init__(screenParams)
        self.board = copy.deepcopy(self.baseBoards[self.sel])
        self.solvedBoard = copy.deepcopy(self.baseBoards[self.sel])
        self.emptyCell = [0, 0]  # Location of First Cell Which is Empty

        # Outputs to self.solvedBoard, Creates a solved copy of the board
        self.initSolve()

        # Program mode
        self.entryMode = False
        self.solveMode = False

        # Position of the cursor during entry mode
        self.position = {"row": 0, "col": 0}

    # Changes the board
    def changeBoard(self, screenParams):
        if self.sel == 2:
            self.sel = 0
        else:
            self.sel += 1

        self.__init__(screenParams)

    # Writes auxiliary data
    def writeData(self):
        textColor = (200, 200, 200)

        if self.entryMode:
            data = [
                "(1 - 9): Enter Number",
                "0: Clear Number",
                "Lft Mouse Clk: Navigation",
                "Bksp: Exit Entry Mode",
            ]
        elif self.solveMode:
            data = ["Solving"]
        else:
            data = [
                "(1 - 9): Highlight Number",
                "0: Remove Highlights",
                "E: Entry Mode",
                "S: Solve Mode",
                "R: Reset Board",
                "C: Change Board",
                "Esc: Exit",
            ]

        for i in range(len(data)):
            super().returnDataFontVar().render_to(
                super().returnScreenVar(),
                (950, 100 + i * 40),
                data[i],
                textColor,
            )

    # Writes numbers in the grid
    def writeNums(self, screenParams, color):
        for i in range(0, 9):
            for j in range(0, 9):
                num = " "

                # General Case, Highlights active numbers
                if screenParams["activeNum"] == 0:
                    textColor = screenParams["activeTextColor"]
                else:
                    if self.board[j][i] == screenParams["activeNum"]:
                        textColor = screenParams["activeTextColor"]
                    else:
                        textColor = screenParams["inactiveTextColor"]

                # Gets number to fill cells
                if self.board[j][i] != 0:
                    num = self.board[j][i]

                # Filling final board
                if self.boardEmptChk(False):
                    if self.baseBoards[self.sel][j][i] != self.board[j][i]:
                        textColor = color

                    # Filling board while solving
                    if not self.solveMode:
                        if self.baseBoards[self.sel][j][i] == 0:
                            if self.board[j][i] == self.solvedBoard[j][i]:
                                textColor = (0, 200, 0)
                            else:
                                textColor = (200, 0, 0)

                # Guard general case to prevent inconsistencies
                if not self.boardEmptChk(False):
                    if screenParams["activeNum"] == 0:
                        textColor = screenParams["activeTextColor"]
                    else:
                        if self.board[j][i] == screenParams["activeNum"]:
                            textColor = screenParams["activeTextColor"]
                        else:
                            textColor = screenParams["inactiveTextColor"]

                super().returnNumFontVar().render_to(
                    super().returnScreenVar(),
                    (66 + (100 * i), 66 + (100 * j)),
                    str(num),
                    textColor,
                )

    # def writeEmptyNums(self, screenParams, rowNum, colNum):
    #     num = ' '
    #
    #     if self.board[colNum][rowNum] != 0:
    #         num = self.board[colNum][rowNum]
    #
    #     if screenParams['activeNum'] == 0:
    #         textColor = screenParams['activeTextColor']
    #     else:
    #         if self.board[colNum][rowNum] == screenParams['activeNum']:
    #             textColor = screenParams['activeTextColor']
    #         else:
    #             textColor = screenParams['inactiveTextColor']
    #
    #     super().returnNumFontVar().render_to(
    #         super().returnScreenVar(),
    #         (66 + (100 * rowNum), 66 + (100 * colNum)),
    #         str(num),
    #         (0, 100, 0)
    #     )

    # Designs board
    def boardDesign(self, screenParams, color):
        super().returnScreenVar().fill(screenParams["bgColor"])

        # Draws gridlines
        for i in range(0, 10):
            if i % 3 == 0:
                lineCol = screenParams["outLineColor"]
            else:
                lineCol = screenParams["inLineColor"]

            pygame.draw.line(
                super().returnScreenVar(),
                lineCol,
                (25, (100 * i + 25)),
                (925, (100 * i + 25)),
                7,
            )

            pygame.draw.line(
                super().returnScreenVar(),
                lineCol,
                ((100 * i + 25), 25),
                ((100 * i + 25), 925),
                7,
            )

            # Writes numbers and auxiliary data
            self.writeNums(screenParams, color)
            self.writeData()

            # Draws cursorbox during entry mode
            if self.entryMode is True:
                pygame.draw.rect(
                    self.screen,
                    (136, 192, 208),
                    pygame.Rect(
                        # position['col'] * 100,
                        # position['row'] * 100,
                        (100 * self.position["col"]) + 25,
                        (100 * self.position["row"]) + 25,
                        100,
                        100,
                    ),
                    7,
                )

    # Prints text version of board
    def boardPrint(self):
        for i in range(9):
            print(self.board[i])
            # print(self.emptyCell)

        print()

    def reset(self):
        self.board = copy.deepcopy(self.baseBoards[self.sel])

    # def solveExt(self, board):
    #     s2 = solver.sudokuSolve(board)
    #     s2.solve()
    #     print(s2.returnBoard())
    #     s2.boardPrint()

    # User entry
    def entry(self, screenParams, color):
        self.entryMode = True

        # Sets initial cursor position
        for i in range(0, 9):
            for j in range(0, 9):
                if self.board[i][j] == 0:
                    self.position["row"] = i
                    self.position["col"] = j
                    break
            else:
                continue

            break

        while self.entryMode:
            for event in pygame.event.get():
                # Translation of mouse click location to cell index
                if event.type == pygame.MOUSEBUTTONUP:
                    mousePosition = pygame.mouse.get_pos()
                    rowMousePosition = math.floor(mousePosition[0] / 100)
                    colMousePosition = math.floor(mousePosition[1] / 100)

                    if (
                        self.baseBoards[self.sel][colMousePosition][
                            rowMousePosition
                        ]
                        == 0
                    ):
                        self.position["col"] = rowMousePosition
                        self.position["row"] = colMousePosition

                # Keyboard commands
                if event.type == pygame.KEYDOWN:
                    # Exit from entry mode
                    if event.key == pygame.K_BACKSPACE:
                        self.entryMode = not self.entryMode

                    # Number entry
                    if event.key == pygame.K_0:
                        self.board[self.position["row"]][
                            self.position["col"]
                        ] = 0
                        break
                    if event.key == pygame.K_1:
                        self.board[self.position["row"]][
                            self.position["col"]
                        ] = 1
                        break
                    if event.key == pygame.K_2:
                        self.board[self.position["row"]][
                            self.position["col"]
                        ] = 2
                        break
                    if event.key == pygame.K_3:
                        self.board[self.position["row"]][
                            self.position["col"]
                        ] = 3
                        break
                    if event.key == pygame.K_4:
                        self.board[self.position["row"]][
                            self.position["col"]
                        ] = 4
                        break
                    if event.key == pygame.K_5:
                        self.board[self.position["row"]][
                            self.position["col"]
                        ] = 5
                        break
                    if event.key == pygame.K_6:
                        self.board[self.position["row"]][
                            self.position["col"]
                        ] = 6
                        break
                    if event.key == pygame.K_7:
                        self.board[self.position["row"]][
                            self.position["col"]
                        ] = 7
                        break
                    if event.key == pygame.K_8:
                        self.board[self.position["row"]][
                            self.position["col"]
                        ] = 8
                        break
                    if event.key == pygame.K_9:
                        self.board[self.position["row"]][
                            self.position["col"]
                        ] = 9
                        break

                    # Program exit
                    if event.key == pygame.K_ESCAPE:
                        sys.exit(0)

            self.boardDesign(screenParams, color)

            pygame.display.update()

    # Checks full board for emptyness
    def boardEmptChk(self, init):
        # For initial solving
        if init:
            for i in range(9):
                for j in range(9):
                    if self.solvedBoard[i][j] == 0:
                        self.emptyCell[0] = i
                        self.emptyCell[1] = j
                        return True
        # For solving triggered by user

        else:
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == 0:
                        self.emptyCell[0] = i
                        self.emptyCell[1] = j
                        return True

        return False

    # Checks existence of number in row
    def inRow(self, rowNum, chkNum, init):
        # For initial solving
        if init:
            for i in range(9):
                if self.solvedBoard[rowNum][i] == chkNum:
                    return True

        # For solving triggered by user
        else:
            for i in range(9):
                if self.board[rowNum][i] == chkNum:
                    return True

        return False

    # Checks existence of number in column
    def inCol(self, colNum, chkNum, init):
        # For initial solving
        if init:
            for i in range(9):
                if self.solvedBoard[i][colNum] == chkNum:
                    return True

        # For solving triggered by user
        else:
            for i in range(9):
                if self.board[i][colNum] == chkNum:
                    return True

        return False

    # Checks existence of number in 3x3 box
    def inBox(self, rowNum, colNum, chkNum, init):
        # For initial solving
        if init:
            for i in range(3):
                for j in range(3):
                    if self.solvedBoard[i + rowNum][j + colNum] == chkNum:
                        return True

        # For solving triggered by user
        else:
            for i in range(3):
                for j in range(3):
                    if self.board[i + rowNum][j + colNum] == chkNum:
                        return True

        return False

    # Solves program
    def solve(self, screenParams):
        # Triggers solvemode
        self.solveMode = True

        # Checks if board is not solved
        if not self.boardEmptChk(False):
            self.solveMode = False
            return True

        pygame.event.get()

        # Location of empty cell
        r, c = self.emptyCell[0], self.emptyCell[1]

        # Cycles through numbers 1 - 9 and tries to fit it within empty cell
        for i in range(1, 10):
            # Checks if number is not in row, column or 3x3 inBox
            if (
                not self.inRow(r, i, False)
                and not self.inCol(c, i, False)
                and not self.inBox(r - r % 3, c - c % 3, i, False)
            ):
                keys = pygame.key.get_pressed()

                # Program exit
                if keys[pygame.K_ESCAPE]:
                    sys.exit(0)

                # Tries to fit in the number
                self.board[r][c] = i

                self.boardDesign(screenParams, (0, 200, 0))
                # self.writeEmptyNums(screenParams, r, c)

                pygame.time.delay(40)
                pygame.display.update()

                # Recursively checks all numbers remaining by backtracking
                if self.solve(screenParams):
                    return True

                self.boardDesign(screenParams, (200, 0, 0))
                pygame.time.delay(40)
                pygame.display.update()

                # Failed entry, try again
                self.board[r][c] = 0

        return False

    # Same logic as above function
    def initSolve(self):
        if not self.boardEmptChk(True):
            return True

        r, c = self.emptyCell[0], self.emptyCell[1]

        for i in range(1, 10):
            if (
                not self.inRow(r, i, True)
                and not self.inCol(c, i, True)
                and not self.inBox(r - r % 3, c - c % 3, i, True)
            ):
                self.solvedBoard[r][c] = i

                if self.initSolve():
                    return True

                self.solvedBoard[r][c] = 0

        return False

    def returnBoard(self):
        return self.board

    # def locSafety(self, rowNum, colNum, numChk):
    #     return (not self.inRow(rowNum, numChk) and
    #             not self.inCol(rowNum, numChk) and
    #             not self.inRow(rowNum, numChk) and)

    # def solve(self):
    #     if not self.boardEmptChk():
    #         return True

    #     r, c = self.emptyCell[0], self.emptyCell[1]

    #     for i in range(1, 10):
    #         if (
    #             not self.inRow(r, i) and
    #             not self.inCol(c, i) and
    #             not self.inBox(
    #                 r - r % 3,
    #                 c - c % 3,
    #                 i
    #             )
    #         ):
    #             self.board[r][c] = str(i)

    #             if self.solve():
    #                 return True

    #             self.board[r][c] = '*'

    #     return False


# Main Program


def main():

    # Parameters needed
    screenParams = {
        "dimensions": [1200, 950],
        "bgColor": (31, 33, 42),
        "outLineColor": (180, 180, 180),
        "inLineColor": (120, 120, 120),
        "caption": "Sudoku",
        "activeTextColor": (200, 200, 200),
        "inactiveTextColor": (100, 100, 100),
        "activeNum": 0,
    }

    # Running variable for pygame
    running = True

    s1 = sudoku(screenParams)
    # s1 = sudoku(board)
    # s1.boardPrint()

    # Loop within which pygame runs
    while running:

        # Initial board creation
        s1.boardDesign(screenParams, (0, 0, 0))

        for event in pygame.event.get():
            # Exit clause
            if event.type == pygame.QUIT:
                running = False

            # Detects keypresses to get instructions
            if event.type == pygame.KEYDOWN:
                # Program exit
                if event.key == pygame.K_ESCAPE:
                    running = not running

                # Active number change
                if event.key == pygame.K_0:
                    screenParams["activeNum"] = 0

                if event.key == pygame.K_1:
                    screenParams["activeNum"] = 1

                if event.key == pygame.K_2:
                    screenParams["activeNum"] = 2

                if event.key == pygame.K_3:
                    screenParams["activeNum"] = 3

                if event.key == pygame.K_4:
                    screenParams["activeNum"] = 4

                if event.key == pygame.K_5:
                    screenParams["activeNum"] = 5

                if event.key == pygame.K_6:
                    screenParams["activeNum"] = 6

                if event.key == pygame.K_7:
                    screenParams["activeNum"] = 7

                if event.key == pygame.K_8:
                    screenParams["activeNum"] = 8

                if event.key == pygame.K_9:
                    screenParams["activeNum"] = 9

                # Solve board
                if event.key == pygame.K_s:
                    # s1.solveExt(board)
                    s1.reset()
                    s1.solve(screenParams)
                    # s1.boardPrint()

                # User entry
                if event.key == pygame.K_e:
                    s1.entry(screenParams, (0, 0, 0))

                # Reset board
                if event.key == pygame.K_r:
                    s1.reset()

                # Cycle through boards
                if event.key == pygame.K_c:
                    s1.changeBoard(screenParams)

        # solver.s1.boardPrint()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
