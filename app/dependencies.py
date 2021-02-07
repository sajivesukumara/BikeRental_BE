from fastapi import Header, HTTPException
print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))


async def get_token_header(x_token: str = Header(...)):
    print("Checking X-Token header param")
    if x_token != "bikerscafe-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "bikerscafe":
        raise HTTPException(status_code=400, detail="No bikerscafe token provided")
