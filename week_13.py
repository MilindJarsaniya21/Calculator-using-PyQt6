import sys
from PyQt6.QtCore import Qt
from functools import partial
from PyQt6.QtWidgets import QApplication, QGridLayout, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget

ERROR_MSG = "ERROR"
WINDOW_SIZE = 235
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40

class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.setupUI()

    def setupUI(self):
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self.createDisplay()
        self.createButtons()

    def createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def createButtons(self):
        self.buttonMap = {}
        buttonsLayout = QGridLayout()
        keyBoard = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", "00", ".", "+", "="],
        ]

        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                buttonsLayout.addWidget(self.buttonMap[key], row, col)

        self.generalLayout.addLayout(buttonsLayout)

class CalculatorLogic:
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self.connectSignalsAndSlots()

    def calculateResult(self):
        result = self._evaluate(self._view.display.text())
        self._view.display.setText(result)

    def buildExpression(self, subexpression):
        if self._view.display.text() == ERROR_MSG:
            self._view.display.clear()
        expression = self._view.display.text() + subexpression
        self._view.display.setText(expression)

    def connectSignalsAndSlots(self):
        for keySymbol, button in self._view.buttonMap.items():
            if keySymbol not in {"=", "C"}:
                button.clicked.connect(
                    partial(self.buildExpression, keySymbol)
                )
        self._view.buttonMap["="].clicked.connect(self.calculateResult)
        self._view.display.returnPressed.connect(self.calculateResult)
        self._view.buttonMap["C"].clicked.connect(self._view.display.clear)

def evaluateExpression(expression):
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
    return result

def main():
    pycalcApp = QApplication([])
    pycalcWindow = CalculatorApp()
    pycalcWindow.show()
    CalculatorLogic(model=evaluateExpression, view=pycalcWindow)
    sys.exit(pycalcApp.exec())

if __name__ == "__main__":
    main()
