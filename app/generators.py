import asyncio
import httpx

from openai import AsyncOpenAI

from config import AITOKEN, PROXY


client = AsyncOpenAI(api_key=AITOKEN,
                     http_client=httpx.AsyncClient(proxy=PROXY,
                                                   transport=httpx.HTTPTransport(local_address="0.0.0.0")))

async def gpt_text(req, model):
    completion = await client.chat.completions.create(
        messages=[{"role" : "user", "content": req}],
        model = model
    )
    return {'response': completion.choices[0].message.content,
            'usage': completion.usage.total_tokens}
    
async def gpt_image(req, model):
    response = await client.images.generate(
        model = "dall-e-3",
        prompt = req,
        size = "1024x1024",
        quality='standard',
        n = 1
    )
    return {'response': response.data[0].url,
            'usage': 1}
  