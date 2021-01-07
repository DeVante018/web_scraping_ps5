import simplejson
import smtplib
import ssl
from bs4 import BeautifulSoup
import requests
import subprocess
import time

usr_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"

headers = {
    'User-Agent': usr_agent
}
version = 10  # This is to change the user agent because amazon catches and send a different html file
audio_file = "/Users/devantefrederick/IdeaProjects/web_scraping/src/Popular_Alarm_Clock_Sound_Effect.mp3"
password = ""
port = 465  # For SSL
# Create a secure SSL context
context = ssl.create_default_context()

# add friends/family to emailing list and hook the homies up


# so I dont get spammed
walmart_available = False
gamestop_available = False
bestbuy_available = False
amazon_available = False
playstation_direct_available = False


# TODO Check logic to make sure you dont spam yours and others emails
# TODO Update the "store"_available variables after the ps5 is out of stock
# TODO Create generic functions for errors and status codes
# TODO refactor code base and variable names
# TODO Add multi-threading for concurrent processes **wait for macbook pro**


def best_buy(url, count):
    global bestbuy_available
    try:
        result = requests.get(url, headers=headers)
    except:
        print('\033[94m' + "Timeout has occurred: Best Buy ", count)
        return False

    if str(result) != "<Response [200]>":
        print('\033[94m' + "Not Found 404 (Best Buy)")
        with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
            server.login("notsecurecodingemail@gmail.com", password)
            sender_email = "notsecurecodingemail@gmail.com"
            message = "404 Best Buy, check site\nhttps://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149\n"
            # server.sendmail(sender_email, devante, message)
        return False

    try:
        # print(result.text)
        soup = BeautifulSoup(result.text, 'html.parser')
        # print(soup.p)
        tag = soup.prettify()
        body = soup.find('body', class_="size-l")
        # print(body)
        div1 = body.find('div', class_="pl-page-content")
        # print(div1)
        main = div1.find('main')
        # print(main)
        div2 = main.find('div', class_="container-v2")
        # print(div2)
        data_sticky = div2.find('div', class_="row v-m-bottom-g")
        # print(data_sticky)
        div3 = data_sticky.find('div', class_="col-xs-5 col-lg-4")
        # print(div3)
        row = div3.find('div', class_="row")

        div4 = row.find('div', class_="col-xs-12")
        # print(div4)
        div5 = div4.find('div', class_="v-m-top-m v-p-top-m v-border v-border-top")
        # print(div5.prettify())
        add_to_cart_button = div5.find('div', class_="None")
        fullfill = add_to_cart_button.find('div', class_="fulfillment-add-to-cart-button")
        find_div = fullfill.find('div')
        find_div = fullfill.find('div')
        button = find_div.find('button')
        # print(button.prettify())
        # print(button.text)

        if button.text == "Sold Out":
            print('\033[94m' + "PS5 sold out (Best Buy)   attempt #: ", count)
            bestbuy_available = False
            return False
        else:
            print('\033[94m' + "PS5 available at Best Buy :", url)
            # print(button.text)
            if not bestbuy_available:
                with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
                    server.login("notsecurecodingemail@gmail.com", password)
                    sender_email = "notsecurecodingemail@gmail.com"
                    message = "THIS IS DEVANTE'S PROGRAMM NOTIFYING YOU IN REAL TIME THAT THE PS5 IS AVAILABLE AT\nhttps://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149\n"
                    server.sendmail(sender_email, devante, message)
                    server.sendmail(sender_email, alycia, message)
                    server.sendmail(sender_email, alex, message)
                    server.sendmail(sender_email, jude, message)
                subprocess.call(["afplay", audio_file])
            bestbuy_available = True
            return True
    except:
        # print(body.prettify())
        print('\033[94m' + "Page HTML contents have changed (Best Buy). Check and update at: ", url)
        # Send notification email
        with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
            server.login("notsecurecodingemail@gmail.com", password)
            sender_email = "notsecurecodingemail@gmail.com"
            message = "Page HTML contents have changed (Best Buy)\nhttps://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149\n"
            server.sendmail(sender_email, devante, message)
        #subprocess.call(["afplay", audio_file])
        return False


def target(url, count):
    try:
        result = requests.get(url, headers=headers)
    except:
        print("timout has occurred: Target")
        return False

    if str(result) != "<Response [200]>":
        print("Not Found 404 (Target)")
        return False
    soup = BeautifulSoup(result.text, 'html.parser')
    # print(soup.prettify())
    body = soup.find('body')
    # print(body.prettify())


def walmart(url, count):
    global walmart_available
    try:
        result = requests.get(url, headers=headers)
    except:
        print('\033[95m' + "Timeout has occurred: Walmart ", count)
        return False
    if str(result) != "<Response [200]>":
        print('\033[95m' + "Not Found 404 (Walmart)")
        with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
            server.login("notsecurecodingemail@gmail.com", password)
            sender_email = "notsecurecodingemail@gmail.com"
            message = "404 Walmart, check site\nhttps://www.walmart.com/ip/PlayStation-5-Console\n"
            # server.sendmail(sender_email, devante, message)
        return False

    try:
        soup = BeautifulSoup(result.text, 'html.parser')
        body = soup.find('body')
        div1 = body.find('div')
        div2 = div1.find('div', class_="error-page-content")
        print('\033[95m' + "Walmart PS5 landing page is not created yet ", count)
        walmart_available = False
    except:
        print('\033[95m' + "Page is no longer an error page: Walmart")
        if not walmart_available:
            with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
                server.login("notsecurecodingemail@gmail.com", password)
                sender_email = "notsecurecodingemail@gmail.com"
                message = "Walmart PS5 page is active, check at\nhttps://www.walmart.com/ip/PlayStation-5-Console\n"
                server.sendmail(sender_email, devante, message)
        walmart_available = True
        subprocess.call(["afplay", audio_file])


def game_stop(url, count):
    global gamestop_available

    try:
        result = requests.get(url, headers=headers)
    except:
        print('\033[92m' + "Timeout has occurred: Gamestop", count)
        return False

    if str(result) != "<Response [200]>":
        print('\033[92m' + "Not Found 404 (Gamestop)")
        with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
            server.login("notsecurecodingemail@gmail.com", password)
            sender_email = "notsecurecodingemail@gmail.com"
            message = "404 GameStop, check site\nhttps//www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html\n"
            # server.sendmail(sender_email, devante, message)
        return False

    try:
        soup = BeautifulSoup(result.text, 'html.parser')
        # print(soup.prettify())
        body = soup.find('body')
        # print(body.prettify())
        page = body.find('div', class_="page")
        div1 = page.find('div', class_="productDetailsReplaceContainer")
        div2 = div1.find('div', class_="product-detail product-wrapper product-detail-redesign")
        div3 = div2.find('div', class_="product-detail-top-section apple-pay-available")
        div4 = div3.find('div', class_="product-details-container")
        div5 = div4.find('div', class_="row justify-content-between main-product-section")
        div6 = div5.find('div', class_="primary-details d-none pr-md-0")
        div7 = div6.find('div', class_="primary-details-row")
        div8 = div7.find('div', class_="cart-and-ipay divider-line no-border-mobile")
        div9 = div8.find('div', class_="add-to-cart-buttons tulsa-atcbutton-toggle")
        # print(div9.prettify())
        div10 = div9.find('div', class_="atc-btns-wrapper")
        # print(div10.prettify())
        div11 = div10.find('div', class_="atc-btn-wrapper")
        # print(div11.prettify())
        # print("---------------------------------------------------\n")
        button = div11.find('button', class_="add-to-cart btn btn-primary")
        # print(button['data-gtmdata'])
        info_jason = button['data-gtmdata']
        info_jason = simplejson.loads(info_jason)
        # print(info_jason)

        if info_jason["productInfo"]["availability"] == "Not Available":
            print('\033[92m' + "PS5 sold out (Game Stop)   attempt #: ", count)
            gamestop_available = False
            return False
        else:
            print('\033[92m' + "PS5 available at Game Stop :", url)
            if not gamestop_available:
                with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
                    server.login("notsecurecodingemail@gmail.com", password)
                    sender_email = "notsecurecodingemail@gmail.com"
                    message = "THIS IS DEVANTE'S PROGRAMM NOTIFYING YOU IN REAL TIME THAT THE PS5 IS AVAILABLE AT\nhttps://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html""?condition=New\n"
                    server.sendmail(sender_email, devante, message)
                    server.sendmail(sender_email, alycia, message)
                    server.sendmail(sender_email, alex, message)
                    server.sendmail(sender_email, jude, message)
                gamestop_available = True
                subprocess.call(["afplay", audio_file])
                return True

    except:
        print('\033[92m' + "Page HTML contents have changed (GameStop). Check and update at: ", url)
        with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
            server.login("notsecurecodingemail@gmail.com", password)
            sender_email = "notsecurecodingemail@gmail.com"
            message = "Gamestop page contents have changed, check now at\nhttps://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html\n"
            # server.sendmail(sender_email, devante, message)
        subprocess.call(["afplay", audio_file])
        return False


def amazon(url, count):
    body = None
    global usr_agent
    global version
    global headers
    if (count % 100) == 0:
        print("Changing user agent to get around Amazon flag...")
        new_list = list(usr_agent)
        new_list[45] = str(version)
        usr_agent = str(new_list)
        version += 1
    try:
        result = requests.get(url, headers=headers)
    except:
        print('\033[91m' + "Timeout has occurred: Amazon", count)
        return False
    if str(result) != "<Response [200]>":
        print('\033[91m' + "Not Found 404 (Amazon)")
        with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
            server.login("notsecurecodingemail@gmail.com", password)
            sender_email = "notsecurecodingemail@gmail.com"
            message = "404 Amazon, check site\nhttps://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG?ref_=ast_sto_dp\n"
            # server.sendmail(sender_email, devante, message)
        return False

    try:
        soup = BeautifulSoup(result.text, 'html.parser')
        # print(soup.prettify())
        body = soup.find('body')
        # print(body.prettify())
        div1 = body.find('div', id="a-page")
        # print(div1.prettify())
        div2 = div1.find('div', class_="video_games en_US")
        # print("div2")
        div3 = div2.find('div', class_="a-container")
        # print("div3")
        div4 = div3.find('div', id="ppd")
        # print("div4")
        div5 = div4.find('div', class_="centerColAlign centerColAlign-bbcxoverride")
        # print("div5")
        div6 = div5.find('div', id="availability_feature_div")
        # print("div6")
        div7 = div6.find('div', class_="a-section a-spacing-none")
        # print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        # print(div7)
        # print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        availability = div7.find('span', class_="a-size-medium a-color-price")
        availability = availability.text
        availability = availability.strip()
        # print(availability)
        if availability == "Currently unavailable.":
            print('\033[91m' + "PS5 sold out (Amazon)   attempt #: ", count)
        else:
            print('\033[91m' + "PS5 available at Amazon :", url)
            global amazon_available
            if not amazon_available:
                with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
                    server.login("notsecurecodingemail@gmail.com", password)
                    sender_email = "notsecurecodingemail@gmail.com"
                    message = "THE PS5 IS AVAILABLE AT\nhttps://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG?ref_=ast_sto_dp\n"
                    server.sendmail(sender_email, devante, message)
                    server.sendmail(sender_email, alycia, message)
                    server.sendmail(sender_email, alex, message)
                    server.sendmail(sender_email, jude, message)
            amazon_available = True
            subprocess.call(["afplay", audio_file])
            return True

    except:
        error_check = body.find('div', class_="a-container a-padding-double-large")
        error_check = error_check.text
        # print(error_check.strip()[0])
        if error_check.strip()[0] == 'E':
            # print('\033[91m'+"Changing user agent to get around Amazon flag...")
            print(body.prettify())
            new_list = list(usr_agent)
            new_list[45] = str(version)
            usr_agent = str(new_list)
            version += 10
            return False
        else:
            print('\033[91m' + "Page HTML contents have changed (Amazon). Check and update at: ", url)
            with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
                server.login("notsecurecodingemail@gmail.com", password)
                sender_email = "notsecurecodingemail@gmail.com"
                message = "Amazon page contents have changed, check now at\nhttps://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG?ref_=ast_sto_dp\n"
                # server.sendmail(sender_email, devante, message)
            subprocess.call(["afplay", audio_file])
            return False


def playstation_direct(url, count):
    global playstation_direct_available

    try:
        result = requests.get(url, headers=headers)
    except:
        print('\033[96m' + "Timeout has occurred: Playstation Direct", count)
        return False

    if str(result) != "<Response [200]>":
        print('\033[96m' + "Not Found 404 (Playstation Direct)")
        with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
            server.login("notsecurecodingemail@gmail.com", password)
            sender_email = "notsecurecodingemail@gmail.com"
            message = "404 Playstation Direct, check site\nhttps://direct.playstation.com/en-us/consoles/console/playstation5-console.3005816\n"
            # server.sendmail(sender_email, devante, message)
        return False

    try:
        soup = BeautifulSoup(result.text, 'html.parser')
        # print(soup.prettify())
        body = soup.find('body', class_="page basicpage")
        # print(body.prettify())
        div1 = body.find('div', class_="root responsivegrid")
        # print(div1)
        div2 = div1.find('div', class_="aem-Grid aem-Grid--12 aem-Grid--default--12")
        # print(div2)
        div3 = div2.find('div', class_="heropdp background-white aem-GridColumn aem-GridColumn--default--12")
        # print(div3)
        div4 = div3.find('producthero-component')
        # print(div4)
        div5 = div4.find('div', class_="container")
        # print(div5)
        div6 = div5.find('div', class_="productHero-component row")
        # print(div6)
        div7 = div6.find('div', class_="productHero-desc col-lg-6 order-lg-2")
        # print(div7)
        div8 = div7.find('producthero-info')
        # print(div8)
        div9 = div8.find('div', class_="productHero-info")
        # print(div9)
        div10 = div9.find('div', class_="button-placeholder")
        # print(div10.prettify())
        div11 = div10.find('div', class_="out-stock-wrpr js-out-stock-wrpr hide")
        # print(div11)
        stock = div11.find('p', class_="sony-text-body-1")
        # print(stock.text)
        if stock.text == "Out of Stock":
            print('\033[96m' + "PS5 sold out (Playstation Direct)   attempt #: ", count)
            playstation_direct_available = False
        else:
            print('\033[96m' + "PS5 available at Playstation Direct :", url)
            if not playstation_direct_available:
                with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
                    server.login("notsecurecodingemail@gmail.com", password)
                    sender_email = "notsecurecodingemail@gmail.com"
                    message = "THE PS5 IS AVAILABLE AT\nhttps://direct.playstation.com/en-us/consoles/console/playstation5-console.3005816\n"
                    server.sendmail(sender_email, devante, message)
                    server.sendmail(sender_email, alycia, message)
                    server.sendmail(sender_email, alex, message)
                    server.sendmail(sender_email, jude, message)
            playstation_direct_available = True
            subprocess.call(["afplay", audio_file])
            return True

    except:
        print('\033[96m' + "Page HTML contents have changed (Playstation Direct). Check and update at: ", url)
        with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
            server.login("notsecurecodingemail@gmail.com", password)
            sender_email = "notsecurecodingemail@gmail.com"
            message = "Playstation Direct page contents have changed, check now at\nhttps://direct.playstation.com/en-us/consoles/console/playstation5-console.3005816\n"
            # server.sendmail(sender_email, devante, message)
        subprocess.call(["afplay", audio_file])
        return False


if __name__ == '__main__':
    qnt = 0
    while True:
        qnt += 1
        best_buy("https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149", qnt)
        game_stop(
            "https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html""?condition=New",
            qnt)
        playstation_direct("https://direct.playstation.com/en-us/consoles/console/playstation5-console.3005816", qnt)
        # amazon("https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG?ref_=ast_sto_dp", qnt)
        walmart("https://www.walmart.com/ip/PlayStation-5-Console", qnt)
        time.sleep(15)  # check in 10 sec intervals
