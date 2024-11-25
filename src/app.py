import os
import asyncio
import logging

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from semantic_kernel.contents.chat_history import ChatHistory


from .speech import Speech
from .kernel import Kernel
from .database import Database
from .orchestrator import Orchestrator


logging.basicConfig(
    filename="app.log",
    format="[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
    filemode="w"
)

logger = logging.getLogger(__name__)


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
    database_service = Database(server_name=server_name, database_name=database_name, credential=credential)

    # Setup the database
    database_service.setup()

    kernel = Kernel(database_service=database_service, credential=credential, openai_endpoint=openai_endpoint, openai_deployment_name=openai_deployment_name)

    # Create a history of the conversation
    chat_history = ChatHistory()

    orchestrator = Orchestrator(speech_service=speech_service, kernel=kernel)

    await orchestrator.run(chat_history=chat_history)


if __name__ == "__main__":
    asyncio.run(main())
