1: User -> parol va login orqali botni ishlata oladi
2: Admin -> User qushadi


Admin vazifasi:
1- User qushish
2- Admin qushish
3- Darslar yuklash -> Dars mavzusi -> Malumot
   video, rasm, matn, ovozli_xabar, dokument va h.k
4- 

User vazifasi:
start bosilganda 
 1 marta Login qiladi

Table Darslar
Dars mavzulari inline key.

Dars mavzusi tanlansa, admin yuklagan dars chiqadi



-----------------------
Userlar Table > users

Admins Table > admins

Darslar Table > lessons

InlineKeyboard(text="Canva", callback_data=f"select_{text}")

F.data.startswith("select_")
video_id


video_url = f"media\select_{video_id}"
FSInputFile = video_url

