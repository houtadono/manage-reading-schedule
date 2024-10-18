import firebase_admin
from firebase_admin import credentials, firestore

class MangaDB:
    def __init__(self, firebase_key_path):
        # Khởi tạo kết nối với Firestore
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_key_path)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.manga_ref = self.db.collection('mangas')

    def add_manga(self, title, dates, link, chapter):
        new_manga = {"Title": title, "Date": dates, "Link": link, "Chapter": chapter}
        self.manga_ref.add(new_manga)

    def get_all_mangas(self):
        mangas = self.manga_ref.stream()
        return {doc.id: doc.to_dict() for doc in mangas}

    def update_manga(self, doc_id, title, dates, link, chapter):
        self.manga_ref.document(doc_id).update({
            "Title": title,
            "Date": dates,
            "Link": link,
            "Chapter": chapter,
        })

    def delete_manga(self, doc_id):
        self.manga_ref.document(doc_id).delete()
