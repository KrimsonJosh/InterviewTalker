import httpx
from fastapi import HTTPException
from src.core.config import get_settings # Load settings

settings = get_settings()

class TranscriptionService:
    @staticmethod
    async def transcribe_audio(audio_content: bytes) -> str:
        """
        Send audio content to Deepgram for transcription.
        Returns the transcribed text.
        """
        try:
            headers = {
                "Authorization": f"Token {settings.DEEPGRAM_API_KEY}",
                "Content-Type": "audio/webm"
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.deepgram.com/v1/listen",
                    headers=headers,
                    content=audio_content
                )

            if response.status_code == 200:
                data = response.json()
                transcript = data.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0].get("transcript", "")
                return transcript
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Deepgram API error: {response.text}"
                )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Transcription error: {str(e)}"
            ) 