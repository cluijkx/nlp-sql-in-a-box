from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, SpeechSynthesizer, ResultReason, CancellationReason
from azure.cognitiveservices.speech.audio import AudioConfig, AudioOutputConfig

from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

aadToken = credential.get_token("https://cognitiveservices.azure.com/.default")

resourceId = "/subscriptions/7465eae3-48a0-4ab0-99ba-0f858bb2aeb3/resourceGroups/rg-NAHACKATHON/providers/Microsoft.CognitiveServices/accounts/cog-sp-NAHACKATHON-fluts"

region = "eastus2"

# You need to include the "aad#" prefix and the "#" (hash) separator between resource ID and Microsoft Entra access token.
authorizationToken = "aad#" + resourceId + "#" + aadToken.token

speechConfig = SpeechConfig(auth_token=authorizationToken, region=region)


synthesizer = SpeechSynthesizer(speech_config=speechConfig, audio_config=AudioOutputConfig(use_default_speaker=True))

'''
text = "Hello World!"

print("Synthesize text to speech and play it through the speaker")

response = synthesizer.speak_text(text)

if response.reason != ResultReason.SynthesizingAudioCompleted:
    cancellation_details = response.cancellation_details
    error = "Speech synthesis canceled: {}".format(cancellation_details.reason)
    if cancellation_details.reason == CancellationReason.Error:
        if cancellation_details.error_details:
            error += "Error details: {}".format(cancellation_details.error_details)
    raise Exception("Speech synthesis failed with error: {}".format(error))

print("Speech synthesized for text [{}]".format(text))
'''


recognizer = SpeechRecognizer(speech_config=speechConfig, audio_config=AudioConfig(use_default_microphone=True))

print("Recognize speech from the microphone and convert it to text")

response = recognizer.recognize_once()

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

print("Recognized text: {}".format(response.text))