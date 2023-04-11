from google.oauth2 import service_account
from google.cloud import translate_v2 as translate


class GoogleTranslateClient:

    def __init__(self, cred_file_path):

        # Load the credentials from the key file
        self._service_account_creds = service_account.Credentials.from_service_account_file(
            cred_file_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

        # Create an instance of the Google Translate client
        self.translate_client = translate.Client(
            credentials=self._service_account_creds
        )

    def translate_text(self, input_text, target_lang):
        translation = self.translate_client.translate(input_text, target_language=target_lang)
        return translation['translatedText']

    def translate_batch(self, input_list, target_lang):
        return self.translate_client.translate(values=input_list, target_language=target_lang)
