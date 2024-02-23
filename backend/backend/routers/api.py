from fastapi import APIRouter

router = APIRouter(
    prefix='/api',
    tags=['api'],
)


@router.get("/")
def root():
    return {"message": "Hello World"}
