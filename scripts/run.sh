uvicorn agents:app --reload


docker run -p 5432:5432 --name rental_db -e POSTGRES_PASSWORD=hpinvent -d postgres

