class Message:
    """Message class.
    Class implementing the message object which is exchanged between agents through a message service
    during communication.

    attr:
        from_agent: the sender of the message (id)
        to_agent: the receiver of the message (id)
        message_performative: the performative of the message
        content: the content of the message
    """

    def __init__(self, from_agent, to_agent, message_performative, content: None):
        """Create a new message."""
        self.__from_agent = from_agent
        self.__to_agent = to_agent
        self.__message_performative = message_performative
        self.__content = content
        self.__str__()

    def get_exp(self):
        """Return the sender of the message."""
        return self.__from_agent

    def get_dest(self):
        """Return the receiver of the message."""
        return self.__to_agent

    def get_performative(self):
        """Return the performative of the message."""
        return self.__message_performative

    def get_content(self):
        """Return the content of the message."""
        return self.__content

    def __str__(self):
        if self.__message_performative.value == 105:
            return print(
                f"{self.get_exp()} to {self.get_dest()}: {self.get_performative()}: {self.get_content()[0].get_name()} {self.get_content()[1].name} {self.get_content()[2].name}"
            )
        else:
            return print(
                f"{self.get_exp()} to {self.get_dest()}: {self.get_performative()}: {self.get_content()}"
            )
