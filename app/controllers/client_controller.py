class ClientController:
    def __init__(self, model):
        self.model = model

    def add_client(self, name, email, document, phone, address):
        client = self.model(name, email, document, phone, address)
        return client
