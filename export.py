from  selenium_scraper import company_websites

with open("example.txt", "w") as f:
        for name,web in company_websites.items():
            f.write(name + " : " + "\n")
            for link in web:
                f.write("   " + link + "\n")