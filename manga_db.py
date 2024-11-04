from datetime import datetime
import firebase_admin
import requests
from bs4 import BeautifulSoup
from firebase_admin import credentials, firestore, db, storage
from unidecode import unidecode
import streamlit as st
from PIL import Image
import io
URL_IMAGE = 'https://s1.urserver.click/reading-comic/cover'
def fix_id_title(title):
    if '-' in title:
        title = " ".join(title.split('-'))
    title = title.title()
    doc_id = unidecode('-'.join(title.lower().split()))
    return doc_id, title

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None

def scan_preview_manga_chapter(title):
    doc_id, title = fix_id_title(title)
    link = f'{st.session_state.scan_site}/truyen-tranh/{doc_id}'
    scaner = scan_manga_chapter(link)
    chapter, date = next(scaner)
    if chapter is not None:
        return chapter, date, doc_id, title

def scan_manga_chapter(url: str):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        chapter_rows = soup.find(id='desc').find_all("li", class_="row")

        first_chapter = chapter_rows[0].find("div", class_="chapter").a.get_text(strip=True)
        first_date = chapter_rows[0].find("div", class_="no-wrap").get_text(strip=True)
        yield int(first_chapter.split()[1]), first_date

        data = []
        for row in chapter_rows:
            chapter = row.find("div", class_="chapter").a.get_text(strip=True)
            date = row.find("div", class_="no-wrap").get_text(strip=True)
            data.append({"Chapter": chapter, "Date": date})
        yield data

    except requests.RequestException as e:
        print(f"Request error: {e}")
        yield None, None

    except Exception as e:
        print(f"An error occurred: {e}")
        yield None, None

class MangaDB:
    def __init__(self,cred_dict=None, optionss_dict=None):
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, optionss_dict)
        self.client = firestore.client()
        self.ref = db.reference()
        self.manga_ref = self.client.collection('mangas')
        self.setting_ref = self.client.collection('setting')
        self.bucket = storage.bucket()
        self.user = None

    def save_reading_site(self, site):
        self.ref.update({'reading_site': site})

    def get_reading_site(self):
        data = self.ref.get()
        return data.get('reading_site') if data else None

    def save_scan_site(self, site):
        self.ref.update({'scan_site': site})

    def get_scan_site(self):
        data = self.ref.get()
        return data.get('scan_site') if data else None

    def add_site(self, site):
        doc_ref = self.setting_ref.add({
            'site': site,
            'date': datetime.now().isoformat()
        })

    def delete_site(self, site):
        query = self.setting_ref.where('site', '==', site).stream()
        for doc in query:
            doc.reference.delete()
            break

    def get_all_sites(self):
        sites_with_dates = []
        sites = []
        docs = self.setting_ref.stream()
        for doc in docs:
            data = doc.to_dict()
            sites.append(data['site'])
            sites_with_dates.append((data['site'], data['date']))
        return sites, sites_with_dates

    #  Home
    #  Image
    def upload_image(self, image_data, file_name):
        blob = self.bucket.blob(file_name)
        if not blob.exists():
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((200, 300), Image.Resampling.LANCZOS)

            # image.thumbnail((200, 300))
            image_buffer = io.BytesIO()
            image.save(image_buffer, format="JPEG")
            image_buffer.seek(0)
            blob.upload_from_file(image_buffer, content_type='image/jpeg')
            blob.make_public()
        return blob.public_url

    def get_image_url(self, file_name):
        blob = self.bucket.blob(file_name)
        blob.make_public()
        return blob.public_url

    # Manga

    def scan_manga(self, doc_id, scan_image=False, scan_chapter=True, all_chapter=False):
        # scan image
        if scan_image:
            url = f"{URL_IMAGE}/{doc_id}.jpg"
            image_data = download_image(url)
            image_manga_url = self.upload_image(image_data, f"{doc_id}.jpg")  if image_data else self.get_image_url('default.jpg')
            self.manga_ref.document(doc_id).update({'Image': image_manga_url})
            st.session_state.mangas[doc_id]['Image'] = image_manga_url

        #scan chapter
        if scan_chapter:
            link = f'{st.session_state.scan_site}/truyen-tranh/{doc_id}'
            scaner = scan_manga_chapter(link)
            chapter, date = next(scaner)
            if chapter is not None:
                if chapter !=  st.session_state.mangas[doc_id]['Chapter']:
                    self.manga_ref.document(doc_id).update({'Chapter': chapter})
                    st.session_state.mangas[doc_id]['Chapter'] = chapter
            if all_chapter:
                yield chapter, date
                yield next(scaner)
            else:
                yield None


    def add_manga(self, title, dates, chapter):
        doc_id, title = fix_id_title(title)
        new_manga = {"Title": title, "Date": dates, "Chapter": chapter}
        self.manga_ref.document(doc_id).set(new_manga)
        st.session_state.mangas[doc_id] = {
            "Title": title,
            "Date": dates,
            "Chapter": chapter,
        }
        next(self.scan_manga(doc_id, scan_image=True, scan_chapter=True, all_chapter=False))

    def get_all_mangas(self):
        mangas = self.manga_ref.stream()
        return {doc.id: doc.to_dict() for doc in mangas}

    def update_manga(self, doc_id, title, dates, chapter):
        new_doc_id, title = fix_id_title(title)
        if new_doc_id != doc_id:
            self.delete_manga(doc_id)
            doc_id = new_doc_id

            self.manga_ref.document(doc_id).set({
                "Title": title,
                "Date": dates,
                "Chapter": chapter,
            })
            st.session_state.mangas[doc_id] = {
                "Title": title,
                "Date": dates,
                "Chapter": chapter,

            }
            self.scan_manga(doc_id, scan_image=True, scan_chapter=True, all_chapter=False)
        else:
            self.manga_ref.document(doc_id).update({
                "Title": title,
                "Date": dates,
                "Chapter": chapter,
            })
            st.session_state.mangas[doc_id].update({
                "Title": title,
                "Date": dates,
                "Chapter": chapter,
            })

    def delete_manga(self, doc_id):
        self.manga_ref.document(doc_id).delete()
        st.session_state.mangas.pop(doc_id, None)