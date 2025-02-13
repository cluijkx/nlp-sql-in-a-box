import logging

from azure.identity import DefaultAzureCredential
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, SpeechSynthesizer, ResultReason, CancellationReason
from azure.cognitiveservices.speech.audio import AudioConfig, AudioOutputConfig


logger = logging.getLogger(__name__)

# see https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-configure-azure-ad-auth?tabs=portal&pivots=programming-language-python#get-a-microsoft-entra-access-token
scope = 'https://cognitiveservices.azure.com/.default'


class Speech:

    def __init__(self, credential: DefaultAzureCredential, resource_id: str, region: str) -> None:
        
        ad_token = credential.get_token("https://cognitiveservices.azure.com/.default")

        auth_token = "aad#" + resource_id + "#" + ad_token.token

        #logger.debug("auth_token: {}".format(auth_token))

        speech_config = SpeechConfig(auth_token=auth_token, region=region, speech_recognition_language="en-US")

        speech_config.speech_synthesis_voice_name = "en-US-GuyNeural"  # Change to your preferred voice

        self._recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=AudioConfig(use_default_microphone=True))
        self._synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=AudioOutputConfig(use_default_speaker=True))


    def recognize(self) -> str:
        """
        Recognize speech from the microphone and convert it to text
        """
        response = self._recognizer.recognize_once()

        reason = response.reason
        if reason != ResultReason.RecognizedSpeech:
            error = 'Failed to recognize speech.'
            if reason == ResultReason.NoMatch:
                error = "No speech could be recognized: {}".format(response.no_match_details)
            elif reason == ResultReason.Canceled:
                cancellation_details = response.cancellation_details
                error = "Speech Recognition canceled: {}".format(cancellation_details.reason)
                if cancellation_details.reason == CancellationReason.Error:
                    error += "Error details: {}".format(cancellation_details.error_details)
            raise Exception("Speech recognition failed with error: {}".format(error))

        logger.info("Recognized text: {}".format(response.text))

        return response.text


    def synthesize(self, text: str) -> None:
        """
        Synthesize text to speech and play it through the speaker
        """
        response = self._synthesizer.speak_text(text)

        if response.reason != ResultReason.SynthesizingAudioCompleted:
            cancellation_details = response.cancellation_details
            error = "Speech synthesis canceled: {}".format(cancellation_details.reason)
            if cancellation_details.reason == CancellationReason.Error:
                if cancellation_details.error_details:
                    error += "Error details: {}".format(cancellation_details.error_details)
            raise Exception("Speech synthesis failed with error: {}".format(error))

        logger.info("Speech synthesized for text [{}]".format(text))
