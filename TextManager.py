def get_recent(text, num):
    lines = text[-num:]
    output = ""

    for line in lines:
        output += line + "\n"

    return output


class TextManager:
    def __init__(self):
        self.__logs = []
        self.__story = []

    def get_recent_logs(self):
        return get_recent(self.__logs,5)

    def get_recent_story(self):
        return get_recent(self.__story,5)

    def add_log(self, log):
        self.__logs.append(log)

    def add_story(self, story):
        self.__story.append(story)
