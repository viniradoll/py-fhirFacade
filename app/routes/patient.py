from fastapi import APIRouter

router = APIRouter(prefix="/patient", tags=["Patient"])

@router.get("")
def return_patients():
    return [{}]

@router.post("", status_code=201)
def return_patients():
    return [{}]

@router.get("/{id}")
def return_patient_by_id(id):
    return [{"id":id}]
