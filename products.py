# import requests
# from bs4 import BeautifulSoup

# url = "https://dummyjson.com/products"
# headers = {"User-Agent": "Mozilla/5.0"}
# response = requests.get(url, headers=headers)
# print("response:::::::",response)

# soup = BeautifulSoup(response.text, "html.parser")
# print("soup",soup)
# products = []

# for item in soup.find_all("div", class_="product-card"):
#     name = item.find("h2").text
#     price = item.find("span", class_="price").text
#     image = item.find("img")["src"]
    
#     products.append({"name": name, "price": price, "image": image})

# print(products)

# import requests

# url = "https://dummyjson.com/products"
# headers = {"User-Agent": "Mozilla/5.0"}
# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     data = response.json()  # Parse JSON response
#     products = data.get("products", [])  # Extract product list

#     # Extract basic details
#     product_list = []
#     for product in products:
#         product_list.append({
#             "name": product["title"],
#             "price": product["price"],
#             "image": product["thumbnail"]
#         })

#     print(product_list)
# else:
#     print(f"Failed to fetch data. Status Code: {response.status_code}")


import requests

url = "https://dummyjson.com/products"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()  # Parse JSON response
    products = data.get("products", [])  # Extract product list

    # Print full product details
    for product in products:
        print(product)  # Print each product as a dictionary
else:
    print(f"Failed to fetch data. Status Code: {response.status_code}")
