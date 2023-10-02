from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def Scrape(hall, meal):  

    # DineOnCampus main URL
    url = 'https://dineoncampus.com/northwestern/whats-on-the-menu'

    # Setup webdriver and wait for page to load
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(12)

    # Fetch the dropdown menu of dining halls
    hallsDiv = driver.find_element(By.ID, 'menu-location-selector')
    hallsDropdown = hallsDiv.find_element(By.CSS_SELECTOR, ":nth-child(2)")

    # Click the dropdown button to open the menu
    hallsButton = driver.find_element(By.ID, 'menu-location-selector__BV_toggle_')
    hallsButton.click()
    time.sleep(2)

    # Select the left main dropdown containing dining hall names
    locationsInnerList = hallsDropdown.find_element(By.CSS_SELECTOR, ":nth-child(1)")
    mainUL = locationsInnerList.find_element(By.CSS_SELECTOR, ":nth-child(2)")

    # Assign to variables each of the <li> elements for the various dining halls
    allisonLI = mainUL.find_element(By.CSS_SELECTOR, ":nth-child(1)")
    sargentLI = mainUL.find_element(By.CSS_SELECTOR, ":nth-child(2)")
    fosterWestLI = mainUL.find_element(By.CSS_SELECTOR, ":nth-child(3)")
    fosterEastLI = mainUL.find_element(By.CSS_SELECTOR, ":nth-child(4)")
    elderLI = mainUL.find_element(By.CSS_SELECTOR, ":nth-child(5)")

    # Now assign to variables the button elements themselves
    allisonButton = allisonLI.find_element(By.CSS_SELECTOR, ":nth-child(1)")
    sargentButton = sargentLI.find_element(By.CSS_SELECTOR, ":nth-child(1)")
    fosterWestButton = fosterWestLI.find_element(By.CSS_SELECTOR, ":nth-child(1)")
    fosterEastButton = fosterEastLI.find_element(By.CSS_SELECTOR, ":nth-child(1)")
    elderButton = elderLI.find_element(By.CSS_SELECTOR, ":nth-child(1)")

    # Switch statement to click and navigate to the appropriate dining hall page via function parameter passed
    match hall:
        case 'allison':
            allisonButton.click()
        case 'sargent':
            sargentButton.click()
        case 'fosterWest':
            fosterWestButton.click()
        case 'fosterEast':
            fosterEastButton.click()
        case 'elder':
            elderButton.click()

    # Wait for page load
    time.sleep(5)

    # Assign to variables the tab buttons for each meal
    if hall == 'allison' or hall == 'sargent':
        breakfastA = driver.find_element(By.XPATH, "//*[text()='Breakfast']")
    
    lunchA = driver.find_element(By.XPATH, "//*[text()='Lunch']")
    dinnerA = driver.find_element(By.XPATH, "//*[text()='Dinner']")

    # Switch statement to click appropriate meal button
    match meal:
        case 'breakfast':
            breakfastA.click()
        case 'lunch':
            lunchA.click()
        case 'dinner':
            dinnerA.click()

    # Wait for page load
    time.sleep(10)

    # Get html for BeautifulSoup scraping
    content = driver.page_source

    with open('output.html', 'w', encoding='utf-8') as f:
        f.write(content)

    with open('output.html','r') as f:
        doc = BeautifulSoup(f, 'html.parser')

    # Print out text of each <strong> tag - these contain the entree/option names
    tags = doc.find_all('strong')
    for tag in tags:
        print(tag.text)


    driver.quit()

# Expected strings for each input, for error catching. 'breakfast' is added to mealExpectedStrings
# If the selected hall offers breakfast
hallExpectedStrings = ["allison", "sargent", "fosterWest", "fosterEast", "elder"]
mealExpectedStrings = ['lunch', 'dinner']

# Loop to catch invalid inputs when getting user hall choice
while True:
    chosenHall = input("Please enter a dining hall (Type Exactly one of the following: allison, sargent, fosterWest, fosterEast, or elder) ")
    if chosenHall in hallExpectedStrings:
        break
    else:
        print("Invalid input. Please enter exactly one of the listed strings")

# mealPrompt variable, to be altered to include breakfast if relevant
mealPrompt = 'Please enter a meal (Type Exactly one of the following: lunch or dinner)'

# Add breakfast as an option if chosen hall offers it 
if chosenHall == 'allison' or chosenHall == 'sargent':
    mealExpectedStrings.append('breakfast')
    mealPrompt = 'Please enter a meal (Type Exactly one of the following: breakfast, lunch, or dinner)'

# Similar loop to prompt for user input with error catches
while True:
    chosenMeal = input(mealPrompt)
    if chosenMeal in mealExpectedStrings:
        print("Fetching meal options...")
        break
    else:
        print("Invalid input. Please enter exactly one of the listed strings")


# Call the Scrape function
Scrape(chosenHall, chosenMeal)
