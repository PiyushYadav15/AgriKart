# AgriKart
AgriKart is a Django-based Farmer-to-Consumer Marketplace that eliminates middlemen and helps farmers sell their crops directly to consumers. It provides a transparent, fair, and efficient platform where farmers can upload, manage, and sell their produce, while consumers can browse and purchase fresh crops at affordable prices.
## ✨ Features  

- 👨‍🌾 **Farmer Dashboard** – Add, edit, and delete crops.  
- 🛒 **Consumer Dashboard** – Browse and buy fresh crops directly.  
- 📂 **Category Filtering** – Farmers see only their own crops under categories.  
- 🚫 **Empty States** – Shows *“No crops available”* if no crop is uploaded.   
- 🔔 **Notifications** – Price alerts, updates, and reminders.  

---

## 🛠️ Tech Stack  

**Frontend**  
- TailwindCSS  
- JavaScript  

**Backend**  
- Python
- Django  
- 

**Database**  
-  SQLite  

**Authentication**  
- Django Auth (Signup, Login, Profile Management)  

---RUN THIS PROJECT 
2️⃣ Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # for Linux/Mac
venv\Scripts\activate      # for Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Start the server
python manage.py runserver

