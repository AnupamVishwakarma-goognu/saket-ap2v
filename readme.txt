# To setup the database, please followup below steps for makemigrations and migrate
# for Anquira
python manage.py makemigrations users
python manage.py migrate
python manage.py makemigrations batches courses enquiries enrolls followups instructors 
python manage.py migrate


# for Ap2v
python manage.py migrate
python manage.py makemigrations blogs events home testimonials
python manage.py migrate
python manage.py makemigrations ap2v_courses learning_paths
python manage.py migrate
python manage.py makemigrations seo landing_page gallery
python manage.py migrate