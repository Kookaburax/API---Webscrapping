from fastapi import APIRouter

router = APIRouter()

@router.get("/model/test", tags=["Model"])
def test_model_endpoint():
    return {"message": "Model endpoint is working!"}