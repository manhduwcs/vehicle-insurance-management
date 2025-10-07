# TODO for VehicleTypes and Vehicles CRUD

- [x] Add Customer model to admin_soft/models.py
- [x] Add VehicleType and Vehicle models to vehicle/models.py
- [x] Create vehicle/forms.py with VehicleTypeForm and VehicleForm
- [x] Create vehicle/urls.py with paths for vehicle_types and vehicles CRUD
- [x] Update vehicle/views.py with CRUD views for VehicleType and Vehicle
- [x] Update vehicle_insurance_management/urls.py to include vehicle.urls
- [x] Create templates for vehicle_types: list.html, detail.html, update.html in vehicle/templates/vehicle_types/
- [x] Create templates for vehicles: list.html, detail.html, update.html in vehicle/templates/vehicles/
- [x] Run makemigrations and migrate (Note: Migrate failed due to MySQL not running. Ensure MySQL is started and configured, then run python manage.py makemigrations && python manage.py migrate)
