from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.services.generate_text import generate_text

router = APIRouter()

@router.post("/generate")
async def generate(request: Request):
    try:
        body = await request.json()
        question = body.get("question")

        if not question:
            return JSONResponse(
                status_code=400,
                content={"error": "Missing 'question' field in request body"},
            )

        answer = generate_text(question)

        return JSONResponse(
            status_code=200,
            content={
                "question": question,
                "answer": answer
            },
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
        )