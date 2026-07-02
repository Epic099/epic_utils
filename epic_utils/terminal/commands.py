def test(num=None, word=None):
    if num is not None and word is not None:
        print(f"{num}, {word}")

class Command:
    def __init__(self, cmd, callback):
        self.command = cmd
        self.callback = callback
    
    def activate(self, arguments):
        self.callback(**arguments)

class CommandManager:
    def __init__(self):
        self.commands: list[Command] = []

    def registerCommand(self, cmd, callback):
        self.commands.append(Command(cmd, callback))

    def run(self):
        while True:
            inp = input("> ")
            split = str.split(inp, " ")
            args = {}
            for i in range(0, len(split)):
                s = split[i]
                if s[0:2] == "--" and i < len(split)-1:
                    args[s[2:]] = split[i+1]

            if inp == "help":
                print("Powered by Epic099´s command-manager")
                print("----------------Help----------------")
                for cmd in self.commands:
                    print(f"- {cmd.command}")
                continue
            elif inp == "exit":
                break
            for cmd in self.commands:
                if inp == cmd.command:
                    cmd.activate()
                    break


if __name__ == "__main__":
    m = CommandManager()
    m.registerCommand("get", test)
    m.run()