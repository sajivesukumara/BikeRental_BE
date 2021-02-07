__author__ = 'sajive'
cd C:\Users\kumasaji\OneDrive - Hewlett Packard Enterprise\Sajive\Projects\BikeRentals\BikeRental_BE\app

uvicorn app.main:app --reload

docker run -p 5432:5432 --name rental_db -e POSTGRES_PASSWORD=hpinvent \
   -v ${HOME}/postgres-data/:/var/lib/postgresql/data -d postgres


docker run -p 8080:80 -e 'PGADMIN_DEFAULT_EMAIL=sajive.sukumar@gmail.com' -e 'PGADMIN_DEFAULT_PASSWORD=hpinvent' --name dev-pgadmin -d dpage/pgadmin4


docker inspect -f "{{ .Mounts }}" d98e907bd588
