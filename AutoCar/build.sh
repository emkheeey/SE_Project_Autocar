   # Install python
   apt-get update
   apt-get install -y python3 python3-pip

   # Install dependencies
   pip3 install -r requirements.txt
   
   # Run migrations
   python3 manage.py migrate