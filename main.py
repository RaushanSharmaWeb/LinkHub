import requests
from bs4 import BeautifulSoup

# Step 1: Wo initial URL jahan aapko ads wale page par bheja jata hai
initial_url = "https://streamfiles.eu.org/task-verify.php" 

# Ek HTTP session banayenge taaki cookies aur state maintain rahein
session = requests.Session()

# Server ko lage ki request kisi real browser se aa rahi hai
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    print("Main page load kar rahe hain...")
    response = session.get(initial_url, headers=headers)
    
    # Step 2: HTML parse karke wo verify wala link nikalna
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Button ke anchor <a> tag ko dhundhna jiske href mein 'task-verify.php' ho
    verify_link_tag = soup.find('a', href=lambda href: href and 'task-verify.php' in href)
    
    if verify_link_tag:
        # Pura URL construct karna (agar href relative path mein ho)
        href_value = verify_link_tag['href']
        verify_url = href_value if href_value.startswith('http') else "https://streamfiles.eu.org/" + href_value.lstrip('/')
        
        print(f"Bypass Link mil gaya! Isko direct hit kar rahe hain...\nLink: {verify_url[:80]}...")
        
        # Step 3: Verify link par hit karna taaki token generate ho jaye
        final_response = session.get(verify_url, headers=headers)
        
        # Step 4: Server dwara bheji gayi nayi cookies nikalna
        final_cookies = session.cookies.get_dict()
        
        if "__Host-access_token" in final_cookies:
            print("\n🎉 Success! Ads bypass ho gaye. Naya Token mil gaya:")
            print(f"Token: {final_cookies['__Host-access_token']}")
        else:
            print("\n⚠️ Link hit kiya, par token nahi mila. Shayad server aur validation kar raha hai.")
            
    else:
        print("Link HTML mein nahi mila. Shayad JavaScript se dynamically aage peeche generate ho raha hai.")

except Exception as e:
    print(f"Error aayi: {e}")
