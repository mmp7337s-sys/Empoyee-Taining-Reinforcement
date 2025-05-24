"""
globals.py

File holding fuctions shared by gui.py and man_gui.py
"""

import hashlib
from fpdf import FPDF
from tkinter import filedialog
from pytubefix import YouTube

#/
    #Attempts to retrieve and download a youtube video with the given link

    #Url (string): The link

    #Return (int/string): returns name of video if found, and -1 otherwise
#/
def get_yt_video(url):
    try:
        yt = YouTube(url)
    except Exception:
        return -1
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    stream.download()
    return stream.default_filename

#/
    #Used to generate a hash

    #data (string): combined data used to generate hash

    #Return (string): Returns the generated hash 
#/
def generate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

#/
    #Used create certificate as a pdf

    #first_name (string): Users first name
    #last_name (string): Users last name
    #dob (sring): Users Date of Birth
    #m_number (string): Users Bear Pass number
    #video_name (string): Name of video to be watched

    #Return (string): Returns the generated hash 
#/
def create_certificate(first_name, last_name, dob, m_number, video_name):
    #Set up pdf
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", 'B', 16)
    pdf.cell(0, 10, "Employee Training Completion Certificate", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Times", size=12)
    pdf.cell(0, 10, f"Name: {first_name} {last_name}", ln=True, align='C')
    pdf.ln(5)
    pdf.cell(0, 10, f"DoB: {dob}", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(0, 10, f"M-Number: {m_number}", ln=True, align='C')
    pdf.ln(5)
    pdf.cell(0, 10, f"Video:{video_name}", ln=True, align='C')
    pdf.ln(10)

    #Generate a unique certificate hash and display for verification 
    certificate_hash = generate_hash(first_name + last_name + dob + m_number + video_name)
    pdf.multi_cell(0, 10, f"Verification Hash: {certificate_hash}")

    location = filedialog.asksaveasfilename(               #open the filedialog to get the mp4 file
            title="Select where to save the file",      #message to user seen in title of filedialog once opened
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
    # n = location.rsplit('/', 1)
    pdf.output(location)
    
    return certificate_hash

#/
    #Calls generate_hash and retreive hash number, then compare hash given by user with hash generated

    #first_name (string): Users first name
    #last_name (string): Users last name
    #dob (sring): Users Date of Birth
    #m_number (string): Users Bear Pass number
    #video_name (string): Name of video to be watched
    #given_hash (string): Hash given by trainee to be tested

    #Return (string): Returns True if the hash given by user and hash generated are the same, false otherwise
#/
def verify_certificate(first_name, last_name, dob, m_number, video_name, given_hash):
    combined_data = first_name + last_name + dob + m_number + video_name
    expected_hash = generate_hash(combined_data)
    
    if expected_hash == given_hash:
        print("Verification Successful")
        return True
    else: 
        print("Verification Failed")
        print(f"Expected Hash: {expected_hash}")
        print(f"Given Hash: {given_hash}")
        return False

#generated_hash = create_certificate("Arthas", "Lee", "1996-02-18", "M03372922", "Employee Training Completion Enforcement System Video")

#verify_certificate("Arthas", "Lee", "1996-02-18", "M03372922", "Employee Training Completion Enforcement System Video", generated_hash)