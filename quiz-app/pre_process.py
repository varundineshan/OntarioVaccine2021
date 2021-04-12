import pandas as pd
import pgeocode
import geopy.distance
import smtplib
from email.message import EmailMessage

df=pd.read_csv("static/data/Ministry_of_Health_Service_Provider_Locations.csv")
df=df[["EN_NAME","SERV_TYPE","ADDRESS_1","POSTALCODE","X","Y","FID"]]
#Checking for duplicates
total_raw=len(set(df.index))
extra=df.shape[0]-total_raw


#Checking for null values
df.isnull().sum()

def find_nearby_vaccine(postalcode):
    nomi = pgeocode.Nominatim('ca')
    postal_code1 = postalcode
    matching=df[df['POSTALCODE'].str.match(postal_code1[:3])]

    distance=[]
    coords_1 = (nomi.query_postal_code(postal_code1).latitude,nomi.query_postal_code(postal_code1).longitude)
    for i in matching.iterrows():
        ziper=i[1][5]
        coords_2 = (i[1][5],i[1][4])
        distance.append(round(geopy.distance.geodesic(coords_1, coords_2).km,2))

    matching['Distance in KM']=distance 
    matching.drop(["X","Y"],axis=1,inplace=True)

    
    sorted_df = matching.sort_values(by=['Distance in KM'])[:5]
    
    sorted_df.index={1,2,3,4,5}
    sorted_df
    return(sorted_df)

def send_mail(fid,otp,email):
    matching=df.loc[(df["FID"] ==int(fid))]
    

    msg = EmailMessage()
    server = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
    server.login("ontariovaccine@gmail.com","Passwordis12345")
    message="""
    Thank you for booking your vaccine with {},

    You can visit any time and show 6 digit OTP to get vaccine. 

    OTP : {}
    Clinic:{}
    Address:{}
    Postal:{}

    """.format(matching.iloc[0]['EN_NAME'],
    otp,
    matching.iloc[0]['EN_NAME'],
    matching.iloc[0]['ADDRESS_1'],
    matching.iloc[0]['POSTALCODE'])

    msg.set_content(message)
    msg['Subject']="Confirmation Booking Vaccine"
    msg['From'] = "ontariovaccine@gmail.com"
    msg['To'] = email

    server.send_message(msg)
    server.quit()
