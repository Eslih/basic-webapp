from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from ..schemas import HTTPError

prime_router = APIRouter()


# Response model & responses are handy for docs
@prime_router.get("/", response_model=List[int], responses={HTTP_400_BAD_REQUEST: {"model": HTTPError}},
                  tags=["primes"])
@prime_router.get("/{lower}/{upper}", response_model=List[int], responses={HTTP_400_BAD_REQUEST: {"model": HTTPError}},
                  tags=["primes"])
def get_primes(lower: int = 0, upper: int = 10000) -> List[int]:
    if lower > 5000:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Please don't overload me! Lower should be less than or equal to 5000.")
    if upper > 50000:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="You exaggerator! Upper should be less than or equal to 50000.")

    p = []

    for num in range(lower, upper + 1):
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                p.append(num)

    return p
