import aiohttp
import os

async def upload_to_catbox(file_path: str) -> str | None:
    url = "https://catbox.moe/user/api.php"
    payload = {
        "reqtype": "fileupload",
        "userhash": ""  # Add your Catbox userhash if required
    }
    try:
        async with aiohttp.ClientSession() as session:
            with open(file_path, "rb") as f:
                files = {"fileToUpload": f}
                async with session.post(url, data=payload, files=files) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        print(f"Catbox upload failed: {response.status}")
                        return None
    except Exception as e:
        print(f"Error uploading to Catbox: {e}")
        return None
