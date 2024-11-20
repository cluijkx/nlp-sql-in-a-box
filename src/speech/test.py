import os
import asyncio
import logging

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential

from service import Speech


async def main():
    load_dotenv()

    credential = DefaultAzureCredential()

    server_name = os.getenv("SQL_SERVER_NAME")
    database_name = os.getenv("SQL_DATABASE_NAME")
    speech_service_id = os.getenv("SPEECH_SERVICE_ID")
    azure_location = os.getenv("AZURE_LOCATION")
    openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai_deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")

    speech_service = Speech(credential=credential, resource_id=speech_service_id, region=azure_location)
    
    """
    Run the orchestrator
    """
    speech_service.synthesize("....Welcome to the Kiosk Bot!! I am here to help you with your queries. I am still learning. So, please bear with me.")

    while True:
        try:
            speech_service.synthesize("Please ask your query through the Microphone:")
            print("Listening:")

            # Collect user input
            user_input = self.speech_service.recognize()
            print("User > " + user_input)

            # Terminate the loop if the user says "exit"
            if user_input == "exit":
                break

            response = await self.kernel.message(user_input=user_input, chat_history=chat_history)

            print("Assistant > " + response)
            speech_service.synthesize(response)

            speech_service.synthesize("Do you have any other query? Say Yes to Continue")

            # Taking Input from the user
            print("Listening:")
            user_input = speech_service.recognize()
            print("User > " + user_input)
            if user_input != 'Yes.':
                speech_service.synthesize("Thank you for using the Kiosk Bot. Have a nice day.")
                break
        except Exception as e:
            speech_service.synthesize("An error occurred. Let's try again.")
            continue


if __name__ == "__main__":
    asyncio.run(main())
