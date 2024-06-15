import firebase_admin
import firebase_admin.auth
from fastapi import Request


# creds = firebase_admin.credentials.Certificate("/workspaces/job-hunter/serviceAccountCreds.json")

# middleware_app = firebase_admin.initialize_app(creds, name="middleware_app")

# Create a auth middleware to check if the user is authenticated
def get_current_user(request: Request):
    # fetch token from authorization header
    try:
        token = request.headers.get("Authorization")
        if not token:
            return {"error": "No token provided"}
        token = token.split(" ")[1]    
        decoded_token = firebase_admin.auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(e)
        return {"error": "Invalid token"}


# # Create an auth api to test it
# from fastapi import FastAPI, Depends
# from fastapi.responses import JSONResponse

# app = FastAPI()

# @app.get("/auth")
# async def auth(token: str = Depends(get_current_user)):
#     if token:
#         return JSONResponse(content={"message": "You are authenticated"})
#     else:
#         return JSONResponse(content={"message": "You are not authenticated"})


# if __name__ == "__main__":
#     print(get_current_user("eyJhbGciOiJSUzI1NiIsImtpZCI6ImRmOGIxNTFiY2Q5MGQ1YjMwMjBlNTNhMzYyZTRiMzA3NTYzMzdhNjEiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQXl1c2ggZGVzaHBhbmRlIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xSTklzNGh4LTFONXZPZXRfT1Z3TEVPMlhHWUw3c05mYXJrSzUyRXBGYTVHWWgwbHM9czk2LWMiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vam9iaHVudC1lYTAxYSIsImF1ZCI6ImpvYmh1bnQtZWEwMWEiLCJhdXRoX3RpbWUiOjE3MTg0Mjg5NjIsInVzZXJfaWQiOiJDT0R4SlpXQnpDUE9RaHEyNFBqa0VWa056bjQzIiwic3ViIjoiQ09EeEpaV0J6Q1BPUWhxMjRQamtFVmtOem40MyIsImlhdCI6MTcxODQyODk2MiwiZXhwIjoxNzE4NDMyNTYyLCJlbWFpbCI6ImF5dXNoZGVzaHBhbmRlODFAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMDAyODkyOTE3MzE1MTgwODk0NzkiXSwiZW1haWwiOlsiYXl1c2hkZXNocGFuZGU4MUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.ET5TaAqWMm3JpM_eKkPmjShMQ04V0WMsZ_xTljD4GWk6lO3NBvxHo21W5s2klZPDj1xEHA43Vzpl0qghq6YVDpInGGCcS1ikgjMfD1tHRLR0eQKd3Hh8NpZ0gUBF3zvfhVhNvdHevcws8dJ9Aax-24vJsmwQtOqrV_1h650JI5jBBkpGS8POkEUC8xLuwMwbTKLud5AzlY6IMY9TIkK_BB-17oXSgwaQD6FpUFR0r3L_FkDqu4UQeDajjqyBw-ymV6IGdpaHJk2dsi1xcf1mvzfug7PkVVuNe5tfxrghq98eiVMWYzl80_3YhlsiIpWDW1N34FYOf2_YLjUqqdNKwA"))