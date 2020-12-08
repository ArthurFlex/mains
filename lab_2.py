from selenium.webdriver import Chrome
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import pymongo
from pymongo import MongoClient
import time



client=MongoClient('localhost', 27017)
db = client['test-farpost']
posts=db.postsers
db.posts.create_index("url")
db.posts.create_index("price")


driver = Chrome()
string='https://www.farpost.ru/vladivostok/realty/sell_flats/?page='

for i in range(1,70):
    last_string=string
    last_string=last_string+str(i)
    driver.get(string)
    content = driver.find_elements_by_class_name('pageableContent')
    if len(content)==0:
        print("Can't find pages!")
        exit()
    

    content=content[0]
    flats=content.find_elements_by_class_name('bull-item-content')
    
    list_of_posts=list()
    results=[]
    for elem in flats:
        document=dict()
        link = elem.find_elements_by_class_name('bull-item__self-link')
        if len(link)==0:
            print("Can't find links!")
            exit()      
        tmp={}
        document['url']=link[0].get_attribute('href')
        data = [i for i in posts.find({'url': link[0].get_attribute('href') })]
        if len(data)!= 0:
            print("Skip")
            continue
       
        
        price=elem.find_elements_by_class_name('price-block__price')
        if len(price)==0:
            print("Can't find price!")
            price=''
        else:
            price=price[0].text
        document['price']=price
    
       
    
        flat_list_handler=driver.current_window_handle
    
        driver.execute_script('window.open()')
        driver.switch_to.window(driver.window_handles[1])
    
        driver.get(document['url'])
        
    
        field_set=driver.find_element_by_id('fieldsetView')
        fields = field_set.find_elements_by_class_name('field')

    
    
        j=1
        for field in fields:
            key=field.find_elements_by_class_name('label') 
            if len(key)==0:
                value=field.find_elements_by_class_name('value')
                if len(value)==0:
                    pass
                else:
                    value=value[0].text
                    key=str(j) 
                    print(key)
                    print(value)             
            else:
                key=key[0].text
                if key=='Вид квартиры' or 'Район' or 'Площадь':
                    print("norm")
                else:
                    continue
                value=field.find_elements_by_class_name('value')
                if len(value)==0:
                    value='None'
                else:
                    value=value[0].text
            document[key]=value
            j+=1
    
        for key,value in document.items():
            print(key," - ",value)
        print("\n\n-------------\n\n")
        list_of_posts.append(document)
        if len(list_of_posts)==5:
            post_id=posts.insert_many(list_of_posts)
            list_of_posts.clear()
        

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        time.sleep(8)
input()
