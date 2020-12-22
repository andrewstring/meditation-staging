class Runtime:
    def __init__(self):
        prompts = ["Select time: ", "Select number of breaths: "]
        self.values = []

        for prompt in prompts:
            self.values.append(self.get_input(prompt))

    def get_input(self, prompt):
        return input(prompt)

run = Runtime()
for value in run.values:
    print(value)
