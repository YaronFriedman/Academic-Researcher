"""Run Deepchecks execute_app against the Vercel-deployed endpoint."""

import asyncio

from deepchecks_llm_client.client import DeepchecksLLMClient
from deepchecks_llm_client.data_types import EnvType

dc_client = DeepchecksLLMClient(
    api_token="Y3MrZGVlcGNoZWNrc2RlbW9AZGVlcGNoZWNrcy5jb20=.b3JnX2RlZXBjaGVja3NfZGVtb184ZGIwNjNlZGViMzIwNmZh.9rO4oGBU3XPghDH7vKXjDA",
    host="https://app.llm.deepchecks.com/",
)


async def main():
    result = await dc_client.execute_app(
        app_name="Google ADK Academic Researcher",
        version_name="v1",
        env_type=EnvType.EVAL,
        dataset_name="Academic Research Dataset",
        deployment_name="Vercel Deployment",
        show_progress=True,
    )
    return result


result = asyncio.run(main())
print(result)
