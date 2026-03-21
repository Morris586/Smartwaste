Responsibility	                Location
Determine truck availability	Truck.is_available property
Assign truck to pickup	        handle_new_pickup()
Set driver to on_job	        handle_new_pickup()
Set driver back to available	admin.save_model() when collected
Filter dropdown	                formfield_for_foreignkey()


!! System definition
A dispatch backend that:
- Receives pickup requests
- Geocodes addresses
- Assigns nearest available truck
- Updates driver state
- Manages availability dynamically