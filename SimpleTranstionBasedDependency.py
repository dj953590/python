class DependencyParser:
    def __init__(self, sentence):
        self.sentence = sentence.split()  # Split the sentence into words
        self.stack = []  # Stack for partial parses
        self.buffer = list(reversed(self.sentence))  # Buffer for remaining words
        self.dependencies = []  # List to store dependencies

    def shift(self):
        """Shift a word from the buffer to the stack."""
        if self.buffer:
            self.stack.append(self.buffer.pop())

    def left_arc(self, relation):
        """Add a left-arc dependency with the given relation."""
        if len(self.stack) > 1:
            dependent = self.stack.pop(-2)
            head = self.stack[-1]
            self.dependencies.append((head, relation, dependent))

    def right_arc(self, relation):
        """Add a right-arc dependency with the given relation."""
        if len(self.stack) > 1:
            head = self.stack.pop()
            dependent = self.stack[-1]
            self.dependencies.append((dependent, relation, head))

    def parse(self):
        """Apply transitions until the sentence is parsed."""
        while self.buffer or len(self.stack) > 1:
            if len(self.stack) > 1 and (not self.buffer or some_decision_function(self.stack[-1], self.stack[-2])):
                self.left_arc('some_relation')
            elif self.buffer:
                self.shift()
            else:
                self.right_arc('some_relation')

# Example usage:
sentence = "I love natural language processing"
parser = DependencyParser(sentence)
parser.parse()
print(parser.dependencies)