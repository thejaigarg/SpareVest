from pydantic import BaseModel

class BankAccountBase(BaseModel):
    bank_name: str
    account_number: str
    currency: str

class BankAccountCreate(BankAccountBase):
    pass

class BankAccountInDB(BankAccountBase):
    id: int
    user_id: int
    balance: float
    is_default: bool = False

    class Config:
        from_attributes = True  # Pydantic v2, formerly orm_mode=True