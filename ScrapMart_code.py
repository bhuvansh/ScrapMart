from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
import os

os.mkdir("C:/Users/HP/OneDrive/Desktop/PythonProjects/scrapping_flipkart")
search_url="https://www.flipkart.com/search?q="

page="&page="
base_url='https://www.flipkart.com'
products=['bean bag','ear phones','tables']#,'bean bag','head phones','books']

for product in products:
    product_name=[]
    buy_link=[]
    MRP=[]
    PRICE=[]
    DISCOUNT=[]
    DESCRIPTION=[]
    # BRAND=[]
    RATING=[]
    SELLER=[]
    SELLER_RATING=[]

    for i in range(1,4):
        raw_data=requests.get(search_url+product+page+str(i))# this fetches the raw_data of the ith page of the given product
        parsed_data=soup(raw_data.content,'html.parser')

    #     link=parsed_data.find("a",class_="_1LKTO3").get('href')
    #     print(raw_data.url)

        data_area=parsed_data.find('div',class_="_1YokD2 _3Mn1Gg")# the area which contains the information of produts and not the review portion 
        individual_link=data_area.find_all('a',class_="s1Q9rs")# list of links to all the individual items of that category on that page

        ## scrapping data from individual objects
        for idx,i in enumerate(individual_link):
            link=base_url+i.attrs['href']
            raw_data=requests.get(link)
            parsed_data=soup(raw_data.content,'html.parser')

            buy_link.append(raw_data.url)# to store the buy link 

            name=parsed_data.find('span',class_="B_NuCI")
            if(name!=None):
                product_name.append(name.text)# to store the product name
            else :
                continue

            mrp=parsed_data.find('div',class_="_3I9_wc _2p6lqe")
            price=parsed_data.find('div',class_="_30jeq3 _16Jk6d")
            discount=parsed_data.find('div',class_="_3Ay6Sb _31Dcoz")
            if(discount!=None):
                DISCOUNT.append(discount.text)
            else:
                DISCOUNT.append('--NA--')
                
            if(price!=None):
                PRICE.append(price.text[1:])
            else :
                PRICE.append('--NA--')
            if(mrp!=None):
                MRP.append(mrp.text[1:])
            else:
                MRP.append('--NA--')

            #description/highlights about the product
            highlight=parsed_data.find('div',class_="_2cM9lP")
            temp=[]
            if(highlight!=None):
                for itr in highlight.find_all('li',class_="_21Ahn-"):
                    temp.append(itr.text)
                description=str(temp)
                description=description.replace(',','|') # because we will have to convert it to csv file therefore removing ',' 
                #from unwanted places to avoid error 
                description=description.replace("'",'')
                DESCRIPTION.append(description[1:-1]) # for removing '[' and ']' from the star and end
            else:
                DESCRIPTION.append('--NA--')


            #product rating
            rating=parsed_data.find('div',class_="_3LWZlK")
            if(rating!=None):
                RATING.append(rating.text)
            else :
                RATING.append('--NA--')

            #seller details
            seller=parsed_data.find('div',class_="_1AtVbE col-12-12")
            seller_name=seller.find('span')
            seller_rating=seller.find('div',class_="_3LWZlK _1D-8OL")

            if seller_name!=None:
                SELLER.append(seller_name.text)
                print(seller_name.text)
            else :
                SELLER.append('--NA--')

            if(seller_rating!=None):
                SELLER_RATING.append(seller_rating.text)
                print(seller_rating.text)
            else :
                SELLER_RATING.append('--NA--')
                
    print(len(product_name),len(buy_link),len(MRP),len(PRICE),len(DISCOUNT),len(DESCRIPTION),len(RATING),len(SELLER),len(SELLER_RATING))
    df=pd.DataFrame({'PRODUCT_NAME':product_name,'PRODUCT_LINK':buy_link,'MRP':MRP,'PRICE':PRICE,'DISCOUNT':DISCOUNT,'DESCRIPTION':DESCRIPTION,'PRODUCT_RATING':RATING})#,'SELLER_NAME':SELLER,'SELLER_RATING':SELLER_RATING})

    df.to_csv("C:/Users/HP/OneDrive/Desktop/PythonProjects/scrapping_flipkart/{}.csv".format(product))