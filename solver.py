class sudokuSolve:
    def __init__(self, board):
        self.board = board
        self.emptyCell = [0, 0]
        self.boardEmptChk()
    
    def boardPrint(self):
        for i in range(9):
            print(self.board[i])
    
    def returnBoard(self):
        return self.board
    
    def boardEmptChk(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    self.emptyCell[0] = i
                    self.emptyCell[1] = j
                    return True
    
        return False
    
    def inRow(self, rowNum, chkNum):
        for i in range(9):
            if self.board[rowNum][i] == chkNum:
                return True
        
        return False
    
    def inCol(self, colNum, chkNum):
        for i in range(9):
            if self.board[i][colNum] == chkNum:
                return True
        
        return False
    
    def inBox(self, rowNum, colNum, chkNum):
        for i in range(3):
            for j in range(3):
                if self.board[i + rowNum][j + colNum] == chkNum:
                    return True
        
        return False
    
    def solve(self):
        if not self.boardEmptChk():
            return True

        r, c = self.emptyCell[0], self.emptyCell[1]
        
        for i in range(1, 10):
            if (
                not self.inRow(r, i) and
                not self.inCol(c, i) and
                not self.inBox(
                    r - r % 3,
                    c - c % 3,
                    i
                )
            ):
                self.board[r][c] = i
                
                if self.solve():
                    return True
                
                self.board[r][c] = 0
        
        return False