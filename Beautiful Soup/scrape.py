#!/usr/bin/python3.7
from bs4 import BeautifulSoup
import sys
import csv
import smtplib
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText
#from email.mime.base import MIMEBase
#from email import encoders

def extract_listings(html_content, query, max_price, num_products):
    soup = BeautifulSoup(html_content, 'html.parser')
    listings = soup.find_all("li", class_="cl-static-search-result")
    extracted_listings = []
    for listing in listings:
        # Extract name of the item
        name = listing.find("div", class_="title").text.strip()
        
        # Extract price of the item
        price_tag = listing.find("div", class_="price")
        price_str = price_tag.text.strip() if price_tag else "N/A"
        location_tag = listing.find("div", class_="location")
        location = location_tag.text.strip() if location_tag else "N/A"
        price_str = price_str.replace(',','')
        if price_str != "N/A" and float(price_str[1:]) == 0:
            continue
	
        # Check if query parameter matches the name of the item
        if not query or query.lower() in name.lower():
            # Check if the price is within the maximum price
            if price_str != "N/A" and float(price_str[1:]) <= max_price:
                extracted_listings.append((name, price_str, location))
                if len(extracted_listings) >= num_products:
                    break
    return extracted_listings

if __name__ == "__main__":
    if len(sys.argv) > 4:
        print("Usage: ./run.py [query] [max_price] [num_products]")
        sys.exit(1)

    query = sys.argv[1] if len(sys.argv) > 1 else ""
    max_price = float(sys.argv[2]) if len(sys.argv) > 2 else 90000
    num_products = int(sys.argv[3]) if len(sys.argv) > 3 else 240

    with open("output1.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    results = extract_listings(html_content, query, max_price, num_products)
    
    # Print the extracted listings
    for i, (name, price, location) in enumerate(results, start=1):
        print(f"Item: {name}, Price: {price}, Location: {location}")

    print("Total number of items:", len(results))
    sorted_results = sorted(results, key=lambda x: float(x[1].replace('$','').replace(',','')))
    with open ("listings.csv", "w",newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Item","Price","Location"])
        for i, (name,price,location) in enumerate(sorted_results,start=1):
            csv_writer.writerow([name,price,location])
    
#    from_email = "studentdent@yahoo.com" 
#    to_email = ["hayatwhitecomp@gmail.com"] 
#    subject = "Listings"
#    body = "Please find attached the listings CSV file."
#    msg = MIMEMultipart()
#    msg['From'] = from_email
#    msg['To'] = ', '.join(to_email)
#    msg['Subject'] = subject
#    msg.attach(MIMEText(body, 'plain'))
#    filename = "listings.csv"
#    attachment = open(filename,"rb")
#    part = MIMEBase('application', 'octet-stream')
#    part.set_payload((attachment).read())
#    encoders.encode_base64(part)
#    part.add_header('Content-Disposition', "attachment; filename %s" % filename)
#    msg.attach(part)
#    server = smtplib.SMTP("smtp.mail.yahoo.com", 587)
#    server.starttls()
#    server.login(from_email, "Jaimeisawesome11!")
 #   text = msg.as_string()
 #   server.sendmail(from_email,to_email,text)
 #   server.quit()
 #   print("EMAIL SENT")
