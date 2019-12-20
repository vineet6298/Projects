from selenium import webdriver
#chrome browser
driver=webdriver.Chrome()
#firefox browser
#driver=webdriver.Firefox
city=str(input("Enter the name of the city you want weather forecast for:"))
driver.get("https://www.weather-forecast.com/locations/"+city+"/forecasts/latest")
print(driver.find_elements_by_class_name("b-forecast__table-description-content")[0].text)
