import constants

class CredManager:

    def __init__(self, api_key=None):
        self.api_key = api_key

    def set_api_key(self, api_key):
        self.api_key = api_key

    def get_api_key(self):
        return self.api_key


def main():
    cred_mgr = CredManager(constants.API_KEY)
    client = ors.Client()
    pass

if __name__ == "__main__":
    main()