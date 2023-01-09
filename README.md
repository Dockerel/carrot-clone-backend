product upload -> buyer 등록 -> review -> 머시기

---

PRODUCT

/products : get, post
/products/pk:int : get, put, delete
/products/pk:int/username:str : put (username 유저가 is_sold를 true로, buyer을 update)
/products/pk:int/photos : post (upload photo)

---

USER

/users : post (signup)
/users/me : get (my profile)
/users/signin : post (signin)
/users/signout : post (signout)
/users/username:str : get
/users/username:str/review : get

---

PHOTO

/photos/pk:int : get, delete (photo detail)

---

REVIEW

/reviews/product_name:str : post (product_name의 product에 review 추가)

---

DMS

/dms/chatting-rooms : get (my chatting rooms)
/dms/chatting-rooms/username:str/create : post (make chatting room if there's no chatting room with usernameUser and owner(current user).)
/dms/chatting-rooms/pk:int/messages : get, post (show and send message)
