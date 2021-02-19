from screenless import Application, Command
from screenless import INPUT_BACKSPACE, INPUT_EXIT
from screenless import INPUT_DOWN, INPUT_LEFT, INPUT_RIGHT, INPUT_UP

from .file_management import load, save


class TextEditor(Application):
    def __init__(self, file_path, cursor=None):
        super(TextEditor, self).__init__(
            [],
            Command(self.write)
        )
        self.file_path = file_path
        self.lines = [""]
        self.cursor = cursor or Cursor()

    def run(self):
        self.lines = load(self.file_path) or [""]
        super(TextEditor, self).run()

    def write(self):
        input_ = self.input()
        while input_ != INPUT_EXIT:
            self.output(input_)

            if input_ == INPUT_BACKSPACE:
                self.backspace()
            if input_ == INPUT_LEFT:
                self.move_left()
            if input_ == INPUT_RIGHT:
                self.move_right()
            if input_ == INPUT_DOWN:
                self.move_down()
            if input_ == INPUT_UP:
                self.move_up()
            if isinstance(input_, str):
                self.insert(input_)

            save(self.file_path, self.lines)

            input_ = self.input()

    def backspace(self):
        if self.cursor.line == 0 and self.cursor.position == 0:
            return

        if self.cursor.position == 0:
            previous_line_length = len(self.lines[self.cursor.line - 1])

            self.lines[self.cursor.line - 1] += self.lines[self.cursor.line]
            del self.lines[self.cursor.line]

            self.cursor.line -= 1
            self.cursor.position = previous_line_length
            return

        left = self.lines[self.cursor.line][:self.cursor.position - 1]
        right = self.lines[self.cursor.line][self.cursor.position:]
        self.lines[self.cursor.line] = left + right

        self.cursor.position -= 1

    def move_left(self):
        self.cursor.position -= 1
        self._fix_cursor_position()

    def move_right(self):
        self.cursor.position += 1
        self._fix_cursor_position()

    def move_up(self):
        self.cursor.line -= 1
        self._fix_cursor_position()

    def move_down(self):
        self.cursor.line += 1
        self._fix_cursor_position()

    def insert(self, text):
        if text == "\r" or text == "\n":
            self._insert_new_line()
            return

        lines = text.splitlines()
        for line in lines[:-1]:
            self._insert_without_new_lines(line)
            self._insert_new_line()

        self._insert_without_new_lines(lines[-1])

    def _insert_without_new_lines(self, text):
        left = self.lines[self.cursor.line][:self.cursor.position]
        right = self.lines[self.cursor.line][self.cursor.position:]

        self.lines[self.cursor.line] = left + text + right
        self.cursor.position += len(text)

    def _insert_new_line(self):
        left = self.lines[self.cursor.line][:self.cursor.position]
        right = self.lines[self.cursor.line][self.cursor.position:]

        self.lines[self.cursor.line] = left
        self.lines.insert(self.cursor.line + 1, right)

        self.cursor.line += 1
        self.cursor.position = 0

    def _write_on_input(self, input_):
        self.output(input_)
        if input_ == INPUT_BACKSPACE:
            self.backspace()
        if input_ == INPUT_LEFT:
            self.move_left()
        if input_ == INPUT_RIGHT:
            self.move_right()
        if input_ == INPUT_DOWN:
            self.move_down()
        if input_ == INPUT_UP:
            self.move_up()
        if isinstance(input_, str):
            self.insert(input_)
        print(self.lines)
        save(self.file_path, self.lines)

    def _fix_cursor_position(self):
        self.cursor.line = max(0, self.cursor.line)
        self.cursor.line = min([self.cursor.line, len(self.lines) - 1])

        self.cursor.position = max(0, self.cursor.position)
        line_length = len(self.lines[self.cursor.line])
        self.cursor.position = min([self.cursor.position, line_length])


class Cursor:
    def __init__(self, line=0, position=0):
        self.line = line
        self.position = position
